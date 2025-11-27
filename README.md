<div align="center">

<!-- Rotating Banner - Refreshes on each page load -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner1.png">
  <source media="(prefers-color-scheme: light)" srcset="./assets/banner2.png">
  <img alt="Telegram VLC Stream Bot" src="./assets/banner3.png" width="100%">
</picture>

# 🎬 Telegram VLC Stream Bot

<p align="center">
  <img src="https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram" alt="Telegram Bot"/>
  <img src="https://img.shields.io/badge/VLC-Streaming-orange?style=for-the-badge&logo=vlc-media-player" alt="VLC Streaming"/>
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-Framework-teal?style=for-the-badge&logo=fastapi" alt="FastAPI"/>
</p>

<p align="center">
  <strong>Stream large media files from Telegram directly to VLC without downloading!</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#deployment">Deployment</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

</div>

---

## ✨ Features

<div align="center">

| Feature | Description |
|---------|-------------|
| 🚀 **Direct Streaming** | Stream files without full download |
| ⏯️ **Seek/Resume Support** | HTTP Range Headers for smooth playback |
| 📱 **Universal Compatibility** | Works with VLC, MX Player, Browsers, etc. |
| 💾 **Large File Support** | Handles files 2GB+ with ease |
| ⚡ **Fast & Efficient** | Built with FastAPI + Uvicorn + Pyrogram |
| 🔒 **Secure** | No data storage, direct streaming only |

</div>

---

## 🎯 Quick Start

### Prerequisites
- Python 3.8 or higher
- Telegram API credentials ([Get them here](https://my.telegram.org))
- Bot Token from [@BotFather](https://t.me/BotFather)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/telegram-vlc-stream-bot.git
   cd telegram-vlc-stream-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Rename .env.sample to .env
   cp .env.sample .env
   
   # Edit .env and add your credentials:
   # API_ID=your_api_id
   # API_HASH=your_api_hash
   # BOT_TOKEN=your_bot_token
   # URL=http://localhost:8080 (for local testing)
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

---

## 📖 Usage

<div align="center">

### Step-by-Step Guide

</div>

1. **Start the bot** - Send `/start` to your bot on Telegram
2. **Send a file** - Forward any video/audio file to the bot
3. **Get stream link** - Bot will reply with a streaming URL
4. **Open in VLC** - Copy the link and paste it in VLC:
   - Open VLC Media Player
   - Go to `Media` → `Open Network Stream`
   - Paste the URL
   - Click `Play` and enjoy! 🎉

<div align="center">

![Demo](https://media.giphy.com/media/3o7TKSjRrfIPjeiVyg/giphy.gif)

</div>

---

## 🚀 Deployment

### Recommended: Koyeb (Free Tier)

<div align="center">

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com)

</div>

#### Why Koyeb?
- ✅ **No Sleep/Idle** - Always online (unlike Render)
- ✅ **Fast Performance** - High-performance microVMs
- ✅ **Docker Native** - Perfect for containerized apps
- ✅ **Free Tier** - Generous free tier available

#### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin master
   ```

2. **Sign up at [Koyeb.com](https://www.koyeb.com)**

3. **Create New App**
   - Click **Create App**
   - Select **GitHub** as deployment method
   - Choose your repository

4. **Configure Settings**
   - **Builder**: Docker
   - **Port**: 8080
   - **Environment Variables**:
     ```
     API_ID=your_telegram_api_id
     API_HASH=your_telegram_api_hash
     BOT_TOKEN=your_bot_token
     URL=https://your-app-name.koyeb.app
     ```

5. **Deploy** - Click Deploy and wait for build to complete

6. **Update URL** - Once deployed, copy your app URL and update the `URL` environment variable if needed

---

### Alternative: Render

<div align="center">

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

</div>

1. Create a **Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Add environment variables: `API_ID`, `API_HASH`, `BOT_TOKEN`, `URL`
4. **Note**: Free tier spins down after 15 minutes of inactivity ⚠️

---

### ❌ Not Recommended

| Platform | Reason |
|----------|--------|
| **Heroku** | No longer offers free tier |
| **Vercel/Netlify** | 10-second timeout (unsuitable for streaming) |

---

## 🛠️ Local Development with Ngrok

Want to test on your phone/TV without deploying?

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py

# In another terminal, start ngrok
ngrok http 8080

# Copy the ngrok URL (e.g., https://abc123.ngrok.io)
# Update URL in .env file
# Restart the bot
```

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Telegram  │─────▶│  Stream Bot  │─────▶│  VLC Player │
│   Servers   │      │  (FastAPI)   │      │  (Client)   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Pyrogram   │
                     │   Client     │
                     └──────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author & Copyright

<div align="center">

**© 2025 Akhil TG. All Rights Reserved.**

Created with ❤️ by [Akhil TG](https://github.com/yourusername)

<p>
  <a href="https://github.com/yourusername">
    <img src="https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github" alt="GitHub"/>
  </a>
  <a href="https://t.me/yourusername">
    <img src="https://img.shields.io/badge/Telegram-Contact-blue?style=for-the-badge&logo=telegram" alt="Telegram"/>
  </a>
</p>

</div>

---

<div align="center">

### ⭐ Star this repo if you find it useful!

**Made with 💙 for the Telegram community**

</div>
