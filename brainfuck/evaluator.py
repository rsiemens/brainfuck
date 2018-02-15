import sys

from ast.parser import Parser


class State(object):
    def __init__(self, istream, ostream, size=30000):
        self.pointer = 0
        self.memory = [0] * size
        self.istream = istream
        self.ostream = ostream


class Evaluator(object):
    def __init__(self, append_newline=False, parser=Parser):
        self.newline = append_newline
        self.parser = parser()

    def evaluate(self, program, istream=sys.stdin, ostream=sys.stdout):
        state = State(istream, ostream)
        ast = self.parser.parse(program)

        ast.interpret(state)
        if self.newline:
            ostream.write('\n')
        ostream.flush()
