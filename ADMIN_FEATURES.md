# 🎛️ Admin Panel Features

## Quick Access
Send `/admin` to your bot in private chat to access the admin panel.

## 🌟 Feature Overview

### 📢 Broadcast Messages
Send announcements to all your users instantly!

**What you can broadcast:**
- 📝 Text messages
- 🖼️ Photos with captions
- 🎥 Videos with captions
- 📎 Documents
- 🎨 Stickers

**Live tracking shows:**
- ✅ Successfully sent
- ❌ Failed deliveries
- 🚫 Users who blocked the bot
- 📊 Real-time progress
- 📈 Final success rate

### 👥 User Management

**View Users**
- See all registered users
- Quick overview of user base
- Total count displayed

**Find User**
Get detailed info about any user:
```
👤 User Found

ID: 123456789
Name: John Doe
Username: @johndoe
Status: Premium
Bot: No
```

### 🖼️ Banner Management
Update your welcome banners without touching the server!

**Simple 3-step process:**
1. Click "Change Banners"
2. Send a photo with caption: `banner1`, `banner2`, `banner3`, or `banner`
3. Done! ✅

**Current banner status:**
- ✅ Shows which banners exist
- 📊 Displays file sizes
- ❌ Highlights missing banners

### 🔒 Force Subscription
Grow your channel while users enjoy the bot!

**Features:**
- View current channel configuration
- See channel name and member count
- Get setup instructions
- Format examples provided

**Setup:**
```env
FORCE_SUB_CHANNEL=@YourChannel
# or
FORCE_SUB_CHANNEL=-100123456789
```

### 📊 Statistics
Quick stats at your fingertips:
- Total registered users
- Bot status
- Force sub status

### 🔄 Bot Control
- Restart bot remotely
- Useful after config changes
- Graceful shutdown with notification

## 🎯 Command Reference

| Command | Action |
|---------|--------|
| `/admin` | Open admin panel |
| `/cancel` | Cancel current action |

## 🔐 Security

**Access Control:**
- Only authorized admins can access
- Configured via `ADMINS` environment variable
- Unauthorized attempts are blocked and logged

**Safe Operations:**
- Confirmation dialogs for critical actions
- Cancel option always available
- Clear feedback on all actions

## 💡 Pro Tips

### Broadcasting
1. **Test first**: Send to yourself before broadcasting
2. **Timing matters**: Broadcast during peak hours for better engagement
3. **Keep it short**: Users appreciate concise messages
4. **Use media**: Photos/videos get more attention than text

### Banner Management
1. **High quality**: Use clear, high-resolution images
2. **Consistent style**: Keep all banners visually cohesive
3. **Aspect ratio**: 4:3 works best for most devices
4. **File size**: Keep under 5MB for fast loading

### User Management
1. **Regular checks**: Monitor user growth weekly
2. **Clean inactive**: Remove users who blocked the bot
3. **Engage users**: Use broadcast for updates and engagement
4. **Privacy**: Respect user data and privacy

### Force Subscription
1. **Value first**: Make your channel worth joining
2. **Clear benefits**: Explain what users get
3. **Bot as admin**: Ensure bot has admin rights in channel
4. **Test it**: Verify it works before going live

## 📱 Mobile-Friendly

All admin features work perfectly on:
- 📱 Telegram mobile apps
- 💻 Telegram desktop
- 🌐 Telegram Web

## 🚀 Quick Start Guide

### First Time Setup
```bash
# 1. Get your Telegram User ID
# Use @userinfobot

# 2. Add to .env file
ADMINS=123456789 987654321

# 3. Restart bot
# Send /admin to test
```

### Daily Operations
```
Morning:
1. Check stats (/admin → Stats)
2. Review user growth

When needed:
- Broadcast announcements
- Update banners seasonally
- Find specific users
- Monitor force sub channel
```

## 🎨 Interface Preview

```
👮‍♂️ Admin Control Panel

📊 Total Users: 1,234
📢 Force Sub: @MyChannel
🤖 Bot Status: Running

Select an action below:

[📢 Broadcast] [📊 Stats]
[👥 View Users] [🔍 Find User]
[🖼️ Change Banners] [🔒 Force Sub]
[🔄 Restart Bot] [❌ Close]
```

## ❓ Troubleshooting

**Broadcast not working?**
- Check if users exist in database
- Verify bot isn't rate-limited
- Ensure proper permissions

**Can't upload banner?**
- Send as photo (not file)
- Include correct caption
- Check file format (PNG recommended)

**Force sub not enforcing?**
- Verify bot is channel admin
- Check channel ID format
- Ensure `FORCE_SUB_CHANNEL` is set

**User search fails?**
- Verify user ID is numeric
- Check if user exists in database
- Ensure user hasn't deleted account

## 🆘 Support

Need help? Check:
1. [Admin Panel Guide](ADMIN_PANEL_GUIDE.md)
2. [Implementation Details](ADMIN_PANEL_IMPLEMENTATION.md)
3. [Main README](README.md)

---

**Made with ❤️ by Akhil TG**  
© 2025 All Rights Reserved
