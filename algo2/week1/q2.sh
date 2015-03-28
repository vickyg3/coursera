#! /bin/bash

cat jobs.txt | \
  # first line is the number of entries. can be ignored.
  sed '1d' | \
  # print the weight/length ratio as 3rd column.
  awk '{ print $1,$2,$1/$2 }' | \
  # sort by the 3rd column, breaking ties with the weight (column #1).
  sort -k3 -k1 -rn | \
  # compute the optimal weighted length.
  awk '{ l+=$2; sum+=l*$1; } END { printf("%.20G\n", sum) }'
