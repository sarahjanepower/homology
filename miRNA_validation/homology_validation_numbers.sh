#!/bin/bash -l
# Script prints number of miRNA families per validation category
# Assumes filtered family categorised validated bedfiles are present in directory as "homo_only*"

directories=($(cat "$1"))

cd /home/people/15391131/scratch/NEW_CONCEPT/genomes/10_benchmark_nums/homology/val/

echo "awk -F'\t' '{ match($4, /\(([^)]+)\)/, arr); print arr[1] "\t" $5 }' homo_only_hsa_Mirbase.map.bed | sort | uniq | awk '{print $1}' | sort | uniq -c"

for dir in homo_only*; do
        echo $dir
        awk -F'\t' '{ match($4, /\(([^)]+)\)/, arr); print arr[1] "\t" $5 }' "$dir" | sort | uniq | awk '{print $1}' | sort | uniq -c
done
