##############################
# 📄 README.md (PASTE THIS) #
##############################

<!-- Animated Banner -->
<p align="center">
  <img src="./assets/banner-scroll.svg" width="100%" />
</p>

<!-- Animated Title -->
<p align="center">
  <img src="./assets/title-animated.svg" width="80%" />
</p>

<!-- Typing Animation -->
<p align="center">
  <img src="./assets/typing.svg" width="80%" />
</p>

<!-- Badges -->
<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>
  <img src="https://img.shields.io/badge/VLC-FF8800?style=for-the-badge&logo=videolan&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
</div>

---

# 🎥 Telegram VLC Stream Bot

A fast and reliable bot that lets you **stream Telegram media files directly on VLC** or any video player **without downloading**.

---

# ✨ Features

| Feature | Description |
|--------|-------------|
| 🎬 Instant Streaming | No downloads — direct streaming |
| 📁 Supports All Files | Video, audio, documents |
| ⚡ Fast Access | Streams start immediately |
| 🖥 Multi-Device | Works on TV, PC, VLC, Android, iOS |
| ⛔ No Size Limits | Stream large Telegram files |
| 🔐 Fully Secure | Uses Telegram API safely |
| 🚀 Easy Deployment | One-click cloud deploy |

---

# 🚀 Deployment (Koyeb)

<p align="center">
  <a href="https://app.koyeb.com">
    <img src="https://www.koyeb.com/static/images/deploy/button.svg" />
  </a>
</p>

### Environment Variables:
```
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN
URL=https://your-app.koyeb.app
```

---

# 🧪 Local Development

```bash
pip install -r requirements.txt
python main.py
```

Expose locally:

```bash
ngrok http 8080
```

---

# 🏗 Architecture

```
Telegram → FastAPI Backend → Pyrogram → VLC Player
```

---

# 🤝 Contributing

- Report issues  
- Suggest features  
- Submit PRs  

---

# 📝 License  
MIT License

---

# 👨‍💻 Author

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=00D9FF&center=true&vCenter=true&width=600&lines=Created+by+Akhil+TG;Full+Stack+Developer;Open+Source+Enthusiast" />
</p>

<p align="center">
  <a href="https://github.com/ytcreatorstudio2001">
    <img src="https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github"/>
  </a>
  <a href="https://t.me/your-telegram-link">
    <img src="https://img.shields.io/badge/Telegram-Contact-blue?style=for-the-badge&logo=telegram"/>
  </a>
</p>

---

# ⭐ Support  
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&duration=2000&pause=800&color=5F27CD&center=true&vCenter=true&repeat=true&width=600&lines=⭐+Star+this+repo+if+you+found+it+useful!;🚀+Happy+Streaming!" />
</p>



##################################
# 📁 /assets/banner-scroll.svg   #
##################################
<svg xmlns="http://www.w3.org/2000/svg"
     width="100%" height="200"
     viewBox="0 0 2000 200"
     preserveAspectRatio="xMinYMid slice">

  <defs>
    <image id="gif" href="banner.gif" width="2000" height="200"/>
  </defs>

  <use href="#gif">
    <animate attributeName="x"
             from="0" to="-2000"
             dur="22s"
             repeatCount="indefinite"/>
  </use>

  <use href="#gif" x="2000">
    <animate attributeName="x"
             from="2000" to="0"
             dur="22s"
             repeatCount="indefinite"/>
  </use>

</svg>



##################################
# 📁 /assets/title-animated.svg  #
##################################
<svg width="900" height="90" xmlns="http://www.w3.org/2000/svg">
  <text x="50%" y="50%" dy=".3em"
        text-anchor="middle"
        font-family="Fira Code"
        font-size="48"
        fill="#4e54c8">
    Telegram VLC Stream Bot
    <animate attributeName="fill"
             values="#4e54c8;#8f94fb;#4e54c8"
             dur="6s"
             repeatCount="indefinite"/>
  </text>
</svg>



##################################
# 📁 /assets/typing.svg          #
##################################
<svg width="1000" height="60" xmlns="http://www.w3.org/2000/svg">
  <text x="50%" y="50%" dy=".35em"
        text-anchor="middle"
        fill="none"
        stroke="#4e54c8"
        stroke-width="1.5"
        font-family="Fira Code"
        font-size="32">
    Stream your Telegram files instantly!
    <animate attributeName="stroke-dasharray"
             from="0,800" to="800,0"
             dur="4s"
             repeatCount="indefinite"/>
  </text>
</svg>
