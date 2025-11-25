# Session Persistence & FloodWait Prevention

## Current Problem
1. **Session files are ephemeral**: Stored in container filesystem (`workdir="."`), deleted on every deployment
2. **Repeated authentication**: Each deployment creates new auth keys, triggering FloodWait
3. **FileMigrate still occurring**: Despite location caching fix (code may not be deployed yet)

## Solutions

### Option 1: Use Koyeb Persistent Volumes (RECOMMENDED)
Koyeb supports persistent volumes that survive deployments.

#### Steps:
1. **Create a persistent volume in Koyeb dashboard**:
   - Go to your service settings
   - Add a persistent volume
   - Mount path: `/app/sessions`
   - Size: 1GB (minimum)

2. **Update code to use persistent directory**:
   ```python
   # In bot_client.py and server/streamer.py
   import os
   
   # Use persistent volume for sessions
   SESSION_DIR = os.getenv("SESSION_DIR", "/app/sessions")
   os.makedirs(SESSION_DIR, exist_ok=True)
   
   # When creating clients:
   Client(
       session_name,
       workdir=SESSION_DIR,  # Instead of "."
       ...
   )
   ```

3. **Update Dockerfile**:
   ```dockerfile
   # Create sessions directory
   RUN mkdir -p /app/sessions
   VOLUME /app/sessions
   ```

### Option 2: Stop Frequent Deployments (IMMEDIATE)
**To avoid FloodWait penalties RIGHT NOW:**

1. **Wait at least 24 hours** before next deployment
2. **Test locally first** before deploying to Koyeb
3. **Use session file backup**: Download session files from a working deployment

### Option 3: Pre-generate Session Files Locally
Generate session files locally and include them in the deployment:

```bash
# Run locally to generate sessions
python -c "
from pyrogram import Client
from config import Config

# Generate main session
client = Client('TelegramStreamBot', 
                api_id=Config.API_ID,
                api_hash=Config.API_HASH,
                bot_token=Config.BOT_TOKEN)
client.start()
client.stop()

# Generate DC 4 session
import asyncio
async def create_dc4():
    dc4 = Client('persistent_dc_4',
                 api_id=Config.API_ID,
                 api_hash=Config.API_HASH,
                 bot_token=Config.BOT_TOKEN)
    await dc4.storage.open()
    await dc4.storage.dc_id(4)
    await dc4.storage.save()
    await dc4.storage.close()
    await dc4.start()
    await dc4.stop()

asyncio.run(create_dc4())
"

# Commit session files to git
git add *.session
git commit -m "Add pre-generated session files"
git push
```

**⚠️ WARNING**: This exposes session files in your repo. Only do this if your repo is private!

## Recommended Action Plan

### Immediate (To avoid more FloodWait):
1. ✅ **STOP deploying** for at least 24 hours
2. ✅ **Test the current deployment** - the location caching fix might already be working
3. ✅ **Monitor logs** to see if FileMigrate spam continues

### Short-term (Next deployment):
1. Implement persistent volumes in Koyeb
2. Update code to use `/app/sessions` directory
3. Deploy once and let it run

### Long-term:
1. Set up local testing environment
2. Only deploy after thorough local testing
3. Consider using a separate test bot token for development

## Why FileMigrate Keeps Happening

Even with our fixes, if Koyeb is using **cached Docker layers**, the old code might still be running. To force a fresh build:

1. In Koyeb dashboard, trigger a **"Redeploy"** (not just auto-deploy from git)
2. Or, make a dummy change to Dockerfile to bust the cache:
   ```dockerfile
   # Add this line with current timestamp
   ENV CACHE_BUST=2025-11-25-08:07
   ```

## Current Status
- ✅ Code fixes pushed to GitHub (commits 169a8ef, 424b823)
- ❌ Koyeb may be using cached/old image
- ⚠️ FloodWait risk from repeated deployments
- 🔄 Session files not persisting between deployments

**RECOMMENDATION**: Wait 24 hours, then implement persistent volumes before next deployment.
