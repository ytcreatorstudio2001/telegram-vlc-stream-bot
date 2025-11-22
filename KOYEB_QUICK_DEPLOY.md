# 🚀 Koyeb Quick Deploy Guide

## ✅ Pre-Deployment Checklist

Before you start, make sure you have:
- [x] Code pushed to GitHub ✅
- [ ] Koyeb account (sign up at https://www.koyeb.com)
- [ ] Your Telegram credentials ready:
  - `API_ID` from https://my.telegram.org
  - `API_HASH` from https://my.telegram.org
  - `BOT_TOKEN` from @BotFather

---

## 📝 Step-by-Step Deployment

### Step 1: Sign In to Koyeb
1. Go to https://app.koyeb.com
2. Sign in with GitHub (recommended) or email
3. Complete the sign-up process if new user

### Step 2: Create New App
1. Click **"Create App"** button (usually top-right)
2. Or click **"Deploy"** if you see that option

### Step 3: Select Deployment Method
1. Choose **"GitHub"** as the deployment source
2. If first time:
   - Click **"Connect GitHub"**
   - Authorize Koyeb to access your repositories
3. Select your repository: **`telegram-vlc-stream-bot`**
4. Select branch: **`master`**

### Step 4: Configure Builder
1. **Builder**: Select **"Docker"** (Koyeb should auto-detect from Dockerfile)
2. **Dockerfile path**: Leave as `Dockerfile` (default)
3. **Build context**: Leave as `/` (root)

### Step 5: Configure Instance
1. **Instance type**: Select **"Free"** (or your preferred tier)
2. **Regions**: Choose closest to you (e.g., Frankfurt, Washington)
3. **Scaling**: Leave as **1 instance** (important!)

### Step 6: Configure Ports
1. Koyeb should auto-detect port **8080** from Dockerfile
2. If not, manually set:
   - **Port**: `8080`
   - **Protocol**: `HTTP`

### Step 7: Add Environment Variables
Click **"Add Variable"** and add these **4 variables**:

| Variable Name | Value | Where to Get |
|--------------|-------|--------------|
| `API_ID` | Your API ID (numbers only) | https://my.telegram.org |
| `API_HASH` | Your API Hash (32 chars) | https://my.telegram.org |
| `BOT_TOKEN` | Your bot token | @BotFather on Telegram |
| `URL` | Leave **BLANK** for now | Will add after deployment |

**Important Notes:**
- `API_ID` should be numbers only (e.g., `12345678`)
- `API_HASH` is a 32-character string
- `BOT_TOKEN` format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
- Don't add quotes around values

### Step 8: Name Your App
1. **App name**: Choose a name (e.g., `telegram-stream-bot`)
2. This will be part of your URL: `https://your-app-name.koyeb.app`
3. Name must be unique across all Koyeb

### Step 9: Deploy!
1. Review all settings
2. Click **"Deploy"** button
3. Wait for deployment (usually 2-5 minutes)

### Step 10: Get Your App URL
1. Once deployed, you'll see your app URL
2. It will be something like: `https://telegram-stream-bot-xyz.koyeb.app`
3. **Copy this URL!**

### Step 11: Update URL Environment Variable
1. Go to your app **Settings** → **Environment Variables**
2. Find the `URL` variable (or add it if you skipped it)
3. Set value to your app URL (e.g., `https://telegram-stream-bot-xyz.koyeb.app`)
4. **Save** changes
5. **Redeploy** the app (click Redeploy button)

### Step 12: Verify Deployment
1. Open your app URL in browser: `https://your-app.koyeb.app/`
2. You should see:
   ```json
   {
     "status": "running",
     "service": "Telegram Stream Bot",
     "version": "1.0.0",
     "message": "Send a file to the bot to get a stream link."
   }
   ```
3. If you see this, **deployment is successful!** ✅

---

## 🧪 Testing Your Bot

### Test 1: Health Check
Open in browser: `https://your-app.koyeb.app/`

Expected: JSON response with status "running"

### Test 2: Bot Commands
1. Open Telegram
2. Search for your bot (the username you set with @BotFather)
3. Send `/start`
4. Expected: Welcome message

### Test 3: File Streaming
1. Send a video or audio file to your bot
2. Bot should reply with a stream link
3. Copy the link
4. Open VLC → Media → Open Network Stream
5. Paste the link and click Play
6. Video should start playing! 🎉

---

## 🔍 Monitoring & Logs

### View Logs
1. Go to your app in Koyeb dashboard
2. Click **"Logs"** tab
3. Look for:
   - ✅ `Bot Started in FastAPI Loop`
   - ✅ `Bot Started!`
   - ✅ `Loading commands plugin...`
   - ✅ `Uvicorn running on http://0.0.0.0:8080`

### Expected Log Output
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
Bot Started in FastAPI Loop
Bot Started!
Loading commands plugin...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

### Common Log Messages

**✅ Good Messages:**
- `Bot Started!` - Bot connected successfully
- `Application startup complete` - Server ready
- `Received /start from USER_ID` - Bot receiving commands

**⚠️ Warning Messages:**
- `FloodWait: Telegram requires a wait of X seconds` - Normal, bot will retry
- `Retrying in 5 seconds...` - Normal retry behavior

**❌ Error Messages:**
- `API_ID, API_HASH, or BOT_TOKEN not found` - Check environment variables
- `Failed to start bot` - Check credentials
- `Connection refused` - Check network/firewall

---

## 🐛 Troubleshooting

### Issue: Bot not responding
**Check:**
1. Is the app running? (Check Koyeb dashboard)
2. Are environment variables set correctly?
3. Is `URL` variable set to your Koyeb app URL?
4. Check logs for errors

**Fix:**
- Verify all 4 environment variables are set
- Make sure `URL` matches your actual app URL
- Redeploy after changing environment variables

### Issue: "FloodWait" in logs
**This is normal!** It happens when:
- You've been testing a lot
- Multiple login attempts
- Telegram rate limiting

**Fix:**
- Wait for the specified time (bot does this automatically)
- Avoid frequent redeployments
- Don't run bot locally while deployed

### Issue: Stream link not working
**Check:**
1. Is the health endpoint working? (`https://your-app.koyeb.app/`)
2. Is the `URL` environment variable correct?
3. Is the file still in Telegram?

**Fix:**
- Test health endpoint first
- Verify `URL` variable matches your app URL exactly
- Try with a different file
- Check link format: `https://your-app.koyeb.app/stream/CHAT_ID/MESSAGE_ID`

### Issue: App keeps restarting
**Check logs for:**
- Missing environment variables
- Invalid credentials
- Port binding issues

**Fix:**
- Verify all environment variables
- Check credentials are correct
- Make sure port is 8080

---

## 🎯 Success Checklist

Your deployment is successful when:
- [x] Code pushed to GitHub
- [ ] App deployed on Koyeb (status: Running)
- [ ] Health endpoint returns JSON response
- [ ] Bot responds to `/start` command
- [ ] Bot generates stream links for files
- [ ] VLC can play the stream links
- [ ] Seeking/resuming works in VLC
- [ ] No errors in logs

---

## 📞 Quick Reference

### Your Repository
https://github.com/ytcreatorstudio2001/telegram-vlc-stream-bot

### Your App URL (after deployment)
`https://YOUR-APP-NAME.koyeb.app`

### Environment Variables Needed
```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
URL=https://YOUR-APP-NAME.koyeb.app
```

### Test Endpoints
- Health: `https://YOUR-APP-NAME.koyeb.app/`
- Stream: `https://YOUR-APP-NAME.koyeb.app/stream/{chat_id}/{message_id}`

---

## 🎉 You're All Set!

Once deployed and tested successfully, your bot will:
- ✅ Run 24/7 on Koyeb
- ✅ Auto-deploy when you push to GitHub
- ✅ Handle file streaming from Telegram
- ✅ Work with VLC and other media players
- ✅ Support seeking and resuming
- ✅ Handle large files (2GB+)

**Enjoy your streaming bot!** 🚀

---

**Need Help?** Check `DEPLOYMENT_CHECKLIST.md` for more detailed troubleshooting.
