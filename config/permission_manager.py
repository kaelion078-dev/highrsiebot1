import json
import os

class PermissionManager:
    def __init__(self, config_file="config/permissions.json"):
        self.config_file = config_file
        
    def _read_file(self):
        """خوندن مستقیم از فایل"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "permissions" not in data:
                        data = {"permissions": []}
                    return data
            else:
                # ایجاد فایل خالی
                default_data = {"permissions": []}
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, indent=4, ensure_ascii=False)
                return default_data
        except Exception as e:
            print(f"❌ خطا در خواندن فایل: {e}")
            return {"permissions": []}
    
    def _write_file(self, data):
        """نوشتن مستقیم در فایل"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ خطا در نوشتن فایل: {e}")
            return False
    
    def get_user_permissions(self, user_id: str, username: str) -> list:
        """دریافت لیست دسترسی‌های یک کاربر - همیشه از فایل می‌خونه"""
        
        # مستقیم از فایل بخون
        data = self._read_file()
        
        # اول با user_id (دقیق‌ترین روش)
        for user in data["permissions"]:
            if user["user_id"] == user_id:
                print(f"✅ {username} با آیدی پیدا شد: {user['permissions']}")
                return user["permissions"]
        
        # بعد با username
        for user in data["permissions"]:
            if user["username"].lower() == username.lower():
                print(f"✅ {username} با یوزرنیم پیدا شد: {user['permissions']}")
                return user["permissions"]
        
        # پیدا نشد
        print(f"❌ {username} در لیست نیست!")
        return []
    
    def has_permission(self, user_id: str, username: str, permission: str) -> bool:
        """بررسی دسترسی خاص"""
        permissions = self.get_user_permissions(user_id, username)
        return permission in permissions
    
    def get_all_users(self) -> list:
        """لیست همه کاربران"""
        data = self._read_file()
        return data["permissions"]
    
    def add_user(self, user_id: str, username: str, permissions: list) -> bool:
        """اضافه کردن کاربر جدید"""
        data = self._read_file()
        
        # چک کن قبلاً نباشه
        for user in data["permissions"]:
            if user["user_id"] == user_id or user["username"].lower() == username.lower():
                print(f"⚠️ {username} قبلاً وجود دارد!")
                return False
        
        # اضافه کن
        new_user = {
            "user_id": user_id,
            "username": username,
            "permissions": permissions
        }
        data["permissions"].append(new_user)
        
        # ذخیره کن
        success = self._write_file(data)
        if success:
            print(f"✅ {username} با دسترسی‌های {permissions} اضافه شد")
        return success
    
    def update_user_permissions(self, user_id: str, username: str, permissions: list) -> bool:
        """به‌روزرسانی دسترسی‌ها"""
        data = self._read_file()
        
        for i, user in enumerate(data["permissions"]):
            if user["user_id"] == user_id or user["username"].lower() == username.lower():
                data["permissions"][i]["permissions"] = permissions
                if user["user_id"] != user_id and user_id:
                    data["permissions"][i]["user_id"] = user_id
                
                success = self._write_file(data)
                if success:
                    print(f"✅ دسترسی‌های {username} به {permissions} تغییر کرد")
                return success
        
        print(f"❌ {username} پیدا نشد")
        return False
    
    def remove_user(self, user_id: str, username: str) -> bool:
        """حذف کاربر"""
        data = self._read_file()
        
        for i, user in enumerate(data["permissions"]):
            if user["user_id"] == user_id or user["username"].lower() == username.lower():
                removed = data["permissions"].pop(i)
                success = self._write_file(data)
                if success:
                    print(f"✅ {removed['username']} حذف شد")
                return success
        
        print(f"❌ {username} پیدا نشد")
        return False
    
    def reload_permissions(self):
        """ریلود - اینجا کاری نمی‌کنه چون همیشه از فایل می‌خونیم"""
        print("🔄 دسترسی‌ها ریلود شدند (همیشه تازه هستند)")
        return self._read_file()