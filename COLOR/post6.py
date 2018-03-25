To celebrate Pi Day, I've written up a couple of algorithms to approximate Pi.  It's interesting to see how fast/slow the different algorithms approximate Pi.

Each algorithms links to its mathematical equivalent on Wikipedia.
<!--more-->

<h3>Bailey-Borwein-Plouffe</h3>

<TOGGLEPYTHON>
####################################
# Bailey-Borwein-Plouffe algorithm
# http://en.wikipedia.org/wiki/Approximations_of_%CF%80#Digit_extraction_methods
# (first example)

def bbp_inner(k):
    return (1.0 / (16 ** k)) * ((4.0 / (8*k + 1)) - (2.0 / (8*k + 4)) - (1.0 / (8*k + 5)) - (1.0 / (8*k + 6)))

def bbp(n):
    return sum(bbp_inner(k) for k in xrange(n))

print bbp(256) # max before OverflowError
<TOGGLEPYTHON>

<h3>Simon Plouffe</h3>

<TOGGLEPYTHON>
####################################
# Simon Plouffe's algorithm
# http://en.wikipedia.org/wiki/Approximations_of_%CF%80#Digit_extraction_methods
# (second example)

# a parallel to sum()
def prod(L):
    p = 1
    for i in L:
        p *= i
    return p

# instead of the builtin math.factorial, let's make our own!
def fact(n):
    return prod(n for n in xrange(1, n+1))

def sp_inner(n):
    return (n * (2 ** n) * (fact(n) ** 2)) / float((fact (2 * n)))

def sp(n):
    return sum(sp_inner(i) for i in xrange(1, n)) - 3

print sp(86) # max before fact() causes an OverflowError
<TOGGLEPYTHON>

<h3>Continued Fractions</h3>

<TOGGLEPYTHON>
####################################
# Continued Fractions
# http://en.wikipedia.org/wiki/Approximations_of_%CF%80#Continued_fractions

def fraction_approx(iterations, i=1):
    if iterations == 0:
        return 0
    else:
        return i**2 / float((6 + fraction_approx(iterations - 1, i + 2)))

def cf(iterations):
    return 3 + fraction_approx(iterations)

print cf(997) # max before reaching max recursion depth and causing a RuntimeError
<TOGGLEPYTHON>

<h3>Last But Not Least...</h3>

<TOGGLEPYTHON>
####################################
# And of course, the most Pythonic way...

import math
print math.pi
<TOGGLEPYTHON>