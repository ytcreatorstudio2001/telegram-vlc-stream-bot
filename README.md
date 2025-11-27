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
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
  }

  @keyframes color-change {
    0% { color: #4e54c8; }
    100% { color: #8f94fb; }
  }

  /* Animated typing SVG containers */
  img[src*="readme-typing-svg"] {
    border-radius: 8px;
    transition: all 0.3s ease;
  }

  img[src*="readme-typing-svg"]:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }

  /* Animated links */
  a {
    transition: all 0.3s ease;
    position: relative;
  }

  a:hover {
    color: #4e54c8 !important;
  }

  a::after {
    content: '';
    position: absolute;
    width: 100%;
    height: 1px;
    bottom: -2px;
    left: 0;
    background-color: #4e54c8;
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
    background: linear-gradient(to right, transparent, #4e54c8, transparent);
  }

  /* Subtle hover effect for feature table cells */
  td:hover, th:hover {
    background: rgba(78, 84, 200, 0.05) !important;
    transition: background 0.3s ease;
  }

  /* Subtle hover effect for deploy buttons */
  [src*="koyeb"], [src*="render"] {
    transition: all 0.3s ease;
  }

  [src*="koyeb"]:hover, [src*="render"]:hover {
    transform: scale(1.03);
  }

  /* Subtle glow for code blocks */
  code {
    background: #f4f4f4;
    color: #e74c3c;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
  }

  /* Subtle animation for the footer */
  img[src*="Footer"] {
    transition: all 0.5s ease;
  }

  img[src*="Footer"]:hover {
    transform: scale(1.05);
  }

  /* Enhanced badges */
  img[alt*="badge"] {
    transition: all 0.3s ease;
  }

  img[alt*="badge"]:hover {
    transform: scale(1.05);
  }

  /* Subtle hover effect for all images */
  img {
    transition: all 0.2s ease;
  }

  img:hover {
    transform: scale(1.02);
  }

  /* Subtle background */
  body {
    background-color: #ffffff;
    color: #333;
  }

  /* Subtle neon glow effect for headings */
  h1, h2, h3 {
    text-shadow: 0 0 3px rgba(78, 84, 200, 0.3);
  }

  /* Subtle hover effect for content containers */
  div[align="center"] {
    transition: transform 0.3s ease;
  }

  div[align="center"]:hover {
    transform: scale(1.005);
  }

  /* Subtle table styling */
  table {
    border-collapse: separate;
    border-spacing: 0;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
  }

  th, td {
    padding: 12px 15px;
  }

  th {
    background-color: #f8f9fa;
  }

  tr:nth-child(even) {
    background-color: #f8f9fa;
  }

  /* Subtle animation for the main title */
  div[align="center"]:first-child h1 {
    animation: titlePulse 4s infinite;
  }

  @keyframes titlePulse {
    0%, 100% { text-shadow: 0 0 5px rgba(78, 84, 200, 0.3); }
    50% { text-shadow: 0 0 10px rgba(78, 84, 200, 0.5); }
  }

  /* Subtle hover effect for emojis */
  span {
    transition: transform 0.2s ease;
  }

  span:hover {
    transform: scale(1.1);
  }

  /* Subtle gradient for special text */
  p[style*="color"] {
    background: linear-gradient(90deg, #4e54c8, #8f94fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* Subtle hover effect for feature icons */
  table img {
    transition: transform 0.3s ease;
  }

  table img:hover {
    transform: scale(1.05);
  }

  /* Subtle animation for badges */
  img[alt*="Telegram"], img[alt*="VLC"], img[alt*="Python"], img[alt*="FastAPI"] {
    transition: all 0.3s ease;
  }

  img[alt*="Telegram"]:hover, img[alt*="VLC"]:hover, img[alt*="Python"]:hover, img[alt*="FastAPI"]:hover {
    transform: scale(1.05);
    filter: brightness(1.1);
  }

  /* Subtle hover effect for links in the navigation */
  p[align="center"] a {
    transition: color 0.3s ease;
  }

  p[align="center"] a:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the about bot section */
  img[src*="About Bot"] {
    transition: all 0.3s ease;
  }

  img[src*="About Bot"]:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }

  /* Subtle animation for the developer section */
  img[src*="Developer"] {
    transition: all 0.5s ease;
  }

  img[src*="Developer"]:hover {
    transform: scale(1.05);
  }

  /* Subtle animation for the copyright section */
  img[src*="Copyright"] {
    transition: all 0.5s ease;
  }

  img[src*="Copyright"]:hover {
    transform: scale(1.05);
  }

  /* Subtle hover effect for GitHub and Telegram follow links */
  img[src*="github"], img[src*="telegram"] {
    transition: all 0.3s ease;
  }

  img[src*="github"]:hover, img[src*="telegram"]:hover {
    transform: scale(1.05);
    filter: brightness(1.2);
  }

  /* Subtle hover effect for architecture diagram */
  code {
    transition: all 0.3s ease;
  }

  code:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }

  /* Subtle hover effect for contributing section */
  li {
    transition: all 0.3s ease;
  }

  li:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the license section */
  a[href*="LICENSE"] {
    transition: all 0.3s ease;
  }

  a[href*="LICENSE"]:hover {
    color: #4e54c8;
  }

  /* Subtle animation for the author section */
  div[align="center"] > br + p a img {
    transition: all 0.3s ease;
  }

  div[align="center"] > br + p a img:hover {
    transform: scale(1.05);
  }

  /* Subtle hover effect for the footer */
  div[align="center"]:last-child img {
    transition: all 0.3s ease;
  }

  div[align="center"]:last-child img:hover {
    transform: scale(1.05);
  }

  /* Subtle hover effect for the quick start section */
  h3[id*="prerequisites"] {
    transition: all 0.3s ease;
  }

  h3[id*="prerequisites"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the deployment section */
  h3[id*="sign"] {
    transition: all 0.3s ease;
  }

  h3[id*="sign"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the architecture section */
  h3[id*="architecture"] {
    transition: all 0.3s ease;
  }

  h3[id*="architecture"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the contributing section */
  h3[id*="contributing"] {
    transition: all 0.3s ease;
  }

  h3[id*="contributing"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the license section */
  h3[id*="license"] {
    transition: all 0.3s ease;
  }

  h3[id*="license"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the author section */
  h3[id*="author"] {
    transition: all 0.3s ease;
  }

  h3[id*="author"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the usage section */
  h3[id*="step"] {
    transition: all 0.3s ease;
  }

  h3[id*="step"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the local development section */
  h3[id*="want"] {
    transition: all 0.3s ease;
  }

  h3[id*="want"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the not recommended section */
  h3[id*="not"] {
    transition: all 0.3s ease;
  }

  h3[id*="not"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the alternative render section */
  h3[id*="alternative"] {
    transition: all 0.3s ease;
  }

  h3[id*="alternative"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the recommended koyeb section */
  h3[id*="recommended"] {
    transition: all 0.3s ease;
  }

  h3[id*="recommended"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the features section */
  h3[id*="features"] {
    transition: all 0.3s ease;
  }

  h3[id*="features"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the about this bot section */
  h3[id*="about"] {
    transition: all 0.3s ease;
  }

  h3[id*="about"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the quick start section */
  h2[id*="quick"] {
    transition: all 0.3s ease;
  }

  h2[id*="quick"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the usage section */
  h2[id*="usage"] {
    transition: all 0.3s ease;
  }

  h2[id*="usage"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the deployment section */
  h2[id*="deployment"] {
    transition: all 0.3s ease;
  }

  h2[id*="deployment"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the local development section */
  h2[id*="local"] {
    transition: all 0.3s ease;
  }

  h2[id*="local"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the architecture section */
  h2[id*="architecture"] {
    transition: all 0.3s ease;
  }

  h2[id*="architecture"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the contributing section */
  h2[id*="contributing"] {
    transition: all 0.3s ease;
  }

  h2[id*="contributing"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the license section */
  h2[id*="license"] {
    transition: all 0.3s ease;
  }

  h2[id*="license"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the author section */
  h2[id*="author"] {
    transition: all 0.3s ease;
  }

  h2[id*="author"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the footer section */
  h2[id*="footer"] {
    transition: all 0.3s ease;
  }

  h2[id*="footer"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the features section */
  h2[id*="features"] {
    transition: all 0.3s ease;
  }

  h2[id*="features"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the about this bot section */
  h2[id*="about"] {
    transition: all 0.3s ease;
  }

  h2[id*="about"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the main title */
  h2[id*="telegram"] {
    transition: all 0.3s ease;
  }

  h2[id*="telegram"]:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for all h2 headings */
  h2 {
    transition: all 0.3s ease;
  }

  h2:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for all h3 headings */
  h3 {
    transition: all 0.3s ease;
  }

  h3:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for all headings */
  h1, h2, h3 {
    transition: all 0.3s ease;
  }

  h1:hover, h2:hover, h3:hover {
    color: #4e54c8;
  }

  /* Subtle hover effect for the main title container */
  div[align="center"]:first-child {
    transition: all 0.3s ease;
  }

  div[align="center"]:first-child:hover {
    box-shadow: 0 4px 12px rgba(78, 84, 200, 0.15);
  }

  /* Subtle hover effect for the banner container */
  div[style*="overflow: hidden"] {
    transition: all 0.3s ease;
  }

  div[style*="overflow: hidden"]:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }

  /* Subtle hover effect for all content containers */
  div[align="center"] {
    transition: all 0.3s ease;
  }

  div[align="center"]:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }

  /* Subtle hover effect for the feature table container */
  div[align="center"] > table {
    transition: all 0.3s ease;
  }

  div[align="center"] > table:hover {
    box-shadow: 0 4px 12px rgba(78, 84, 200, 0.15);
  }

  /* Enhanced code styling */
  code, pre {
    font-family: 'Fira Code', 'Courier New', monospace;
  }

  /* Responsive design */
  @media (max-width: 768px) {
    h1 {
      font-size: 2.5em;
    }

    table {
      display: block;
      overflow-x: auto;
    }
  }
</style>

# 🎥 Telegram VLC Stream Bot

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=32&duration=3000&pause=1000&color=4E54C8&center=true&vCenter=true&width=800&lines=%F0%9F%92%A5+Stream+your+files+from+Telegram+to+VLC+Player;Direct+streaming+from+Telegram+to+any+device!;Access+your+files+without+downloading!" alt="Main Title" />

<div class="badge-container" align="center" style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram" />
  <img src="https://img.shields.io/badge/VLC-FF8800?style=for-the-badge&logo=videolan&logoColor=white" alt="VLC" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />

</div>

<div align="center">

## 🤖 About This Bot

**Telegram VLC Stream Bot** allows you to stream any media file from your Telegram chat directly to VLC player or any other streaming application on your devices without downloading the entire file. This is especially useful for large files like movies, TV series, or documents.

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎬 **Direct Streaming** | Stream files directly without downloading |
| 📁 **File Support** | Support for all media file formats |
| 📱 **Multi-device** | Stream to any device with VLC or similar player |
| ⚡ **Fast Access** | Instant access to your Telegram files |
| 🔐 **Secure** | End-to-end encryption |
| 🚀 **No Limits** | No file size restrictions |
| 📖 **Document Preview** | View documents directly in browser |
| 🧩 **Easy Integration** | Simple setup and configuration |

---

## 🚀 Quick Start

### 📋 Prerequisites

- Telegram API ID and API Hash ([get it from my.telegram.org](https://my.telegram.org))
- Bot token from [@BotFather](https://t.me/BotFather)
- Docker or Python 3.8+

### 🛠️ Deployment

<div align="center">
  
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com)

</div>

### Step 1: Sign Up on Koyeb
1. Visit [Koyeb](https://app.koyeb.com) and create an account
2. Verify your email address

### Step 2: Deploy with One Click
1. Click the "Deploy to Koyeb" button above
2. Sign in to your Koyeb account
3. You'll be redirected to the deployment page

### Step 3: Configure Settings
1. **Builder**: Docker
2. **Port**: 8080
3. **Environment Variables**:
   ```
   API_ID=your_telegram_api_id
   API_HASH=your_telegram_api_hash
   BOT_TOKEN=your_bot_token
   URL=https://your-app-name.koyeb.app
   ```

### Step 4: Deploy
- Click Deploy and wait for build to complete

### Step 5: Update URL
- Once deployed, copy your app URL and update the `URL` environment variable if needed

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
<br/>
<p>
  <a href="https://github.com/your-username-here">
    <img src="https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github" alt="GitHub"/>
  </a>
  <a href="https://t.me/your-username-here">
    <img src="https://img.shields.io/badge/Telegram-Contact-blue?style=for-the-badge&logo=telegram" alt="Telegram"/>
  </a>
</p>

</div>

---

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&duration=2000&pause=800&color=5F27CD&center=true&vCenter=true&repeat=true&width=600&lines=%E2%AD%90+Star+this+repo+if+useful!;%F0%9F%92%99+Made+for+Telegram+Community;%F0%9F%9A%80+Happy+Streaming!" alt="Footer" />

</div>

</div>