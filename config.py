"""
Telegram VLC Stream Bot - Configuration Module
Copyright (c) 2025 Akhil TG. All Rights Reserved.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    PORT = int(os.getenv("PORT", "8080"))
    HOST = os.getenv("HOST", "0.0.0.0")
    URL = os.getenv("URL", "http://localhost:8080")
    # Directory to store small thumbnails or temporary data if needed
    WORK_DIR = "work_dir"

if not os.path.exists(Config.WORK_DIR):
    os.makedirs(Config.WORK_DIR)
