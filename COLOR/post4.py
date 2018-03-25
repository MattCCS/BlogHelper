(Continued from <a href="/2014/02/26/python-iterables-part-2/">Part 2</a>)

In the previous post, we covered creating a very simple custom <strong>iterable</strong> class by implementing the <code>__iter__</code> method.  Now, we'll take a look at implementing our own <strong>iterator</strong> class, and then we'll combine the two.
<!--more-->&nbsp;<hr />&nbsp;
<strong>Example 3:  A Custom Iterator Class</strong>
As we discussed before, an iterator only needs to implement the <code>next</code> method (and the <code>__iter__</code> method, which just returns <code>self</code>).  Let's define our simple <strong>iterator</strong> class below:

<TOGGLEPYTHON>
class MyIteratorClass:
    def __init__(self, values):
        self.L = list(values) # coerces into list, allowing .pop(0) calls.
    def __iter__(self):
        return self

    def next(self):
        try:
            return self.L.pop(0)
        except IndexError:
            raise StopIteration
<TOGGLEPYTHON>

As you can see, our custom iterator is pretty trivial -- its <code>next</code> method just returns the first of its list of values, removing it in the process.  If it tries to remove the first item but can't because there <em>are</em> none, it catches that <strong>IndexError</strong> and raises a <strong>StopIteration</strong> exception instead.

<em>(NOTE: this is by no means a perfect or universal solution -- the assumption we make is that the sequence "values" given upon instantiation can actually be made into a list.  If it can't, this code crashes... but for experimentation purposes with built-ins, this system works just fine.)</em>

Now, what can we do with this class?  The same things we did with the Python-provided iterator from our "MyIterableClass" example.  Let's try out the built-in <code>next</code> function with our custom iterator.  If we run:

<TOGGLEPYTHON>
myIterator = MyIteratorClass("Bye?")
print next(myIterator) # prints 'B'
print next(myIterator) # prints 'y'
print next(myIterator) # prints 'e'
print next(myIterator) # prints '?'
print next(myIterator) # throws StopIteration exception!
<TOGGLEPYTHON>

... we get the following (correct) output:

<TOGGLEOUT>
B
y
e
?
Traceback (most recent call last):
File "/Users/Matt/PYTHON_FILES/BLOG_POSTS/sandbox/sandbox.py", line 28, in
    print next(myIterator) # throws StopIteration exception!
StopIteration
<TOGGLEOUT>

Now for something cool:  we can even perform a "for X in Y" loop with our <strong>iterator</strong> object as the "Y"!  See below:

<TOGGLEPYTHON>
myIterator = MyIteratorClass("Bye?")
for X in myIterator:
    print X
<TOGGLEPYTHON>

... produces:

<TOGGLEOUT>
B
y
e
?
<TOGGLEOUT>

<em>"How can this be, though?  It's an <strong>iterator</strong>, not an <strong>iterable</strong>!"</em>  Well, recall that, to be <em>considered an <strong>iterable</strong> by Python</em>, an object must simply implement the <code>__iter__</code> method, which must return an <strong>iterator</strong> object -- and that is exactly what our class does!  It just returns <em>itself</em>, which is already an <strong>iterator</strong>!

This actually introduces a very important concept in Python called  <strong>duck typing</strong>.  "<strong>Duck typing</strong>" refers to the concept that, if something walks like a duck, talks like a duck, and otherwise does everything that a duck does, it is functionally the same as a duck, and thus <em>can be considered a duck</em>.

By this same token: because our <strong>MyIteratorClass</strong> implements the <code>next</code> method, it can be considered an <strong>iterator</strong>.  <em>Furthermore</em>, because the same class implements the <code>__iter__</code> method, it can <em>also</em> be considered an <strong>iterable</strong>!

This is made possible by the fact that Python does not perform "<strong>type checking</strong>" (<em>checking</em> whether arguments/parameters are of a certain <em>type</em> before running) like Java and C++ do.  While this makes possible a whole host of misuses, it also allows for interestingly abstract and dynamic programs.  That's Python for you.
&nbsp;<hr />&nbsp;
<strong>Example 4:  All Together Now...</strong>
Blah blah blah, enough talk.  Let's put it all together.  See below for both of our classes defined:

<TOGGLEPYTHON>
class MyIterableClass:
    def __init__(self, s):
        self.s = s
    def __iter__(self):
        return MyIteratorClass(self.s)

class MyIteratorClass:
    def __init__(self, values):
        self.L = list(values) # coerces into list, allowing .pop(0) calls.

    def __iter__(self):
        return self

    def next(self):
        try:
            return self.L.pop(0)
        except IndexError:
            raise StopIteration
<TOGGLEPYTHON>

Note that the only change we made to our original <strong>MyIterableClass</strong> was altering its <code>__iter__</code> method -- it now returns our custom <strong>MyIteratorClass</strong> object, instead of a Python built-in iterator object.

Testing it with the code below:

<TOGGLEPYTHON>
Y = MyIterableClass("Bye?")
for X in Y:
    print X
<TOGGLEPYTHON>

... produces:

<TOGGLEOUT>
B
y
e
?
<TOGGLEOUT>

BONUS:  Since our <strong>MyIteratorClass</strong> implements <code>__iter__</code>, which just returns itself, we can prove that our custom <strong>iterator</strong> works just like the Python built-in ones!  See the silliness below:

<TOGGLEPYTHON>
Y = MyIterableClass("ABC")
L = [1,2,3]
myIter = iter(iter(iter(iter(iter(Y))))) # dumb.
otherIter = iter(iter(iter(iter(iter(L))))) # dumber.

for X in myIter:
    print X

for X in otherIter:
    print X
<TOGGLEPYTHON>

... produces:

<TOGGLEOUT>
A
B
C
1
2
3
<TOGGLEOUT>

... as it should.  Success!