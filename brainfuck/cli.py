"""Brainfuck interpreter cli"""
import sys
from time import time
from argparse import ArgumentParser
from contextlib import contextmanager

from brainfuck import eval


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",
        help="brainfuck program file (or code with -c) to run"
    )
    parser.add_argument(
        "-t",
        action="store_true",
        help="output execution time after running"
    )
    parser.add_argument(
        "-n",
        action="store_true",
        help="append a newline to the programs output"
    )
    parser.add_argument(
        "-c",
        action="store_true",
        help="brainfuck code string to run"
    )
    parser.add_argument(
        "-o",
        action="store_true",
        help="perform runtime optimization to speed up execution"
    )
    return parser.parse_args()


@contextmanager
def time_run(should_time):
    start_time = time()
    yield
    if should_time:
        print("-- Execution time of %s seconds --" % (time() - start_time))


def run():
    args = parse_args()

    if args.c:
        code = args.file
    else:
        with open(args.file, 'r') as f:
            code = f.read()

    with time_run(args.t):
        eval(code, append_newline=args.n, optimize=args.o)
