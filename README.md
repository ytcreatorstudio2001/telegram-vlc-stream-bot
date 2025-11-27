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
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=00D9FF&center=true&vCenter=true&multiline=true&repeat=true&width=800&height=100&lines=Stream+Large+Media+Files+from+Telegram;Directly+to+VLC+Without+Downloading!;Fast+%E2%9A%A1+Secure+%F0%9F%94%92+Efficient+%F0%9F%9A%80" alt="Typing SVG" />
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

<div align="center">

## 🤖 About This Bot

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2000&pause=500&color=F75C7E&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=120&lines=%F0%9F%8E%AC+Your+Personal+Telegram+Media+Streamer;%E2%9A%A1+Lightning+Fast+%7C+%F0%9F%94%92+100%25+Secure;%F0%9F%93%B1+Works+on+Any+Device;%F0%9F%8E%AF+No+Downloads+%7C+Direct+Streaming" alt="About Bot" />

<p style="font-size: 16px; color: #888;">
This bot transforms how you consume media from Telegram. No more waiting for downloads!<br/>
Just send a file, get a link, and start streaming instantly in VLC or any media player.
</p>

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

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=00D9FF&center=true&vCenter=true&width=600&lines=%F0%9F%91%A8%E2%80%8D%F0%9F%92%BB+Created+by+Akhil+TG;%E2%9C%A8+Full+Stack+Developer;%F0%9F%9A%80+Open+Source+Enthusiast" alt="Developer" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=4000&pause=1000&color=F7B731&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=80&lines=%C2%A9+2025+Akhil+TG+-+All+Rights+Reserved;Made+with+%E2%9D%A4%EF%B8%8F+for+the+Telegram+Community" alt="Copyright" />

<br/>
<br/><p>
  <a href="https://github.com/yourusername">
    <img src="https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github" alt="GitHub"/>
  </a>
  <a href="https://t.me/yourusername">
    <img src="https://img.shields.io/badge/Telegram-Contact-blue?style=for-the-badge&logo=telegram" alt="Telegram"/>
  </a>
</p>

</div>

</div>

---

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&duration=2000&pause=800&color=5F27CD&center=true&vCenter=true&repeat=true&width=600&lines=%E2%AD%90+Star+this+repo+if+useful!;%F0%9F%92%99+Made+for+Telegram+Community;%F0%9F%9A%80+Happy+Streaming!" alt="Footer" />

</div>
