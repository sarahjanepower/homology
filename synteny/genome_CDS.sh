#!/bin/bash

module load bedtools

directories=($(cat "$1"))

for dir in "${directories[@]}"; do

    cd /home/people/15391131/scratch/NEW_CONCEPT/genomes/$dir/
    gff2bed < "$dir"_genomic.gff > "$dir"_genomic.bed
    mv "$dir"_genomic.bed synteny/
    cd synteny/
    awk '$8 == "CDS"' "$dir"_genomic.bed > "$dir"_bed_CDS_only.bed  
    cat "$dir"_Mirbase.map.bed "$dir"_bed_CDS_only.bed > "$dir"_mirs_genomic_merged_sorted.bed
    mv "$dir"_mirs_genomic_merged.bed /home/people/15391131/scratch/NEW_CONCEPT/genomes/9_synteny/synteny_CDS_files

done

