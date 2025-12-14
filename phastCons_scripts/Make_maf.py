#!/usr/bin/env python

# Creates MAF alignment from existing fasta alignments and using fai dictionary created my make_fai.dict.py

import os
import glob
import re

species_chrom_lengths = {}

with open("species_chrom_lengths.tsv") as f:
    next(f)  # skip header
    for line in f:
        species, chrom, length = line.strip().split("\t")
        if species not in species_chrom_lengths:
            species_chrom_lengths[species] = {}
        species_chrom_lengths[species][chrom] = int(length)

for input_fasta in sorted(glob.glob("*.aln")):
    newlines_maf = []

    with open(input_fasta) as f:

        for line in f:
            line = line.strip()
            if line.startswith('>'):
                print(line)
                species = re.search(r'>([a-z]{3})', line).group(1)
                mir_id = re.search(r'>(.*)::', line).group(1)
                scaffold = re.search(r'::(.*):', line).group(1)
                start = int(re.search(r':([0-9]*)-([0-9]*)', line).group(1))
                end = int(re.search(r':([0-9]*)-([0-9]*)', line).group(2))
                strand = "-" if mir_id.endswith('_neg') else "+"

                chrom_length = species_chrom_lengths.get(species, {}).get(scaffold)

            else:
                line = line.strip()
                aln = line

                size = len(aln.replace("-", ""))

                maf_line = f"s {species}.{scaffold} {start} {size} {strand} {chrom_length} {aln}"
                newlines_maf.append(maf_line)

    base, ext = os.path.splitext(input_fasta)
    output_maf = base + ".maf"
    with open(output_maf, "w") as out:
        out.write("##maf version=1 scoring=blastz\n\na score=0\n")
        for line in newlines_maf:
            out.write(line + "\n")