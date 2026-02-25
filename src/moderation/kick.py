from highrise import User
from config.permission_manager import PermissionManager

perm_manager = PermissionManager()

async def kick_command(bot, user: User, message: str):
    """مدیریت دستور /kick"""
    
    print(f"🔍 اجرای دستور kick توسط {user.username}")

    perm_manager.reload_permissions()
    
    # بررسی دسترسی
    if not perm_manager.has_permission(user.id, user.username, "kick"):
        await bot.highrise.send_whisper(user.id, "❌ شما اجازه استفاده از این دستور را ندارید!")
        return
    
    parts = message.split()
    
    if len(parts) != 2:
        await bot.highrise.send_whisper(user.id, "❌ فرمت صحیح: /kick @username")
        return
    
    # استخراج یوزرنیم
    if "@" not in parts[1]:
        username = parts[1]
    else:
        username = parts[1][1:]
    
    # پیدا کردن کاربر
    room_users = (await bot.highrise.get_room_users()).content
    target_id = None
    
    for room_user, pos in room_users:
        if room_user.username.lower() == username.lower():
            target_id = room_user.id
            break
    
    if not target_id:
        await bot.highrise.send_whisper(user.id, f"❌ کاربر {username} در روم نیست!")
        return
    
    if target_id == user.id:
        await bot.highrise.send_whisper(user.id, "❌ نمی‌تونی خودت رو kick کنی!")
        return
    
    try:
        await bot.highrise.moderate_room(target_id, "kick")
        await bot.highrise.chat(f"👢 {username} از روم اخراج شد!")
        await bot.highrise.send_whisper(user.id, f"✅ {username} با موفقیت kick شد!")
        
    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"❌ خطا: {e}")