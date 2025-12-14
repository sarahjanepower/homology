#!/bin/bash

list=$1
file=$2

while read -r -u 9 old new; do
    sed -ri "s/$old/$new/g" "$file"
done 9< "$list"
