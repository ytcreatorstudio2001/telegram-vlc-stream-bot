# Telegram Media Streaming Bot

This bot allows you to stream large files (video/audio) from Telegram directly to VLC or any media player without downloading them fully to your device.

## Features
- Stream files without full download (Direct Streaming).
- Supports Seek/Resume (HTTP Range Headers).
- Works with VLC, MX Player, Browser, etc.
- Handles large files (2GB+).
- Deployed with FastAPI + Uvicorn + Pyrogram.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   - Rename `.env.sample` to `.env`.
   - Fill in your `API_ID`, `API_HASH`, and `BOT_TOKEN`.
   - `API_ID` and `API_HASH` can be obtained from [my.telegram.org](https://my.telegram.org).
   - `BOT_TOKEN` from [@BotFather](https://t.me/BotFather).

3. **Run the Bot**
   ```bash
   python main.py
   ```

4. **Usage**
   - Start the bot: `/start`
   - Forward a file to the bot or reply to a file with `/stream`.
   - Copy the generated link.
   - Open VLC -> Media -> Open Network Stream -> Paste Link -> Play.

## 🚀 Deployment (Recommended: Koyeb)

### Why Koyeb?
Koyeb is currently the best free-tier option for this bot because:
- **No Sleep/Idle**: Unlike Render, it doesn't spin down after inactivity (in the free tier, though check current terms).
- **Fast**: High-performance microVMs.
- **Docker Native**: Works perfectly with our Dockerfile.

### 1. Deploy to Koyeb
1.  **Push to GitHub**: Make sure this code is in a GitHub repository.
2.  **Sign Up**: Go to [Koyeb.com](https://www.koyeb.com) and sign up.
3.  **Create App**:
    - Click **Create App**.
    - Select **GitHub** as the deployment method.
    - Choose your repository (`Telegram-VLC-Stream-Bot`).
4.  **Configure**:
    - **Builder**: Select **Docker**.
    - **Privileged**: Leave unchecked (not needed).
    - **Environment Variables** (Click "Add Variable"):
        - `API_ID`: Your Telegram API ID.
        - `API_HASH`: Your Telegram API Hash.
        - `BOT_TOKEN`: Your Bot Token.
        - `URL`: Leave blank for now, or set to `https://<your-app-name>.koyeb.app` if you know it.
5.  **Deploy**: Click **Deploy**.
6.  **Final Step**: Once deployed, copy your App's public URL (e.g., `https://my-bot-123.koyeb.app`) and update the `URL` environment variable in Koyeb settings if you haven't already. Redeploy if you changed it.

### Alternative: Render
If you prefer Render:
1. Create a "Web Service" on [Render](https://render.com).
2. Connect your repo.
3. Add Env Vars: `API_ID`, `API_HASH`, `BOT_TOKEN`, `URL`.
4. **Note**: Render Free Tier spins down after 15 mins of inactivity.

### ❌ NOT Recommended
*   **Heroku**: No longer free.
*   **Vercel / Netlify**: Will timeout after 10 seconds (useless for streaming).

## 🛠 Local Development (Ngrok)
To test on your phone/TV without a server:
1. `pip install -r requirements.txt`
2. `python main.py`
3. `ngrok http 8080`
4. Set `URL` in `.env` to the Ngrok URL.
