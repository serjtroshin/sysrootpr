import numpy as np
import pickle
from notes1 import *
def n(a, b):
    x = 2 * a.dot(b)
    if x % b.dot(b) != 0:
        raise Exception("Not Z-div")
    else:
        return x // b.dot(b)

def kartan(Rs):
    kart = np.zeros((len(Rs), len(Rs)), np.int)
    for i in range(len(Rs)):
        for j in range(len(Rs)):
            kart[i,j] = n(Rs[i], Rs[j])
    return kart

a = np.array((0, 2, -2, 0))
b = np.array((0, 0, 2, -2))
c = np.array((0, 0, 0, 2))
d = np.array((1, -1, -1, -1))
f4_sr = np.array(([a, b, c, d]), dtype=np.int)
print("kartan matrix\n", kartan([a, b, c, d]))


# найдем фундаментальные веса
weights = np.array([
    [2, 3, 4, 2],
    [3, 6, 8, 4],
    [2, 4, 6, 3],
    [1, 2, 3, 2]])
fundamental_vectors = weights.dot(f4_sr)
print("fundamental vectors\n", fundamental_vectors)
fundamental_weights = np.array(
[(2, 2, 0, 0),
 (4, 2, 2, 0),
 (3, 1, 1, 1),
 (2, 0, 0, 0)], dtype=np.int
)

#print(f4_sr.dot(fundamental_weights.T))


def reflection(v, root):
    return v - n(v, root) * root



def spread(simple_roots, base):
    # spread base vectors with Veil group (simple_roots)
    s = set()
    S = []
    deque = list(base)
    it = 0
    while (it < len(deque)):
        elem = deque[it]
        it += 1
        for sroot in simple_roots:
            next = reflection(elem, sroot)
            if not str(list(next)) in s:
                s.add(str(list(next)))
                S.append(next)
                deque.append(next)
    return S
s = list(spread(f4_sr, fundamental_weights))
print("|S| =", len(s))

# test (orbits)
lW = 2**7 * 3**2
print("F4 Weil group:", lW)
for weight in fundamental_weights:
    orb = len(spread(f4_sr, [weight]))
    print(orb)
    assert lW % orb == 0

sub = []
print("-------------")
mt = np.array([s[0], s[1], s[2], s[3]], np.int32)
print(mt)
print("Гаусс:", gauss(mt))
print("ФСР:", fundsys(mt))

print("Независимость:", is_full_rank(mt))


print("\n\n\n\nперебор")
vectors = []
ans = []
ans_set = set()
full = 3

found = 0
visited = 0
COUNTER = 0

out = open("out.txt", "w")
def write(v, out):
    s = ",".join(map(str, list(v))) + '\n'
    out.write(s)
    out.write(",".join(map(str, list(-v))) + '\n')

def f(vectors, cur, full):
    global found, s, visited
    visited += 1
    if (len(vectors) == full):
        found += 1
        if (found % 100 == 0):
            print(found, visited, COUNTER)
        v = fundsys(np.array(vectors))[0]
        write(v, out)
        return
    while cur < len(s):
        vectors.append(s[cur])
        #print("TASK")
        #print(np.array(vectors))
        try:
            if not is_full_rank(np.array(vectors)):
                vectors.pop()
            else:
                f(vectors, cur + 1, full)
                vectors.pop()
        except Exception:
            print(vectors)
            exit(1)
        cur += 1
f(vectors, 0, 3)
print("calculated")
out.close()






