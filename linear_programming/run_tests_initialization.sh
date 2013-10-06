#! /bin/bash

bin=../../initialization.py
OUTPUT=../../initialization_output
OLDPWD=`pwd`

cd initializationTests/assignmentTests
rm -rf ${OUTPUT}
mkdir -p ${OUTPUT}

for i in {1..6}
do
	${bin} "part${i}.dict" > "${OUTPUT}/part${i}.txt"
done

cd "${OLDPWD}"

echo "all done :)"