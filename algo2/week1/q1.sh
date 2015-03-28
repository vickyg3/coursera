#! /bin/bash

# In this programming problem and the next you'll code up the greedy algorithms
# from lecture for minimizing the weighted sum of completion times.. Download
# the # text file here. This file describes a set of jobs with positive and
# integral weights and lengths. It has the format
# [number_of_jobs]
# [job_1_weight] [job_1_length]
# [job_2_weight] [job_2_length]
# ...
# For example, the third line of the file is "74 59", indicating that the second
#   job has weight 74 and length 59. You should NOT assume that edge weights or
#   lengths are distinct.
#
#   Your task in this problem is to run the greedy algorithm that schedules jobs
#   in decreasing order of the difference (weight - length). Recall from lecture
#   that this algorithm is not always optimal. IMPORTANT: if two jobs have equal
#   difference (weight - length), you should schedule the job with higher weight
#   first. Beware: if you break ties in a different way, you are likely to get
#   the wrong answer. You should report the sum of weighted completion times of
#   the resulting schedule --- a positive integer --- in the box below.
#
#   ADVICE: If you get the wrong answer, try out some small test cases to debug
#   your algorithm (and post your test cases to the discussion forum)!

cat jobs.txt | \
  # first line is the number of entries. can be ignored.
  sed '1d' | \
  # print weight-length as 3rd column.
  awk '{ print $1,$2,$1-$2 }' | \
  # sort by the 3rd column, breaking ties with the weight (column #1).
  sort -k3 -k1 -rn | \
  # compute the weighted length.
  awk '{ l+=$2; sum+=l*$1; } END { printf("%.20G\n", sum) }'
