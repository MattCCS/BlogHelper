Ever wished you could use C-style pointers in Python?  Of course not!  But just for kicks, we will implement them anyways.

Below, we define a class <strong>Pointer</strong>:
<!--more-->
<TOGGLEPYTHON>
class Pointer:
    def __init__(self, deref):
        self.deref = deref
    def __neg__(self):
        return self.deref
<TOGGLEPYTHON>

When instantiated, our <strong>Pointer</strong> will be passed the object that it should point to, which it will save as <code>deref</code>.  Notice that this class also implements the <code>__neg__()</code> method, which is a built-in, <strong>special method</strong>, called by using the unary "negative" operator <code>(-)</code>.  Calling this will essentially de-reference our <strong>Pointer</strong>, returning the object it points to.

(The unary "positive" operator will likewise be later used as the equivalent C/C++ reference operator... i.e., in our code, <strong>+ is to - as &amp; is to *</strong>.)

See below our <strong>Pointed</strong> class:

<TOGGLEPYTHON>
class Pointed:
    def __init__(self, obj):
        self.obj = obj
        self.ref = Pointer(self)
    def __pos__(self):
        return self.ref

    def __neg__(self):
        return self.obj
<TOGGLEPYTHON>

It is similar to -- but slightly more involved than -- our <strong>Pointer</strong> class.  Like our first class, it too is passed an object upon instantiation, which it saves.  <em>However</em>, when instantiated, our <strong>Pointed</strong> class also creates a <strong>Pointer</strong> to itself (<em>passing ITSELF, a Pointed, as the 'deref' to the Pointer it creates!</em>).  This will all be more explained in time.  Note that the user will not be expected to actually instantiate from this class manually -- this will be done with a cute little function.

Note also that we also implement the <code>__pos__()</code> and <code>__neg__()</code> magic methods, representing the <strong>reference</strong> and <strong>de-reference</strong> operators, respectively.  Their return statements confirm this.

Finally, our cute little public function <code>new()</code>:

<TOGGLEPYTHON>
def new(obj):
    return +Pointed(obj)
<TOGGLEPYTHON>

As you can see, <code>new()</code> actually takes an object, makes it into a <strong>Pointed</strong> object -- which implicitly creates a <strong>Pointer</strong> to itself -- and then <em>returns that implicitly-created Pointer</em> using our <code>(+)</code> "reference operator", just as a call to the C/C++ built-in function <code>new</code> would (effectively) do!  Ta-da!

Now for some tests.  These calls:

<TOGGLEPYTHON>
p_hi = new("Hello") # gives us a "Pointer" to the "Pointed" string
print p_hi
print -p_hi # dereference
print +-p_hi # dereference and re-reference (the original Pointer)
print --p_hi # double-dereference (gets the "true" object)
<TOGGLEPYTHON>

... print something along these lines:

<TOGGLEOUT>
<__main__.Pointer instance at 0x10a727710>
<__main__.Pointed instance at 0x10a727638>
<__main__.Pointer instance at 0x10a727710>
Hello
<TOGGLEOUT>

As they should!  Success!

<em>(Note: Yes, double-dereferencing a C-pointer isn't valid, but since we are essentially wrapping the "true" object in the Pointed class, we must if we want to get access to it.  This is certainly not a *good* solution, but it sure is a simple one!)</em>