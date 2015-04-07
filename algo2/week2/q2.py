#! /usr/bin/python

# In this question your task is again to run the clustering algorithm from
# lecture, but on a MUCH bigger graph. So big, in fact, that the distances
# (i.e., edge costs) are only defined implicitly, rather than being provided as
# an explicit list. The data set is here. The format is:
# [# of nodes] [# of bits for each node's label]
# [first bit of node 1] ... [last bit of node 1]
# [first bit of node 2] ... [last bit of node 2]
# ...
# For example, the third line of the file:
# "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1" denotes the 24 bits
# associated with node #2.
# 
# The distance between two nodes u and v in this problem is defined as the
# Hamming distance--- the number of differing bits --- between the two nodes'
# labels. For example, the Hamming distance between the 24-bit label of node #2
# above and the label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is 3
# (since they differ in the 3rd, 7th, and 21st bits).
# 
# The question is: what is the largest value of k such that there is a
# k-clustering with spacing at least 3? That is, how many clusters are needed to
# ensure that no pair of nodes with all but 2 bits in common get split into
# different clusters?
# 
# NOTE: The graph implicitly defined by the data file is so big that you
# probably can't write it out explicitly, let alone sort the edges by cost. So
# you will have to be a little creative to complete this part of the question.
# For example, is there some way you can identify the smallest distances without
# explicitly looking at every pair of nodes?

leaders = {}

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
    f = open("clustering_big.txt", "r")
    num_nodes, num_bits = map(int, f.readline().strip().split(' '))
    print num_nodes, num_bits
    nodes = []
    count = 0
    while True:
        line = f.readline().strip().replace(' ', '')
        if not line:
            break
        nodes.append(int(line, 2))
        count += 1
    nodes = set(nodes)
    print len(nodes)
    # initialize the leaders for each vertex.
    # tuples of the form (leader, size of group)
    for node in nodes:
        leaders[node] = [node, 1] # initially each vertex is its own leader.
    # generate all possible numbers that could result in hamming distance 1
    hds = []
    for i in range(num_bits):
        hds.append(1 << i)
    # generate all possible numbers that could result in hamming distance 2
    for i in range(num_bits):
        for j in range(i + 1, num_bits):
            hds.append(1 << i | 1 << j)
    print len(hds)
    k = len(nodes)
    count = 0
    for hd in hds:
        if count % 100 == 0:
            print "iteration: %(count)d" % locals()
        for node in nodes:
            p = node
            q = node ^ hd
            # if xor result is in the set and they are not in the same cluster,
            # then merge them into a single cluster
            if q in nodes:
                pl = find(p)
                ql = find(q)
                if pl[0] != ql[0]:
                    old_leader = find(ql[0]) if pl[1] > ql[1] else find(pl[0])
                    new_leader = find(pl[0]) if pl[1] > ql[1] else find(ql[0])
                    union(old_leader, new_leader)
                    k -= 1
        count += 1
    print count
    print k
    f.close()

if __name__ == "__main__":
    main()
