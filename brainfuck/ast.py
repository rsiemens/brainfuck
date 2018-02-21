class Expression(object):
    def interpret(self, state):
        raise NotImplementedError()


class PointerIncrement(Expression):
    def interpret(self, state):
        amount = getattr(self, 'amount', 1)
        state.pointer = (state.pointer + amount) % len(state.memory)


class PointerDecrement(Expression):
    def interpret(self, state):
        amount = getattr(self, 'amount', 1)
        state.pointer = (state.pointer - amount) % len(state.memory)


class ByteIncrement(Expression):
    def interpret(self, state):
        amount = getattr(self, 'amount', 1)
        value = state.memory[state.pointer]
        state.memory[state.pointer] = (value + amount) % 256


class ByteDecrement(Expression):
    def interpret(self, state):
        amount = getattr(self, 'amount', 1)
        value = state.memory[state.pointer]
        state.memory[state.pointer] = (value - amount) % 256


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


class Loop(Expression):
    def __init__(self, children):
        self.children = children

    def interpret(self, state):
        while state.memory[state.pointer] != 0:
            for child in self.children:
                child.interpret(state)


class AST(Expression):
    def __init__(self, children):
        self.children = children

    def interpret(self, state):
        for child in self.children:
            child.interpret(state)
