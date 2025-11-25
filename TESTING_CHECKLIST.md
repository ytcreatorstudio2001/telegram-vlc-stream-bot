# Testing Current Deployment - Checklist

## Objective
Test if the location caching fix (commit `424b823`) is actually working in the current Koyeb deployment, despite the logs showing repeated FileMigrate warnings.

## Why This Might Work
The current deployment *should* have the location caching fix because:
- Commit `424b823` was pushed 30+ minutes ago
- Koyeb rebuilt and deployed (new image hash: `761562d5`)
- The repeated FileMigrate might be from a different issue

## Test Procedure

### Step 1: Send a Fresh Video File
1. Send a **NEW** video file to your bot (not one you've sent before)
2. This ensures we're testing with a clean slate
3. Wait for the bot to respond with the stream link

### Step 2: Open Stream in VLC
1. Copy the stream URL from the bot
2. Open VLC → Media → Open Network Stream
3. Paste the URL and click Play

### Step 3: Monitor Koyeb Logs
**Watch for these patterns:**

#### ✅ GOOD (Fix is working):
```
[Time] DC Migration detected (DC 4). Switching to persistent temp client...
[Time] DEBUG: Initializing new persistent client for DC 4...
[Time] DEBUG: Client for DC 4 started and cached.
... (then SILENCE - no more DC migration messages)
```

#### ❌ BAD (Fix not deployed):
```
[Time] DC Migration detected (DC 4). Switching to persistent temp client...
[Time] DEBUG: Client for DC 4 started and cached.
[Time+1s] DC Migration detected (DC 4). Switching to persistent temp client...
[Time+1s] DEBUG: Reusing existing client for DC 4
[Time+2s] DC Migration detected (DC 4). Switching to persistent temp client...
[Time+2s] DEBUG: Reusing existing client for DC 4
... (repeats every ~1.2 seconds)
```

### Step 4: Test Seeking/Skipping
1. In VLC, skip forward 30 seconds
2. Skip backward 10 seconds
3. Jump to middle of video
4. Check logs - should still be silent (no new FileMigrate messages)

### Step 5: Monitor for 5-10 Minutes
- Let the video play for 5-10 minutes
- Check logs periodically
- Count how many "DC Migration detected" messages appear

## Expected Results

### If Fix is Working:
- **1 DC migration message** when stream starts
- **Silence** for the rest of the stream
- **Smooth playback** in VLC
- **No buffering** when seeking

### If Fix is NOT Working:
- **50+ DC migration messages** per minute
- **Possible buffering** in VLC
- **Logs filled with spam**

## What to Do Based on Results

### ✅ If It's Working:
1. **Celebrate!** 🎉
2. The location caching fix is deployed and working
3. **Do NOT push the new session persistence code yet**
4. Monitor for FloodWait errors over next 24 hours
5. If no FloodWait, you're good!

### ❌ If It's Still Broken:
1. The fix is NOT deployed (Koyeb cache issue)
2. **Wait 24 hours** to avoid more FloodWait
3. Then deploy the session persistence fix (commit `91c44c0`)
4. The cache-busting ENV will force fresh build

### ⚠️ If You Get FloodWait Errors:
```
FloodWait: sleeping 3600s
```
1. **Stop all testing immediately**
2. Let the bot rest for the specified time
3. Don't send any more files
4. Wait 24+ hours before next deployment

## Monitoring Commands

### Check Koyeb Logs:
```bash
# In Koyeb dashboard, filter logs by:
- "DC Migration detected"
- "FloodWait"
- "ERROR"
```

### Count DC Migration Messages:
Look for the pattern:
- First occurrence: Normal (expected)
- Subsequent occurrences within 60 seconds: BAD (fix not working)

## Timeline

| Time | Action |
|------|--------|
| Now | Send test video |
| +1 min | Check initial logs |
| +5 min | Verify no spam |
| +10 min | Test seeking |
| +1 hour | Final check |
| +24 hours | If broken, deploy fix |

## Notes
- Use a **small video file** (< 100MB) for initial testing
- Don't test with multiple files simultaneously
- One test is enough - don't spam the bot
- If it works, let it run and monitor passively

---

**Current Time**: 2025-11-25 08:11 IST  
**Safe to Deploy**: 2025-11-26 08:00 IST (if needed)  
**Status**: Ready to test current deployment
