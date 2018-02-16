import unittest

from brainfuck.parser import Parser, ParserError
from brainfuck.ast import AST

from test.fixtures import error_inputs


class ParserTestCase(unittest.TestCase):
    def test_parse(self):
        p = Parser()

        for error_input in error_inputs:
            with self.assertRaises(ParserError):
                p.parse(error_input)

        ast = p.parse(",[.[-]]")
        self.assertIsInstance(ast, AST)
        self.assertEqual(len(ast.children), 2)
        self.assertEqual(len(ast.children[1].children), 2)
        self.assertEqual(len(ast.children[1].children[1].children), 1)
