Having just discussed Python's iterators and iterables (Parts <a href="/2014/02/24/python-iterables/">1</a> <a href="/2014/02/26/python-iterables-part-2/">2</a> and <a href="/2014/02/27/python-iterables-part-3/">3</a>), now is a good time to discuss a smarter, sleeker way of dealing with long (or infinite) lists of values to iterate over.

Enter, <strong>generators</strong>.

<!--more-->

In simplest terms, Python generators are objects that act like lists (i.e., are "duck typed" to act as lists) since they implement a <code>next()</code> method.  The distinction that generators hold over lists is that generators are <strong>"lazily evaluated"</strong>, which is to say they only yield values when they <em>need</em> to.  Let's see an example below:

<TOGGLEPYTHON>
def my_gen():
    yield 'a'
    yield 'b'
    yield 'c'

print my_gen()

for i in my_gen():
    print i
<TOGGLEPYTHON>

yields

<TOGGLEOUT>
<generator object my_gen at 0x10ea04f50>
a
b
c
<TOGGLEOUT>

We see here that calling the function <code>my_gen()</code> is what actually returns the generator object.  We also see that we're using a special keyword "yield" here (as opposed to "return").  This indicates to Python that the function should return a generator, as opposed to the value indicated.  Yields and returns don't mix, as we can observe below:

<TOGGLEPYTHON>
def f():
    yield 'x'
    return 'y'
<TOGGLEPYTHON>

yields

<TOGGLEOUT>
SyntaxError: 'return' with argument inside generator (<pyshell#104>, line 3)
<TOGGLEOUT>

<h3>Breaking it Down</h3>
But let's dissect how <code>my_gen()</code> is actually operating.  How does the for-loop know when the generator is exhausted?  Well, since we know the generator implements the <code>next()</code> method, let's invoke it manually below:

<TOGGLEPYTHON>
def my_gen():
    yield 'a'
    yield 'b'
    yield 'c'

g = my_gen()

print g.next()
print g.next()
print g.next()
print g.next() # oops
<TOGGLEPYTHON>

yields

<TOGGLEOUT>
a
b
c
Traceback (most recent call last):
  File "/Users/Matt/PYTHON_FILES/COLOR/CODE/source.py", line 11, in <module>
    print g.next() # oops
StopIteration
<TOGGLEOUT>

Ah, of course.  <em>Generators are duck-typed to be like lists.</em>  So, of course, they indicate that it's time to stop iterating with a <strong>StopIteration exception</strong>.

<a href="/2014/09/16/python-generators-part-2/" />Part 2 here...</a>