# 🔐 Koyeb Environment Variables

## Copy these to Koyeb when deploying

### 1. API_ID
**Where to get:** https://my.telegram.org → API Development Tools
**Format:** Numbers only (e.g., `12345678`)
**Your value:**
```
[PASTE YOUR API_ID HERE]
```

---

### 2. API_HASH
**Where to get:** https://my.telegram.org → API Development Tools
**Format:** 32-character alphanumeric string
**Your value:**
```
[PASTE YOUR API_HASH HERE]
```

---

### 3. BOT_TOKEN
**Where to get:** @BotFather on Telegram → /newbot or /token
**Format:** `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
**Your value:**
```
[PASTE YOUR BOT_TOKEN HERE]
```

---

### 4. URL
**When to set:** AFTER first deployment
**Format:** `https://your-app-name.koyeb.app`
**Your value:**
```
[PASTE YOUR KOYEB APP URL HERE AFTER DEPLOYMENT]
```

---

## 📋 Quick Copy Format for Koyeb

Once you have all values, add them in Koyeb like this:

| Variable | Value |
|----------|-------|
| API_ID | [your_api_id] |
| API_HASH | [your_api_hash] |
| BOT_TOKEN | [your_bot_token] |
| URL | [leave blank initially] |

---

## ⚠️ Important Notes

1. **Don't add quotes** around the values in Koyeb
2. **API_ID** should be numbers only (no quotes, no spaces)
3. **URL** should be left blank on first deployment, then updated after you get your app URL
4. **Never commit this file** if you fill in the actual values
5. After adding/changing variables, you must **redeploy** the app

---

## 🔍 How to Get Your Credentials

### Getting API_ID and API_HASH:
1. Go to https://my.telegram.org
2. Log in with your phone number
3. Click on "API Development Tools"
4. Fill in the form:
   - App title: `Telegram Stream Bot` (or any name)
   - Short name: `streambot` (or any short name)
   - Platform: `Other`
5. Click "Create application"
6. You'll see your **API_ID** and **API_HASH**
7. Copy both values

### Getting BOT_TOKEN:
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot` (if creating new bot) or `/mybots` (if bot exists)
4. Follow the prompts to create/select your bot
5. Copy the **bot token** (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

---

## ✅ Verification

Before deploying, verify:
- [ ] API_ID is numbers only
- [ ] API_HASH is 32 characters
- [ ] BOT_TOKEN has the format `numbers:letters`
- [ ] You have all 3 credentials ready
- [ ] You know you'll add URL after first deployment

---

**Ready to deploy?** Follow the steps in `KOYEB_QUICK_DEPLOY.md`!
