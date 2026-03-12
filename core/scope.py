# ~/awa/core/scope.py
# 作用域管理

class ScopeManager:
    def __init__(self, error_callback, debug_callback):
        self.scopes = [{}]
        self.error = error_callback
        self.debug = debug_callback
        self.apology_needed = False

    def get_var(self, name, line_num):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        self.error(f"Variable {name} not declared", line_num)
        self.apology_needed = True
        return None

    def set_var(self, name, value, var_type, line_num):
        for i in range(len(self.scopes)-1, -1, -1):
            if name in self.scopes[i]:
                self.scopes[i][name] = (var_type, value)
                return
        self.scopes[-1][name] = (var_type, value)

    def declare_var(self, name, value, var_type):
        self.scopes[-1][name] = (var_type, value)

    def enter_scope(self, scope_type):
        self.scopes.append({})
        self.debug(f"Entered {scope_type} scope")

    def exit_scope(self):
        if len(self.scopes) > 1:
            exited_vars = list(self.scopes[-1].keys())
            self.scopes.pop()
            self.debug(f"Exited scope, lost vars: {exited_vars}")
            return exited_vars
        return []

    def get_all_vars(self):
        all_vars = {}
        for scope in self.scopes:
            all_vars.update(scope)
        return all_vars
