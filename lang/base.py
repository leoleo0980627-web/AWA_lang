# ~/awa/lang/base.py
# 語言處理器基底類別

class BaseLanguageHandler:
    def __init__(self, compiler):
        self.compiler = compiler
        self.error = compiler.error
        self.debug = compiler.debug
        self.shared = compiler.shared

    def run(self, lines):
        """每個語言必須實作此方法"""
        raise NotImplementedError("Each language handler must implement run()")
