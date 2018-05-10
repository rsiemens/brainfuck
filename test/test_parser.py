import unittest

from brainfuck.parser import Parser, ParserError
from brainfuck.ast import AST, ResetLoop

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

    def test_compress(self):
        p = Parser()
        ast = p.parse('++--+++>><<<-+-+')
        expressions = p.compress(ast.children)
        self.assertEqual(len(expressions), 9)

        ast = p.parse('++[--[++]]++[+[-]+]>><<<-+-+',)
        expressions = p.compress(ast.children)
        self.assertEqual(len(expressions), 10)
        self.assertEqual(len(expressions[1].children), 2)
        self.assertEqual(len(expressions[1].children[1].children), 1)
        self.assertEqual(len(expressions[3].children), 3)

    def test_reset_loops(self):
        p = Parser()
        ast = p.parse('[-]')
        expressions = p.reset_loops(ast.children)
        self.assertIsInstance(expressions[0], ResetLoop)

        ast = p.parse('[+]')
        expressions = p.reset_loops(ast.children)
        self.assertIsInstance(expressions[0], ResetLoop)

        ast = p.parse('[[-][--][+][++]]')
        expressions = p.reset_loops(ast.children)
        self.assertIsInstance(expressions[0].children[0], ResetLoop)
        self.assertNotIsInstance(expressions[0].children[1], ResetLoop)
        self.assertIsInstance(expressions[0].children[2], ResetLoop)
        self.assertNotIsInstance(expressions[0].children[3], ResetLoop)
