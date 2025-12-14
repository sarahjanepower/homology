#!/bin/bash

# File containing the list with two columns
list_file="replace_tree_names"

echo $list_file

while read -r search replace; do

    sed -i "s/$search/$replace/g" $1

    echo -i "s/$search/$replace/g" $1

done < "$list_file"
