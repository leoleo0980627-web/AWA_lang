# ~/awa/lang/python.py
from .base import BaseLanguageHandler
import types

class PythonHandler(BaseLanguageHandler):
    def run(self, lines):
        # 讀取共享變數（從 py 命名空間）
        shared_vars = self.shared.import_to_python('py')
        exec_globals = {**shared_vars}
        
        code = '\n'.join(lines)
        try:
            exec(code, exec_globals)
            
            # 過濾：只存非 module、非 function、非 class 的變數
            filtered_globals = {}
            for k, v in exec_globals.items():
                if k.startswith('_'):
                    continue
                if k in ('__builtins__', '__name__', '__doc__', '__package__', '__loader__', '__spec__'):
                    continue
                # 跳過 module、function、class、type
                if isinstance(v, (types.ModuleType, types.FunctionType, types.MethodType, types.BuiltinFunctionType, type)):
                    continue
                filtered_globals[k] = v
            
            # 存回共享（只存 py 命名空間）
            self.shared.export_from_python('py', filtered_globals)
            
        except ModuleNotFoundError as e:
            self.error(f"Python module missing: {e}")
            self.error("Try: pkg install python-numpy")
        except IndentationError as e:
            self.error(f"Python indentation error: {e}")
        except Exception as e:
            self.error(f"Python error: {e}")
