from highrise import User, Position, AnchorPosition
from config.permission_manager import PermissionManager

perm_manager = PermissionManager()

async def come_command(bot, user: User, message: str):
    """دستور /come - بات به سمت ادمین می‌آید"""
    
    print(f"🔍 اجرای دستور come توسط {user.username}")
    
    # بررسی دسترسی
    if not perm_manager.has_permission(user.id, user.username, "come"):
        await bot.highrise.send_whisper(user.id, "❌ شما اجازه استفاده از این دستور را ندارید!")
        return
    
    if not hasattr(bot, 'bot_id') or not bot.bot_id:
        await bot.highrise.send_whisper(user.id, "❌ آیدی بات پیدا نشد!")
        return
    
    try:
        room_users_response = await bot.highrise.get_room_users()
        room_users = room_users_response.content
        
        # پیدا کردن موقعیت ادمین
        admin_position = None
        for room_user, pos in room_users:
            if room_user.id == user.id:
                if isinstance(pos, Position):
                    admin_position = pos
                elif isinstance(pos, AnchorPosition):
                    admin_position = Position(pos.x, pos.y, pos.z)
                break
        
        if not admin_position:
            await bot.highrise.send_whisper(user.id, "❌ نمی‌تونم موقعیت شما رو پیدا کنم!")
            return
        
        # تلپورت بات
        await bot.highrise.teleport(bot.bot_id, admin_position)
        await bot.highrise.send_whisper(user.id, f"✅ بات به سمت شما آمد!")
        
    except Exception as e:
        await bot.highrise.send_whisper(user.id, f"❌ خطا: {str(e)}")