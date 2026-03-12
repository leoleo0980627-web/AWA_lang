# ~/awa/lang/csharp.py
import subprocess
import tempfile
import os
import platform
from .base import BaseLanguageHandler

class CSharpHandler(BaseLanguageHandler):
    def run(self, lines):
        # 讀 Python 的共享變數
        shared_vars = self.shared.import_to_other('py')
        
        # 產生 shared 類別
        shared_code = self._generate_shared_code(shared_vars)
        
        code = 'using System;\n'
        code += 'using System.Collections.Generic;\n\n'
        code += shared_code + '\n'
        code += 'class Program {\n'
        code += '    static void Main() {\n'
        for line in lines:
            code += '        ' + line + '\n'
        code += '    }\n'
        code += '}\n'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cs', delete=False) as f:
            f.write(code)
            f.flush()
            exe_file = f.name.replace('.cs', '.exe')
            try:
                if platform.system() == 'Windows':
                    subprocess.run(['csc', f.name], timeout=10, check=True)
                else:
                    subprocess.run(['mcs', f.name], timeout=10, check=True)
                runner = ['mono', exe_file] if platform.system() != 'Windows' else [exe_file]
                result = subprocess.run(runner, capture_output=True, text=True, timeout=5)
                if result.stdout:
                    print(result.stdout, end='')
                if result.stderr:
                    self.error(f"C# stderr: {result.stderr.strip()}")
            except FileNotFoundError:
                self.error("C# compiler not installed")
            except subprocess.TimeoutExpired:
                self.error("C# timeout")
            except subprocess.CalledProcessError as e:
                self.error(f"C# compilation failed: {e}")
            finally:
                os.unlink(f.name)
                if os.path.exists(exe_file):
                    os.unlink(exe_file)

    def _generate_shared_code(self, shared_vars):
        if not shared_vars:
            return ""
        
        code = "public static class SharedData {\n"
        for key, value in shared_vars.items():
            cs_type = self._cs_type(value)
            cs_val = self._to_cs_literal(value)
            code += f"    public static {cs_type} {key} = {cs_val};\n"
        code += "}\n"
        return code

    def _cs_type(self, value):
        if isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "double"
        elif isinstance(value, bool):
            return "bool"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            if all(isinstance(x, int) for x in value):
                return "int[]"
            elif all(isinstance(x, str) for x in value):
                return "string[]"
            else:
                return "object[]"
        else:
            return "object"

    def _to_cs_literal(self, value):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(value)
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            items = [self._to_cs_literal(x) for x in value]
            return "new " + self._cs_type(value) + " {" + ", ".join(items) + "}"
        else:
            return "null"