
import asyncio
import os
from pathlib import Path
from pyrogram.storage import FileStorage

async def test_storage():
    session_dir = os.path.abspath(".")
    print(f"Session Dir: {session_dir}")
    
    session_name = "test_storage_v1"
    storage = FileStorage(name=session_name, workdir=Path(session_dir))
    
    print("Opening storage...")
    await storage.open()
    
    print("Setting DC ID to 4...")
    await storage.dc_id(4)
    
    print("Saving storage...")
    await storage.save()
    
    print("Closing storage...")
    await storage.close()
    
    expected_path = os.path.join(session_dir, f"{session_name}.session")
    if os.path.exists(expected_path):
        print(f"SUCCESS: File created at {expected_path}")
        # Verify content (sqlite)
        import sqlite3
        conn = sqlite3.connect(expected_path)
        c = conn.cursor()
        c.execute("SELECT dc_id FROM sessions")
        row = c.fetchone()
        print(f"DC ID in DB: {row[0]}")
        conn.close()
    else:
        print(f"FAILURE: File not found at {expected_path}")

if __name__ == "__main__":
    asyncio.run(test_storage())
