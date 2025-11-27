# 👮‍♂️ Admin Panel Guide

Your bot now has a powerful Admin Panel to manage users, settings, and content!

## 🛠️ Setup

1.  **Get your Telegram User ID**:
    *   Use a bot like `@userinfobot` to find your numeric ID (e.g., `123456789`).

2.  **Configure Admin**:
    *   Add your ID to the `ADMINS` variable in your environment or `.env` file.
    *   Example: `ADMINS=123456789 987654321` (space separated for multiple admins).

## 🚀 Usage

Send the command **/admin** to your bot in private chat.

### 📊 Dashboard Features

#### 1. **📊 Stats**
*   View the total number of users who have started your bot.
*   Quick popup showing current user count.

#### 2. **📢 Broadcast**
*   Send messages to all your users at once!
*   **How to use:**
    1. Click "📢 Broadcast" button
    2. Send the message you want to broadcast (text, photo, video, document, sticker)
    3. Confirm the broadcast
    4. Watch real-time progress as messages are sent
*   **Features:**
    - Real-time progress tracking
    - Success/failure/blocked user statistics
    - Automatic FloodWait handling
    - Final success rate report

#### 3. **👥 View Users**
*   See a list of all registered users
*   Displays first 20 user IDs
*   Shows total user count

#### 4. **🔍 Find User**
*   Search for specific users by their ID
*   Get detailed user information:
    - User ID
    - Full name
    - Username
    - Premium status
    - Bot status

#### 5. **🖼️ Change Banners**
*   Update welcome message banners directly from Telegram!
*   **How to use:**
    1. Click "🖼️ Change Banners"
    2. View current banner status (file size, exists/missing)
    3. Send a photo with caption: `banner`, `banner1`, `banner2`, or `banner3`
    4. The banner will be automatically saved and used in welcome messages
*   **Supported banners:**
    - `banner.png` - Main banner
    - `banner1.png` - Alternate banner 1
    - `banner2.png` - Alternate banner 2
    - `banner3.png` - Alternate banner 3

#### 6. **🔒 Force Subscription**
*   View current Force Subscribe channel configuration
*   See channel name and member count (if accessible)
*   Get instructions on how to update the channel
*   **To enable/change:**
    1. Set `FORCE_SUB_CHANNEL` in your environment variables
    2. Format: `@YourChannel` or `-100123456789`
    3. Make sure the bot is an **Admin** in that channel

#### 7. **🔄 Restart Bot**
*   Remotely restart the bot instance
*   Useful after configuration changes
*   **Note:** May take a few seconds to come back online

## 📝 User Tracking

The bot automatically tracks every user who sends `/start`.
*   Data is saved in MongoDB (if configured) or `users.json` (fallback)
*   This allows you to see accurate user counts and broadcast to all users

## 🎯 Admin Commands

*   `/admin` - Open admin control panel
*   `/cancel` - Cancel any ongoing admin action (broadcast, find user, banner upload)

## 🔐 Security

*   Only users listed in `ADMINS` can access the admin panel
*   Unauthorized users receive an error message
*   All admin actions are logged

## 💡 Tips

*   **Broadcast wisely** - Test with a small group first
*   **Update banners** - Keep your welcome message fresh with new images
*   **Monitor stats** - Check user growth regularly
*   **Force Sub** - Great for building your channel community

## ⚠️ Important Notes

*   Broadcast messages cannot be undone - double-check before confirming
*   Banner images should be in PNG format for best quality
*   Force Subscribe requires the bot to be a channel admin
*   User data is persistent only if MongoDB is configured

