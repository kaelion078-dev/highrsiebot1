from highrise import User, Position, AnchorPosition
from config.permission_manager import PermissionManager

perm_manager = PermissionManager()

async def userinfo_command(bot, user: User, message: str):
    """دستور /userinfo - نمایش اطلاعات کاربر"""
    
    print(f"🔍 اجرای دستور userinfo توسط {user.username}")

    perm_manager.reload_permissions()
    
    # بررسی دسترسی (فقط ادمین‌ها)
    user_permissions = perm_manager.get_user_permissions(user.id, user.username)
    if not user_permissions:
        await bot.highrise.send_whisper(user.id, "❌ شما اجازه استفاده از این دستور را ندارید!")
        return
    
    parts = message.split()
    
    # اگه فقط /userinfo زده باشه
    if len(parts) == 1:
        await bot.highrise.send_whisper(user.id, "❌ فرمت صحیح: /userinfo @username یا /userinfo [user_id]")
        return
    
    target = parts[1]
    target_id = None
    target_username = None
    
    # گرفتن لیست کاربران آنلاین
    room_users_response = await bot.highrise.get_room_users()
    room_users = room_users_response.content
    
    # اگه با @ زده باشه
    if target.startswith("@"):
        username = target[1:]  # حذف @
        for room_user, pos in room_users:
            if room_user.username.lower() == username.lower():
                target_id = room_user.id
                target_username = room_user.username
                user_position = pos
                break
    
    # اگه با آیدی زده باشه
    else:
        for room_user, pos in room_users:
            if room_user.id == target:
                target_id = room_user.id
                target_username = room_user.username
                user_position = pos
                break
    
    # اگه کاربر پیدا نشد
    if not target_id:
        await bot.highrise.send_whisper(user.id, f"❌ کاربر '{target}' در روم پیدا نشد!")
        return
    
    # استخراج مختصات
    if isinstance(user_position, Position):
        x, y, z = user_position.x, user_position.y, user_position.z
        pos_type = "عادی"
    elif isinstance(user_position, AnchorPosition):
        x, y, z = user_position.x, user_position.y, user_position.z
        pos_type = "Anchor"
    else:
        x, y, z = "?", "?", "?"
        pos_type = "نامشخص"
    
    # ساخت پیام اطلاعات
    info_text = f"📊 اطلاعات کاربر {target_username}:\n"
    info_text += f"🆔 آیدی: {target_id}\n"
    info_text += f"📍 موقعیت: X={x}, Y={y}, Z={z}\n"
    info_text += f"📌 نوع موقعیت: {pos_type}"
    
    # دسترسی‌های کاربر (اگه توی پرمیشن هست)
    user_perms = perm_manager.get_user_permissions(target_id, target_username)
    if user_perms:
        perms_text = "، ".join(user_perms)
        info_text += f"\n🔑 دسترسی‌ها: {perms_text}"
    else:
        info_text += f"\n🔑 دسترسی‌ها: ندارد"
    
    await bot.highrise.send_whisper(user.id, info_text)
    print(f"✅ اطلاعات {target_username} برای {user.username} ارسال شد")