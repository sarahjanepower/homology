#!/bin/bash -l

# specify number of tasks/cores per node required


# specify the walltime e.g 20 mins
#SBATCH -t 72:00:00

# set to email at start,end and failed jobs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=sarahjane.power@ucdconnect.ie

cd /home/people/15391131/scratch/NEW_CONCEPT/genomes/9_synteny/synteny_CDS_files

python synteny_mydata_allfiles.py $1
