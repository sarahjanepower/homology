#!/bin/bash -l

mirs=($(cat "$1"))

cd /home/people/15391131/scratch/NEW_CONCEPT/genomes/9_synteny/synteny_scripts

for mir in "${mirs[@]}"; do
        sbatch -J " ${mir} $(basename $0 .sh)" synteny_slurm.sh $mir
        echo "Submitted job for $mir"
done
