#!/bin/bash

# a 2D geographic position
echo "run the script with X=$1 Y=$2"

POS="$1 $2"

python /usr/src/app/georender/src/main.py $POS

## this will be done via the web3 storage.
LAS_NAME=$(cat filepath.txt | sed -e "s/\\$/\\\\$/g")

## downloading this file in the browser format 

echo "wget --user-agent="Mozilla/5.0" $LAS_NAME" > dl.sh

source dl.sh

## and then unzip all of the  resulting files.

7z x $(cat filename.txt)