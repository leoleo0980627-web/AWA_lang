# ~/awa/lang/sh.py
import subprocess
import os
from .base import BaseLanguageHandler

class ShHandler(BaseLanguageHandler):
    def run(self, lines):
        # 讀 shared 變數
        shared_vars = self.shared.import_to_other('py')
        
        # 轉成環境變數 (給 shell 用)
        env = os.environ.copy()
        for key, value in shared_vars.items():
            if isinstance(value, (str, int, float, bool)):
                env[f"SHARED_{key.upper()}"] = str(value)
            elif isinstance(value, list):
                env[f"SHARED_{key.upper()}"] = " ".join(str(x) for x in value)
        
        script = '\n'.join(lines)
        
        try:
            result = subprocess.run(
                script,
                shell=True,
                executable='/bin/sh',
                env=env,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout:
                print(result.stdout, end='')
            
            if result.stderr:
                self.error(f"sh stderr: {result.stderr.strip()}")
            
            # 把 exit code 存回 shared
            self.shared.set('py', 'sh_exit_code', result.returncode)
            
        except subprocess.TimeoutExpired:
            self.error("sh timeout")
            self.shared.set('py', 'sh_timeout', True)
        except Exception as e:
            self.error(f"sh error: {e}")
