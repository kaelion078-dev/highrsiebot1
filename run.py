import asyncio
import os
from highrise import *
from highrise.models import *
from bot import Mybot
from keep_alive import keep_alive

# شروع وب سرور
keep_alive()

async def main():
    room_id = os.getenv("ROOM_ID")
    bot_token = os.getenv("BOT_TOKEN")
    
    if not room_id or not bot_token:
        print("❌ ROOM_ID یا BOT_TOKEN تنظیم نشده!")
        return
    
    bot = Mybot()
    await bot.highrise.main(room_id, bot_token)

if __name__ == "__main__":
    asyncio.run(main())