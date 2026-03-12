# ~/awa/lang/js.py
import subprocess
import tempfile
import os
import json
from .base import BaseLanguageHandler

class JavaScriptHandler(BaseLanguageHandler):
    def run(self, lines):
        # 讀取共享變數
        shared_vars = self.shared.import_to_python('py')
        
        # 轉成 JSON 字串
        shared_json = json.dumps(shared_vars)
        
        # 產生 JS 程式碼，把共享變數注入成全域物件
        code = f"const shared = {shared_json};\n\n"
        code += '\n'.join(lines)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            f.flush()
            try:
                result = subprocess.run(['node', f.name], capture_output=True, text=True, timeout=5)
                if result.stdout:
                    print(result.stdout, end='')
                if result.stderr:
                    self.error(f"JS stderr: {result.stderr.strip()}")
            except FileNotFoundError:
                self.error("Node.js not installed")
            except subprocess.TimeoutExpired:
                self.error("JS timeout")
            finally:
                os.unlink(f.name)