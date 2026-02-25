from highrise import User, Position, AnchorPosition
from src.emote import emote_manager

async def welcome_user(bot, user: User, position: Position | AnchorPosition):
    """تابع خوشامدگویی به فارسی - فقط برای خود کاربر نمایش داده میشه"""
    
    # تعداد کل ایموت‌ها
    total_emotes = len(emote_manager.emotes)
    
    # پیام خوشامدگویی - ارسال به صورت خصوصی
    welcome_text = f"👋 سلام {user.username}! به روم خوش اومدی!\n"
    welcome_text += f"🎮 {total_emotes} تا ایموت دنس داریم!\n"
    welcome_text += "💃 برای اجرا: عدد یا اسم ایموت رو بنویس\n"
    welcome_text += "⏹️ برای توقف: stop"
    
    # ارسال به صورت whisper (فقط خود کاربر می‌بینه)
    await bot.highrise.send_whisper(user.id, welcome_text)
    
