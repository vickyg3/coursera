#! /usr/bin/python

# In this programming problem and the next you'll code up the clustering
# algorithm from lecture for computing a max-spacing k-clustering. Download the
# text file here. This file describes a distance function (equivalently, a
# complete graph with edge costs). It has the following format:
# [number_of_nodes]
# [edge 1 node 1] [edge 1 node 2] [edge 1 cost]
# [edge 2 node 1] [edge 2 node 2] [edge 2 cost]
# ...
# There is one edge (i,j) for each choice of 1<=i<j<=n, where n is the number of
# nodes. For example, the third line of the file is "1 3 5250", indicating that
# the distance between nodes 1 and 3 (equivalently, the cost of the edge (1,3))
# is 5250. You can assume that distances are positive, but you should NOT assume
# that they are distinct.
# 
# Your task in this problem is to run the clustering algorithm from lecture on
# this data set, where the target number k of clusters is set to 4. What is the
# maximum spacing of a 4-clustering?
# 
# ADVICE: If you're not getting the correct answer, try debugging your algorithm
# using some small test cases. And then post them to the discussion forum!
#
# Maximum spacing is defined as the minimum distance between two points that are
# in different clusters after k-clustering (i.e.) it is the candidate for the
# k+1th merge.

# This impements Union by path compression.

leaders = []

def find(i):
    global leaders
    li = i
    while leaders[li][0] != li:
        li = leaders[li][0]
    # path compression
    while leaders[i][0] != i:
        temp = leaders[i][0] # store current parent
        leaders[i][0] = li # set new parent (compression of path)
        i = leaders[temp][0] # traverse to old parent and continue
    return leaders[li]

def union(old_leader, new_leader):
    # increase the leader group size by 1
    new_leader[1] += old_leader[1]
    # lazy union
    old_leader[0] = new_leader[0]

def main():
    global leaders
    f = open("clustering1.txt", "r")
    num_nodes = int(f.readline().strip())
    k = 4
    print num_nodes
    distances = []
    count = 0
    # read the file and store the edge cost in sorted order.
    while True:
        line = f.readline().strip()
        if not line:
            break
        i, j, distance = map(int, line.split(' '))
        distances.append((i - 1, j - 1, distance))
        if count == -1:
            break
        count += 1
    distances = sorted(distances, key = lambda x: x[2])
    # initialize the leaders for each vertex.
    # tuples of the form (leader, size of group)
    for i in range(num_nodes):
        leaders.append([i, 1]) # initially each vertex is its own leader.
    # clustering loop
    num_clusters = num_nodes
    edge_index = 0 # index of the edge to look at next.
    spacing = 0
    while num_clusters != k - 1:
        while True:
            p, q, distance = distances[edge_index]
            edge_index += 1
            pl = find(p)
            ql = find(q)
            if pl[0] != ql[0]:
                break
        spacing = distance
        # merge the clusters containing p and q.
        old_leader = find(ql[0]) if pl[1] > ql[1] else find(pl[0])
        new_leader = find(pl[0]) if pl[1] > ql[1] else find(ql[0])
        union(old_leader, new_leader)
        num_clusters -= 1
    print spacing
    f.close()

if __name__ == "__main__":
    main()
