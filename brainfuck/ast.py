"""For optimization we can compress something like `+++` from 3 `ByteIncrement`
objects to just one that increments by 3.

To do this we use wrapping counters. The fastests are as follows:
    1. increment by n and perform bitwise-AND (requires power of 2)
    2. increment compare and reset
    3. increment and mod (slow and not used)
"""


class Expression(object):
    def interpret(self, state):
        raise NotImplementedError()


class AdjustableAmount(Expression):
    def __init__(self):
        self.amount = 1

    def increment(self):
        self.amount += 1


class PointerIncrement(AdjustableAmount):
    def interpret(self, state):
        state.pointer += self.amount
        if state.pointer > len(state.memory) - 1:
            state.pointer = state.pointer - len(state.memory)


class PointerDecrement(AdjustableAmount):
    def interpret(self, state):
        state.pointer -= self.amount
        if state.pointer < 0:
            state.pointer = len(state.memory) + state.pointer


class ByteIncrement(AdjustableAmount):
    def interpret(self, state):
        value = state.memory[state.pointer]
        state.memory[state.pointer] = (value + self.amount) & 0xFF


class ByteDecrement(AdjustableAmount):
    def interpret(self, state):
        value = state.memory[state.pointer]
        state.memory[state.pointer] = (value - self.amount) & 0xFF


class ByteIn(Expression):
    def interpret(self, state):
        try:
            state.memory[state.pointer] = ord(state.istream.read(1))
        except TypeError:  # thrown on EOF when calling ord('')
            pass


class ByteOut(Expression):
    def interpret(self, state):
        char = chr(state.memory[state.pointer])
        state.ostream.write(char)
        state.ostream.flush()


class Loop(Expression):
    def __init__(self, children):
        self.children = children

    def interpret(self, state):
        while state.memory[state.pointer] != 0:
            for child in self.children:
                child.interpret(state)


class ResetLoop(Expression):
    """Common bf idiom to set a memory value to 0 `[-]`"""
    def interpret(self, state):
        state.memory[state.pointer] = 0


class AST(Expression):
    def __init__(self, children):
        self.children = children

    def interpret(self, state):
        for child in self.children:
            child.interpret(state)
