from highrise import User
from config.permission_manager import PermissionManager

perm_manager = PermissionManager()

async def help_command(bot, user: User, message: str):
    """دستور /help - نمایش لیست دستورات"""
    
    print(f"🔍 اجرای دستور help توسط {user.username}")
    
    user_permissions = perm_manager.get_user_permissions(user.id, user.username)
    
    if not user_permissions:
        await bot.highrise.send_whisper(user.id, "❌ شما دسترسی به ربات ندارید!")
        return
    
    commands = ["/help"]
    
    if "kick" in user_permissions:
        commands.append("/kick @user")
    
    if "come" in user_permissions:
        commands.append("/come")
    
    if "equip" in user_permissions:
        commands.append("/equip")
    
    if "userinfo" in user_permissions:
        commands.append("/userinfo @user")
    
    if "admin" in user_permissions or user.username == "PhaNtOMExe_":
        commands.append("/admin")
    
    commands_text = " | ".join(commands)
    
    # یه توضیح برای ایموت‌ها اضافه کن
    emote_help = "\n\n💃 برای ایموت: فقط عدد یا اسمش رو بنویس (مثلا: 5 یا dance)\nبرای توقف: stop"
    
    await bot.highrise.send_whisper(user.id, f"📌 دستورات شما: {commands_text}{emote_help}")