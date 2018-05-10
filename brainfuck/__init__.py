"""A brainfuck interpreter"""
import sys

from brainfuck.evaluator import Evaluator

__author__ = "Ryan Siemens"
__email__ = "ryanjsiemens@gmail.com"
__version__ = "0.3.0"
__license__ = "MIT"


def eval(program, input_stream=sys.stdin, output_stream=sys.stdout,
         append_newline=False, optimize=False):
    evaluator = Evaluator(append_newline, optimize)
    return evaluator.evaluate(program, input_stream, output_stream)
