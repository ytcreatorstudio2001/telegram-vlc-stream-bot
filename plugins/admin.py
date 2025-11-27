import os
import sys
import time
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import Config
from database import db

logger = logging.getLogger(__name__)

# Fallback JSON storage if DB is not available
import json
USERS_FILE = "users.json"

# Store broadcast state
broadcast_state = {}

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

async def add_user(user_id, user_obj=None, client=None):
    """Add user without blocking - runs in background"""
    try:
        is_new = False
        if db:
            # Prepare user data from user object
            user_data = None
            if user_obj:
                user_data = {
                    'username': user_obj.username,
                    'first_name': user_obj.first_name,
                    'last_name': user_obj.last_name,
                    'is_premium': getattr(user_obj, 'is_premium', False),
                    'language_code': getattr(user_obj, 'language_code', None)
                }
            
            # Try to add user
            if await db.add_user(user_id, user_data):
                is_new = True
        else:
            if user_id not in load_users_local():
                save_user_local(user_id)
                is_new = True
        
        # Log new user if configured
        if is_new and client and Config.LOG_CHANNEL and user_obj:
            try:
                log_text = (
                    "**#NEW_USER**\n\n"
                    f"**User:** [{user_obj.first_name}](tg://user?id={user_id})\n"
                    f"**ID:** `{user_id}`\n"
                    f"**Username:** @{user_obj.username if user_obj.username else 'None'}\n"
                    f"**Language:** {getattr(user_obj, 'language_code', 'N/A')}"
                )
                await client.send_message(Config.LOG_CHANNEL, log_text)
            except Exception as e:
                logger.error(f"Error sending new user log: {e}")
                
    except Exception as e:
        # Only log non-duplicate errors
        if "duplicate" not in str(e).lower():
            logger.error(f"Error adding user {user_id}: {e}")
        # Fallback to local storage on any error
        try:
            save_user_local(user_id)
        except:
            pass  # Silent fail for user tracking

async def get_users_count():
    try:
        if db:
            count = await db.total_users_count()
            # If MongoDB returns 0 but we have local users, use local count
            if count == 0:
                local_count = len(load_users_local())
                return local_count if local_count > 0 else 0
            return count
        else:
            return len(load_users_local())
    except Exception as e:
        logger.error(f"Error getting user count: {e}")
        # Fallback to local storage
        return len(load_users_local())

async def get_all_users():
    """Get list of all user IDs"""
    try:
        if db:
            users = await db.get_all_users()
            # If MongoDB returns empty but we have local users, use local
            if not users:
                local_users = list(load_users_local())
                return local_users if local_users else []
            return users
        else:
            return list(load_users_local())
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        # Fallback to local storage
        return list(load_users_local())

# Admin Filter
def is_admin(user_id):
    return user_id in Config.ADMINS

@Client.on_message(filters.command("admin") & filters.private)
async def admin_panel(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("❌ You are not authorized to use this command.")
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
            InlineKeyboardButton("👥 View Users", callback_data="admin_users"),
            InlineKeyboardButton("🔍 Find User", callback_data="admin_find_user")
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
        broadcast_state[callback_query.from_user.id] = "waiting_for_message"
        await callback_query.edit_message_text(
            "📢 **Broadcast Message**\n\n"
            "Send me the message you want to broadcast to all users.\n\n"
            "**Supported:**\n"
            "✅ Text messages\n"
            "✅ Photos with captions\n"
            "✅ Videos with captions\n"
            "✅ Documents\n"
            "✅ Stickers\n\n"
            "Send /cancel to cancel the broadcast.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
        )
        
    elif data == "admin_users":
        users = await get_all_users()
        users_count = len(users)
        
        # Show first 20 users
        user_list = "\n".join([f"• `{uid}`" for uid in users[:20]])
        
        text = (
            f"👥 **User List** (Total: {users_count})\n\n"
            f"{user_list}\n\n"
        )
        
        if users_count > 20:
            text += f"_Showing first 20 users. Total: {users_count}_"
        
        await callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
        )
        
    elif data == "admin_find_user":
        broadcast_state[callback_query.from_user.id] = "waiting_for_user_id"
        await callback_query.edit_message_text(
            "🔍 **Find User**\n\n"
            "Send me the User ID to get information.\n\n"
            "Send /cancel to cancel.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
        )
        
    elif data == "admin_banners":
        # Check existing banners
        banners_info = []
        banner_files = ["banner.png", "banner1.png", "banner2.png", "banner3.png"]
        
        for banner in banner_files:
            path = f"assets/{banner}"
            if os.path.exists(path):
                size = os.path.getsize(path) / 1024  # KB
                banners_info.append(f"✅ `{banner}` ({size:.1f} KB)")
            else:
                banners_info.append(f"❌ `{banner}` (Missing)")
        
        broadcast_state[callback_query.from_user.id] = "waiting_for_banner"
        await callback_query.edit_message_text(
            "🖼️ **Banner Management**\n\n"
            "**Current Banners:**\n" + "\n".join(banners_info) + "\n\n"
            "**To update a banner:**\n"
            "Send me a photo with caption:\n"
            "`banner1` or `banner2` or `banner3` or `banner`\n\n"
            "The photo will replace the corresponding banner.\n\n"
            "Send /cancel to cancel.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
        )
        
    elif data == "admin_forcesub":
        status = Config.FORCE_SUB_CHANNEL if Config.FORCE_SUB_CHANNEL else "Disabled"
        
        # Try to get channel info if configured
        channel_info = ""
        if Config.FORCE_SUB_CHANNEL:
            try:
                chat = await client.get_chat(Config.FORCE_SUB_CHANNEL)
                channel_info = f"\n**Channel Name:** {chat.title}\n**Members:** {chat.members_count if hasattr(chat, 'members_count') else 'N/A'}"
            except:
                channel_info = "\n⚠️ Unable to fetch channel info"
        
        await callback_query.edit_message_text(
            f"🔒 **Force Subscription**\n\n"
            f"**Current Channel:** `{status}`{channel_info}\n\n"
            "**How to change:**\n"
            "Update `FORCE_SUB_CHANNEL` in your environment variables.\n\n"
            "**Format:**\n"
            "• Username: `@YourChannel`\n"
            "• ID: `-100123456789`\n\n"
            "**Note:** Make sure the bot is admin in the channel!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
        )
        
    elif data == "admin_restart":
        await callback_query.answer("🔄 Restarting bot...", show_alert=True)
        await callback_query.edit_message_text("🔄 **Restarting bot...**\n\nPlease wait...")
        await asyncio.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)

    elif data.startswith("refresh_user_"):
        user_id = int(data.split("_")[2])
        
        # Reuse the logic from handle_admin_input for displaying user details
        # We need to construct a fake message object or refactor the display logic
        # For simplicity, we'll just trigger the display logic again
        
        try:
            # Try to get user from Telegram
            user = await client.get_users(user_id)
            
            # Get detailed info from database
            user_db_data = None
            if db:
                # Update last seen before refreshing
                await db.update_user_activity(user_id)
                user_db_data = await db.get_user_details(user_id)
            
            # Format timestamps
            def format_time(dt):
                if not dt:
                    return "N/A"
                from datetime import datetime
                if isinstance(dt, str):
                    return dt
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            
            def time_ago(dt):
                if not dt:
                    return "N/A"
                from datetime import datetime
                if isinstance(dt, str):
                    return "N/A"
                delta = datetime.now() - dt
                
                if delta.days > 0:
                    return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
                elif delta.seconds >= 3600:
                    hours = delta.seconds // 3600
                    return f"{hours} hour{'s' if hours > 1 else ''} ago"
                elif delta.seconds >= 60:
                    minutes = delta.seconds // 60
                    return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
                else:
                    return "Just now"
            
            # Build comprehensive user info
            user_info = (
                "╔═══════════════════════════╗\n"
                "║   👤 **USER DETAILS**   ║\n"
                "╚═══════════════════════════╝\n\n"
                "**📋 PROFILE INFORMATION**\n"
                f"┣━ 🆔 **ID:** `{user.id}`\n"
                f"┣━ 👤 **Name:** {user.first_name} {user.last_name or ''}\n"
                f"┣━ 📱 **Username:** @{user.username if user.username else 'None'}\n"
                f"┣━ 💎 **Premium:** {'✅ Yes' if getattr(user, 'is_premium', False) else '❌ No'}\n"
                f"┣━ 🤖 **Bot:** {'Yes' if user.is_bot else 'No'}\n"
                f"┣━ 🌐 **Language:** {getattr(user, 'language_code', 'N/A').upper() if getattr(user, 'language_code', None) else 'N/A'}\n"
            )
            
            # Add database statistics if available
            if user_db_data:
                user_info += (
                    f"┗━ 🔐 **Status:** {'Verified' if user.is_verified else 'Active'}\n\n"
                    "**📊 ACTIVITY STATISTICS**\n"
                    f"┣━ 🎬 **Total Streams:** `{user_db_data.get('total_streams', 0)}`\n"
                    f"┣━ 📁 **Total Files:** `{user_db_data.get('total_files', 0)}`\n"
                    f"┣━ 📦 **Batch Requests:** `{user_db_data.get('total_batch_requests', 0)}`\n"
                    f"┗━ 📈 **Total Actions:** `{user_db_data.get('total_streams', 0) + user_db_data.get('total_files', 0) + user_db_data.get('total_batch_requests', 0)}`\n\n"
                    "**⏰ TIMESTAMPS**\n"
                    f"┣━ 🎯 **First Seen:** `{format_time(user_db_data.get('first_seen'))}`\n"
                    f"┃   _{time_ago(user_db_data.get('first_seen'))}_\n"
                    f"┣━ 👁️ **Last Seen:** `{format_time(user_db_data.get('last_seen'))}`\n"
                    f"┃   _{time_ago(user_db_data.get('last_seen'))}_\n"
                    f"┗━ 📅 **Join Date:** `{format_time(user_db_data.get('join_date'))}`\n\n"
                )
            else:
                user_info += (
                    f"┗━ 🔐 **Status:** {'Verified' if user.is_verified else 'Active'}\n\n"
                    "**📊 ACTIVITY STATISTICS**\n"
                    "⚠️ _No activity data available_\n"
                    "_User has not been tracked in database_\n\n"
                )
            
            # Add user engagement level
            if user_db_data:
                total_actions = user_db_data.get('total_streams', 0) + user_db_data.get('total_files', 0) + user_db_data.get('total_batch_requests', 0)
                
                if total_actions >= 100:
                    engagement = "🔥 **Power User**"
                elif total_actions >= 50:
                    engagement = "⭐ **Active User**"
                elif total_actions >= 10:
                    engagement = "✅ **Regular User**"
                elif total_actions > 0:
                    engagement = "🆕 **New User**"
                else:
                    engagement = "😴 **Inactive**"
                
                user_info += (
                    f"**🎯 ENGAGEMENT LEVEL**\n"
                    f"{engagement}\n\n"
                )
            
            user_info += (
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "_© 2025 VLC Stream Bot Admin Panel_"
            )
            
            # Create action buttons
            action_buttons = [
                [
                    InlineKeyboardButton("💬 Message User", url=f"tg://user?id={user.id}"),
                    InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_user_{user.id}")
                ],
                [InlineKeyboardButton("🔙 Back to Admin", callback_data="back_to_admin")]
            ]
            
            await callback_query.edit_message_text(
                user_info,
                reply_markup=InlineKeyboardMarkup(action_buttons)
            )
            await callback_query.answer("✅ User details refreshed!")
            
        except Exception as e:
            await callback_query.answer(f"❌ Error refreshing: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("^back_to_admin$"))
async def back_to_admin(client: Client, callback_query: CallbackQuery):
    if not is_admin(callback_query.from_user.id):
        return
    # Clear any pending state
    if callback_query.from_user.id in broadcast_state:
        del broadcast_state[callback_query.from_user.id]
    await show_admin_panel(callback_query.message, is_edit=True)

@Client.on_callback_query(filters.regex("^close_admin$"))
async def close_admin(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id in broadcast_state:
        del broadcast_state[callback_query.from_user.id]
    await callback_query.message.delete()

# Handle admin state-based messages (exclude media files for auto_stream)
@Client.on_message(
    filters.private & 
    ~filters.command(["start", "help", "about", "stream", "batch", "admin", "cancel"]) &
    ~filters.document & ~filters.video & ~filters.audio  # Don't catch media files
)
async def handle_admin_input(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return
    
    user_id = message.from_user.id
    
    if user_id not in broadcast_state:
        return
    
    state = broadcast_state[user_id]
    
    # Handle broadcast message
    if state == "waiting_for_message":
        del broadcast_state[user_id]
        
        # Confirm broadcast
        confirm_text = (
            "📢 **Confirm Broadcast**\n\n"
            "Are you sure you want to send this message to all users?\n\n"
            "This action cannot be undone!"
        )
        
        buttons = [
            [
                InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_broadcast_{message.id}"),
                InlineKeyboardButton("❌ Cancel", callback_data="back_to_admin")
            ]
        ]
        
        await message.reply_text(
            confirm_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    # Handle user ID search
    elif state == "waiting_for_user_id":
        del broadcast_state[user_id]
        
        try:
            search_id = int(message.text.strip())
            
            # Try to get user from Telegram
            try:
                user = await client.get_users(search_id)
                
                # Get detailed info from database
                user_db_data = None
                if db:
                    user_db_data = await db.get_user_details(search_id)
                
                # Format timestamps
                def format_time(dt):
                    if not dt:
                        return "N/A"
                    from datetime import datetime
                    if isinstance(dt, str):
                        return dt
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
                
                def time_ago(dt):
                    if not dt:
                        return "N/A"
                    from datetime import datetime
                    if isinstance(dt, str):
                        return "N/A"
                    delta = datetime.now() - dt
                    
                    if delta.days > 0:
                        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
                    elif delta.seconds >= 3600:
                        hours = delta.seconds // 3600
                        return f"{hours} hour{'s' if hours > 1 else ''} ago"
                    elif delta.seconds >= 60:
                        minutes = delta.seconds // 60
                        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
                    else:
                        return "Just now"
                
                # Build comprehensive user info
                user_info = (
                    "╔═══════════════════════════╗\n"
                    "║   👤 **USER DETAILS**   ║\n"
                    "╚═══════════════════════════╝\n\n"
                    "**📋 PROFILE INFORMATION**\n"
                    f"┣━ 🆔 **ID:** `{user.id}`\n"
                    f"┣━ 👤 **Name:** {user.first_name} {user.last_name or ''}\n"
                    f"┣━ 📱 **Username:** @{user.username if user.username else 'None'}\n"
                    f"┣━ 💎 **Premium:** {'✅ Yes' if getattr(user, 'is_premium', False) else '❌ No'}\n"
                    f"┣━ 🤖 **Bot:** {'Yes' if user.is_bot else 'No'}\n"
                    f"┣━ 🌐 **Language:** {getattr(user, 'language_code', 'N/A').upper() if getattr(user, 'language_code', None) else 'N/A'}\n"
                )
                
                # Add database statistics if available
                if user_db_data:
                    user_info += (
                        f"┗━ 🔐 **Status:** {'Verified' if user.is_verified else 'Active'}\n\n"
                        "**📊 ACTIVITY STATISTICS**\n"
                        f"┣━ 🎬 **Total Streams:** `{user_db_data.get('total_streams', 0)}`\n"
                        f"┣━ 📁 **Total Files:** `{user_db_data.get('total_files', 0)}`\n"
                        f"┣━ 📦 **Batch Requests:** `{user_db_data.get('total_batch_requests', 0)}`\n"
                        f"┗━ 📈 **Total Actions:** `{user_db_data.get('total_streams', 0) + user_db_data.get('total_files', 0) + user_db_data.get('total_batch_requests', 0)}`\n\n"
                        "**⏰ TIMESTAMPS**\n"
                        f"┣━ 🎯 **First Seen:** `{format_time(user_db_data.get('first_seen'))}`\n"
                        f"┃   _{time_ago(user_db_data.get('first_seen'))}_\n"
                        f"┣━ 👁️ **Last Seen:** `{format_time(user_db_data.get('last_seen'))}`\n"
                        f"┃   _{time_ago(user_db_data.get('last_seen'))}_\n"
                        f"┗━ 📅 **Join Date:** `{format_time(user_db_data.get('join_date'))}`\n\n"
                    )
                else:
                    user_info += (
                        f"┗━ 🔐 **Status:** {'Verified' if user.is_verified else 'Active'}\n\n"
                        "**📊 ACTIVITY STATISTICS**\n"
                        "⚠️ _No activity data available_\n"
                        "_User has not been tracked in database_\n\n"
                    )
                
                # Add user engagement level
                if user_db_data:
                    total_actions = user_db_data.get('total_streams', 0) + user_db_data.get('total_files', 0) + user_db_data.get('total_batch_requests', 0)
                    
                    if total_actions >= 100:
                        engagement = "🔥 **Power User**"
                    elif total_actions >= 50:
                        engagement = "⭐ **Active User**"
                    elif total_actions >= 10:
                        engagement = "✅ **Regular User**"
                    elif total_actions > 0:
                        engagement = "🆕 **New User**"
                    else:
                        engagement = "😴 **Inactive**"
                    
                    user_info += (
                        f"**🎯 ENGAGEMENT LEVEL**\n"
                        f"{engagement}\n\n"
                    )
                
                user_info += (
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    "_© 2025 VLC Stream Bot Admin Panel_"
                )
                
                # Create action buttons
                action_buttons = [
                    [
                        InlineKeyboardButton("💬 Message User", url=f"tg://user?id={user.id}"),
                        InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_user_{user.id}")
                    ],
                    [InlineKeyboardButton("🔙 Back to Admin", callback_data="back_to_admin")]
                ]
                
                await message.reply_text(
                    user_info,
                    reply_markup=InlineKeyboardMarkup(action_buttons)
                )
                
            except Exception as e:
                # User not found on Telegram or error fetching
                users = await get_all_users()
                if search_id in users:
                    # User exists in DB but can't fetch from Telegram
                    user_db_data = None
                    if db:
                        user_db_data = await db.get_user_details(search_id)
                    
                    if user_db_data:
                        user_info = (
                            "╔═══════════════════════════╗\n"
                            "║   👤 **USER DETAILS**   ║\n"
                            "╚═══════════════════════════╝\n\n"
                            "**📋 PROFILE INFORMATION**\n"
                            f"┣━ 🆔 **ID:** `{search_id}`\n"
                            f"┣━ 👤 **Name:** {user_db_data.get('first_name', 'N/A')} {user_db_data.get('last_name', '') or ''}\n"
                            f"┣━ 📱 **Username:** @{user_db_data.get('username') if user_db_data.get('username') else 'None'}\n"
                            f"┣━ 💎 **Premium:** {'✅ Yes' if user_db_data.get('is_premium', False) else '❌ No'}\n"
                            f"┗━ 🌐 **Language:** {user_db_data.get('language_code', 'N/A').upper() if user_db_data.get('language_code') else 'N/A'}\n\n"
                            "**📊 ACTIVITY STATISTICS**\n"
                            f"┣━ 🎬 **Total Streams:** `{user_db_data.get('total_streams', 0)}`\n"
                            f"┣━ 📁 **Total Files:** `{user_db_data.get('total_files', 0)}`\n"
                            f"┣━ 📦 **Batch Requests:** `{user_db_data.get('total_batch_requests', 0)}`\n"
                            f"┗━ 📈 **Total Actions:** `{user_db_data.get('total_streams', 0) + user_db_data.get('total_files', 0) + user_db_data.get('total_batch_requests', 0)}`\n\n"
                            "⚠️ _Unable to fetch live Telegram data_\n"
                            "_Showing cached database information_\n\n"
                            "━━━━━━━━━━━━━━━━━━━━━━\n"
                            "_© 2025 VLC Stream Bot Admin Panel_"
                        )
                    else:
                        user_info = f"✅ User ID `{search_id}` exists in database.\n\n❌ But couldn't fetch details: {str(e)}"
                    
                    await message.reply_text(
                        user_info,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
                    )
                else:
                    await message.reply_text(
                        f"❌ **User Not Found**\n\n"
                        f"User ID `{search_id}` does not exist in the database.\n\n"
                        f"**Possible reasons:**\n"
                        f"• User has never interacted with the bot\n"
                        f"• Invalid User ID\n"
                        f"• User data was deleted\n\n"
                        f"_Error: {str(e)}_",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
                    )
        except ValueError:
            await message.reply_text(
                "❌ **Invalid User ID**\n\n"
                "Please send a valid numeric User ID.\n\n"
                "**Example:** `123456789`",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")]])
            )
    
    # Handle banner upload
    elif state == "waiting_for_banner":
        del broadcast_state[user_id]
        
        if not message.photo:
            await message.reply_text("❌ Please send a photo!")
            return
        
        caption = message.caption.strip().lower() if message.caption else ""
        
        if caption not in ["banner", "banner1", "banner2", "banner3"]:
            await message.reply_text(
                "❌ Invalid banner name!\n\n"
                "Please send photo with caption:\n"
                "`banner` or `banner1` or `banner2` or `banner3`"
            )
            return
        
        # Download and save banner
        try:
            file_path = f"assets/{caption}.png"
            await message.download(file_path)
            
            await message.reply_text(
                f"✅ **Banner Updated!**\n\n"
                f"Successfully updated `{caption}.png`\n\n"
                f"The new banner will be used in the welcome message."
            )
        except Exception as e:
            await message.reply_text(f"❌ Error saving banner: {str(e)}")

@Client.on_message(filters.command("cancel") & filters.private)
async def cancel_admin_action(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return
    
    if message.from_user.id in broadcast_state:
        del broadcast_state[message.from_user.id]
        await message.reply_text("✅ Action cancelled.")
    else:
        await message.reply_text("ℹ️ No active action to cancel.")

# Handle broadcast confirmation
@Client.on_callback_query(filters.regex("^confirm_broadcast_"))
async def confirm_broadcast(client: Client, callback_query: CallbackQuery):
    if not is_admin(callback_query.from_user.id):
        await callback_query.answer("❌ You are not an admin!", show_alert=True)
        return
    
    # Extract message ID
    msg_id = int(callback_query.data.split("_")[2])
    
    # Get the message to broadcast
    try:
        broadcast_msg = await client.get_messages(callback_query.message.chat.id, msg_id)
    except:
        await callback_query.answer("❌ Message not found!", show_alert=True)
        return
    
    await callback_query.edit_message_text("📢 **Broadcasting...**\n\nPlease wait...")
    
    # Get all users
    users = await get_all_users()
    
    success = 0
    failed = 0
    blocked = 0
    
    for user_id in users:
        try:
            await broadcast_msg.copy(user_id)
            success += 1
            
            # Update progress every 10 users
            if success % 10 == 0:
                await callback_query.edit_message_text(
                    f"📢 **Broadcasting...**\n\n"
                    f"✅ Success: {success}\n"
                    f"❌ Failed: {failed}\n"
                    f"🚫 Blocked: {blocked}\n"
                    f"📊 Progress: {success + failed + blocked}/{len(users)}"
                )
            
            await asyncio.sleep(0.05)  # Avoid flood
            
        except (UserIsBlocked, InputUserDeactivated):
            blocked += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await broadcast_msg.copy(user_id)
                success += 1
            except:
                failed += 1
        except Exception as e:
            failed += 1
            logger.error(f"Broadcast error for user {user_id}: {e}")
    
    # Final report
    await callback_query.edit_message_text(
        f"✅ **Broadcast Complete!**\n\n"
        f"📊 **Results:**\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}\n"
        f"🚫 Blocked: {blocked}\n"
        f"📈 Total: {len(users)}\n\n"
        f"Success Rate: {(success/len(users)*100):.1f}%"
    )


# Hook into start command to save users (non-blocking)
@Client.on_message(filters.command("start"), group=-1)
async def log_user(client: Client, message: Message):
    # Run user tracking in background without blocking the response
    asyncio.create_task(add_user(message.from_user.id, message.from_user, client))
