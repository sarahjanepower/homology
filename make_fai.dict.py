#!/usr/bin/env python

# This script makes a dictionary of chromosome lengths from .fai files. This was created to assist in manually creating MAF files from fasta alignments
# Paths and file names are hardcoded in

import os
import glob

species_list_file = "sp"
base_path = "/home/people/15391131/scratch/NEW_CONCEPT/genomes/"
output_file = "species_chrom_lengths.tsv"

species_chrom_lengths = {}

with open(species_list_file) as f:
    species_list = [line.strip() for line in f if line.strip()]

with open(output_file, "w") as out:
    out.write("species\tchromosome\tlength\n")  # header
    for species in species_list:
        species_dir = os.path.join(base_path, species)
        fai_files = glob.glob(os.path.join(species_dir, "*.fai"))

        if not fai_files:
            print(f"⚠️ No .fai file found for {species} in {species_dir}")
            continue

        fai_path = fai_files[0]

        with open(fai_path) as fai:
            for line in fai:
                chrom, length = line.strip().split()[:2]
                out.write(f"{species}\t{chrom}\t{length}\n")
