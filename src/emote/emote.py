from highrise import User
import os
from .emote_manager import EmoteManager

# ایجاد نمونه از مدیریت ایموت
emote_manager = EmoteManager()

async def emote_command(bot, user: User, message: str):
    """دستور /emote - اجرای ایموت و دنس"""
    
    print(f"🔍 اجرای دستور emote توسط {user.username}")
    
    parts = message.split()
    
    # اگه فقط /emote زده باشه
    if len(parts) == 1:
        # صفحه اول رو نشون بده
        emote_list = emote_manager.get_emote_list_text(0)
        if emote_list:
            await bot.highrise.send_whisper(user.id, emote_list)
        else:
            await bot.highrise.send_whisper(user.id, "❌ لیست ایموت‌ها خالی است!")
        return
    
    # دستور stop
    if parts[1].lower() == "stop":
        if emote_manager.is_active(user.id):
            await emote_manager.stop_emote_loop(user.id)
            await bot.highrise.send_whisper(user.id, "⏹️ حلقه ایموت متوقف شد!")
        else:
            await bot.highrise.send_whisper(user.id, "❌ شما حلقه فعالی ندارید!")
        return
    
    # دستور next page
    if parts[1].lower() == "next":
        # پیدا کردن صفحه فعلی از روی پیام قبلی نمیشه، پس از اول نشون میدیم
        emote_list = emote_manager.get_emote_list_text(0)
        if emote_list:
            await bot.highrise.send_whisper(user.id, emote_list)
        else:
            await bot.highrise.send_whisper(user.id, "❌ لیست ایموت‌ها خالی است!")
        return
    
    # جستجوی ایموت
    search_term = ' '.join(parts[1:])
    emote = emote_manager.get_emote_by_name(search_term)
    
    if not emote:
        await bot.highrise.send_whisper(user.id, f"❌ ایموت '{search_term}' پیدا نشد!")
        return
    
    # شروع حلقه ایموت
    await emote_manager.start_emote_loop(
        bot, 
        user.id, 
        emote["value"], 
        emote["time"]
    )
    
    await bot.highrise.send_whisper(
        user.id, 
        f"▶️ شروع حلقه '{emote['text']}'\nبرای توقف: /emote stop"
    )