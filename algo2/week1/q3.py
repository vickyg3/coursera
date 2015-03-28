#! /usr/bin/python

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
