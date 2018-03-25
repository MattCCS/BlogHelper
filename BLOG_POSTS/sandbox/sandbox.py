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


Y = MyIterableClass("ABC")
L = [1,2,3]

myIter = iter(iter(iter(iter(iter(Y)))))
otherIter = iter(iter(iter(iter(iter(L)))))

for X in myIter:
    print X

for X in otherIter:
    print X