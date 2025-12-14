#!/bin/bash -l

# specify number of tasks/cores per node required
#SBATCH -N 1
#SBATCH -n 22

# specify the walltime e.g 20 mins
#SBATCH -t 72:00:00

# set to email at start,end and failed jobs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=sarahjane.power@ucdconnect.ie

cd scratch/MirMachine_Run/deutero_allnodes/

module load bedtools

MirMachine.py --model deutero --node Metazoa --add-all-nodes --species Balaenoptera_acutorostrata --genome /home/people/15391131/scratch/NEW_CONCEPT/genomes/bac/GCF_949987535.1_mBalAcu1.1_genomic.fna -c 22
