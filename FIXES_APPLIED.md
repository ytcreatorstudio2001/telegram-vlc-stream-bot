# Fixes Applied

## 2025-11-26: DC Migration and FileStorage Fixes

### Issues Addressed
1. **NameError: name 'ExportAuthorization' is not defined**
   - The `dc_manager.py` script was missing imports for `ExportAuthorization` and `ImportAuthorization`.
   - **Fix**: Added `from pyrogram.raw.functions.auth import ExportAuthorization, ImportAuthorization`.

2. **TypeError: unsupported operand type(s) for /: 'str' and 'str'**
   - Pyrogram's `FileStorage` expects `workdir` to be a `pathlib.Path` object to use the `/` operator. Passing a string caused a crash on some environments.
   - **Fix**: Wrapped `SESSION_DIR` in `Path()` when initializing `Client` and `FileStorage` in `dc_manager.py`.

3. **Infinite DC Migration Loop**
   - The bot was getting stuck in a loop where it connected to the wrong DC (likely DC 2) but thought it was on DC 4, causing `FileMigrate` errors to persist.
   - **Fixes**:
     - Bumped session file version to `v4` (`persistent_dc_{dc_id}_v4`) to force creation of fresh session files.
     - Implemented `invalidate_dc_client` in `dc_manager.py` to remove bad clients from the in-memory cache.
     - Updated `streamer.py` to call `invalidate_dc_client` if migration attempts fail more than once, forcing a reconnection.

### Verification
- `server/dc_manager.py` syntax checked.
- `server/streamer.py` syntax checked.
- `test_storage.py` verified `FileStorage` creation works locally.

### Next Steps
- Redeploy to Koyeb.
- Monitor logs for "Successfully authorized on DC X" and ensure `FileMigrate` errors resolve quickly (1-2 attempts max).
