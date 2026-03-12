# ~/awa/utils/colors.py
# 顏色定義與輸出函式

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    END = '\033[0m'

def color_print(text, color=Colors.WHITE):
    print(f"{color}{text}{Colors.END}")

def error_print(text):
    print(f"{Colors.RED}{text}{Colors.END}")
