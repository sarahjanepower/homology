import sys
import os
import re

file_path = sys.argv[1]
file_name = os.path.basename(file_path)
output = f"orientation_{file_name}"

let7_coords = {}  # species -> list of (start, end, strand)
with open("let-7.fa") as f:
    for line in f:
        if line.startswith(">"):
            header = line[1:].strip()
            species_field = header.split("::")[0]      # 'ppy-let-7'
            species = species_field.split("-let-7")[0] # 'ppy'

            match = re.search(r":(\d+-\d+)\(([+-])\)$", line)

            if match:
                coords, strand = match.groups()

            let7_coords.setdefault(species, []).append((coords, strand))

new_lines = []
with open(file_name) as f:
    for line in f:
        fields = line.strip().split('\t')  # or split('\t') depending on your file
        first_field = fields[0]  # 'ppy_(103782094-103840402)'

        first_field = first_field.replace(")", "")
        first_field = first_field.replace("(", "")
        species, coords = first_field.split('_')

        orientation = None
        if species in let7_coords:
            for let_coords, strand in let7_coords[species]:
                if coords == let_coords:
                    orientation = 'pos' if strand == '+' else 'neg'
                    break

    fields[0] = f"{species}_{orientation}"
    new_lines.append("\t".join(fields))

with open(output, 'w') as out_f:
    for line in new_lines:
        out_f.write(line + '\n')