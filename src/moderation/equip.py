from highrise import User
from config.permission_manager import PermissionManager
from .clothes import ClothesManager  # این خط درسته

perm_manager = PermissionManager()
clothes_manager = ClothesManager()

async def equip_command(bot, user: User, message: str):
    """دستور /equip - تغییر لباس بات"""
    
    print(f"🔍 اجرای دستور equip توسط {user.username}")

    perm_manager.reload_permissions()
    
    user_permissions = perm_manager.get_user_permissions(user.id, user.username)
    if not user_permissions:
        await bot.highrise.send_whisper(user.id, "❌ شما اجازه استفاده از این دستور را ندارید!")
        return
    
    parts = message.split()
    
    if len(parts) == 1:
        outfits = clothes_manager.list_outfits(reload=True)
        outfits_text = "، ".join(outfits)
        await bot.highrise.send_whisper(user.id, f"📋 ست‌های موجود: {outfits_text}\nبرای استفاده: /equip [نام ست]")
        return
    
    if parts[1] == "reload":
        clothes_manager.reload_outfits()
        await bot.highrise.send_whisper(user.id, "🔄 لباس‌ها دوباره بارگذاری شدند!")
        return
    
    try:
        outfit_name = parts[1]
        selected_outfit = clothes_manager.get_outfit(outfit_name, reload=True)
        
        if not selected_outfit:
            await bot.highrise.send_whisper(user.id, f"❌ ست لباس '{outfit_name}' وجود ندارد!")
            return
        
        await bot.highrise.set_outfit(outfit=selected_outfit)
        await bot.highrise.send_whisper(user.id, f"✅ لباس بات به ست '{outfit_name}' تغییر کرد!")
        
    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"❌ خطا: {str(e)}")