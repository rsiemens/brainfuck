[![Build Status](https://travis-ci.org/rsiemens/brainfuck.svg?branch=master)](https://travis-ci.org/rsiemens/brainfuck)

Brainfuck is an esoteric programming language created in 1993 by Urban Müller,
and notable for its extreme minimalism.[1]

The language consists of eight simple commands, which make it a nice language to
implement when learning about compilers and interpreters. Which is exactly what
this is.

Basic usage looks like...
```
python -m brainfuck -n examples/fibo.bf
>> 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
```
> Note: the example programs here can be found in the [examples](examples/) directory

stdin and stdout are the default i/o streams so you can do something like this.
```
python -m brainfuck examples/echo.bf < macbeth.txt >> shakespeare.txt
```

You can also import it as a python module.
```python
>>> from io import StringIO
>>> import brainfuck
>>>
>>> out_stream = StringIO()
>>> with open('examples/hello.bf') as f:
...     brainfuck.eval(f.read(), output_stream=out_stream, optimize=True)
...
<State pointer:6 value:10>
>>> out_stream.getvalue()
'Hello World!\n'
```

You can use the optimize flag `-o` (or `brainfunk.eval(..., optimize=True)`) to
perform some parsing optimizations. Since it adds additional parsing time only
more complex programs will benefit from it.

Currently the following optimizations are performed with the `-o` flag:
- Token compressions - Repeat tokens are compacted into one command `+++` becomes `+3`
- Reset loops - `[-]` and `[+] which decrements/increment a memory value to 0
will simply set them to 0

Depending on your program this can significantly reduce runtime. Consider
[hanoi.bf](examples/hanoi.bf) which without optimization takes about 30min to run.
With optimizations on it runs in about 2min.

Running the unit tests can be done from the project directory.
```
python -m unittest discover
```
[1]: https://en.wikipedia.org/wiki/Brainfuck
