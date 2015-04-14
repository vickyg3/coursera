#! /usr/bin/python

# This problem also asks you to solve a knapsack instance, but a much bigger
# one. Download the text file here. This file describes a knapsack instance, and
# it has the following format:
#     [knapsack_size][number_of_items]
#     [value_1] [weight_1]
#     [value_2] [weight_2]
#     ...
# For example, the third line of the file is "50074 834558", indicating that
# the second item has value 50074 and size 834558, respectively. As before,
# you should assume that item weights and the knapsack capacity are integers.
# 
# This instance is so big that the straightforward iterative implemetation
# uses an infeasible amount of time and space. So you will have to be creative
# to compute an optimal solution. One idea is to go back to a recursive
# implementation, solving subproblems --- and, of course, caching the results
# to avoid redundant work --- only on an "as needed" basis. Also, be sure to
# think about appropriate data structures for storing and looking up solutions
# to subproblems.

import sys

sys.setrecursionlimit(50000)

# NOTE: this implementation takes about 3 minutes for the big dataset in my
# macbook air.

def compute(i, x, w, v, memo):
    if (i, x) not in memo: # compute only if we don't already have it
        if i == 0:
            # base case
            memo[(i, x)] = 0
        elif i == 1:
            # base case
            memo[(i, x)] = v[1] if w[1] <= x else 0
        else:
            # recursive case
            s1 = compute(i - 1, x, w, v, memo)
            s2 = (compute(i - 1, x - w[i], w, v, memo) + v[i]) if (x - w[i]) >= 0 else -1
            memo[(i, x)] = max(s1, s2)
    return memo[(i, x)]

def main():
    f = open('knapsack_big.txt', 'r')
    size, n = map(int, f.readline().strip().split(' '))
    w = [-1] # ignore the 0'th index in w and v
    v = [-1]
    while True:
        line = f.readline().strip()
        if not line:
            break
        v.append(int(line.split(' ')[0]))
        w.append(int(line.split(' ')[1]))
    memo = {}
    print compute(n, size, w, v, memo)
    print 'done :)'

if __name__ == "__main__":
    main()
