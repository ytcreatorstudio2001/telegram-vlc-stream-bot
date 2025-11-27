<div align="center">

  <img src="assets/banner.gif" alt="Telegram VLC Stream Bot Banner" width="60%">

  <br>

  <a href="https://github.com/ytcreatorstudio2001/telegram-vlc-stream-bot">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=30&duration=3000&pause=1000&color=2CA5E0&center=true&vCenter=true&width=600&lines=Telegram+VLC+Stream+Bot;Stream+Movies+Directly;No+Downloads+Required;Fast+Simple+Secure" alt="Typing SVG" />
  </a>

  <br>

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>
  <img src="https://img.shields.io/badge/VLC-FF8800?style=for-the-badge&logo=videolan&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>

</div>

<br>

## 🚀 Overview

**Telegram VLC Stream Bot** is a high-performance bot designed to let you stream media files from Telegram directly to **VLC Media Player** (or any other player) without waiting for downloads to complete. It acts as a bridge, creating a streaming URL that pipes the file content in real-time.

---

## ✨ Features

<div align="center">

| Feature | Description |
| :--- | :--- |
| 🎬 **Instant Streaming** | Start watching immediately, no waiting for downloads. |
| 📁 **Universal Support** | Works with Videos, Audio, and Documents. |
| ⚡ **High Speed** | Optimized for fast buffering and low latency. |
| 🖥️ **Multi-Platform** | Compatible with PC, Android, iOS, and TV. |
| ⛔ **No Limits** | Supports large files (2GB+) with ease. |
| 🔐 **Secure** | Safe interaction with Telegram API. |
| ☁️ **Easy Deploy** | Ready for Koyeb, Heroku, and VPS. |

</div>

---

## 🛠️ Deployment

### One-Click Deploy (Koyeb)

<div align="center">
  <a href="https://app.koyeb.com/deploy?type=git&repository=github.com/ytcreatorstudio2001/telegram-vlc-stream-bot&branch=main&name=telegram-vlc-bot">
    <img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy to Koyeb" width="200"/>
  </a>
</div>

### Environment Variables

| Variable | Description |
| :--- | :--- |
| `API_ID` | Your Telegram API ID (from my.telegram.org) |
| `API_HASH` | Your Telegram API Hash (from my.telegram.org) |
| `BOT_TOKEN` | Your Bot Token (from @BotFather) |
| `URL` | The public URL of your app (e.g., `https://your-app.koyeb.app`) |

---

## 🧪 Local Development

Run the bot locally for testing or development.

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/ytcreatorstudio2001/telegram-vlc-stream-bot.git
    cd telegram-vlc-stream-bot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the bot:**
    ```bash
    python main.py
    ```

4.  **Expose locally (Optional):**
    ```bash
    ngrok http 8080
    ```

---

## 🏗️ Architecture

```mermaid
graph LR
    A[Telegram Cloud] -->|File Stream| B(Bot Server / FastAPI)
    B -->|HTTP Stream| C[VLC Player / User]
    D[User Command] -->|Request| B
```

---

## 👨‍💻 Author

<div align="center">
  <a href="https://github.com/ytcreatorstudio2001">
    <img src="https://img.shields.io/badge/GitHub-Akhil_TG-181717?style=for-the-badge&logo=github"/>
  </a>
  <a href="https://t.me/akhil_tg">
    <img src="https://img.shields.io/badge/Telegram-Contact_Me-2CA5E0?style=for-the-badge&logo=telegram"/>
  </a>
</div>

---

## ⭐ Support

If you find this project useful, please give it a star!

