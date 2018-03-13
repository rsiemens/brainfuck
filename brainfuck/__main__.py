import sys

from brainfuck.cli import run

try:
    sys.exit(run())
except KeyboardInterrupt:
    sys.exit(0)
