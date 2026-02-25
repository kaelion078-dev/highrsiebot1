from highrise import *
from highrise.models import *
from events.welcomem import welcome_user
from src.moderation.kick import kick_command
from src.moderation.come import come_command
from src.moderation.equip import equip_command
from src.moderation.userinfo import userinfo_command
from src.moderation.admin import admin_command
from src.commands.help_command import help_command
from src.emote import emote_manager
from config.permission_manager import PermissionManager
import asyncio

perm_manager = PermissionManager()

class Mybot(BaseBot):
    def __init__(self):
        super().__init__()
        self.bot_id = None
        self.bot_emote_task = None
        # ایموت ثابت برای بات
        self.bot_emote = {
            "value": "idle-loop-annoyed",  # ایموت ربات
            "time": 17.058522,              # تایمش
            "name": "Annoyed"           # اسمش
        }
    
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("✅ ربات با موفقیت وصل شد!")
        self.bot_id = session_metadata.user_id
        await self.highrise.chat("🟢 ربات فعال شد!")
        
        # شروع ایموت لوپ برای بات
        await self.start_bot_emote_loop()
    
    async def start_bot_emote_loop(self):
        """شروع حلقه ایموت برای خود بات"""
        if self.bot_emote_task and not self.bot_emote_task.done():
            self.bot_emote_task.cancel()
        
        self.bot_emote_task = asyncio.create_task(
            self._bot_emote_loop(
                self.bot_emote["value"], 
                self.bot_emote["time"]
            )
        )
        print(f"🤖 ایموت '{self.bot_emote['name']}' برای بات شروع شد")
    
    async def stop_bot_emote_loop(self):
        """متوقف کردن ایموت لوپ بات"""
        if self.bot_emote_task and not self.bot_emote_task.done():
            self.bot_emote_task.cancel()
            print(f"🤖 ایموت '{self.bot_emote['name']}' برای بات متوقف شد")
    
    async def _bot_emote_loop(self, emote_value: str, emote_time: float):
        """حلقه داخلی برای اجرای ایموت بات"""
        try:
            while True:
                await self.highrise.send_emote(emote_value, self.bot_id)
                await asyncio.sleep(emote_time)
        except asyncio.CancelledError:
            print("✅ ایموت لوپ بات متوقف شد")
        except Exception as e:
            print(f"❌ خطا در ایموت لوپ بات: {e}")
    
    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        await welcome_user(self, user, position)
    
    async def on_chat(self, user: User, message: str) -> None:
        print(f"💬 پیام از {user.username}: {message}")
        
        # دستورات با /
        if message.startswith("/"):
            command = message[1:].lower()
            
            if command.startswith("kick"):
                await kick_command(self, user, command)
            
            elif command.startswith("come"):
                await come_command(self, user, command)
            
            elif command.startswith("equip"):
                await equip_command(self, user, command)
            
            elif command.startswith("userinfo"):
                await userinfo_command(self, user, command)
            
            elif command.startswith("admin"):
                await admin_command(self, user, command)
            
            elif command.startswith("help"):
                await help_command(self, user, command)
            
            # دستور botemote با بررسی پرمیشن از فایل JSON
            elif command.startswith("botemote"):
                # بررسی دسترسی admin از پرمیشن‌ها
                user_permissions = perm_manager.get_user_permissions(user.id, user.username)
                
                if "admin" not in user_permissions:
                    await self.highrise.send_whisper(user.id, "❌ شما اجازه استفاده از این دستور را ندارید!")
                    return
                
                parts = command.split()
                if len(parts) > 1:
                    emote_name = ' '.join(parts[1:])
                    emote = emote_manager.get_emote_by_name(emote_name)
                    if emote:
                        self.bot_emote = {
                            "value": emote["value"],
                            "time": emote["time"],
                            "name": emote["text"]
                        }
                        await self.start_bot_emote_loop()
                        await self.highrise.send_whisper(user.id, f"✅ ایموت بات به {emote['text']} تغییر کرد!")
                    else:
                        await self.highrise.send_whisper(user.id, "❌ ایموت پیدا نشد!")
                else:
                    await self.highrise.send_whisper(user.id, f"🤖 ایموت فعلی بات: {self.bot_emote['name']}")
            
            return
        
        # پیام‌های بدون /
        msg_lower = message.lower().strip()
        
        # دستور stop
        if msg_lower == "stop":
            if emote_manager.is_active(user.id):
                await emote_manager.stop_emote_loop(user.id)
                await self.highrise.send_whisper(user.id, "✅ ایموت متوقف شد!")
            else:
                await self.highrise.send_whisper(user.id, "❌ شما ایموت فعالی ندارید!")
            return
        
        # بررسی ایموت
        emote = emote_manager.get_emote_by_name(msg_lower)
        
        if emote:
            await emote_manager.start_emote_loop(
                self, 
                user.id, 
                emote["value"], 
                emote["time"],
                emote["text"]
            )
            
            await self.highrise.send_whisper(
                user.id, 
                f"✅ ایموت '{emote['text']}' شروع شد!\nبرای توقف: stop"
            )