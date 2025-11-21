"""
Quick diagnostic script to test if bot credentials work
Run this locally to verify your bot token is correct
"""
import asyncio
from pyrogram import Client
from config import Config

async def test_bot():
    print("Testing bot connection...")
    print(f"API_ID: {Config.API_ID}")
    print(f"API_HASH: {Config.API_HASH[:10]}..." if Config.API_HASH else "API_HASH: NOT SET")
    print(f"BOT_TOKEN: {Config.BOT_TOKEN[:20]}..." if Config.BOT_TOKEN else "BOT_TOKEN: NOT SET")
    
    if not Config.API_ID or not Config.API_HASH or not Config.BOT_TOKEN:
        print("\n❌ ERROR: Missing credentials in .env file!")
        return
    
    try:
        bot = Client(
            "test_session",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            in_memory=True
        )
        
        await bot.start()
        me = await bot.get_me()
        print(f"\n✅ Bot connected successfully!")
        print(f"Bot username: @{me.username}")
        print(f"Bot name: {me.first_name}")
        print(f"Bot ID: {me.id}")
        await bot.stop()
        
    except Exception as e:
        print(f"\n❌ Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot())
