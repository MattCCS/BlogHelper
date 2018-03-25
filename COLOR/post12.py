If you thought manipulating the global namespace could not get any worse, you were horribly mistaken.

Today, through the use of duck typing and an optional parameter of <code>execfile</code>, I make things much, much worse.  Exponentially worse.

<!--more-->
Suffice it to say, the following program does something very questionable:  it runs itself, but replaces the global namespace with a custom class with very "nontraditional" features.
<TOGGLEPYTHON>
#!/usr/bin/env python

####################################
# CHILD check
# guarantees CHILD == True only for the child code
try:
    assert CHILD
except NameError:
    CHILD = False

print "I am {}the child.".format('' if CHILD else "NOT ")
<TOGGLEPYTHON>
The preceeding code exists so that, when we re-execute this Python file, we will inject a variable <code>CHILD</code> set to <code>True</code>.  That way, we can tell that we are in the child program and avoid an infinite loop of file execution.  The <code>CHILD</code> variable will be defined later.

Next, we define a class <code>Fauxcals</code> (read "faux locals") which we will use to <em>replace</em> the global namespace (or at least stand in between the true global namespace and the rest of the program).
<TOGGLEPYTHON>
####################################
# GLOBALS
import re
import sys

TITLE_REGEX = r"^(?P<a>[^_]+)(?P<op>(_[^_]+)+_)(?P<b>[^_]+)$"

####################################
# my evil class
class Fauxcals(dict):

    def __init__(self, d):
        self.d = d

    def __len__(self):
        return len(self.d)

    def __getitem__(self, key):
        if re.match(TITLE_REGEX, key) and key not in self.d:
            c(key, self)
        return self.d[key]
    
    def __setitem__(self, key, value):
        self.d[key] = value
    
    def __delitem__(self, key):
        del self.d[key]
    
    def __iter__(self):
        return iter(self.d)
    
    def __reversed__(self):
        return reversed(self.d)
    
    def __contains__(self, item):
        return item in self.d
    
    def __missing__(self, key):
        return self.d.__missing__(key)
<TOGGLEPYTHON>
As you can see, the above class implements most things you would want out of a namespace -- a mapping of names to values, the ability to add and delete items, etc.

However, it also includes something odd:  if its <code>__getitem__</code> method fails, but the requested variable matches a regular expression, this satanic namespace will <em>silently create it</em> -- using our handy "c" function from the previous post:
<TOGGLEPYTHON>
# the original function, mostly
def c(s, surrogate_globals=None):

    class Evaluable:

        def __init__(self, a, b, op, surrogate_globals=None):
            self.glob = surrogate_globals if surrogate_globals is not None else globals()
            self.a = a if not a.isdigit() else int(a)
            self.b = b if not b.isdigit() else int(b)
            self.op = op

        def coerce_if_live(self, o):
            return o if not (type(o) == str) else self.glob[o]

        def __nonzero__(self):
            a = self.coerce_if_live(self.a)
            b = self.coerce_if_live(self.b)

            return self.op(a,b)

    M = re.match(TITLE_REGEX, s)
    if not M:
        raise SyntaxError

    # because screw the "operator" module, that's why.
    D = {
        "_is_less_than_" :   lambda a,b: a < b,
        "_is_greater_than_": lambda a,b: a > b,
        "_is_less_than_or_equal_to_":    lambda a,b: a <= b,
        "_is_greater_than_or_equal_to_": lambda a,b: a >= b,
        "_is_not_equal_to_": lambda a,b: a != b,
        "_is_equal_to_": lambda a,b: a == b,
        "_is_identical_to_": lambda a,b: a is b,
        "_is_not_identical_to_": lambda a,b: a is not b,
        "_is_inside_": lambda a,b: a in b,
        "_is_not_inside_": lambda a,b: a not in b,
    }

    M_D = M.groupdict()

    a  = M_D['a']
    b  = M_D['b']
    op = D[M_D['op']]

    E = Evaluable(a, b, op, surrogate_globals=surrogate_globals)

    if not surrogate_globals:
        globals()[s] = E
    else:
        surrogate_globals[s] = E

    return E # feel free to use this, or the global one
<TOGGLEPYTHON>
As you can see, we have not changed the "c" function very much.  It still does what we <del>hate</del> love:  returns an object whose booleanness is re-evaluated every time you ask for it.

Below, however, is the true black magic:
<TOGGLEPYTHON>
# our surrogate namespace object
pure_evil = Fauxcals({"CHILD":True})

if not CHILD:
    execfile(__file__, pure_evil)
    sys.exit()
<TOGGLEPYTHON>
Here, we define a surrogate namespace (aptly called "pure_evil").  We also inject the variable <code>CHILD</code> whose value is <code>True</code> for when we re-execute this file.

But most importantly, if our process is not the child process, we execute this file again... <em>with our devilish global namespace instead of the default one!</em>

This is possible because <code>execfile</code> takes optional global/local namespaces, and all they need to do is be duck-typed like a dictionary!  Easily done by our <code>Fauxcals</code> class.

And now, for the <del>disgusting repercussions</del> cool results:
<TOGGLEPYTHON>
# code will only proceed past here if child...

x = 5
y = -3

while x_is_greater_than_y:
    print x
    x -= 1

if x_is_identical_to_y:
    print "they're the same now!"

print type(globals())
<TOGGLEPYTHON>
Running the above program yields:
<pre>I am NOT the child.
I am the child.
5
4
3
2
1
0
-1
-2
they're the same now!
&lt;class '__main__.Fauxcals'&gt;</pre>

Now, you don't even have to call <code>c('...')</code> like you did in the first post.

Now you can <em>just write your code</em> and our Lovecraftian bastard-of-a-namespace will create your tools purely when you ask for them.

<del>Despicable.</del>  Intuitive!

<h2>Bad Ideas...</h2>

If one even thinks for a few moments about it, this nightmarish concept of injecting a totally custom namespace class into a program allows lots of interesting things, like:
<ul>
- Always creating variables when asked.  Yay, no more NameErrors!
- <em>Usually</em> creating variables when asked.  Yay, no repeatability of bugs!
- Internet-linked lookups for variables.  Maybe "five" maps to 5 because a Google search said so?  Maybe strings are translated to other languages?
- A <a href="http://gkoberger.github.io/stacksort/">stacksort</a>-like implementation, where missing functions are searched for online and used?
- Keeping a history of variable mappings.  Maybe you want to "revert" a variable's value?  ... Hmm, actually...  (post pending)
</ul>