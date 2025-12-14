#!/usr/bin/env python3

## This script runs validation on input file. Output is flushed

import os
import re
import sys
from urllib.request import urlopen

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

#mirbase_page = urlopen('https://www.mirbase.org/download/CURRENT/hairpin.fa').read().decode('utf-8')

species_file = file_name
sp = species_file.split('_')[0]
benchmark_species = ['bac', 'bta', 'cfa', 'hsa', 'laf', 'mmu', 'oan', 'pku', 'sha', 'ssc']

mirbase_support_dict = {}
with open("mirbase_family_species_support.tsv") as f:
    for line in f:
        family, species_str = line.strip().split('\t')
        species = species_str.strip()
        if species:
            mirbase_support_dict[family] = set(species.split(','))

benchmark_support_dict = {}
with open("benchmark_only_family_support.tsv") as f:
    for line in f:
        if len(line.strip().split('\t')) == 2:
            family, species_str = line.strip().split('\t')
            species = species_str.strip()
            if species:
                benchmark_support_dict[family] = set(species.split(','))

with open(species_file, 'r') as mapping, open(f'{species_file}_VAL', 'w') as output:

        print(f"Processing file {species_file}")
        updated_lines = []
        for line in mapping:
            line_parts = line.strip().split('\t')
            family = line_parts[4]
            whole_mirna_ID = line_parts[3]
            mirna_sp = whole_mirna_ID.split('-')[0]
            mirna_ID = whole_mirna_ID[4:]

            if family in benchmark_support_dict and (benchmark_support_dict[family] - {sp}):
                line_parts[3] += "(benchmark_support)"

            elif family in mirbase_support_dict and (mirbase_support_dict[family] - {sp}):
                line_parts[3] += "(mirbase_support)"

            else:
                line_parts[3] += "(unsupported)"

            new_line = '\t'.join(line_parts)
            output.write(new_line + '\n')
            output.flush()


