# ~/awa/lang/__init__.py
# 語言處理器工廠

from .python import PythonHandler
from .java import JavaHandler
from .js import JavaScriptHandler
from .c import CHandler
from .cpp import CppHandler
from .rust import RustHandler
from .go import GoHandler
from .csharp import CSharpHandler
from .ruby import RubyHandler
from .ts import TypeScriptHandler
from .intercal import IntercalHandler
from .sh import ShHandler

class LanguageHandler:
    def __init__(self, compiler):
        self.compiler = compiler
        self.handlers = {
            'py': PythonHandler(compiler),
            'java': JavaHandler(compiler),
            'js': JavaScriptHandler(compiler),
            'c': CHandler(compiler),
            'cpp': CppHandler(compiler),
            'rust': RustHandler(compiler),
            'go': GoHandler(compiler),
            'cs': CSharpHandler(compiler),
            'ruby': RubyHandler(compiler),
            'ts': TypeScriptHandler(compiler),
            'intercal': IntercalHandler(compiler),
            'sh': ShHandler(compiler),
        }

    def run_language_block(self, lang, lines):
        if lang in self.handlers:
            self.compiler.debug(f"Executing {lang} block with {len(lines)} lines")
            try:
                self.handlers[lang].run(lines)
            except Exception as e:
                self.compiler.error(f"Error in {lang} block: {e}")
        else:
            self.compiler.error(f"Language {lang} not supported")
