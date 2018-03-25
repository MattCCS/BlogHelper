# 1
L = [1,2,3]

for i in L:
    print i


# 2
with open("lines.txt","r") as f:
    lines = f.readlines()

for l in lines:
    print l


# 3
s = "hello!"

for c in s:
    print c


# 4
with open("lines.txt","r") as f:
    for each_line in f:
        print each_line