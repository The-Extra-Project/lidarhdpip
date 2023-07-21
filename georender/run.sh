#!/bin/sh
## parameters are the function call with the parameter:

params = []

## iterates over the command like input , stores it into the params array.
for i in "$@"
do
    echo $i
    params[${i}]=$i
done

python3 georender.py "${params[@]}"
