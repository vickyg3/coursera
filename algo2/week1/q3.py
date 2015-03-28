#! /usr/bin/python

# In this programming problem you'll code up Prim's minimum spanning tree
# algorithm. Download the text file here. This file describes an undirected
# graph with integer edge costs. It has the format
# [number_of_nodes] [number_of_edges]
# [one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
# [one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
# ...
#
# For example, the third line of the file is "2 3 -8874", indicating that there
# is an edge connecting vertex #2 and vertex #3 that has cost -8874. You should
# NOT assume that edge costs are positive, nor should you assume that they are
# distinct.
#
# Your task is to run Prim's minimum spanning tree algorithm on this graph. You
# should report the overall cost of a minimum spanning tree --- an integer,
# which may or may not be negative --- in the box below.
#
# IMPLEMENTATION NOTES: This graph is small enough that the straightforward
# O(mn) time implementation of Prim's algorithm should work fine. OPTIONAL: For
# those of you seeking an additional challenge, try implementing a heap-based
# version. The simpler approach, which should already give you a healthy
# speed-up, is to maintain relevant edges in a heap (with keys = edge costs).
# The superior approach stores the unprocessed vertices in the heap, as
# described in lecture.Note this requires a heap that supports deletions, and
# you'll probably need to maintain some kind of mapping between vertices and
# their positions in the heap.

f = open('edges.txt', 'r')
n, m = map(int, f.readline().strip().split(' '))
edges = []
vertices = []
i = 0
while i < m:
    u, v, w = map(int, f.readline().strip().split(' '))
    edges.append((u, v, w))
    edges.append((v, u, w))
    vertices.append(u)
    vertices.append(v)
    i += 1
vertices = list(set(vertices))
X = [vertices[0]]
del vertices[0]
mst_cost = 0
while vertices:
    frontier_edges = [t for t in edges if t[0] in X and t[1] not in X]
    min_frontier_edge_index = \
        list(zip(*frontier_edges)[2]).index(map(min, zip(*frontier_edges))[2])
    min_frontier_edge = frontier_edges[min_frontier_edge_index]
    mst_cost += min_frontier_edge[2]
    X.append(min_frontier_edge[1])
    del vertices[vertices.index(X[-1])]
print "min cost: ", mst_cost
