#! /usr/bin/python

# In this programming problem and the next you'll code up the knapsack algorithm
# from lecture. Let's start with a warm-up. Download the text file here. This
# file describes a knapsack instance, and it has the following format:
#     [knapsack_size][number_of_items]
#     [value_1] [weight_1]
#     [value_2] [weight_2]
#     ...
# For example, the third line of the file is "50074 659", indicating that the
# second item has value 50074 and size 659, respectively.
# You can assume that all numbers are positive. You should assume that item
# weights and the knapsack capacity are integers.

def main():
    f = open('knapsack1.txt', 'r')
    size, n = map(int, f.readline().strip().split(' '))
    w = [-1] # ignore the 0'th index in w and v
    v = [-1]
    while True:
        line = f.readline().strip()
        if not line:
            break
        v.append(int(line.split(' ')[0]))
        w.append(int(line.split(' ')[1]))
    A = [[0 for x in range(size + 1)] for i in range(n + 1)] 
    for i in range(1, n + 1):
        for x in range(size + 1):
            if x - w[i] < 0:
                A[i][x] = A[i - 1][x]
            else:
                A[i][x] = max(A[i - 1][x], A[i - 1][x - w[i]] + v[i])
    f.close()
    print A[n][size]
    print 'done :)'

if __name__ == "__main__":
    main()
