# ~/awa/lang/rust.py
import subprocess
import tempfile
import os
from .base import BaseLanguageHandler

class RustHandler(BaseLanguageHandler):
    def run(self, lines):
        # 讀 Python 的共享變數
        shared_vars = self.shared.import_to_python('py')
        
        # 產生 shared 結構
        shared_code = self._generate_shared_code(shared_vars)
        
        code = shared_code + '\n'
        code += 'fn main() {\n'
        for line in lines:
            code += '    ' + line + '\n'
        code += '}\n'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.rs', delete=False) as f:
            f.write(code)
            f.flush()
            exe_file = f.name.replace('.rs', '')
            try:
                subprocess.run(['rustc', f.name, '-o', exe_file], capture_output=True, text=True, timeout=10, check=True)
                if os.path.exists(exe_file):
                    run_result = subprocess.run([exe_file], capture_output=True, text=True, timeout=5)
                    if run_result.stdout:
                        print(run_result.stdout, end='')
                    if run_result.stderr:
                        self.error(f"Rust stderr: {run_result.stderr.strip()}")
                else:
                    self.error("Rust compilation produced no executable")
            except FileNotFoundError:
                self.error("Rust not installed")
            except subprocess.TimeoutExpired:
                self.error("Rust timeout")
            except subprocess.CalledProcessError as e:
                self.error(f"Rust compilation failed: {e}")
                if e.stderr:
                    print(e.stderr)
            finally:
                os.unlink(f.name)
                if os.path.exists(exe_file):
                    os.unlink(exe_file)

    def _generate_shared_code(self, shared_vars):
        if not shared_vars:
            return ""
        
        code = "struct SharedData {\n"
        for key, value in shared_vars.items():
            rust_type = self._rust_type(value)
            code += f"    {key}: {rust_type},\n"
        code += "}\n\n"
        
        code += "static SHARED: SharedData = SharedData {\n"
        for key, value in shared_vars.items():
            rust_val = self._to_rust_literal(value)
            code += f"    {key}: {rust_val},\n"
        code += "};\n\n"
        return code

    def _rust_type(self, value):
        if isinstance(value, int):
            return "i32"
        elif isinstance(value, float):
            return "f64"
        elif isinstance(value, bool):
            return "bool"
        elif isinstance(value, str):
            return "&'static str"
        elif isinstance(value, list):
            if all(isinstance(x, int) for x in value):
                return "&'static [i32]"
            elif all(isinstance(x, str) for x in value):
                return "&'static [&'static str]"
            else:
                return "&'static [&'static dyn std::any::Any]"
        else:
            return "&'static str"

    def _to_rust_literal(self, value):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(value)
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            items = [self._to_rust_literal(x) for x in value]
            return "&[" + ", ".join(items) + "]"
        else:
            return '""'