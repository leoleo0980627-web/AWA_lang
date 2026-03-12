# ~/awa/lang/ts.py
import subprocess
import tempfile
import os
import json
from .base import BaseLanguageHandler

class TypeScriptHandler(BaseLanguageHandler):
    def run(self, lines):
        # 讀 Python 的共享變數
        shared_vars = self.shared.import_to_python('py')
        
        # 轉成 TypeScript 型別定義
        ts_type = self._generate_ts_type(shared_vars)
        shared_json = json.dumps(shared_vars)
        
        code = ts_type + '\n'
        code += f"const shared: SharedData = {shared_json};\n\n"
        code += '\n'.join(lines)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write(code)
            f.flush()
            js_file = f.name.replace('.ts', '.js')
            try:
                subprocess.run(['tsc', f.name], timeout=5, check=True)
                result = subprocess.run(['node', js_file], capture_output=True, text=True, timeout=5)
                if result.stdout:
                    print(result.stdout, end='')
                if result.stderr:
                    self.error(f"TypeScript stderr: {result.stderr.strip()}")
            except FileNotFoundError:
                self.error("TypeScript or Node.js not installed")
            except subprocess.TimeoutExpired:
                self.error("TypeScript timeout")
            except subprocess.CalledProcessError as e:
                self.error(f"TypeScript compilation failed: {e}")
            finally:
                os.unlink(f.name)
                if os.path.exists(js_file):
                    os.unlink(js_file)

    def _generate_ts_type(self, d):
        if not d:
            return "type SharedData = {};"
        code = "type SharedData = {\n"
        for k, v in d.items():
            ts_type = self._ts_type(v)
            code += f"    {k}: {ts_type};\n"
        code += "};\n"
        return code

    def _ts_type(self, value):
        if isinstance(value, int):
            return "number"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            if not value:
                return "any[]"
            return self._ts_type(value[0]) + "[]"
        elif isinstance(value, dict):
            return "Record<string, any>"
        else:
            return "any"