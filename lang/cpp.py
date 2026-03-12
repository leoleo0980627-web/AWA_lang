# ~/awa/lang/cpp.py
import subprocess
import tempfile
import os
from .base import BaseLanguageHandler

class CppHandler(BaseLanguageHandler):
    def run(self, lines):
        includes = ['#include <iostream>', '#include <string>', '#include <vector>', '#include <map>']
        main_code = []
        
        for line in lines:
            if line.strip().startswith('#include'):
                if line.strip() not in includes:
                    includes.append(line.strip())
            else:
                main_code.append(line)
        
        # 讀 Python 的共享變數（已轉換布林值為字串）
        shared_vars = self.shared.import_to_other('py')
        shared_code = self._generate_shared_code(shared_vars)
        
        code = '\n'.join(includes) + '\n'
        code += 'using namespace std;\n\n'
        code += shared_code + '\n'
        code += 'int main() {\n'
        
        for line in main_code:
            code += '    ' + line + '\n'
        code += '    return 0;\n}\n'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write(code)
            f.flush()
            exe_file = f.name + '.out'
            try:
                compile_cmd = ['g++', f.name, '-o', exe_file, '-std=c++11']
                if any('#include <cmath>' in line for line in includes):
                    compile_cmd.append('-lm')
                subprocess.run(compile_cmd, timeout=5, check=True)
                result = subprocess.run([exe_file], capture_output=True, text=True, timeout=5)
                if result.stdout:
                    print(result.stdout, end='')
                if result.stderr:
                    self.error(f"C++ stderr: {result.stderr.strip()}")
            except FileNotFoundError:
                self.error("G++ not installed")
            except subprocess.TimeoutExpired:
                self.error("C++ timeout")
            except subprocess.CalledProcessError as e:
                self.error(f"C++ compilation failed: {e}")
            finally:
                os.unlink(f.name)
                if os.path.exists(exe_file):
                    os.unlink(exe_file)

    def _generate_shared_code(self, shared_vars):
        if not shared_vars:
            return ""
        
        code = "struct SharedData {\n"
        for key, value in shared_vars.items():
            cpp_type = self._cpp_type(value)
            code += f"    static {cpp_type} {key};\n"
        code += "};\n\n"
        
        for key, value in shared_vars.items():
            cpp_type = self._cpp_type(value)
            cpp_val = self._to_cpp_literal(value)
            code += f"{cpp_type} SharedData::{key} = {cpp_val};\n"
        code += "\n"
        return code

    def _cpp_type(self, value):
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "double"
        elif isinstance(value, str):
            if value in ("true", "false"):
                return "bool"
            return "std::string"
        elif isinstance(value, list):
            if not value:
                return "std::vector<auto>"
            if all(isinstance(x, int) for x in value):
                return "std::vector<int>"
            elif all(isinstance(x, str) for x in value):
                return "std::vector<std::string>"
            else:
                return "std::vector<auto>"
        elif isinstance(value, dict):
            # 統一用 string->string map
            return "std::map<std::string, std::string>"
        else:
            return "auto"

    def _to_cpp_literal(self, value):
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(value)
        elif isinstance(value, str):
            if value in ("true", "false"):
                return value
            return f'"{value}"'
        elif isinstance(value, list):
            if not value:
                return "{}"
            items = [self._to_cpp_literal(x) for x in value]
            if all(isinstance(x, int) for x in value):
                return "{" + ", ".join(items) + "}"
            elif all(isinstance(x, str) for x in value):
                return "{" + ", ".join(items) + "}"
            else:
                return "{}"
        elif isinstance(value, dict):
            if not value:
                return "{}"
            items = []
            for k, v in value.items():
                items.append(f'{{"{k}", {self._to_cpp_literal(v)}}}')
            return "std::map<std::string, std::string>{{" + ", ".join(items) + "}}"
        else:
            return "{}"