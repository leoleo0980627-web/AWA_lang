#!/usr/bin/env python3
# ~/awa/awa.py
# AWA Language - Main Entry Point

import sys

from .core.compiler import AwaCompiler
from .core.executor import Executor
from .utils.colors import Colors, color_print

def main():
    if len(sys.argv) != 2:
        print("AWA Language v5.1 - 'Modular Edition'")
        print("=" * 50)
        print("The Most Polite Yet Annoying Programming Language")
        print("Usage: python -m awa <filename>.awa")
        return

    filename = sys.argv[1]
    compiler = AwaCompiler()
    compiler.executor = Executor(compiler)

    # 將 execute_line 方法綁到 compiler 上
    compiler.execute_line = lambda line, line_num: compiler.executor.handle_line(line, line_num)

    compiler.run(filename)

if __name__ == '__main__':
    main()
