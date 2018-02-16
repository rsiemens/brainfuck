import sys
from argparse import ArgumentParser

from brainfuck import eval


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("file", help="brainfuck program file to run")
    parser.add_argument(
        "-n",
        action="store_true",
        help="append a newline to the programs output"
    )
    return parser.parse_args()


def run():
    args = parse_args()
    with open(args.file, 'r') as f:
        eval(f.read(), append_newline=args.n)
