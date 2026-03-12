# ~/awa/lang/python.py
from .base import BaseLanguageHandler

class PythonHandler(BaseLanguageHandler):
    def run(self, lines):
        # 讀取共享變數（從 py 命名空間）
        shared_vars = self.shared.import_to_python('py')
        exec_globals = {**shared_vars}
        
        code = '\n'.join(lines)
        try:
            exec(code, exec_globals)
            # 存回共享（只存 py 命名空間）
            self.shared.export_from_python('py', exec_globals)
        except ModuleNotFoundError as e:
            self.error(f"Python module missing: {e}")
            self.error("Try: pkg install python-numpy")
        except IndentationError as e:
            self.error(f"Python indentation error: {e}")
        except Exception as e:
            self.error(f"Python error: {e}")