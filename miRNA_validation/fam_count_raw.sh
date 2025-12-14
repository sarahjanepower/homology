#!/bin/bash

suffix="map.bed_cat"

for file in *"$suffix"; do

    fam_count="$(awk '{print $5}' $file | sort | uniq | wc -l)"

    echo "$file: $fam_count"
    
done
