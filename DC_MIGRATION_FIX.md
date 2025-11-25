# DC Migration Fix - November 25, 2025

## Problem Identified
The bot was detecting DC migration on **every single chunk request** (approximately every 1-1.5 seconds), even after the correct DC 4 client was created and cached.

### Root Cause
In `server/streamer.py`, the `yield_chunks()` method was resetting the download client to the main client at the start of each call:

```python
# BEFORE (lines 56-57) - BUGGY CODE
download_client = self.client  # ❌ Reset on every chunk!
is_temp_client = False
```

This meant:
1. **First chunk**: Uses main client (DC 2) → FileMigrate exception → creates DC 4 client ✓
2. **Second chunk**: `download_client` reset to DC 2 client → FileMigrate again ✗
3. **Third chunk**: Same issue repeats... ✗
4. **Every chunk thereafter**: Continuous FileMigrate detection ✗

### Solution
Moved `download_client` and `is_temp_client` to **instance variables** that persist across all chunk requests for the same file stream.

## Changes Made

### 1. Added Instance Variables (lines 22-24)
```python
class TelegramFileStreamer:
    def __init__(self, client: Client, file_id: str, file_size: int):
        # ... existing code ...
        # ✅ NEW: Persist the download client across all chunk requests
        self.download_client = client
        self.is_temp_client = False
```

### 2. Removed Local Variables (removed lines 59-61)
```python
# ❌ REMOVED - No longer needed
# download_client = self.client
# is_temp_client = False
```

### 3. Updated All References
Changed all references from `download_client` to `self.download_client`:
- Line 87: `await self.download_client.invoke(...)`
- Lines 117-118: `self.download_client = temp_clients[target_dc]`
- Lines 147-148: `self.download_client = new_client`

## Expected Behavior After Fix

### Before (BUGGY):
```
[02:22:26] DC Migration detected (DC 4). Creating client...
[02:22:36] Client for DC 4 started and cached. ✓
[02:22:38] DC Migration detected (DC 4). Reusing... ❌
[02:22:39] DC Migration detected (DC 4). Reusing... ❌
[02:22:40] DC Migration detected (DC 4). Reusing... ❌
... (repeats every ~1.2 seconds for EVERY chunk)
```

### After (FIXED):
```
[02:22:26] DC Migration detected (DC 4). Creating client...
[02:22:36] Client for DC 4 started and cached. ✓
... (streaming continues silently with DC 4 client) ✓
```

## Performance Impact
- **Before**: ~50 log messages per minute + repeated exception handling overhead
- **After**: 1 log message initially, then clean streaming
- **Result**: Significantly reduced CPU usage and improved streaming performance

## Testing Recommendations
1. Deploy to Koyeb
2. Send a video file to the bot
3. Request a stream link
4. Open in VLC and monitor logs
5. **Expected**: Only ONE "DC Migration detected" message, then clean streaming

## Files Modified
- `server/streamer.py` (3 changes)

---
**Status**: ✅ Ready for deployment
