#! /usr/bin/python

import sys
from operator import add

def merge(a, b):
	""" takes  an integer and a list and merges them to a single list """
	retval = [a]
	retval.extend(b)
	return retval

def sort_dictionary(d, basic, non_basic):
	# not pythonic, but still
	# sort by non basic variables
	for i in range(len(non_basic)):
		for j in range(i):
			if non_basic[i] < non_basic[j]:
				non_basic[i], non_basic[j] = non_basic[j], non_basic[i]
				for k in range(len(d)):
					d[k][i + 1], d[k][j + 1] = d[k][j + 1], d[k][i + 1]
	# sort by basic variables
	for i in range(len(basic)):
		for j in range(i):
			if basic[i] < basic[j]:
				basic[i], basic[j] = basic[j], basic[i]
				d[i], d[j] = d[j], d[i]

def main():
	if len(sys.argv) != 2:
		print "Usage: %s <dict_file>" % sys.argv[0]
		sys.exit(0)
	# read values from the file
	lines = tuple(open(sys.argv[1]))
	k = 0
	m, n = map(int, filter(None, lines[k].strip().split(" ")))
	k += 1
	basic = map(int, filter(None, lines[k].strip().split(" ")))
	k += 1
	non_basic = map(int, filter(None, lines[k].strip().split(" ")))
	k += 1
	basic_values = map(float, filter(None, lines[k].strip().split(" ")))
	k += 1
	co_efficients = []
	for i in range(m):
		co_efficients.append(map(float, filter(None, lines[k].strip().split(" "))))
		k += 1
	last_row = map(float, filter(None, lines[k].strip().split(" ")))

	d = [] # dictionary variable

	# construct the dictionary
	for i in range(m + 1):
		d.append(merge(basic_values[i], co_efficients[i]) if i != m else last_row)

	# sort the dictionary by columns to make sure we select the smallest indexed
	# variable as entering variable in case of multiple possibilities
	sort_dictionary(d, basic, non_basic)

	# find the entering variable
	entering_variable = -1
	for i in range(1, n + 1):
		if d[m][i] > 0:
			entering_variable = i
			break
	else:
		print "final dictionary already"

	# find the leaving variable for chosen entering variable
	leaving_variable = -1
	zero_factor = ([], [])
	for i in range(m):
		if d[i][entering_variable] < 0:
			zero_factor[0].append(-1.0 * (d[i][0] / d[i][entering_variable]))
			zero_factor[1].append(i)

	if len(zero_factor[0]) == 0:
		print "UNBOUNDED"
		sys.exit(0)

	min_index = zero_factor[0].index(min(zero_factor[0]))
	leaving_variable = zero_factor[1][min_index]

	# row operations to get the new dictionary
	# first compute the leaving variable's row
	for i in range(n + 1):
		if i != entering_variable:
			# divide by the entering variable's co-efficient
			d[leaving_variable][i] /= -1 * d[leaving_variable][entering_variable]
		else:
			# always -1
			d[leaving_variable][i] = -1
	# compute all the other rows
	for i in range(m + 1):
		if i != leaving_variable:
			co_efficient = d[i][entering_variable]
			# current row with entering variable set to 0
			r1 = [d[i][j] if j != entering_variable else 0 for j in range(n + 1)]
			# new co-efficients to be added with r1
			r2 = [co_efficient * d[leaving_variable][j] for j in range(n + 1)]
			for j, value in enumerate(map(add, r1, r2)):
				d[i][j] = value

	print non_basic[entering_variable - 1]
	print basic[leaving_variable]
	print round(d[m][0], 4)

if __name__ == "__main__":
	main()