#! /bin/bash

# For this problem, use the same data set as in the previous problem. Your task
# now is to run the greedy algorithm that schedules jobs (optimally) in
# decreasing order of the ratio (weight/length). In this algorithm, it does not
# matter how you break ties. You should report the sum of weighted completion
# times of the resulting schedule --- a positive integer --- in the box below.

cat jobs.txt | \
  # first line is the number of entries. can be ignored.
  sed '1d' | \
  # print the weight/length ratio as 3rd column.
  awk '{ print $1,$2,$1/$2 }' | \
  # sort by the 3rd column, breaking ties with the weight (column #1).
  sort -k3 -k1 -rn | \
  # compute the optimal weighted length.
  awk '{ l+=$2; sum+=l*$1; } END { printf("%.20G\n", sum) }'
