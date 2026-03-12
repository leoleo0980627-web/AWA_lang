# ~/awa/lang/intercal.py
import subprocess
import tempfile
import os
from utils.colors import Colors
from .base import BaseLanguageHandler

class IntercalHandler(BaseLanguageHandler):
    def run(self, lines):
        print(f"{Colors.MAGENTA}Good luck. You'll need it.{Colors.END}")
        code = '\n'.join(lines)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.i', delete=False) as f:
            f.write(code)
            f.flush()
            exe_file = f.name.replace('.i', '')
            try:
                compile_result = subprocess.run(['ick', f.name], capture_output=True, text=True, timeout=5)
                
                if compile_result.stderr:
                    if "ICL079I" in compile_result.stderr or "PLEASE" in compile_result.stderr:
                        print(compile_result.stderr.strip())
                
                if os.path.exists(exe_file):
                    run_result = subprocess.run([exe_file], capture_output=True, text=True, timeout=5)
                    if run_result.stdout:
                        print(run_result.stdout, end='')
                    if run_result.stderr:
                        if run_result.stderr.strip():
                            self.error(f"INTERCAL runtime: {run_result.stderr.strip()}")
                else:
                    self.error("INTERCAL compilation produced no executable")
                    
            except FileNotFoundError:
                self.error("ICK compiler not installed. Did you compile INTERCAL?")
            except subprocess.TimeoutExpired:
                print("INTERCAL timeout (that's actually good, means it didn't infinite loop)")
            except Exception as e:
                self.error(f"INTERCAL error: {e}")
            finally:
                os.unlink(f.name)
                if os.path.exists(exe_file):
                    os.unlink(exe_file)
