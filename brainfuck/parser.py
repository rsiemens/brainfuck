from brainfuck.ast import (
    AST,
    PointerIncrement,
    PointerDecrement,
    ByteIncrement,
    ByteDecrement,
    ByteIn,
    ByteOut,
    Loop,
    ResetLoop,
    AdjustableAmount,
)


class ParserError(Exception):
    pass


class Parser(object):
    def brackets_balanced(self, program):
        brackets = [c for c in program if c in "[]"]
        stack = []

        if len(brackets) == 0:
            return True
        if len(brackets) % 2 != 0:
            return False

        for bracket in brackets:
            if bracket == "[":
                stack.append(bracket)
            else:
                try:
                    stack.pop()
                except IndexError:
                    return False

        if len(stack):
            return False
        return True

    def parse(self, program, optimize=False):
        expressions = []

        if not self.brackets_balanced(program):
            raise ParserError("Unmatched opening/closing square brackets")

        for token in program:
            if token == ">":
                expressions.append(PointerIncrement())
            elif token == "<":
                expressions.append(PointerDecrement())
            elif token == "+":
                expressions.append(ByteIncrement())
            elif token == "-":
                expressions.append(ByteDecrement())
            elif token == ".":
                expressions.append(ByteOut())
            elif token == ",":
                expressions.append(ByteIn())
            elif token == "[":
                expressions.append(token)
            elif token == "]":
                children = []
                expression = expressions.pop()
                while expression != "[":
                    children.append(expression)
                    expression = expressions.pop()
                # children expressions are backwards since we pop'd them
                expressions.append(Loop(children[::-1]))

        if optimize:
            expressions = self.compress(self.reset_loops(expressions))

        return AST(expressions)

    def compress(self, expressions):
        """Compress expressions like +++-- into a single addition of 3 and
        subtraction of two instead of three additions and two subtractions.
        """
        optimized = []

        for exp in expressions:
            last = optimized[len(optimized) - 1] if optimized else None
            if type(last) == type(exp) and isinstance(last, AdjustableAmount):
                last.increment()
            elif type(exp) == Loop:
                optimized.append(exp)
                exp.children = self.compress(exp.children)
            else:
                optimized.append(exp)

        return optimized

    def reset_loops(self, expressions):
        """Common bf idiom of reseting a memory value to 0 `[-]` or `[+]` which
        performs O(n). This reduces it to O(1).
        """
        optimized = []
        candidates = [ByteDecrement, ByteIncrement]

        for exp in expressions:
            if type(exp) == Loop:
                if len(exp.children) == 1 and any(
                    [isinstance(exp.children[0], t) for t in candidates]
                ):
                    optimized.append(ResetLoop())
                else:
                    exp.children = self.reset_loops(exp.children)
                    optimized.append(exp)
            else:
                optimized.append(exp)

        return optimized
