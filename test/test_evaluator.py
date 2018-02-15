import sys
import unittest
if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO

from brainfuck.evaluator import Evaluator

from test.fixtures import programs


class EvaluatorTestCase(unittest.TestCase):
    def create_istream(self, data):
        istream = StringIO()
        istream.write(data)
        istream.seek(0)
        return istream

    def test_evaluate(self):
        e = Evaluator()
        for program in programs:
            istream = self.create_istream(program['input'])
            ostream = StringIO()
            e.evaluate(program['program'], istream, ostream)
            ostream.seek(0)
            self.assertEqual(ostream.read(), program['output'])
