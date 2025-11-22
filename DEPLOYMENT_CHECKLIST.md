# 🚀 Deployment Checklist for Koyeb

## ✅ Pre-Deployment Checklist

### 1. Environment Variables Required
Make sure you have these values ready:
- [ ] `API_ID` - Get from https://my.telegram.org
- [ ] `API_HASH` - Get from https://my.telegram.org
- [ ] `BOT_TOKEN` - Get from @BotFather on Telegram
- [ ] `URL` - Will be `https://your-app-name.koyeb.app` (set after first deployment)

### 2. Code Verification
- [x] Port consistency (8080) ✅
- [x] In-memory session storage enabled ✅
- [x] FloodWait retry logic implemented ✅
- [x] Single worker configuration ✅
- [x] Session files not tracked in git ✅

### 3. GitHub Repository
- [ ] All code pushed to GitHub
- [ ] `.env` file NOT pushed (should be in `.gitignore`)
- [ ] Session files NOT pushed (should be in `.gitignore`)

---

## 📋 Koyeb Deployment Steps

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Koyeb deployment"
git push origin master
```

### Step 2: Create Koyeb App
1. Go to https://www.koyeb.com
2. Sign up / Log in
3. Click **"Create App"**
4. Select **"GitHub"** as deployment method
5. Authorize Koyeb to access your GitHub
6. Select your repository

### Step 3: Configure Build Settings
- **Builder**: Select **Docker**
- **Dockerfile path**: `Dockerfile` (default)
- **Port**: `8080` (should auto-detect from EXPOSE)

### Step 4: Add Environment Variables
Click "Add Variable" and add these:

| Variable Name | Value | Example |
|--------------|-------|---------|
| `API_ID` | Your API ID | `12345678` |
| `API_HASH` | Your API Hash | `abcdef1234567890abcdef1234567890` |
| `BOT_TOKEN` | Your Bot Token | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `URL` | Leave blank initially | Will update after deployment |

### Step 5: Deploy
1. Click **"Deploy"**
2. Wait for deployment to complete (2-5 minutes)
3. Copy your app URL (e.g., `https://my-bot-xyz.koyeb.app`)

### Step 6: Update URL Environment Variable
1. Go to your app settings in Koyeb
2. Update the `URL` environment variable with your app URL
3. **Important**: Redeploy the app for changes to take effect

---

## 🧪 Testing After Deployment

### 1. Check Health Endpoint
Open in browser: `https://your-app-name.koyeb.app/`

Expected response:
```json
{
  "status": "running",
  "service": "Telegram Stream Bot",
  "version": "1.0.0",
  "message": "Send a file to the bot to get a stream link."
}
```

### 2. Test Bot Commands
1. Open Telegram and find your bot
2. Send `/start` - Should get welcome message
3. Send a video/audio file
4. Bot should reply with a stream link
5. Copy the link and test in VLC:
   - VLC → Media → Open Network Stream
   - Paste the link
   - Click Play

---

## 🐛 Troubleshooting Common Issues

### Issue 1: Bot Not Responding
**Symptoms**: Bot doesn't reply to messages

**Solutions**:
1. Check Koyeb logs for errors
2. Verify all environment variables are set correctly
3. Make sure `URL` variable is set to your Koyeb app URL
4. Check if bot is running: `curl https://your-app.koyeb.app/`

### Issue 2: FloodWait Error
**Symptoms**: Logs show "FloodWait: Telegram requires a wait of X seconds"

**Solutions**:
- This is normal if you've been testing a lot
- The bot will automatically retry after the wait time
- Avoid frequent restarts/redeployments
- Wait for the specified time before trying again

### Issue 3: Stream Link Not Working
**Symptoms**: VLC can't play the stream link

**Solutions**:
1. Verify the `URL` environment variable is correct
2. Test the health endpoint first
3. Make sure the file is still in Telegram (not deleted)
4. Try a different file
5. Check if the link format is correct: `https://your-app.koyeb.app/stream/CHAT_ID/MESSAGE_ID`

### Issue 4: Database Locked Error
**Symptoms**: `sqlite3.OperationalError: database is locked`

**Solutions**:
- ✅ Already fixed! Bot uses in-memory storage (`in_memory=True`)
- Make sure `workers=1` in Dockerfile (already set)
- This shouldn't happen with current configuration

### Issue 5: Multiple Bot Instances
**Symptoms**: Bot replies multiple times to same message

**Solutions**:
- ✅ Already fixed! Using `workers=1` in Dockerfile
- Don't run the bot locally while it's deployed
- Only one instance should be running at a time

---

## 📊 Monitoring

### View Logs in Koyeb
1. Go to your app in Koyeb dashboard
2. Click on "Logs" tab
3. Look for:
   - `Bot Started in FastAPI Loop` ✅
   - `Bot Started!` ✅
   - Any error messages ❌

### Expected Log Output
```
INFO:     Started server process
INFO:     Waiting for application startup.
Bot Started in FastAPI Loop
Bot Started!
Loading commands plugin...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080
```

---

## 🔄 Updating Your Bot

When you make code changes:

1. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin master
   ```

2. **Koyeb auto-deploys**:
   - Koyeb will automatically detect the push
   - It will rebuild and redeploy your app
   - Wait 2-5 minutes for deployment

3. **Manual redeploy** (if auto-deploy is off):
   - Go to Koyeb dashboard
   - Click "Redeploy"

---

## 💡 Best Practices

1. **Don't commit sensitive data**:
   - Never push `.env` file
   - Never push session files
   - Use environment variables in Koyeb

2. **Test locally first**:
   ```bash
   python main.py
   ```
   - Make sure bot works locally before deploying

3. **Monitor logs regularly**:
   - Check for errors after deployment
   - Watch for FloodWait warnings

4. **Avoid frequent restarts**:
   - Telegram may rate-limit your bot
   - Only redeploy when necessary

5. **Keep dependencies updated**:
   - Regularly update `requirements.txt`
   - Test updates locally first

---

## 🎯 Quick Reference

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run bot locally
python main.py

# Test with ngrok (optional)
ngrok http 8080
# Update URL in .env to ngrok URL
```

### Git Commands
```bash
# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "Your message"

# Push to GitHub
git push origin master
```

### Useful Links
- Telegram API: https://my.telegram.org
- BotFather: https://t.me/BotFather
- Koyeb Dashboard: https://app.koyeb.com
- Your GitHub Repo: (add your repo URL here)

---

## ✨ Success Criteria

Your deployment is successful when:
- ✅ Health endpoint returns JSON response
- ✅ Bot responds to `/start` command
- ✅ Bot generates stream links for files
- ✅ VLC can play the stream links
- ✅ Seeking/resuming works in VLC
- ✅ No errors in Koyeb logs

---

**Last Updated**: 2025-11-22
**Bot Version**: 1.0.0
