import sys; import os; sys.path.insert(0, os.path.dirname(__file__))
# ~/awa/__main__.py
# 允許 python -m awa 執行

from awa.awa import main

if __name__ == '__main__':
    main()
