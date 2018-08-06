import numpy as np
import time

VERBOSE = False
def eucl(a, b):
    # return gcd(a, b), linear coeffs
    a0 = a
    b0 = b
    if b == 0:
        return 1, 0, 1
    d = a // b
    m = a % b
    c1 = np.array([0, 1])
    c2 = np.array([1, -d])
    a = b
    b = m
    while m != 0:
        d = a // b
        m = a % b
        c2_ = c2
        c2 = c1 - d * c2
        c1 = c2_
        a = b
        b = m
    #print(a,"=",a0,"*",c1[0],"+",b0,"*",c1[1])
    #print(a0 * c1[0] + b0 * c1[1])
    return c1[0], c1[1], a

#print("eucl", eucl(2, 3))

def gcd(ar):
    if (len(ar) == 1):
        return [1], ar[0]
    linear_coeffs = [0] * len(ar)
    linear = [[0,0] for i in range(len(ar) - 1)] # for each pair
    prev = ar[0]
    for i in range(len(ar) - 1):
        linear[i][0], linear[i][1], nd = eucl(prev, ar[i+1])
        prev = nd
    #print(linear)
    nd = prev
    m = 1
    for i in range(len(ar) - 2, -1, -1):
        linear_coeffs[i + 1] = m * linear[i][1]
        if (i != 0):
            m *= linear[i][0]
    linear_coeffs[0] = m * linear[0][0]
    #print(linear_coeffs)
    #print("ar=",ar)
    #print("gcd =", nd)
    #print(sum([i * j for i,j in zip(ar, linear_coeffs)]))
    return linear_coeffs, nd

print(gcd([2, 3, 3]))

def lcd(a, b):
    return a * b // gcd([a, b])[-1]
def gauss(mt, zero_bellow_main=True, verbose=VERBOSE):

    #takes matrix
    #returns gaussian enhanced form of matrix
    n = len(mt)
    m = len(mt[0])
    main_elements = []
    free_columns = []
    r = 0 # row
    for i in range(m):
        unders = []
        indexes = []
        for j in range(r, n):
            if (mt[j, i] != 0):
                unders.append(mt[j, i])
                indexes.append(j)
        if len(unders) == 0:
            free_columns.append(i)
            continue
        else:
            main_elements.append([r, i])
        linear, gcd_value = gcd(unders)
        if verbose:
            print("gcd, linear", gcd_value, linear)
        gcd_vector = np.zeros((m), np.int32)
        for ind, coef in zip(indexes, linear):
            gcd_vector += mt[ind] * coef
        if verbose:
            print("gcd_vector", gcd_vector)
        main_index = i
        for j in range(len(linear)):
            if (linear[j] != 0):
                main_index = indexes[j]
        mt[main_index] = gcd_vector
        mt[[r, main_index]], mt[[main_index, r]] = mt[[main_index, r]], mt[[r, main_index]]
        if verbose:
            print(mt)
        for j in range(r + 1, n):
            if (mt[j, i] != 0):
                d = mt[j, i] // gcd_value
                mt[j,:] -= d * gcd_vector
        if verbose:
            print(mt)
            print("MOVE")
        r += 1
    if zero_bellow_main:
        for main_elem in main_elements:
            i, j = main_elem
            lcd_ = mt[i, j]
            for k in range(i - 1, -1, -1):
                if (mt[k, j] != 0):
                    lcd_ = lcd(lcd_, mt[k, j])
            for k in range(i - 1, -1, -1):
                if (mt[k, j] != 0):
                    mt[k] *= lcd_ // mt[k, j]
            if verbose:
                print(mt)
            for k in range(i - 1, -1, -1):
                if (mt[k, j] != 0):
                    mt[k] -= mt[i] * (mt[k,j] // mt[i,j])
            if verbose:
                print(mt)
            if verbose:
                print("next")


    return mt, main_elements, free_columns

def is_full_rank(mt):
    mt, main, _ = gauss(mt, False, VERBOSE)
    return len(main) == len(mt)


mt = np.array(
    [
        [2,  0,  2,  0],
        [3,  1,  1,  1],
        [3,  1,  1, -1]
    ]
)
print(mt)
#print("result:")
#print(gauss(mt, True, True))


def fundsys(mt):
    mt, main_elements, free_columns = gauss(mt)
    #print("main_elems", main_elements)
    free_columns = set(free_columns)
    #print("free_columns", free_columns)
    n = len(mt)
    m = len(mt[0])
    main_col = dict()
    main_row = dict()
    for elem in main_elements:
        main_col[elem[1]] = elem[0]
        main_row[elem[0]] = elem[1]
    lcd_ = 1
    fund = []
    for col in range(m):
        if col in free_columns:
            new_vector = np.zeros((m,), np.int32)
            new_vector[col] = lcd_
            j = 0
            while j < len(main_elements) and main_elements[j][1] < col:
                new_vector[main_elements[j][1]] = -lcd_ // mt[main_elements[j][0], main_elements[j][1]] * mt[j, col]
                j += 1
            _, gcd_ = gcd(list(filter(lambda x: x!=0, list(new_vector))))
            new_vector //= gcd_
            fund.append(new_vector)
        else:
            lcd_ = lcd(lcd_, mt[main_col[col], col])
    return fund


