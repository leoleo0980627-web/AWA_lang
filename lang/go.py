# ~/awa/lang/go.py
import subprocess
import tempfile
import os
from .base import BaseLanguageHandler

class GoHandler(BaseLanguageHandler):
    def run(self, lines):
        # 讀 Python 的共享變數
        shared_vars = self.shared.import_to_other('py')
        
        # 產生 shared 結構
        shared_code = self._generate_shared_code(shared_vars)
        
        code = 'package main\n\n'
        code += 'import "fmt"\n\n'
        code += shared_code + '\n'
        code += 'func main() {\n'
        for line in lines:
            code += '    ' + line + '\n'
        code += '}\n'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
            f.write(code)
            f.flush()
            exe_file = f.name.replace('.go', '')
            try:
                subprocess.run(['go', 'build', '-o', exe_file, f.name], timeout=10, check=True)
                result = subprocess.run([exe_file], capture_output=True, text=True, timeout=5)
                if result.stdout:
                    print(result.stdout, end='')
                if result.stderr:
                    self.error(f"Go stderr: {result.stderr.strip()}")
            except FileNotFoundError:
                self.error("Go not installed")
            except subprocess.TimeoutExpired:
                self.error("Go timeout")
            except subprocess.CalledProcessError as e:
                self.error(f"Go compilation failed: {e}")
            finally:
                os.unlink(f.name)
                if os.path.exists(exe_file):
                    os.unlink(exe_file)

    def _generate_shared_code(self, shared_vars):
        if not shared_vars:
            return ""
        
        code = "var Shared = struct {\n"
        for key, value in shared_vars.items():
            go_type = self._go_type(value)
            code += f"    {key} {go_type}\n"
        code += "}{\n"
        for key, value in shared_vars.items():
            go_val = self._to_go_literal(value)
            code += f"    {key}: {go_val},\n"
        code += "}\n"
        return code

    def _go_type(self, value):
        if isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float64"
        elif isinstance(value, bool):
            return "bool"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            if not value:
                return "[]interface{}"
            if all(isinstance(x, int) for x in value):
                return "[]int"
            elif all(isinstance(x, str) for x in value):
                return "[]string"
            else:
                return "[]interface{}"
        else:
            return "interface{}"

    def _to_go_literal(self, value):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(value)
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            items = [self._to_go_literal(x) for x in value]
            if all(isinstance(x, int) for x in value):
                return "[]int{" + ", ".join(items) + "}"
            elif all(isinstance(x, str) for x in value):
                return "[]string{" + ", ".join(items) + "}"
            else:
                return "[]interface{}{" + ", ".join(items) + "}"
        else:
            return "nil"