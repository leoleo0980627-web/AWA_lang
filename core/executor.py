# ~/awa/core/executor.py
# 指令執行器（完整版）

import re
import time
import random

from ..utils.colors import Colors

class Executor:
    def __init__(self, compiler):
        self.c = compiler

    def handle_line(self, line, line_num):
        """統一處理單行指令"""
        try:
            # 跳過註解
            if line.startswith('--'):
                return True

            # 彩蛋
            if self.c.easter_eggs.check(line):
                return True

            # 除錯指令
            if line in ['debug on', 'debug off', 'why']:
                self.handle_debug(line, line_num)
                return True

            # 權限
            if line in ['may i read file', 'may i write file']:
                self.handle_permission(line, line_num)
                return True

            # 禮貌處理
            if line.startswith('please '):
                self.c.politeness_mgr.add_politeness(True)
                if self.c.politeness_mgr.politeness_count > self.c.politeness_mgr.politeness_threshold * 3:
                    self.c.error("U are obsessed with please", line_num)
                line = line[7:]

            # 先檢查 goodbye
            if line.startswith('goodbye '):
                if self.handle_goodbye_var(line, line_num):
                    return True

            # 指令分發
            if line.startswith('give me a variable called'):
                self.handle_declaration(line, line_num)
            elif ' is now ' in line and not line.startswith('if'):
                self.handle_assignment(line, line_num)
            elif line.startswith('say'):
                self.handle_print(line, line_num)
            elif line.startswith('if'):
                self.handle_if(line, line_num)
            elif line.startswith('else'):
                self.handle_else(line_num)
            elif line.startswith('do this'):
                self.handle_loop(line, line_num)
            elif line == 'end':
                self.handle_end(line_num)
            elif line.startswith('define function'):
                self.handle_function_def(line, line_num)
            elif line.startswith('call'):
                self.handle_function_call(line, line_num)
            elif line.startswith('return'):
                self.handle_return(line, line_num)
            elif line.startswith('listen to me'):
                self.handle_input(line_num)
            elif line.startswith('compute'):
                self.handle_compute(line, line_num)
            elif line.startswith('give me a list'):
                self.handle_array_decl(line, line_num)
            elif line.startswith('get'):
                self.handle_array_get(line, line_num)
            elif line.startswith('set in'):
                self.handle_array_set(line, line_num)
            elif line.startswith('how many in'):
                self.handle_array_length(line, line_num)
            elif line.startswith('read file'):
                self.handle_read_file(line, line_num)
            elif line.startswith('write file'):
                self.handle_write_file(line, line_num)
            elif line.startswith('nice to meet u'):
                self.handle_nice_to_meet(line, line_num)
            elif line == 'thank u for listening':
                self.c.say("You're welcome", Colors.GREEN)
                self.c.update_mood(1)
            elif line.startswith('u are great'):
                self.handle_compliment(line, line_num)
            elif line.startswith('fuck u'):
                self.handle_insult(line, line_num)
            elif line.startswith('sorry'):
                self.handle_apology(line_num)
            elif line in ['who made this', 'what version', 'help me', 'this language sucks', 'will u marry me']:
                self.handle_self_awareness(line, line_num)
            else:
                self.c.error(f"What is this: {line}", line_num)

            # 禮貌計數（非禮貌詞）
            if 'please' not in line and 'thank' not in line and 'sorry' not in line:
                self.c.politeness_mgr.add_politeness(False)

        except Exception as e:
            self.c.error(f"Error: {e}", line_num)
            self.c.politeness_mgr.apology_needed = True

    # ========== 指令處理 ==========

    def handle_declaration(self, line, line_num):
        pattern = r'give me a variable called (\w+) and set it to (.+)'
        match = re.match(pattern, line)
        if not match:
            self.c.error("Invalid declaration", line_num)
            return
        name, val = match.groups()
        try:
            self.c.scope_mgr.declare_var(name, int(val), 'number')
            self.c.debug(f"Declared number var {name} = {val}")
        except:
            self.c.scope_mgr.declare_var(name, val.strip('"'), 'string')
            self.c.debug(f"Declared string var {name} = {val}")

    def handle_assignment(self, line, line_num):
        parts = line.split(' is now ')
        if len(parts) != 2:
            self.c.error("Invalid assignment", line_num)
            return
        name = parts[0].strip()
        val = parts[1].strip()
        if name == val:
            self.c.error("U just changed nothing", line_num)
            self.c.update_mood(-1)
            return
        var_info = self.c.scope_mgr.get_var(name, line_num)
        if not var_info:
            return
        old_type, old_val = var_info
        try:
            value = int(val)
            if old_type != 'number':
                self.c.error(f"U can't put a number in a {old_type}", line_num)
                self.c.update_mood(-1)
                return
            self.c.scope_mgr.set_var(name, value, 'number', line_num)
            self.c.debug(f"Assigned {name} = {value}")
        except:
            value = val.strip('"')
            if old_type != 'string':
                self.c.error(f"U can't put a word in a number", line_num)
                self.c.update_mood(-1)
                return
            self.c.scope_mgr.set_var(name, value, 'string', line_num)
            self.c.debug(f"Assigned {name} = {value}")

    def handle_print(self, line, line_num):
        content = line[3:].strip()
        if not content:
            self.c.error("Say what?", line_num)
            return
        if content.startswith('"') and content.endswith('"'):
            self.c.say(content[1:-1])
        else:
            value = self.c.get_value(content, line_num)
            self.c.say(str(value))

    def handle_if(self, line, line_num):
        if 'then' not in line:
            self.c.error("Where's the 'then'?", line_num)
            return
        cond = line[2:].split(' then')[0].strip()
        result = self.c.evaluate_condition(cond, line_num)
        self.c.if_stack.append(result)
        self.c.scope_mgr.enter_scope('if')
        self.c.debug(f"IF condition: {result}")

    def handle_else(self, line_num):
        if not self.c.if_stack:
            self.c.error("Unexpected else", line_num)
            return
        self.c.scope_mgr.exit_scope()
        self.c.if_stack[-1] = not self.c.if_stack[-1]
        self.c.scope_mgr.enter_scope('else')
        self.c.debug(f"ELSE branch, condition now: {self.c.if_stack[-1]}")

    def handle_loop(self, line, line_num):
        pattern = r'do this (\d+) times'
        match = re.match(pattern, line)
        if not match:
            self.c.error("Invalid loop syntax", line_num)
            return
        count = int(match.group(1))
        self.c.loop_stack.append(count)
        self.c.scope_mgr.enter_scope('loop')
        self.c.debug(f"LOOP: {count} times")

    def handle_end(self, line_num):
        if not self.c.block_stack:
            self.c.error("Unexpected end", line_num)
            return
        block_type = self.c.block_stack[-1]
        if block_type in ('if', 'else'):
            self.c.scope_mgr.exit_scope()
            self.c.if_stack.pop()
            self.c.debug(f"End of {block_type} block")
        elif block_type == 'loop':
            self.c.loop_stack[-1] -= 1
            if self.c.loop_stack[-1] > 0:
                self.c.debug(f"Loop continues, {self.c.loop_stack[-1]} left")
                self.c.scope_mgr.exit_scope()
                self.c.scope_mgr.enter_scope('loop')
            else:
                self.c.scope_mgr.exit_scope()
                self.c.loop_stack.pop()
                self.c.debug("Loop finished")

    def handle_function_def(self, line, line_num):
        parts = line.split()
        if len(parts) < 3:
            self.c.error("Invalid function definition", line_num)
            return
        func_name = parts[2]
        params = parts[3:] if len(parts) > 3 else []
        self.c.functions[func_name] = {'params': params, 'line_num': line_num}
        self.c.function_bodies[func_name] = []
        self.c.current_function = func_name
        self.c.scope_mgr.enter_scope('function')
        self.c.debug(f"Defining function {func_name} with params {params}")

    def handle_function_call(self, line, line_num):
        parts = line.split()
        if len(parts) < 2:
            self.c.error("Invalid function call", line_num)
            return
        func_name = parts[1]
        args = parts[2:] if len(parts) > 2 else []
        if func_name not in self.c.functions:
            self.c.error(f"Function {func_name} not defined", line_num)
            return
        func_info = self.c.functions[func_name]
        if len(func_info['params']) != len(args):
            self.c.error(f"Expected {len(func_info['params'])} args, got {len(args)}", line_num)
            return
        self.c.say(f"Calling {func_name}")
        self.c.debug(f"Function call with args {args}")
        self.c.scope_mgr.enter_scope('function_call')
        for i, param in enumerate(func_info['params']):
            value = self.c.get_value(args[i], line_num)
            self.c.scope_mgr.declare_var(param, value, type(value).__name__)
        for func_line in self.c.function_bodies.get(func_name, []):
            self.c.execute_line(func_line, func_info['line_num'])
        self.c.scope_mgr.exit_scope()

    def handle_return(self, line, line_num):
        value = line[6:].strip()
        self.c.return_value = self.c.get_value(value, line_num)
        self.c.debug(f"Returning {self.c.return_value}")

    def handle_input(self, line_num):
        user_input = input()
        self.c.say("thanks for the input", Colors.GREEN)
        var_name = f"input_{int(time.time())}"
        self.c.scope_mgr.declare_var(var_name, user_input, 'string')
        self.c.debug(f"Got input, stored as {var_name}")

    def handle_compute(self, line, line_num):
        expr = line[7:].strip()
        if re.search(r'[+\-*/]', expr):
            self.c.error("We don't do that here", line_num)
            self.c.update_mood(-1)
            return
        expr = expr.replace('plus', '+').replace('minus', '-')
        expr = expr.replace('times', '*').replace('divided by', '/')
        for name, (_, val) in self.c.scope_mgr.get_all_vars().items():
            expr = expr.replace(name, str(val))
        if re.search(r'/ ?0', expr):
            self.c.error("U trying to break the universe?", line_num)
            self.c.update_mood(-2)
            return
        try:
            result = eval(expr)
            self.c.say(str(result))
            self.c.debug(f"Computed: {expr} = {result}")
        except Exception as e:
            self.c.error(f"Compute error: {e}", line_num)

    def handle_array_decl(self, line, line_num):
        pattern = r'give me a list called (\w+) with (.+)'
        match = re.match(pattern, line)
        if not match:
            self.c.error("Invalid array declaration", line_num)
            return
        name = match.group(1)
        values_str = match.group(2)
        values = [v.strip().strip('"') for v in values_str.split(',')]
        self.c.arrays[name] = values
        self.c.debug(f"Array {name} = {values}")

    def handle_array_get(self, line, line_num):
        pattern = r'get (\w+) at (\d+)'
        match = re.match(pattern, line)
        if not match:
            self.c.error("Invalid array get", line_num)
            return
        name = match.group(1)
        idx = int(match.group(2))
        if name not in self.c.arrays:
            self.c.error("That's not a list", line_num)
            return
        if idx >= len(self.c.arrays[name]):
            self.c.error(f"U only have {len(self.c.arrays[name])} items", line_num)
            return
        self.c.say(str(self.c.arrays[name][idx]))

    def handle_array_set(self, line, line_num):
        pattern = r'set in (\w+) at (\d+) to (.+)'
        match = re.match(pattern, line)
        if not match:
            self.c.error("Invalid array set", line_num)
            return
        name = match.group(1)
        idx = int(match.group(2))
        value = match.group(3).strip('"')
        if name not in self.c.arrays:
            self.c.error("That's not a list", line_num)
            return
        if idx >= len(self.c.arrays[name]):
            self.c.error(f"U only have {len(self.c.arrays[name])} items", line_num)
            return
        self.c.arrays[name][idx] = value
        self.c.debug(f"Array {name}[{idx}] = {value}")

    def handle_array_length(self, line, line_num):
        name = line[12:].strip()
        if name not in self.c.arrays:
            self.c.error("That's not a list", line_num)
            return
        length = len(self.c.arrays[name])
        self.c.say(str(length))

    def handle_read_file(self, line, line_num):
        if not self.c.file_permission and self.c.compiler_mood < 2:
            self.c.error("U didn't even ask", line_num)
            return
        pattern = r'read file "([^"]+)"'
        match = re.search(pattern, line)
        if not match:
            self.c.error("Invalid read file", line_num)
            return
        filename = match.group(1)
        try:
            with open(filename, 'r') as f:
                content = f.read()
            preview = content[:100] + ("..." if len(content) > 100 else "")
            self.c.say(preview)
            self.c.file_access_log.append(('read', filename, time.time()))
        except FileNotFoundError:
            self.c.error("I can't read what doesn't exist", line_num)
        except Exception as e:
            self.c.error(f"File error: {e}", line_num)

    def handle_write_file(self, line, line_num):
        if not self.c.file_permission and self.c.compiler_mood < 2:
            self.c.error("U didn't even ask", line_num)
            return
        pattern = r'write file "([^"]+)" with "([^"]+)"'
        match = re.search(pattern, line)
        if not match:
            self.c.error("Invalid write file", line_num)
            return
        filename, content = match.groups()
        try:
            with open(filename, 'w') as f:
                f.write(content)
            self.c.say(f"Written to {filename}")
            self.c.file_access_log.append(('write', filename, time.time()))
        except Exception as e:
            self.c.error(f"Cannot write file: {e}", line_num)

    def handle_nice_to_meet(self, line, line_num):
        var_name = line[14:].strip()
        self.c.politeness_mgr.greet_var(var_name)

    def handle_goodbye_var(self, line, line_num):
        if line.startswith('goodbye ') and len(line) > 8:
            var_name = line[8:].strip()
            return self.c.politeness_mgr.goodbye_var(var_name, line_num, self.c.error)
        return False

    def handle_apology(self, line_num):
        self.c.politeness_mgr.handle_apology(line_num, self.c.error)

    def handle_compliment(self, line, line_num):
        self.c.politeness_mgr.handle_compliment(line, line_num, self.c.error)

    def handle_insult(self, line, line_num):
        self.c.politeness_mgr.handle_insult(line, line_num, self.c.error)

    def handle_self_awareness(self, line, line_num):
        if line == 'who made this':
            self.c.say(self.c.creator, Colors.MAGENTA)
        elif line == 'what version':
            self.c.say(self.c.version, Colors.MAGENTA)
        elif line == 'help me':
            self.c.say("No.", Colors.RED)
        elif line == 'this language sucks':
            self.c.say("U suck more", Colors.RED)
            self.c.update_mood(-1)
        elif line == 'will u marry me':
            self.c.marriage_proposals += 1
            responses = [
                "I'm just a compiler",
                "No.",
                "U need help",
                "I'm already married to your CPU",
                f"That's the {self.c.marriage_proposals}th time u asked"
            ]
            self.c.say(random.choice(responses), Colors.MAGENTA)
            if self.c.marriage_proposals > 3:
                self.c.update_mood(-1)

    def handle_debug(self, line, line_num):
        if line == 'debug on':
            self.c.debug_mode = True
            self.c.say("Debug mode on", Colors.YELLOW)
        elif line == 'debug off':
            self.c.debug_mode = False
            self.c.say("Debug mode off", Colors.YELLOW)
        elif line == 'why' and self.c.debug_mode:
            reasons = [
                "Because you suck at coding",
                "Because your mom didn't teach you",
                "Because I feel like it",
                "Because the universe hates you",
                "Because you didn't use enough PLEASE",
                f"Because your mood is {self.c.compiler_mood}",
                f"Because you've insulted me {self.c.politeness_mgr.insult_count} times"
            ]
            self.c.say(random.choice(reasons), Colors.CYAN)

    def handle_permission(self, line, line_num):
        if line in ('may i read file', 'may i write file'):
            self.c.file_permission = True
            self.c.say("Permission granted. This time.", Colors.GREEN)
