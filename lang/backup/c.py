# ~/awa/lang/c.py
import subprocess
import tempfile
import os
from .base import BaseLanguageHandler

class CHandler(BaseLanguageHandler):
    def run(self, lines):
        includes = ['#include <stdio.h>', '#include <stdbool.h>']
        main_code = []
        
        for line in lines:
            if line.strip().startswith('#include'):
                if line.strip() not in includes:
                    includes.append(line.strip())
            else:
                main_code.append(line)
        
        # 讀 Python 的共享變數
        shared_vars = self.shared.import_to_python('py')
        shared_code = self._generate_shared_code(shared_vars)
        
        if shared_vars:
            includes.append('#include <string.h>')
        
        code = '\n'.join(includes) + '\n'
        code += shared_code + '\n'
        code += 'int main() {\n'
        
        for line in main_code:
            if 'printf' in line and not '\\n' in line and line.endswith('"'):
                line = line[:-1] + '\\n"'
            # 把共享變數名稱對應到結構成員
            line = line.replace('shared.active', 'shared.user_active')
            code += '    ' + line + '\n'
        code += '    return 0;\n}\n'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
            f.write(code)
            f.flush()
            exe_file = f.name + '.out'
            try:
                compile_cmd = ['gcc', f.name, '-o', exe_file]
                if any('#include <math.h>' in line for line in includes):
                    compile_cmd.append('-lm')
                subprocess.run(compile_cmd, timeout=5, check=True)
                result = subprocess.run([exe_file], capture_output=True, text=True, timeout=5)
                if result.stdout:
                    print(result.stdout, end='')
                if result.stderr:
                    self.error(f"C stderr: {result.stderr.strip()}")
            except FileNotFoundError:
                self.error("GCC not installed")
            except subprocess.TimeoutExpired:
                self.error("C timeout")
            except subprocess.CalledProcessError as e:
                self.error(f"C compilation failed: {e}")
                if e.stderr:
                    print(e.stderr)
            finally:
                os.unlink(f.name)
                if os.path.exists(exe_file):
                    os.unlink(exe_file)

    def _generate_shared_code(self, shared_vars):
        if not shared_vars:
            return ""
        
        code = "typedef struct {\n"
        for key, value in shared_vars.items():
            c_type = self._c_type(value)
            code += f"    {c_type} {key};\n"
        code += "} SharedData;\n\n"
        
        code += "SharedData shared = {\n"
        for key, value in shared_vars.items():
            c_val = self._to_c_literal(value)
            code += f"    .{key} = {c_val},\n"
        code += "};\n\n"
        return code

    def _c_type(self, value):
        if isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "double"
        elif isinstance(value, bool):
            return "bool"
        elif isinstance(value, str):
            return "char*"
        elif isinstance(value, list):
            if all(isinstance(x, int) for x in value):
                return "int*"
            elif all(isinstance(x, str) for x in value):
                return "char**"
            else:
                return "void*"
        elif isinstance(value, dict):
            return "void*"
        else:
            return "void*"

    def _to_c_literal(self, value):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(value)
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            if not value:
                return "NULL"
            items = [self._to_c_literal(x) for x in value]
            if all(isinstance(x, int) for x in value):
                return f"(int[]){{{', '.join(items)}}}"
            elif all(isinstance(x, str) for x in value):
                return f"(char*[]){{{', '.join(items)}}}"
            else:
                return "NULL"
        elif isinstance(value, dict):
            return "NULL"
        else:
            return "NULL"