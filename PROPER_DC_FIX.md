# Proper DC Migration Fix - Resource Mapping

## The Real Problem (Finally Identified!)

The issue wasn't just about client persistence or location caching. The **root cause** was:

**We were not remembering which DC each file belongs to.**

### What Was Happening
1. First chunk: Use default client → FileMigrate to DC 4 → Create DC 4 client ✓
2. Second chunk: **Create new TelegramFileStreamer instance** → Use default client again → FileMigrate to DC 4 again ✗
3. Every chunk: Same pattern repeats...

### Why This Happened
Each HTTP range request creates a **new TelegramFileStreamer instance**. The instance variables (`self.download_client`) don't persist across HTTP requests, only across chunks within a single request.

## The Proper Solution

### 1. Global DC Client Registry
```python
# Global registry: DC ID → Client
dc_clients = {}
```
- Maintains one client per DC
- Persists across all HTTP requests
- Reused for all files on that DC

### 2. Global File-to-DC Mapping
```python
# Global mapping: file_id → DC ID
file_dc_mapping = {}
```
- Remembers which DC each file belongs to
- Persists across all HTTP requests
- Prevents repeated migration detection

### 3. Smart Client Selection in __init__
```python
if file_id in file_dc_mapping:
    # We already know which DC this file is on
    target_dc = file_dc_mapping[file_id]
    self.download_client = dc_clients.get(target_dc, client)
else:
    # First time seeing this file, use default client
    self.download_client = client
```

### 4. Save Mapping After Migration
```python
except FileMigrate as e:
    target_dc = e.value
    # ... create/get DC client ...
    
    # CRITICAL: Save the mapping!
    file_dc_mapping[self.file_id] = target_dc
```

## How It Works Now

### First Request for a File
```
HTTP Request 1 (bytes 0-524287):
  ├─ Create TelegramFileStreamer(file_id="ABC...")
  ├─ file_id not in mapping → use default client
  ├─ First chunk: FileMigrate to DC 4
  ├─ Create DC 4 client → save to dc_clients[4]
  ├─ Save mapping: file_dc_mapping["ABC..."] = 4
  └─ Continue streaming with DC 4 client
```

### Second Request for Same File (Seeking/Resume)
```
HTTP Request 2 (bytes 1048576-1572863):
  ├─ Create NEW TelegramFileStreamer(file_id="ABC...")
  ├─ file_id IS in mapping → file_dc_mapping["ABC..."] = 4
  ├─ Use dc_clients[4] immediately
  ├─ NO FileMigrate exception!
  └─ Stream directly with DC 4 client
```

### Third Request, Fourth Request, etc.
```
All future requests:
  ├─ file_id in mapping → use DC 4 client immediately
  └─ Zero FileMigrate exceptions
```

## Expected Log Pattern

### First Stream (New File)
```
[Time] DC Migration: File is on DC 4
[Time] Creating new client for DC 4...
[Time] Starting client for DC 4...
[Time] DC 4 client started and cached.
[Time] Saved mapping: file ABC... → DC 4
... (streaming continues silently)
```

### Second Stream (Same File, Seeking)
```
[Time] Using cached DC 4 client for file ABC...
... (streaming continues silently, NO migration)
```

### Third Stream (Different File, Also on DC 4)
```
[Time] DC Migration: File is on DC 4
[Time] Reusing existing DC 4 client
[Time] Saved mapping: file XYZ... → DC 4
... (streaming continues silently)
```

## Benefits

1. **Zero Repeated Migrations**: Each file triggers migration exactly once
2. **Instant Subsequent Requests**: No migration check on seek/resume
3. **DC Client Reuse**: Multiple files on same DC share one client
4. **Memory Efficient**: Only create clients for DCs actually needed
5. **Persistent Across Requests**: Mappings survive between HTTP requests

## Key Differences from Previous Attempts

| Previous Approach | New Approach |
|-------------------|--------------|
| Instance variables | Global dictionaries |
| Reset on each HTTP request | Persist across all requests |
| Client per file | Client per DC |
| No file→DC mapping | Explicit mapping saved |
| Migration on every request | Migration once per file |

## Files Modified
- `server/streamer.py`:
  - Added `dc_clients` global registry
  - Added `file_dc_mapping` global mapping
  - Smart client selection in `__init__`
  - Save mapping after migration

## Testing
After deployment, you should see:
1. First video: 1 migration message + mapping saved
2. Seeking in same video: Zero migration messages
3. Second video (same DC): Zero migration messages (reuses client)
4. Third video (different DC): 1 migration message for new DC

---

**Status**: ✅ Proper fix implemented  
**Ready for**: Deployment and testing
