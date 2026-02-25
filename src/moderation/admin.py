from highrise import User
from config.permission_manager import PermissionManager
import json
import os

perm_manager = PermissionManager()

async def admin_command(bot, user: User, message: str):
    """دستور /admin - مدیریت ساده ادمین‌ها"""
    
    print(f"🔍 اجرای دستور admin توسط {user.username}")

    perm_manager.reload_permissions()
    
    # بررسی دسترسی
    user_permissions = perm_manager.get_user_permissions(user.id, user.username)
    
    if "admin" not in user_permissions and user.username != "PhaNtOMExe_":
        await bot.highrise.send_whisper(user.id, "❌ شما اجازه ندارید!")
        return
    
    parts = message.split()
    
    if len(parts) < 2:
        help_text = "📌 راهنما:\n"
        help_text += "/admin list - لیست ادمین‌ها\n"
        help_text += "/admin new @user [perm1 perm2] - ادمین جدید\n"
        help_text += "/admin edit @user [perm1 perm2] - ویرایش دسترسی\n"
        help_text += "/admin remove @user - حذف ادمین"
        await bot.highrise.send_whisper(user.id, help_text)
        return
    
    action = parts[1].lower()
    
    # خوندن فایل JSON
    config_file = "config/permissions.json"
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = {"permissions": []}
    
    # ================ لیست ادمین‌ها ================
    if action == "list":
        if not data["permissions"]:
            await bot.highrise.send_whisper(user.id, "📋 هیچ ادمینی نیست!")
            return
        
        msg = "👑 **لیست ادمین‌ها**\n"
        msg += "────────────────\n"
        
        for i, admin in enumerate(data["permissions"], 1):
            # نام کاربر
            msg += f"{i}. **{admin['username']}**\n"
            
            # دسترسی‌ها
            perms = admin['permissions']
            if perms:
                msg += f"   └ "
                for j, perm in enumerate(perms):
                    if j > 0:
                        msg += " • "
                    msg += f"`{perm}`"
                msg += "\n"
            else:
                msg += "   └ `بدون دسترسی`\n"
            
            # خط جداکننده
            if i < len(data["permissions"]):
                msg += "────────────────\n"
        
        await bot.highrise.send_whisper(user.id, msg)
        return
    
    if len(parts) < 3:
        await bot.highrise.send_whisper(user.id, "❌ کاربر رو مشخص کن!")
        return
    
    # استخراج یوزرنیم
    if parts[2].startswith("@"):
        username = parts[2][1:]
    else:
        username = parts[2]
    
    # پیدا کردن آیدی کاربر
    room_users_response = await bot.highrise.get_room_users()
    room_users = room_users_response.content
    
    user_id = None
    for room_user, pos in room_users:
        if room_user.username.lower() == username.lower():
            user_id = room_user.id
            break
    
    # پیدا کردن کاربر توی فایل
    target_user = None
    target_index = -1
    
    for i, existing_user in enumerate(data["permissions"]):
        if existing_user["username"].lower() == username.lower() or existing_user["user_id"] == user_id:
            target_user = existing_user
            target_index = i
            break
    
    # ================ ادمین جدید ================
    if action == "new":
        if target_user:
            await bot.highrise.send_whisper(user.id, f"❌ {username} قبلاً ادمینه!")
            return
        
        if not user_id:
            await bot.highrise.send_whisper(user.id, f"❌ {username} تو روم نیست!")
            return
        
        # دسترسی‌ها
        if len(parts) > 3:
            perms = parts[3:]
        else:
            perms = ["kick", "come", "equip", "help", "userinfo"]
        
        new_admin = {
            "user_id": user_id,
            "username": username,
            "permissions": perms
        }
        
        data["permissions"].append(new_admin)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        perm_manager.reload_permissions()
        
        perms_text = " ".join(perms)
        await bot.highrise.send_whisper(user.id, f"✅ {username} ادمین شد با دسترسی: {perms_text}")
        
        if user_id:
            try:
                await bot.highrise.send_whisper(user_id, f"🎉 شما ادمین شدید! دسترسی‌ها: {perms_text}")
            except:
                pass
        return
    
    # ================ ویرایش دسترسی ================
    elif action == "edit":
        if not target_user:
            await bot.highrise.send_whisper(user.id, f"❌ {username} ادمین نیست!")
            return
        
        if len(parts) < 4:
            # نمایش دسترسی‌های فعلی
            current_perms = " ".join(target_user["permissions"])
            await bot.highrise.send_whisper(user.id, f"📋 دسترسی‌های فعلی {username}: {current_perms}")
            return
        
        new_perms_input = parts[3:]
        current_perms = target_user["permissions"]
        
        added = []
        removed = []
        
        for perm in new_perms_input:
            if perm.startswith("-"):
                # حذف دسترسی
                perm_name = perm[1:]
                if perm_name in current_perms:
                    current_perms.remove(perm_name)
                    removed.append(perm_name)
            elif perm.startswith("+"):
                # اضافه کردن دسترسی
                perm_name = perm[1:]
                if perm_name not in current_perms:
                    current_perms.append(perm_name)
                    added.append(perm_name)
            else:
                # اگه + یا - نداشت، خودکار تشخیص بده
                if perm in current_perms:
                    current_perms.remove(perm)
                    removed.append(perm)
                else:
                    current_perms.append(perm)
                    added.append(perm)
        
        if added or removed:
            target_user["permissions"] = current_perms
            data["permissions"][target_index] = target_user
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            perm_manager.reload_permissions()
            
            result_msg = []
            if added:
                result_msg.append(f"➕ {', '.join(added)}")
            if removed:
                result_msg.append(f"➖ {', '.join(removed)}")
            
            await bot.highrise.send_whisper(user.id, f"✅ {username}: {' | '.join(result_msg)}")
            
            if user_id:
                try:
                    await bot.highrise.send_whisper(user_id, f"🔄 دسترسی‌های شما تغییر کرد: {' | '.join(result_msg)}")
                except:
                    pass
        else:
            await bot.highrise.send_whisper(user.id, "❌ هیچ تغییری اعمال نشد!")
        return
    
    # ================ حذف ادمین ================
    elif action == "remove":
        if not target_user:
            await bot.highrise.send_whisper(user.id, f"❌ {username} ادمین نیست!")
            return
        
        data["permissions"].pop(target_index)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        perm_manager.reload_permissions()
        
        await bot.highrise.send_whisper(user.id, f"✅ {username} از ادمینی حذف شد!")
        
        if user_id:
            try:
                await bot.highrise.send_whisper(user_id, f"⚠️ شما از ادمینی حذف شدید!")
            except:
                pass
        return
    
    else:
        await bot.highrise.send_whisper(user.id, "❌ دستور نامعتبر! از help استفاده کن.")