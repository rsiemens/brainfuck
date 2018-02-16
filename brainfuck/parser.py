from brainfuck.ast import (
    AST,
    PointerIncrement,
    PointerDecrement,
    ByteIncrement,
    ByteDecrement,
    ByteIn,
    ByteOut,
    Loop
)


class ParserError(Exception):
    pass


class Parser(object):
    def brackets_balanced(self, program):
        brackets = [c for c in program if c in '[]']
        stack = []

        if len(brackets) == 0:
            return True
        if len(brackets) % 2 != 0:
            return False

        for bracket in brackets:
            if bracket == '[':
                stack.append(bracket)
            else:
                try:
                    stack.pop()
                except IndexError:
                    return False

        if len(stack):
            return False
        return True

    def parse(self, program):
        expressions = []

        if not self.brackets_balanced(program):
            raise ParserError('Unmatched opening/closing square brackets')

        for token in program:
            if token == '>':
                expressions.append(PointerIncrement())
            elif token == '<':
                expressions.append(PointerDecrement())
            elif token == '+':
                expressions.append(ByteIncrement())
            elif token == '-':
                expressions.append(ByteDecrement())
            elif token == '.':
                expressions.append(ByteOut())
            elif token == ',':
                expressions.append(ByteIn())
            elif token == '[':
                expressions.append(token)
            elif token == ']':
                children = []
                expression = expressions.pop()
                while expression != '[':
                    children.append(expression)
                    expression = expressions.pop()
                # children expressions are backwards since we pop'd them
                expressions.append(Loop(children[::-1]))
        return AST(expressions)
