<div align="center">

<!-- Scrolling Banner -->
<div style="width: 100%; overflow: hidden; height: 200px;">
  <div style="display: inline-block; white-space: nowrap; animation: scroll-banner 30s linear infinite;">
    <img src="./assets/banner.gif" alt="Telegram VLC Stream Bot Banner" style="display: inline-block; height: 200px;">
    <img src="./assets/banner.gif" alt="Telegram VLC Stream Bot Banner" style="display: inline-block; height: 200px;">
  </div>
</div>

<style>
  @keyframes scroll-banner {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
  }

  /* Header animation */
  h1 {
    animation: color-change 8s infinite alternate;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  }

  @keyframes color-change {
    0% { color: #4e54c8; }
    25% { color: #8f94fb; }
    50% { color: #ff6b6b; }
    75% { color: #4ecdc4; }
    100% { color: #ff9a76; }
  }

  /* Animated badges */
  img[alt*="badge"] {
    transition: all 0.3s ease;
    animation: float 3s ease-in-out infinite;
  }

  img[alt*="badge"]:hover {
    transform: scale(1.1);
  }

  @keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-5px); }
    100% { transform: translateY(0px); }
  }

  /* Animated typing SVG containers */
  img[src*="readme-typing-svg"] {
    border-radius: 10px;
    animation: glow 2s ease-in-out infinite alternate;
  }

  @keyframes glow {
    from { box-shadow: 0 5px #fff, 0 0 10px #3498db, 0 0 15px #3498db; }
    to { box-shadow: 0 0 10px #fff, 0 0 20px #3498db, 0 0 30px #3498db; }
  }

  /* Animated table rows */
  table tr:nth-child(even) {
    animation: fadeIn 1s ease-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Animated links */
  a {
    transition: all 0.3s ease;
    position: relative;
  }

  a:hover {
    color: #ff6b6b !important;
    text-shadow: 0 0 5px rgba(255, 107, 107, 0.7);
  }

  a::after {
    content: '';
    position: absolute;
    width: 100%;
    height: 2px;
    bottom: -2px;
    left: 0;
    background-color: #ff6b6b;
    visibility: hidden;
    transform: scaleX(0);
    transition: all 0.3s ease;
  }

  a:hover::after {
    visibility: visible;
    transform: scaleX(1);
  }

  /* Animated section dividers */
  hr {
    border: 0;
    height: 1px;
    background: linear-gradient(to right, transparent, #3498db, transparent);
    animation: slideIn 1s ease-out;
  }

  @keyframes slideIn {
    from { width: 0%; }
    to { width: 100%; }
  }

  /* Animated content containers */
  div[align="center"] {
    transition: transform 0.3s ease;
  }

  div[align="center"]:hover {
    transform: scale(1.01);
  }

  /* Pulse animation for buttons */
  [src*="deploy"] {
    transition: all 0.3s ease;
  }

  [src*="deploy"]:hover {
    transform: scale(1.05);
    filter: brightness(1.2);
  }

  /* Fade-in animation for page load */
  body > div {
    animation: fadeInUp 1s ease-out;
  }

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Bounce animation for emojis */
  span, img {
    transition: transform 0.2s ease;
  }

  span:hover, img:hover:not([src*="readme-typing-svg"]):not([src*="deploy"]):not([alt*="badge"]) {
    transform: scale(1.1);
  }

  /* Breathing animation for the footer */
  [src*="readme-typing-svg"]:last-child {
    animation: breathe 4s ease-in-out infinite;
  }

  @keyframes breathe {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
  }

  /* Glowing effect for special elements */
  [src*="github.com"] {
    filter: drop-shadow(0 0 3px rgba(255, 215, 0, 0.7));
  }

  /* Animated code blocks */
  code {
    background: linear-gradient(45deg, #1a1a2e, #16213e);
    color: #00d9ff;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    animation: codeGlow 3s ease-in-out infinite alternate;
  }

  @keyframes codeGlow {
    from { box-shadow: 0 0 2px rgba(0, 217, 25, 0.5); }
    to { box-shadow: 0 0 8px rgba(0, 217, 255, 0.8); }
  }

  /* Animated table */
  table {
    border-collapse: separate;
    border-spacing: 0 10px;
    animation: tableSlide 1s ease-out;
  }

  @keyframes tableSlide {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }

  /* Pulse animation for feature icons */
  table img {
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
  }

  /* Slide-in for quick start section */
  h3[id*="quick"] {
    animation: slideInLeft 1s ease-out;
  }

  @keyframes slideInLeft {
    from { transform: translateX(-30px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }

  /* Slide-in for other headings */
  h2 {
    animation: slideInDown 1s ease-out;
  }

  @keyframes slideInDown {
    from { transform: translateY(-30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }

  /* Rotate animation for the copyright section */
  [src*="developer"] {
    animation: rotate 20s linear infinite;
  }

  @keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  /* Shimmer effect for special text */
  p[style*="color"] {
    background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ffeaa7);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient 8s ease infinite;
  }

  @keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }

  /* Floating effect for badges */
  img[alt*="Telegram"], img[alt*="VLC"], img[alt*="Python"], img[alt*="FastAPI"] {
    animation: floatBadge 3s ease-in-out infinite;
  }

  @keyframes floatBadge {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
  }

  /* Delayed animations for elements */
  img[src*="readme-typing-svg"]:nth-child(2) {
    animation-delay: 0.5s;
  }

  img[src*="readme-typing-svg"]:nth-child(3) {
    animation-delay: 1s;
  }

  img[src*="readme-typing-svg"]:nth-child(4) {
    animation-delay: 1.5s;
  }

  /* Hover effect for feature table cells */
  td:hover, th:hover {
    background: rgba(52, 152, 219, 0.2) !important;
    transition: background 0.3s ease;
  }

  /* Pulse animation for the star message */
  img[src*="Footer"] {
    animation: pulseFooter 3s infinite;
  }

  @keyframes pulseFooter {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
  }

  /* Gradient border animation */
  div[align="center"]:not(:first-child):not(:last-child) {
    position: relative;
  }

  div[align="center"]:not(:first-child):not(:last-child)::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #3498db, transparent);
    animation: borderSlide 3s linear infinite;
  }

  @keyframes borderSlide {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }

  /* Enhanced hover effects for deploy buttons */
  [src*="koyeb"], [src*="render"] {
    transition: all 0.4s ease;
  }

  [src*="koyeb"]:hover, [src*="render"]:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 10px 20px rgba(0,0,0.2);
  }

  /* Animated scroll indicator */
  body::after {
    content: '⬇️';
    position: fixed;
    right: 20px;
    top: 50%;
    animation: bounceScrollIndicator 2s infinite;
    z-index: 9999;
    opacity: 0.7;
  }

  @keyframes bounceScrollIndicator {
    0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
    40% {transform: translateY(-20px);}
    60% {transform: translateY(-10px);}
  }

  /* Sparkle effect for special elements */
  [src*="star"], [src*="heart"] {
    animation: sparkle 1.5s infinite alternate;
  }

  @keyframes sparkle {
    0% { filter: brightness(1) drop-shadow(0 2px gold); }
    100% { filter: brightness(1.5) drop-shadow(0 0 8px gold); }
  }

  /* Neon glow effect for headings */
  h1, h2, h3 {
    text-shadow: 0 0 5px rgba(52, 152, 219, 0.7);
  }

  /* Wave animation for horizontal rules */
  hr {
    position: relative;
    overflow: hidden;
  }

  hr::after {
    content: '';
    position: absolute;
    top: 0;
    left: -10%;
    width: 20%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: wave 2s linear infinite;
  }

  @keyframes wave {
    0% { left: -10%; }
    100% { left: 100%; }
  }

  /* Enhanced hover effect for all images */
  img {
    transition: all 0.3s ease;
  }

  img:hover {
    transform: scale(1.02);
    z-index: 100;
  }

  /* Pulsing effect for the main title */
  div[align="center"]:first-child h1 {
    animation: titlePulse 3s infinite;
  }

  @keyframes titlePulse {
    0% { text-shadow: 0 0 5px rgba(78, 84, 200, 0.5); }
    50% { text-shadow: 0 0 20px rgba(78, 84, 200, 0.8), 0 0 30px rgba(142, 148, 251, 0.6); }
    100% { text-shadow: 0 0 5px rgba(78, 84, 200, 0.5); }
  }

  /* Animated background gradient */
  body {
    background: linear-gradient(-45deg, #091428, #1a1a2e, #16213e, #091428);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #ecf0f1;
  }

  @keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }

  /* Parallax effect for banner */
  .banner-container {
    transform: translateZ(0);
    will-change: transform;
  }

  /* Animated loading effect for content */
  * {
    opacity: 0;
    animation: fadeInContent 0.8s ease-in forwards;
  }

  @keyframes fadeInContent {
    to {
      opacity: 1;
    }
  }

  /* Staggered animation delays */
  *:nth-child(2) { animation-delay: 0.1s; }
  *:nth-child(3) { animation-delay: 0.2s; }
  *:nth-child(4) { animation-delay: 0.3s; }
  *:nth-child(5) { animation-delay: 0.4s; }
  *:nth-child(6) { animation-delay: 0.5s; }
  *:nth-child(7) { animation-delay: 0.6s; }
  *:nth-child(8) { animation-delay: 0.7s; }
  *:nth-child(9) { animation-delay: 0.8s; }
  *:nth-child(10) { animation-delay: 0.9s; }
</style>

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
