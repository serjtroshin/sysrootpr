from itertools import permutations
import numpy as np
a = np.array((1, -1, 0, 0))
b = np.array((0, 1, -1, 0))
c = np.array((0, 0, 1, -1))
d = np.array((0, 0, 0, 2))

def n(a, b):
    return 2.0 * a.dot(b) / b.dot(b)

def kartan(Rs):
    kart = np.zeros((len(Rs), len(Rs)), np.float32)
    for i in range(len(Rs)):
        for j in range(len(Rs)):
            kart[i,j] = n(Rs[i], Rs[j])
    return kart

print(kartan([a, b, c, d]))

s = set()
for i in range(-2, 3):
    for j in range(-2, 3):
        for k in range(-2, 3):
            for z in range(-2, 3):
                s.add((i, j, k, z))

print(len(s))
F4 = np.array([
    [2., -1., 0., 0.],
    [-1., 2., 2., 0.],
    [0., -1., 2., -1.],
    [0., 0., -1., 2.]]
)
for a1 in [a]:
    for b1 in [a]:
        for c1 in s:
            for d1 in s:
                if np.sum((kartan(tuple(map(np.array, (a1, b1, c1, d1)))) - F4)**2) < 0.000000001:
                    print(a1, b1, c1, d1)
                    exit(0)

"""



def f(mx = 2):
    for i in range(-mx, mx):
        for j in range(-mx, mx):
            for k in range(-mx, mx):
                for z in range(-mx, mx):
                    yield (i, j, k, z)

def check(a, b, c, d):

def n(a, b):
    return 2 * a.dot(b) // b.dot(b)
for c1 in f():
    c = np.array(c1)
    if (c.dot(a)) != 0:
        continue
    if not(n(b, c) == -2 and n(c, b) == -1):
        continue
    for d1 in f():

        d  = np.array(d1)
        if check(a, b, c, d):
            print(a, b, c, d)
            exit(0)


"""