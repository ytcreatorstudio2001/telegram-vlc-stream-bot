import os
import sys
import time
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import db

logger = logging.getLogger(__name__)

# Fallback JSON storage if DB is not available
import json
USERS_FILE = "users.json"

def load_users_local():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_user_local(user_id):
    users = load_users_local()
    if user_id not in users:
        users.add(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(list(users), f)

async def add_user(user_id):
    if db:
        if not await db.is_user_exist(user_id):
            await db.add_user(user_id)
    else:
        save_user_local(user_id)

async def get_users_count():
    if db:
        return await db.total_users_count()
    else:
        return len(load_users_local())

# Admin Filter
def is_admin(user_id):
    return user_id in Config.ADMINS

@Client.on_message(filters.command("admin") & filters.private)
async def admin_panel(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return
    
    await show_admin_panel(message)

async def show_admin_panel(message: Message, is_edit=False):
    users_count = await get_users_count()
    
    text = (
        "👮‍♂️ **Admin Control Panel**\n\n"
        f"📊 **Total Users:** `{users_count}`\n"
        f"📢 **Force Sub:** `{Config.FORCE_SUB_CHANNEL or 'Disabled'}`\n"
        f"🤖 **Bot Status:** `Running`\n\n"
        "Select an action below:"
    )
    
    buttons = [
        [
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
            InlineKeyboardButton("📊 Stats", callback_data="admin_stats")
        ],
        [
            InlineKeyboardButton("🖼️ Change Banners", callback_data="admin_banners"),
            InlineKeyboardButton("🔒 Force Sub", callback_data="admin_forcesub")
        ],
        [
            InlineKeyboardButton("🔄 Restart Bot", callback_data="admin_restart"),
            InlineKeyboardButton("❌ Close", callback_data="close_admin")
        ]
    ]
    
    if is_edit:
        await message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^admin_"))
async def admin_callbacks(client: Client, callback_query: CallbackQuery):
    if not is_admin(callback_query.from_user.id):
        await callback_query.answer("❌ You are not an admin!", show_alert=True)
        return

    data = callback_query.data
    
    if data == "admin_stats":
        users_count = await get_users_count()
        await callback_query.answer(f"📊 Total Users: {users_count}", show_alert=True)
        
    elif data == "admin_broadcast":
        await callback_query.edit_message_text(
            "📢 **Broadcast Message**\n\n"
            "Reply to this message with the content you want to broadcast to all users.\n"
            "Supports: Text, Photo, Video, Sticker, etc.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
        )
        # Note: Actual broadcast logic needs a state machine or listener, 
        # for simplicity we'll just show instructions here. 
        # A full broadcast implementation requires more complex handling.
        
    elif data == "admin_banners":
        await callback_query.edit_message_text(
            "🖼️ **Banner Management**\n\n"
            "To change banners, you need to replace the files in `assets/` folder.\n"
            "Currently, this can only be done via file access.\n\n"
            "**Current Banners:**\n"
            "1. `banner.png`\n"
            "2. `banner1.png`\n"
            "3. `banner2.png`\n"
            "4. `banner3.png`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
        )
        
    elif data == "admin_forcesub":
        status = Config.FORCE_SUB_CHANNEL if Config.FORCE_SUB_CHANNEL else "Disabled"
        await callback_query.edit_message_text(
            f"🔒 **Force Subscription**\n\n"
            f"Current Channel: `{status}`\n\n"
            "To change this, update `FORCE_SUB_CHANNEL` in your environment variables or config.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
        )
        
    elif data == "admin_restart":
        await callback_query.answer("🔄 Restarting...", show_alert=True)
        os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_callback_query(filters.regex("^back_to_admin$"))
async def back_to_admin(client: Client, callback_query: CallbackQuery):
    if not is_admin(callback_query.from_user.id):
        return
    await show_admin_panel(callback_query.message, is_edit=True)

@Client.on_callback_query(filters.regex("^close_admin$"))
async def close_admin(client: Client, callback_query: CallbackQuery):
    await callback_query.message.delete()

# Hook into start command to save users
# We need to modify the existing start command or add a handler that runs before it.
# Since Pyrogram handlers run in groups, we can add a watcher.

@Client.on_message(filters.command("start"), group=-1)
async def log_user(client: Client, message: Message):
    await add_user(message.from_user.id)
