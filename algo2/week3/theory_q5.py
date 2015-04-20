#! /usr/bin/python

# Consider an instance of the optimal binary search tree problem with 7 keys
# (say 1,2,3,4,5,6,7 in sorted order) and frequencies 
# w1=.05,w2=.4,w3=.08,w4=.04,w5=.1,w6=.1,w7=.23.
# What is the minimum-possible average search time of a binary search tree
# with these keys?

def main():
	w = [0.05, 0.4, 0.08, 0.04, 0.1, 0.1, 0.23]
	n = len(w)
	A = [[0 for x in range(n)] for i in range(n)]
	for s in range(n): # s represents j - i
		for i in range(n - s): # now, j = i + s
			j = i + s
			sum_wk = 0
			for k in range(i, j + 1):
				sum_wk += w[k]
			candidate_roots = []
			for r in range(i, j + 1):
				try:
					t1 = A[i][r - 1]
				except:
					t1 = 0 # if index is out of bound
				try:
					t2 = A[r + 1][j]
				except:
					t2 = 0 # if index is out of bound
				candidate_roots.append(sum_wk + t1 + t2)
			A[i][j] = min(candidate_roots)
	print A[0][n - 1]
	print "done :)"

if __name__ == "__main__":
	main()