class Debugger(object):
    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.current = None
        evaluator.add_hook(self._pre_interpret_hook)

    def next(self):
        pass

    def quit(self):
        pass

    def debug(self):
        pass

    def _pre_interpret_hook(self, ast):
        """Monkey patches each ast node's interpret function to provide
        interactive debugging.
        """
        ast
        pass

    def _patched_interpret(self, state):
        pass
