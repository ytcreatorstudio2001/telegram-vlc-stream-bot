# 👮‍♂️ Admin Panel Guide

Your bot now has a powerful Admin Panel to manage users and settings!

## 🛠️ Setup

1.  **Get your Telegram User ID**:
    *   Use a bot like `@userinfobot` to find your numeric ID (e.g., `123456789`).

2.  **Configure Admin**:
    *   Add your ID to the `ADMINS` variable in your environment or `.env` file.
    *   Example: `ADMINS=123456789 987654321` (space separated for multiple admins).

## 🚀 Usage

Send the command **/admin** to your bot in private chat.

### 📊 Dashboard Features

*   **Stats**: View the total number of users who have started your bot.
*   **Broadcast**: (Coming Soon) Send messages to all your users.
*   **Force Sub**: View the currently configured Force Subscribe channel.
*   **Change Banners**: View instructions on how to update the welcome banners.
*   **Restart Bot**: Remotely restart the bot instance.

## 📝 User Tracking

The bot now automatically tracks every user who sends `/start`.
*   Data is saved in `users.json`.
*   This allows you to see accurate user counts.

## 🔒 Force Subscription

To enable Force Subscription:
1.  Set the `FORCE_SUB_CHANNEL` variable in your environment.
    *   Example: `FORCE_SUB_CHANNEL=@MyChannel` or `FORCE_SUB_CHANNEL=-100123456789`.
2.  Make sure the bot is an **Admin** in that channel.
