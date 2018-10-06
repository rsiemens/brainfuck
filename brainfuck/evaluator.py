import sys

from brainfuck.parser import Parser


class State(object):
    def __init__(self, istream, ostream, size=30000):
        self.pointer = 0
        self.memory = [0] * size
        self.istream = istream
        self.ostream = ostream

    def __repr__(self):
        return "<State pointer:%d value:%d>" % (self.pointer, self.memory[self.pointer])

    def __getitem__(self, key):
        return self.memory[key]

    def __iter__(self):
        return iter(self.memory)


class Evaluator(object):
    def __init__(self, append_newline=False, optimize=False, parser=Parser):
        self.newline = append_newline
        self.optimize = optimize
        self.parser = parser()

    def evaluate(self, program, istream=sys.stdin, ostream=sys.stdout):
        state = State(istream, ostream)
        ast = self.parser.parse(program, optimize=self.optimize)

        ast.interpret(state)
        if self.newline:
            ostream.write("\n")
        ostream.flush()
        return state
