# ~/awa/shared/storage.py
# 共享儲存層（MessagePack 版 + 布林值自動轉換）

import os
import msgpack

SHARED_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'shared.msgpack')

class SharedStorage:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        """從檔案載入共享資料"""
        if os.path.exists(SHARED_FILE):
            try:
                with open(SHARED_FILE, 'rb') as f:
                    self.data = msgpack.unpackb(f.read())
            except:
                self.data = {}
        else:
            self.data = {}

    def save(self):
        """儲存共享資料到檔案"""
        # 確保目錄存在
        os.makedirs(os.path.dirname(SHARED_FILE), exist_ok=True)
        with open(SHARED_FILE, 'wb') as f:
            f.write(msgpack.packb(self.data))

    def get_namespace(self, lang):
        """取得特定語言的命名空間"""
        if lang not in self.data:
            self.data[lang] = {}
        return self.data[lang]

    def set(self, lang, key, value):
        """設定共享變數"""
        self.get_namespace(lang)[key] = value
        self.save()

    def get(self, lang, key, default=None):
        """取得共享變數"""
        return self.get_namespace(lang).get(key, default)

    def delete(self, lang, key):
        """刪除共享變數"""
        if lang in self.data and key in self.data[lang]:
            del self.data[lang][key]
            self.save()

    def clear_lang(self, lang):
        """清除特定語言的所有共享變數"""
        if lang in self.data:
            del self.data[lang]
            self.save()

    def clear_all(self):
        """清除所有共享資料"""
        self.data = {}
        self.save()

    def _convert_bools(self, obj):
        """遞迴轉換布林值為字串 "true"/"false"（給其他語言用）"""
        if isinstance(obj, dict):
            return {k: self._convert_bools(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_bools(x) for x in obj]
        elif isinstance(obj, bool):
            return str(obj).lower()  # True → "true", False → "false"
        else:
            return obj

    def import_to_python(self, lang):
        """將共享變數轉成 Python dict（供 exec 使用）"""
        raw = self.get_namespace(lang)
        return raw.copy()  # Python 保留 True/False

    def import_to_other(self, lang):
        """將共享變數轉成其他語言可用的格式（布林值轉成字串）"""
        raw = self.get_namespace(lang)
        return self._convert_bools(raw)

    def export_from_python(self, lang, globals_dict):
        """從 Python globals 取出變數存回共享"""
        namespace = self.get_namespace(lang)
        changed = False
        for k, v in globals_dict.items():
            if not k.startswith('_') and k not in ('__builtins__', '__name__', '__doc__', '__package__', '__loader__', '__spec__'):
                if k not in namespace or namespace[k] != v:
                    namespace[k] = v
                    changed = True
        if changed:
            self.save()