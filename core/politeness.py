# ~/awa/core/politeness.py
# 禮貌系統與情緒

class PolitenessManager:
    def __init__(self, say_callback, debug_callback, update_mood_callback):
        self.say = say_callback
        self.debug = debug_callback
        self.update_mood = update_mood_callback

        self.politeness_count = 0
        self.block_politeness = 0
        self.politeness_threshold = 3
        self.current_block_type = 'global'
        self.perfect_politeness_count = 0

        self.greeted_vars = set()
        self.apology_needed = False
        self.compliment_count = 0
        self.insult_count = 0

    def check_politeness(self, line_num, error_callback):
        if self.block_politeness == 0:
            error_callback("INSUFFICIENTLY POLITE", line_num)
            self.apology_needed = True
            self.update_mood(-1)
        elif self.block_politeness > self.politeness_threshold:
            error_callback("Stop begging", line_num)
            self.apology_needed = True
            self.update_mood(-1)
        elif self.block_politeness == 2:
            self.perfect_politeness_count += 1
            if self.perfect_politeness_count % 3 == 0:
                self.say("U got it right... this time", '\033[92m')
                self.update_mood(1)

    def reset_block_politeness(self, new_block):
        self.block_politeness = 0
        self.current_block_type = new_block
        self.debug(f"Politeness reset for {new_block}")

    def add_politeness(self, is_polite=True):
        if is_polite:
            self.politeness_count += 1
            self.block_politeness += 1
        else:
            self.block_politeness += 1

    def greet_var(self, var_name):
        self.greeted_vars.add(var_name)
        self.say(f"{var_name} says hi back", '\033[92m')
        self.update_mood(1)

    def goodbye_var(self, var_name, line_num, error_callback):
        if var_name in self.greeted_vars:
            self.greeted_vars.remove(var_name)
            self.say(f"{var_name} left quietly", '\033[96m')
            return True
        else:
            error_callback(f"{var_name} wasn't even here", line_num)
            self.update_mood(-1)
            return False

    def handle_apology(self, line_num, error_callback):
        if self.apology_needed:
            self.say("Apology accepted, but fix it", '\033[92m')
            self.apology_needed = False
            self.update_mood(1)
        else:
            error_callback("U didn't even do anything wrong", line_num)
            self.update_mood(-1)

    def handle_compliment(self, line, line_num, error_callback):
        self.compliment_count += 1
        if line == 'u are great':
            if self.compliment_count > 3:
                error_callback("U trying to bribe me?", line_num)
                self.update_mood(-1)
            else:
                self.say("I know", '\033[93m')
                self.update_mood(1)
        elif line.startswith('u are great,'):
            prog = line[12:].strip()
            responses = [
                f"{prog} is pretty good, I guess",
                f"{prog}? Meh",
                f"{prog} is better than u"
            ]
            self.say(random.choice(responses), '\033[96m')

    def handle_insult(self, line, line_num, error_callback):
        self.insult_count += 1
        self.update_mood(-1)
        if line == 'fuck you':
            if self.insult_count > 3:
                responses = [
                    "U just mad cuz u can't code",
                    "U need therapy",
                    "U again?",
                    "I'm telling mom"
                ]
                self.say(random.choice(responses), '\033[91m')
            else:
                self.say("fuck u too", '\033[91m')
        elif line.startswith('fuck u,'):
            prog = line[7:].strip()
            if random.random() > 0.5:
                self.say(f"Yeah, {prog} sucks", '\033[91m')
            else:
                self.say(f"Actually {prog} is better than u", '\033[93m')
