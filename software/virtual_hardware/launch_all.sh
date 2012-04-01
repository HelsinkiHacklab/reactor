#!/bin/bash -ex
for vh in $( find ./ -name '*.py' | grep -v '\._' )
do
    python $vh &
done
