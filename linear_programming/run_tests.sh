#! /bin/bash

bin=../../pivot1.py
OUTPUT=../../pivot1_output
OLDPWD=`pwd`
cd part1TestCases/unitTests/

# run unittests
for i in {1..10}
do
	diff -B <(${bin} "dict${i}") <(cat dict${i}.output) > /dev/null 2>&1 || echo "Failed for dict${i}"
done

rm -rf ${OUTPUT}
mkdir -p ${OUTPUT}

cd ../../part1TestCases/assignmentParts
for i in {1..5}
do
	${bin} "part${i}.dict" > "${OUTPUT}/part${i}.txt"
done

cd "${OLDPWD}"

echo "all done :)"