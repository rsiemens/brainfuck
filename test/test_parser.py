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

        ast = p.parse(",[.[-],]")
        self.assertIsInstance(ast, AST)
        self.assertEqual(len(ast.children), 2)
        self.assertEqual(len(ast.children[1].children), 3)
        self.assertEqual(len(ast.children[1].children[1].children), 1)

    def test_brackets_balanced(self):
        p = Parser()
        self.assertTrue(p.brackets_balanced('[[[]]]'))
        self.assertTrue(p.brackets_balanced('[90ua\n][asdf][826$%[}{|]]'))
        self.assertFalse(p.brackets_balanced('[]]'))
        self.assertFalse(p.brackets_balanced('[[]'))
        self.assertFalse(p.brackets_balanced('[]]]'))
        self.assertFalse(p.brackets_balanced('[[]['))

    def test_optimize(self):
        p = Parser()
        ast = p.parse('++--+++>><<<-+-+', optimize=True)
        self.assertEqual(len(ast.children), 9)

        ast = p.parse('++[--[++]]++[+[-]+]>><<<-+-+', optimize=True)
        self.assertEqual(len(ast.children), 10)
        self.assertEqual(len(ast.children[1].children), 2)
        self.assertEqual(len(ast.children[1].children[1].children), 1)
        self.assertEqual(len(ast.children[3].children), 3)
