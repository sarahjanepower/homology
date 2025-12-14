#!/bin/bash
# This script filters the categorised and validated bedfiles to contain only those that are unique to the homology pipeline for the species in question
# The categorised validated bedfiles and uniq files should be present in directory in order to run
# Output will be "homo_only*"
# Benchmark species are hardcoded in


directories=("bta" "bac" "hsa" "oan" "sha" "ssc" "pku" "laf" "mmu" "cfa")

for dir in "${directories[@]}"; do

    awk -F '\t' 'NR==FNR {keep[$1]; next} $5 in keep' "$dir"_uniq.txt "$dir"_Mirbase.map.bed_cat_VAL > homo_only_"$dir"_Mirbase.map.bed
done
