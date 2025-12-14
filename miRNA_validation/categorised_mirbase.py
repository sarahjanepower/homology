#!/usr/bin/env python

import os
import re
import sys

fa_path = sys.argv[1]
fa_name = os.path.basename(fa_path)

mirna_families = {}
with open('fam_ID_dictionary_fixed_060425', 'r') as file:
    next(file)  # Skip header line
    for line in file:
        mirna_id, family = line.strip().split()
        mirna_families[mirna_id] = family

mir_ID_with_fam = []
mir_ID_with_fam.append(f"mir_ID\tfamily")
with open(fa_name, 'r') as fasta:
    for line in fasta:
        line = line.strip()
        if line.startswith('>'):
            seq_name = line
            mirna_ID = seq_name[5:]
            family = mirna_families.get(mirna_ID)
            if family:
                new_header = f"{line}\t{family}"
                mir_ID_with_fam.append(new_header)
            else:
                new_header = f"{line}\tNOFAM"
                mir_ID_with_fam.append(new_header)

output_file = fa_name + "_categorised"

with open(output_file, 'w') as out_f:
    for line in mir_ID_with_fam:
        out_f.write(line + "\n")