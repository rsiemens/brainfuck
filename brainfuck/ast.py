class Expression(object):
    def interpret(self, state):
        raise NotImplementedError()


class PointerIncrement(Expression):
    def interpret(self, state):
        state.pointer += 1
        if state.pointer > len(state.memory) - 1:
            state.pointer = 0


class PointerDecrement(Expression):
    def interpret(self, state):
        state.pointer -= 1
        if state.pointer < 0:
            state.pointer = len(state.memory) - 1


class ByteIncrement(Expression):
    def interpret(self, state):
        state.memory[state.pointer] += 1
        if state.memory[state.pointer] > 255:
            state.memory[state.pointer] = 0


class ByteDecrement(Expression):
    def interpret(self, state):
        state.memory[state.pointer] -= 1
        if state.memory[state.pointer] < 0:
            state.memory[state.pointer] = 255


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
