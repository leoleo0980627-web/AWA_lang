# ~/awa/core/compiler.py
# 主編譯器類別（完整版 + Shared Storage + 修正 LanguageHandler 參數）

import sys
import os
import datetime
import time
import random
import re

from ..utils.colors import Colors, color_print, error_print
from ..utils.helpers import check_holidays, set_birthday, random_fortune
from .scope import ScopeManager
from .politeness import PolitenessManager
from ..easter.eggs import EasterEggs
from ..lang import LanguageHandler  # 從 __init__ 導入
from ..shared.storage import SharedStorage

class AwaCompiler:
    def __init__(self):
        # ========== 核心資料 ==========
        self.vars = {}
        self.functions = {}
        self.function_bodies = {}
        self.arrays = {}
        self.current_function = None
        self.function_params = {}
        self.return_value = None

        # ========== 語言嵌入 ==========
        self.in_lang_block = False
        self.current_lang = None
        self.lang_lines = []

        # ========== 流程控制 ==========
        self.loop_stack = []
        self.if_stack = []
        self.block_stack = []
        self.block_lines = {}
        self.current_block_lines = []
        self.collecting_block = False
        self.block_type = None
        self.block_name = None

        # ========== 除錯模式 ==========
        self.debug_mode = False
        self.debug_explanations = []

        # ========== 時間感知 ==========
        self.today = datetime.date.today()
        self.christmas_mode, self.new_year_mode, self.april_fools_mode = check_holidays()
        self.birthday_mode = False
        self.user_birthday = None

        # ========== 檔案操作 ==========
        self.file_permission = False
        self.file_access_log = []

        # ========== 輸出緩衝 ==========
        self.output_buffer = []
        self.greeting_done = False

        # ========== 自我意識 ==========
        self.creator = "Some genius who hates u"
        self.version = "5.1 - 'Shared Storage Edition'"
        self.marriage_proposals = 0
        self.insults_received = 0
        self.compliments_received = 0

        # ========== 共享儲存 ==========
        self.shared = SharedStorage()

        # ========== 初始化管理器 ==========
        self.scope_mgr = ScopeManager(self.error, self.debug)
        self.politeness_mgr = PolitenessManager(self.say, self.debug, self.update_mood)
        self.easter_eggs = EasterEggs(self.say, self.today, random_fortune)
        self.lang_handler = LanguageHandler(self)  # ← 修正：只傳 self

        # ========== 情緒 ==========
        self.compiler_mood = 0

    # ========== 工具函數 ==========

    def say(self, msg, color=Colors.WHITE):
        print(f"{color}{msg}{Colors.END}")
        self.output_buffer.append(msg)

    def error(self, msg, line_num=None):
        prefix = f"Line {line_num}: " if line_num else ""
        print(f"{Colors.RED}{prefix}{msg}{Colors.END}")
        if self.debug_mode:
            self.debug_explanations.append(f"ERROR: {msg}")

    def debug(self, msg):
        if self.debug_mode:
            print(f"{Colors.YELLOW}[DEBUG] {msg}{Colors.END}")
            self.debug_explanations.append(msg)

    def update_mood(self, change):
        old_mood = self.compiler_mood
        self.compiler_mood = max(-3, min(3, self.compiler_mood + change))
        if old_mood != self.compiler_mood:
            self.debug(f"Mood changed from {old_mood} to {self.compiler_mood}")

    def set_birthday(self, month, day):
        self.user_birthday = (month, day)
        self.birthday_mode = set_birthday(month, day)

    # ========== 取值與條件 ==========

    def get_value(self, expr, line_num):
        expr = expr.strip()
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        try:
            return int(expr)
        except:
            pass
        var_info = self.scope_mgr.get_var(expr, line_num)
        if var_info:
            return var_info[1]
        return expr

    def evaluate_condition(self, cond, line_num):
        cond = cond.strip()
        self.debug(f"Evaluating condition: {cond}")
        if ' is ' in cond:
            parts = cond.split(' is ')
            if len(parts) != 2:
                self.error("Invalid condition", line_num)
                return False
            left = parts[0].strip()
            right = parts[1].strip()
            left_val = self.get_value(left, line_num)
            right_val = self.get_value(right, line_num)
            result = str(left_val) == str(right_val)
            self.debug(f"Condition result: {result}")
            return result
        return False

    # ========== 主執行 ==========

    def run(self, filename):
        if not filename.endswith('.awa'):
            self.error("File must have extension .awa")
            return

        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.error(f"File {filename} not found")
            return

        # 檢查打招呼
        if not lines or not lines[0].strip() == 'good morning compiler':
            self.error("You didn't say good morning. Rude.")
            return

        # 節日問候
        if self.christmas_mode:
            self.say("merry christmas, hope ur code works", Colors.GREEN)
            response = input("(say 'merry christmas to u too'): ")
            if response != 'merry christmas to u too':
                self.error("Rude. Now compiler is sad.")
                self.update_mood(-2)
            else:
                self.say("Good human.", Colors.GREEN)
                self.update_mood(1)
        elif self.new_year_mode:
            self.say("Happy New Year! write better code this year", Colors.YELLOW)
        elif self.april_fools_mode:
            self.say("April Fools! Your code is a joke.", Colors.MAGENTA)

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            if line == 'good morning compiler':
                i += 1
                continue

            if line == 'thank u and goodbye':
                # 檢查沒道別的變數
                for var in self.politeness_mgr.greeted_vars:
                    if var in self.vars or var in self.arrays:
                        self.error(f"{var} died alone because of u")

                # 根據 mood 說道別
                goodbye_msgs = {
                    -3: "I hate u. Don't come back.",
                    -2: "Ugh. Finally.",
                    -1: "Bye.",
                    0: "Goodbye.",
                    1: "See u later",
                    2: "Bye! Come back soon",
                    3: "I'll miss u"
                }
                msg = goodbye_msgs.get(self.compiler_mood, "Goodbye.")
                color = Colors.RED if self.compiler_mood < 0 else Colors.GREEN
                self.say(msg, color)
                break

            # 語言嵌入
            if line.startswith('please let me use '):
                lang = line[18:].strip()
                if lang not in self.lang_handler.handlers:
                    self.error(f"Language {lang} not supported", i+1)
                    i += 1
                    continue
                self.in_lang_block = True
                self.current_lang = lang
                self.lang_lines = []
                i += 1
                continue

            if self.in_lang_block:
                if line == 'thank you for the translation':
                    self.lang_handler.run_language_block(self.current_lang, self.lang_lines)
                    self.in_lang_block = False
                    self.current_lang = None
                    self.lang_lines = []
                else:
                    original_line = lines[i].rstrip('\n')
                    self.lang_lines.append(original_line)
                i += 1
                continue

            # 檢查是否執行當前區塊
            execute_line = True
            if self.if_stack and not self.if_stack[-1]:
                execute_line = False

            if execute_line:
                self.execute_line(line, i+1)

            i += 1
