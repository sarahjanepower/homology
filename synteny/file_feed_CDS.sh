#!/bin/bash -l

species=($(cat "$1"))

cd /home/people/15391131/scratch/NEW_CONCEPT/genomes

for sp in "${species[@]}"; do
        cd /home/people/15391131/scratch/NEW_CONCEPT/genomes/"$sp"/synteny/
        sbatch -J " ${sp} $(basename $0 .sh)" /home/people/15391131/scratch/NEW_CONCEPT/genomes/9_synteny/synteny_scripts/genome_CDS_single_file.sh $sp
        echo "Submitted job for $sp"
done
