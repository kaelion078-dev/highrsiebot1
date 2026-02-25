import json
import asyncio
import os
import re

class EmoteManager:
    def __init__(self, config_file="config/emotes.json"):
        self.config_file = config_file
        self.emotes = self._load_emotes()
        self.active_loops = {}  # {user_id: {"task": task, "emote": emote, "name": name}}
    
    def _load_emotes(self):
        """بارگذاری لیست ایموت‌ها از فایل JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"⚠️ فایل {self.config_file} یافت نشد!")
                return []
        except Exception as e:
            print(f"❌ خطا در خواندن فایل JSON: {e}")
            return []
    
    def _normalize_text(self, text: str) -> str:
        """حذف فاصله‌ها و علائم و کوچک کردن حروف"""
        text = text.lower()
        text = text.replace(" ", "")
        text = re.sub(r'[^\w]', '', text)
        return text
    
    def get_emote_by_name(self, name: str):
        """پیدا کردن ایموت بر اساس اسم یا عدد"""
        if name.isdigit():
            index = int(name) - 1
            if 0 <= index < len(self.emotes):
                return self.emotes[index]
            return None
        
        search_name = self._normalize_text(name)
        
        for emote in self.emotes:
            emote_text = self._normalize_text(emote["text"])
            emote_value = self._normalize_text(emote["value"])
            
            if search_name in emote_text or search_name in emote_value:
                return emote
            
            if search_name == emote_text or search_name == emote_value:
                return emote
        
        return None
    
    async def start_emote_loop(self, bot, user_id: str, emote_value: str, emote_time: float, emote_name: str = ""):
        """شروع حلقه ایموت برای یک کاربر - 5 پارامتر"""
        
        # اگه اسم ایموت داده نشده، از مقدار پیش‌فرض استفاده کن
        if not emote_name:
            emote_name = emote_value
        
        # اگه قبلاً حلقه فعال داشته، متوقفش کن
        await self.stop_emote_loop(user_id)
        
        # ایجاد تسک جدید
        task = asyncio.create_task(self._emote_loop(bot, user_id, emote_value, emote_time))
        self.active_loops[user_id] = {
            "task": task,
            "emote": emote_value,
            "name": emote_name
        }
        return True
    
    async def stop_emote_loop(self, user_id: str):
        """متوقف کردن حلقه ایموت برای یک کاربر"""
        if user_id in self.active_loops:
            self.active_loops[user_id]["task"].cancel()
            del self.active_loops[user_id]
            return True
        return False
    
    async def _emote_loop(self, bot, user_id: str, emote_value: str, emote_time: float):
        """حلقه داخلی برای اجرای مداوم ایموت"""
        try:
            while True:
                # ارسال ایموت به کاربر
                await bot.highrise.send_emote(emote_value, user_id)
                # منتظر موندن به اندازه تایم ایموت
                await asyncio.sleep(emote_time)
        except asyncio.CancelledError:
            print(f"✅ حلقه ایموت برای کاربر {user_id} متوقف شد")
        except Exception as e:
            print(f"❌ خطا در حلقه ایموت: {e}")
    
    def is_active(self, user_id: str) -> bool:
        """بررسی اینکه آیا کاربر حلقه فعال دارد"""
        return user_id in self.active_loops
    
    def get_active_emote(self, user_id: str):
        """دریافت ایموت فعال کاربر"""
        if user_id in self.active_loops:
            return self.active_loops[user_id]["name"]
        return None