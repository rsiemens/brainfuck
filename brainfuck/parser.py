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
    def parse(self, program):
        expressions = []
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
                    try:
                        expression = expressions.pop()
                    except IndexError:
                        raise ParserError(
                            'Unmatched opening closing square brackets'
                        )
                # children expressions are backwards since we pop'd them
                expressions.append(Loop(children[::-1]))
        return AST(expressions)
