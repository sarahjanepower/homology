#!/usr/bin/env python3

import sys
import os
import re

MM_mirs_path = "/home/people/15391131/scratch/MirMachine_Run/deutero_allnodes/results/predictions/filtered_gff"

valid_mirnas = set()
with open("mammalian_mirs_mirmachine", "r") as mir_file:
    for line in mir_file:
        valid_mirnas.add(line.strip())

print(valid_mirnas)

for filename in os.listdir(MM_mirs_path):
    filepath = os.path.join(MM_mirs_path, filename)

    if os.path.isfile(filepath) and filename.endswith('PRE.gff'):  # Ensure it's a file
        output_filename = f"{filename}_mammalfiltered"
        output_path = os.path.join(MM_mirs_path, output_filename)

        pattern = re.compile(r'gene_id=([^.]*)\.PRE')

        filtered_predictions = []
        with open(filepath, "r") as MM_file:
            for line in MM_file:
                match = pattern.search(line)

                if match:
                    gene_id = match.group(1)
                    gene_id = gene_id.lower()
                    print(f"matching {gene_id}")
                    if gene_id in valid_mirnas:  # Check the 3rd column
                        filtered_predictions.append(line)

        with open(output_path, "w") as out_file:
            out_file.writelines(filtered_predictions)

