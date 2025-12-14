#!/bin/bash

input="$1"

line_number=$(grep -n "From" "$input" | cut -d: -f1)

sed -n "$((line_number + 1)),\$p" "$input" > temp1

sed 's/ \+/,/g' temp1 | \
sed 's/^,\([.10]\{5\}\)/,,,,\1/' | \
sed 's/^,//g' | \
sed 's/,/\t/3;s/,/\t/2;s/,/\t/1' | \
sed 's/,//g' > temp2

python process_outfile.py temp2
mv temp2.processed "$input".proccessed
rm temp1 temp2
