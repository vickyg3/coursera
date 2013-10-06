#! /bin/bash

bin=../../pivot2.py
OUTPUT=../../pivot2_output
OLDPWD=`pwd`

cd part2TestCases/assignmentParts
rm -rf ${OUTPUT}
mkdir -p ${OUTPUT}

for i in {1..5}
do
	${bin} "part${i}.dict" > "${OUTPUT}/part${i}.txt"
done

cd "${OLDPWD}"

echo "all done :)"