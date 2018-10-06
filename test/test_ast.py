import unittest
from string import printable

from brainfuck.evaluator import State
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
)

from test.fixtures import StringIO


class AstTestCase(unittest.TestCase):
    def setUp(self):
        self.size = 10
        self.istream = StringIO()
        self.ostream = StringIO()
        self.state = State(self.istream, self.ostream, size=self.size)

    def test_pointer_increment(self):
        PointerIncrement().interpret(self.state)
        self.assertEqual(self.state.pointer, 1)

        # incrementing past the memory size wraps back to 0
        self.state.pointer = self.size - 1
        PointerIncrement().interpret(self.state)
        self.assertEqual(self.state.pointer, 0)

    def test_pointer_decrement(self):
        self.state.pointer = 1
        PointerDecrement().interpret(self.state)
        self.assertEqual(self.state.pointer, 0)

        # decrementing below 0 wraps back to the states memory size
        PointerDecrement().interpret(self.state)
        self.assertEqual(self.state.pointer, self.size - 1)

    def test_byte_increment(self):
        for i in range(1, 256):
            ByteIncrement().interpret(self.state)
            self.assertEqual(self.state.memory[self.state.pointer], i)

        # incrementing the value at a mem location past 255 will wrap back to 0
        ByteIncrement().interpret(self.state)
        self.assertEqual(self.state.memory[self.state.pointer], 0)

    def test_byte_decrement(self):
        self.state.memory[self.state.pointer] = 255
        for i in range(1, 256):
            ByteDecrement().interpret(self.state)
            self.assertEqual(self.state.memory[self.state.pointer], 255 - i)

        # incrementing the value at a mem location past 255 will wrap back to 0
        ByteDecrement().interpret(self.state)
        self.assertEqual(self.state.memory[self.state.pointer], 255)

    def test_byte_in(self):
        self.istream.write(printable)
        self.istream.seek(0)
        for c in printable:
            ByteIn().interpret(self.state)
            self.assertEqual(self.state.memory[0], ord(c))

    def test_byte_out(self):
        for c in printable:
            self.state.memory[0] = ord(c)
            ByteOut().interpret(self.state)
        self.ostream.seek(0)
        self.assertEqual(self.ostream.read(), printable)

    def test_reset_loop(self):
        self.state.pointer = 3
        self.state.memory[self.state.pointer] = 123
        reset_loop = ResetLoop()
        reset_loop.interpret(self.state)
        self.assertEqual(self.state.memory[self.state.pointer], 0)

    def test_loop(self):
        pass
