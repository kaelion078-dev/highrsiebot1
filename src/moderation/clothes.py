from highrise import Item
import json
import os

# خط زیر رو پاک کن یا کامنت کن:
# from .clothes import ClothesManager  ← ❌ این رو بردار

class ClothesManager:
    def __init__(self, config_file="config/clothes.json"):
        self.config_file = config_file
        self.outfits = self._load_outfits()
    
    def _load_outfits(self):
        """بارگذاری لباس‌ها از فایل JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # تبدیل دیکشنری‌ها به آبجکت Item
                    outfits = {}
                    for outfit_name, items_data in data.items():
                        outfits[outfit_name] = [
                            Item(
                                type=item["type"],
                                amount=item["amount"],
                                id=item["id"],
                                account_bound=item["account_bound"],
                                active_palette=item["active_palette"]
                            ) for item in items_data
                        ]
                    return outfits
            else:
                print(f"⚠️ فایل {self.config_file} یافت نشد!")
                return {"default": []}
        except Exception as e:
            print(f"❌ خطا در خواندن فایل JSON: {e}")
            return {"default": []}
    
    def get_outfit(self, outfit_name="default", reload=True):
        """دریافت یک ست لباس - با قابلیت بارگذاری مجدد"""
        if reload:
            self.outfits = self._load_outfits()
        return self.outfits.get(outfit_name, self.outfits.get("default", []))
    
    def list_outfits(self, reload=True):
        """لیست همه ست‌های موجود - با قابلیت بارگذاری مجدد"""
        if reload:
            self.outfits = self._load_outfits()
        return list(self.outfits.keys())
    
    def get_outfit_names(self, outfit_name="default"):
        """دریافت نام فارسی لباس‌های یک ست (برای نمایش)"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                items = data.get(outfit_name, [])
                return [item.get("name", item["id"]) for item in items if "name" in item]
        except:
            return []
    
    def reload_outfits(self):
        """بارگذاری مجدد فایل JSON"""
        self.outfits = self._load_outfits()
        print("🔄 لباس‌ها دوباره بارگذاری شدند")