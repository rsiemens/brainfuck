from distutils.core import setup

import brainfuck

setup(
    name='Brainfuck',
    version=brainfuck.__version__,
    description=brainfuck.__doc__,
    author=brainfuck.__author__,
    author_email=brainfuck.__email__,
    license=brainfuck.__license__,
    url='https://github.com/rsiemens/brainfuck',
    packages=['brainfuck'],
 )
