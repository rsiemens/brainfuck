import sys

from brainfuck.evaluator import Evaluator


def eval(program, input_stream=sys.stdin, output_stream=sys.stdout,
         append_newline=False):
    Evaluator(append_newline).evaluate(program, input_stream, output_stream)
