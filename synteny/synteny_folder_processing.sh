#!/bin/bash -l

species=($(cat "$1"))

for sp in "${species[@]}"; do
        echo Processing "$sp"...
        cd /home/people/15391131/scratch/NEW_CONCEPT/genomes/"$sp"/
        #mkdir synteny_mirgenedb
        #cp *genomic.g* synteny_mirgenedb
        #cp mirgenedb_"$sp"/"$sp"_mirgenedb.map.bed_merged* synteny_mirgenedb
        cd synteny_mirgenedb
        rm *merged*

done
