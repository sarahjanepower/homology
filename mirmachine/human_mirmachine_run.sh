#!/bin/bash -l

# specify number of tasks/cores per node required
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=4

# specify the walltime e.g 20 mins
#SBATCH -t 72:00:00

# set to email at start,end and failed jobs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=sarahjane.power@ucdconnect.ie

cd scratch/MirMachine_Run/deutero_allnodes/

module load bedtools

MirMachine.py --model deutero --node Metazoa --add-all-nodes --species Homo_sapiens --genome /home/people/15391131/scratch/NEW_CONCEPT/genomes/hsa/GCF_000001405.40_GRCh38.p14_genomic.fna -c 4
