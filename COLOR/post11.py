The quest to produce code that is both sensibly designed and easily readable is the eternal ambition of the programmer (one hopes).

Today I pursue that goal in the worst way possible.

<!--more-->

Consider the following constructs in Python:
<TOGGLEPYTHON>
while x <= y: ...
while n != 10: ...
while a is not b: ...
<TOGGLEPYTHON>
What obscure symbols are being used!  The "while" is perfectly readable, but "<=" is hardly proper English.  And what is "!=" even supposed to mean?  These symbols offer no intuition to the reader.

Wouldn't it be better if those statements read like this?...
<TOGGLEPYTHON>
while x_is_less_than_or_equal_to_y: ...
while n_is_not_equal_to_10: ...
while a_is_not_identical_to_b: ...
<TOGGLEPYTHON>

Of course it would.  Below, I humbly offer a way to address this obvious oversight present in most "mainstream" langauges.

<TOGGLEPYTHON>
def c(s):

    class Evaluable:

        def __init__(self, a, b, op):
            self.a = a if not a.isdigit() else int(a)
            self.b = b if not b.isdigit() else int(b)
            self.op = op

        def coerce_if_live(self, o):
            return o if not (type(o) == str) else globals()[o]

        def __nonzero__(self):
            a = self.coerce_if_live(self.a)
            b = self.coerce_if_live(self.b)

            return self.op(a,b)

    import re

    title_regex = r"^(?P<a>[^_]+)(?P<op>(_[^_]+)+_)(?P<b>[^_]+)$"

    M = re.match(title_regex, s)
    if not M:
        raise SyntaxError

    # because screw the "operator" module, that's why.
    D = {
        "_is_less_than_" :   lambda a,b: a < b,
        "_is_greater_than_": lambda a,b: a > b,
        "_is_less_than_or_equal_to_":    lambda a,b: a <= b,
        "_is_greater_than_or_equal_to_": lambda a,b: a >= b,
        "_is_equal_to_": lambda a,b: a == b,
        "_is_not_equal_to_": lambda a,b: a != b,
        "_is_identical_to_": lambda a,b: a is b,
        "_is_not_identical_to_": lambda a,b: a is not b,
    }

    M_D = M.groupdict()

    a  = M_D['a']
    b  = M_D['b']
    op = D[M_D['op']]

    E = Evaluable(a, b, op)

    globals()[s] = E

    return E # feel free to use this, or the global one

<TOGGLEPYTHON>
What the above code does is <del>diabolical</del> perfectly straightforward and desirable:  the function c takes a string as input (which should match one of the acceptible conditional patterns) and dynamically creates an "evaluate-able" object that is added to the global namespace with the name provided.

For example, a call to <code>c("a_is_less_than_b")</code> creates a global object <code>a_is_less_than_b</code> that can be invoked later to check the eponymous condition.  This is possible because the "Evaluable" class implements a custom __nonzero__ method which performs dynamic lookups every time it is called.

Using the above system, code such as this becomes possible:
<TOGGLEPYTHON>

c("x_is_less_than_or_equal_to_y")

x = 2
y = 7

while x_is_less_than_or_equal_to_y:
    print x
    x += 1
<TOGGLEPYTHON>
And our output, as any native English speaker could easily tell us, is
<TOGGLEPYTHON>
2
3
4
5
6
7
<TOGGLEPYTHON>
And imagine, such a system even allows header-file-like coding conventions in Python code, in which all future conditionals are listed conveniently at the top of the program -- or even in another file!  A godsend, to be sure.

As an act of <del>sadism</del> charity, I am more than happy to release this code into the public domain.  Please feel free to use it in all of your future Python projects;  I'm sure your coworkers will appreciate your code's newfound readability.