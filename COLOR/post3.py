(Continued from <a href="/2014/02/24/python-iterables/">Part 1</a>)

Python is very nice in that it gives you the "for X in Y" abstraction of iterating over sequential data structures such as lists and files, but it's important to know what's <em>really</em> going on with Python iterables, especially if we want to make our own iterables.
<!--more-->
The answer is actually quite simple:
1) To be an <strong>iterable</strong> (in Python), an object must implement the <code>__iter__</code> method.
2) The <code>__iter__</code> method must return an <strong>iterator</strong> (similar, in principle, to those found in Java, C++, etc.)

And what is an <strong>iterator</strong>, then?  An iterator is simply an object that implements the <code>next</code> method which, when called, returns the next element in the sequence -- be it the next letter in a string, the next line in a file, etc.  If there <em>is</em> no element to return, the <code>next</code> method must simply raise a <strong>StopIteration</strong> exception.  (An <strong>iterator</strong> must also implement the <code>__iter__</code> method, though this just returns <code>self</code>.)

Thus, a "for" loop simply <strong>calls the <code>next</code> method of the given object's iterator until a StopIteration exception is raised!</strong>  In terms of "for X in Y", the "for" loop gets the <strong>iterator</strong> of Y and calls its <code>next</code> method over and over, saving each result (temporarily) to a local variable "X".
&nbsp;<hr />&nbsp;
Yadda yadda, that's a lot of talk.  What does this mean in <em>practice</em>?  Let's look at a few examples of implementing <em>custom iterables and iterators</em>!

<strong>Example 1:  A Super-Simple Custom Iterable</strong>
Below, I've defined a very simple class that takes a string "s" upon initialization.  It also implements the <code>__iter__</code> method (in a silly but valid way), thus making this class <strong>iterable</strong>.

<TOGGLEPYTHON>
class MyIterableClass:
    def __init__(self, s):
        self.s = s
    def __iter__(self):
        return iter(self.s)
<TOGGLEPYTHON>

Because our above class is <strong>iterable</strong>, we can do the following:

<TOGGLEPYTHON>
Y = MyIterableClass("Hi!")
for X in Y:
    print X
<TOGGLEPYTHON>

... which, when run, produces:

<TOGGLEOUT>
H
i
!
<TOGGLEOUT>

<strong>Example 2:  Playing Around with Iterators</strong>
We know that <strong>iterators</strong> are simply objects that implement the <code>next</code> method.  Does that mean we can emulate a "for" loop manually?  Absolutely.  First, let's experiment with manual calls to <code>next</code>.

Using our <strong>iterable</strong> variable "Y" from before, we can <em>manually</em> get its <strong>iterator</strong> by using the built-in Python function <code>iter()</code> as such:

<TOGGLEPYTHON>
myIter = iter(Y)
<TOGGLEPYTHON>

Now, "myIter" is the actual <strong>iterator</strong> of "Y" -- that is, it implements the <code>next</code> method, which we can call manually.  Executing:

<TOGGLEPYTHON>
print next(myIter) # prints 'H'
print next(myIter) # prints 'i'
print next(myIter) # prints '!'
print next(myIter) # throws a StopIteration exception, since there are no elements left!
<TOGGLEPYTHON>

... yields...

<TOGGLEOUT>
H
i
!
Traceback (most recent call last):
File "/Users/Matt/PYTHON_FILES/BLOG_POSTS/sandbox/sandbox.py", line 18, in
    print next(myIter)
StopIteration
<TOGGLEOUT>

And we see that the <code>next</code> method did what it should've:  it gave us each character of the string "Hi!", in order, and then errored out when we asked for the next element that it didn't have.

Of course, this is <em>too</em> manual -- what if we don't want to copy-and-paste our calls to <code>next()</code>?  Well, we can effectively emulate a "for" loop with the below code, instead:

<TOGGLEPYTHON>
myIter = iter(Y) # if we've already run through 'myIter', we need to reset it.
while True:
    try:
        print myIter.next() # print the next element
    except StopIteration:
        break # stop -- we've hit the end
<TOGGLEPYTHON>

This way, we avoid raising the <strong>StopException</strong> error, catching it instead.  This is effectively what a "for X in Y" loop does -- it gets the <strong>iterator</strong> via <code>iter(Y)</code> and calls its <code>next()</code> method repeatedly until there are no elements left.

When we run our "manual for loop", we see printed to the console:

<TOGGLEOUT>
H
i
!
<TOGGLEOUT>

... which is exactly what our "for X in Y" call from example 1 produced.  Hooray!

(To be continued in Part 3...)