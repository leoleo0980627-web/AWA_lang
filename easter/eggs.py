# ~/awa/easter/eggs.py
# 彩蛋系統

import time

class EasterEggs:
    def __init__(self, say_callback, today, fortune_callback):
        self.say = say_callback
        self.today = today
        self.fortune = fortune_callback
        self.count = {}

        self.eggs = {
            'the answer': lambda: self.say("42"),
            'to be or not to be': lambda: self.say("that is the question"),
            'sudo make me a sandwich': lambda: self.say("make it yourself"),
            'hello world': lambda: self.say("original"),
            "i'm done": self.emergency_exit,
            'the meaning of life': lambda: self.say("42... obviously"),
            '42': lambda: self.say("u get it"),
            'what is love': lambda: self.say("Baby don't hurt me, don't hurt me, no more"),
            'never gonna give you up': lambda: self.say("U just got rickrolled by a compiler"),
            'ping': lambda: self.say("pong"),
            'whoami': lambda: self.say("A failure"),
            'date': lambda: self.say(self.today.strftime("%Y-%m-%d")),
            'time': lambda: self.say(time.strftime("%H:%M:%S")),
            'weather': lambda: self.say("Cloudy with a chance of syntax errors"),
            'fortune': lambda: self.say(self.fortune()),
        }

    def check(self, line):
        if line in self.eggs:
            self.eggs[line]()
            self.count[line] = self.count.get(line, 0) + 1
            if self.count[line] > 3:
                self.say("U really like this, huh?", '\033[96m')
            return True
        return False

    def emergency_exit(self):
        print("\nFinally. Get out.")
        sys.exit(0)
