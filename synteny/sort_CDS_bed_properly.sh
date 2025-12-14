#!/bin/bash

directories=($(cat "$1"))

for dir in "${directories[@]}"; do
    echo Processing "$dir"
    cd /home/people/15391131/scratch/NEW_CONCEPT/genomes/$dir/synteny/mirgenedb/
    awk '$8 == "CDS"' "$dir"_genomic.bed > "$dir"_bed_CDS_only.bed
    cat mirIDupdated* "$dir"_bed_CDS_only.bed > "$dir"_mirs_genomic.bed
    awk 'BEGIN{OFS="\t"} {print $0}' "$dir"_mirs_genomic.bed | sort -k1,1 -k2,2n -k3,3n > "$dir"_mirs_genomic_sorted.bed
    cp "$dir"_mirs_genomic_sorted.bed /home/people/15391131/scratch/NEW_CONCEPT/genomes/9_synteny/mirgenedb/mirgenedb_bedfiles 

done

