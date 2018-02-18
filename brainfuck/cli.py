import sys
from time import time
from argparse import ArgumentParser
from contextlib import contextmanager

from brainfuck import eval


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("file", help="brainfuck program file to run")
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
    return parser.parse_args()


@contextmanager
def time_run(should_time):
    start_time = time()
    yield
    if should_time:
        print("-- Execution time of %s seconds --" % (time() - start_time))


def run():
    args = parse_args()
    with open(args.file, 'r') as f:
        with time_run(args.t):
            eval(f.read(), append_newline=args.n)
