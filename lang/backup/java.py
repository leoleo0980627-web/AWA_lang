# ~/awa/lang/java.py
import subprocess
import tempfile
import os
import random
from .base import BaseLanguageHandler

class JavaHandler(BaseLanguageHandler):
    def run(self, lines):
        class_name = "AwaTemp" + str(random.randint(1000, 9999))
        imports = []
        main_code = []
        
        for line in lines:
            if line.strip().startswith('import '):
                imports.append(line.strip())
            else:
                main_code.append(line)
        
        # 讀 Python 的共享變數
        shared_vars = self.shared.import_to_python('py')
        shared_code = self._generate_shared_code(shared_vars)
        
        code = '\n'.join(imports) + '\n'
        code += shared_code + '\n'
        code += f'public class {class_name} {{\n'
        code += '    public static void main(String[] args) {\n'
        
        for line in main_code:
            code += '        ' + line + '\n'
        code += '    }\n'
        code += '}\n'
        
        tmp_dir = "/data/data/com.termux/files/usr/tmp"
        java_file = f"{tmp_dir}/{class_name}.java"
        
        with open(java_file, 'w') as f:
            f.write(code)
            
        try:
            subprocess.run(['javac', java_file], timeout=5, check=True)
            result = subprocess.run(
                ['java', '-cp', tmp_dir, class_name],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout:
                print(result.stdout, end='')
            if result.stderr:
                self.error(f"Java stderr: {result.stderr.strip()}")
        except FileNotFoundError:
            self.error("Java not installed")
        except subprocess.TimeoutExpired:
            self.error("Java timeout")
        except subprocess.CalledProcessError as e:
            self.error(f"Java compilation failed: {e}")
        finally:
            if os.path.exists(java_file):
                os.unlink(java_file)
            class_file = f"{tmp_dir}/{class_name}.class"
            if os.path.exists(class_file):
                os.unlink(class_file)

    def _generate_shared_code(self, shared_vars):
        if not shared_vars:
            return ""
        
        code = "\nclass SharedData {\n"
        for key, value in shared_vars.items():
            java_type = self._java_type(value)
            java_value = self._to_java_literal(value)
            code += f"    public static {java_type} {key} = {java_value};\n"
        code += "}\n"
        return code

    def _java_type(self, value):
        if isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "double"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, str):
            return "String"
        elif isinstance(value, list):
            if all(isinstance(x, int) for x in value):
                return "int[]"
            elif all(isinstance(x, str) for x in value):
                return "String[]"
            else:
                return "Object[]"
        elif isinstance(value, dict):
            return "java.util.Map<String, Object>"
        else:
            return "Object"

    def _to_java_literal(self, value):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(value)
        elif isinstance(value, bool):
            return str(value).lower()  # True → true, False → false
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            items = [self._to_java_literal(x) for x in value]
            if all(isinstance(x, int) for x in value):
                return "{" + ", ".join(items) + "}"
            elif all(isinstance(x, str) for x in value):
                return "{" + ", ".join(items) + "}"
            else:
                return "new Object[]{" + ", ".join(items) + "}"
        elif isinstance(value, dict):
            items = self._dict_to_java(value)
            return f'new java.util.HashMap<String, Object>(){{{{ {items} }}}}'
        else:
            return "null"

    def _dict_to_java(self, d):
        items = []
        for k, v in d.items():
            items.append(f'put("{k}", {self._to_java_literal(v)})')
        return "; ".join(items) + ";"