#! /usr/bin/python

# This python implementation is way too slow. It takes about 4 hours to compute
# the solution. The replica implementation in C++ is much faster.

# In this assignment you will implement one or more algorithms for the all-pairs
# shortest-path problem. Here are data files describing three graphs: graph #1;
# graph #2; graph #3.
#
# The first line indicates the number of vertices and edges, respectively. Each
# subsequent line describes an edge (the first two numbers are its tail and
# head, respectively) and its length (the third number).
# NOTE: some of the edge lengths are negative.
# NOTE: These graphs may or may not have negative-cost cycles.
# 
# Your task is to compute the "shortest shortest path". Precisely, you must
# first identify which, if any, of the three graphs have no negative cycles. For
# each such graph, you should compute all-pairs shortest paths and remember the
# smallest one (i.e., compute min u,v d(u,v), where d(u,v) denotes the
# shortest-path distance from u to v).
# 
# If each of the three graphs has a negative-cost cycle, then enter "NULL" in
# the box below. If exactly one graph has no negative-cost cycles, then enter
# the length of its shortest shortest path in the box below. If two or more of
# the graphs have no negative-cost cycles, then enter the smallest of the
# lengths of their shortest shortest paths in the box below.
# 
# OPTIONAL: You can use whatever algorithm you like to solve this question. If
# you have extra time, try comparing the performance of different all-pairs
# shortest-path algorithms!

from numpy import empty, iinfo, add, transpose, matrix
import time

INFINITY = iinfo(int).max

def main():
    floyd_warshall('g1.txt')
    floyd_warshall('g2.txt')
    floyd_warshall('g3.txt')

def check_cycle(A, n, n_index):
    negative_cycle = False
    for i in range(1, n + 1):
        if A[i][i][n_index] < 0:
            print i, A[i][i][n_index]
            negative_cycle = True
            break
    return negative_cycle

def floyd_warshall(filename):
    f = open(filename, 'r')
    n, m = map(int, f.readline().strip().split(' '))
    print n, m
    #G = empty((n, n), int)
    #G.fill(INFINITY)
    G = {}
    while True:
        line = f.readline().strip()
        if not line:
            break
        src, dst, cost = map(int, line.split(' '))
        #G[src - 1][dst - 1] = cost
        G[(src, dst)] = cost
    f.close()
    print 'allocating 3d array'
    A = empty((n + 1, n + 1, 2), int)
    print 'allocated 3d array'
    # base case
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j:
                A[i][j][0] = 0
            elif (i, j) in G:
                A[i][j][0] = G[(i, j)]
            else:
                A[i][j][0] = INFINITY
    print 'done with base cases'
    # floyd warshall's loop
    for k in range(1, n + 1):
        if k % 100 == 1:
            print k
        start = time.time()
        curr_k = k % 2
        prev_k = (k - 1) % 2
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                # use prev_k for k - 1 and curr_k for k
                # prevent overflows
                if A[i][k][prev_k] == INFINITY or A[k][j][prev_k] == INFINITY:
                    A[i][j][curr_k] = A[i][j][prev_k]
                else:
                    A[i][j][curr_k] = min(
                            A[i][j][prev_k], # case 1 - doesn't include vertex vk.
                            A[i][k][prev_k] + A[k][j][prev_k]) # case 2 - includes vk.
        if check_cycle(A, n, curr_k):
            break
        print 'took ', (time.time() - start), ' seconds'
    # see if the graph has a negative length cycle
    negative_cycle = check_cycle(A, n, curr_k)
    print "negative_cycle: ", negative_cycle
    # compute the shortest shortest path if there are no negative cycles
    if not negative_cycle:
        shortest = INFINITY
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                shortest = min(shortest, A[i][j][curr_k])
        print "shortest: :", shortest
    print 'done :)'
if __name__ == "__main__":
    main()
