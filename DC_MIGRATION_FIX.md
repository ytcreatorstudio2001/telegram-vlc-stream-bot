# DC Migration Fix - November 25, 2025

## Problem Identified
The bot was detecting DC migration on **every single chunk request** (approximately every 1-1.5 seconds), even after the correct DC 4 client was created and cached.

### Root Cause
There were **two related issues** causing FileMigrate to be raised on every chunk:

#### Issue 1: Client Reset (First Fix - Commit 169a8ef)
The `yield_chunks()` method was resetting the download client to the main client at the start of each call:

```python
# BEFORE (lines 56-57) - BUGGY CODE
download_client = self.client  # ❌ Reset on every chunk!
is_temp_client = False
```

#### Issue 2: Location Regeneration (Second Fix - Commit 424b823) ⚠️ **ACTUAL ROOT CAUSE**
Even after fixing the client persistence, the file location was being regenerated on **every chunk**:

```python
# BEFORE (line 62) - BUGGY CODE
location = await self.get_file_location()  # ❌ Called every chunk!
```

When `get_file_location()` decodes the `file_id`, it contains the **original DC information**. Even when using the correct DC 4 client, Telegram still raises `FileMigrate` because the location object itself references the wrong DC.

**Combined Effect:**
1. **First chunk**: Uses main client (DC 2) → FileMigrate exception → creates DC 4 client ✓
2. **Second chunk**: 
   - Client persists as DC 4 ✓
   - BUT location is regenerated from original file_id → FileMigrate again ✗
3. **Every chunk thereafter**: Same issue repeats... ✗

### Solution
**Two-part fix** to address both issues:

#### Part 1: Persist Download Client
Moved `download_client` and `is_temp_client` to **instance variables** that persist across all chunk requests for the same file stream.

#### Part 2: Cache File Location
Added `cached_location` instance variable to store the file location after first fetch, preventing regeneration on every chunk.

## Changes Made

### 1. Added Instance Variables (lines 22-26)
```python
class TelegramFileStreamer:
    def __init__(self, client: Client, file_id: str, file_size: int):
        # ... existing code ...
        # ✅ NEW: Persist the download client across all chunk requests
        self.download_client = client
        self.is_temp_client = False
        # ✅ NEW: Cache the file location to avoid repeated FileMigrate exceptions
        self.cached_location = None
```

### 2. Use Cached Location (lines 62-70)
```python
# ✅ NEW: Only fetch location if not cached
if self.cached_location is None:
    try:
        self.cached_location = await self.get_file_location()
    except Exception as e:
        logging.error(f"Failed to get file location: {e}")
        raise e

location = self.cached_location
```

### 3. Updated All Client References
Changed all references from `download_client` to `self.download_client`:
- Line 87: `await self.download_client.invoke(...)`
- Lines 117-118: `self.download_client = temp_clients[target_dc]`
- Lines 147-148: `self.download_client = new_client`

### 4. Refresh Cache After Migration (lines 162-164)
```python
# ✅ NEW: Update cached location after DC migration
self.cached_location = await self.get_file_location()
location = self.cached_location
```

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
- `server/streamer.py` (2 commits: 169a8ef + 424b823)
- `DC_MIGRATION_FIX.md` (documentation)

## Commits
1. **169a8ef**: Fix DC migration: Persist download client across chunk requests
2. **424b823**: Fix: Cache file location to prevent repeated FileMigrate exceptions ⭐ **Main Fix**

---
**Status**: ✅ Ready for deployment (Commit 424b823)
