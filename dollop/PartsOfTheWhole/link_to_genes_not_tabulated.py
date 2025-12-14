## This script takes the dollop outfile and corresponding input gene names and outputs the changes for each individual gene which can be manually inspected.
#!/usr/bin/env python3

import sys
import os

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

genes_path = sys.argv[2]
gene_names = os.path.basename(genes_path)

with open(file_name, 'r') as file:
    lines = file.readlines()

line_number = None
for i, line in enumerate(lines):
    if "From" in line:
        line_number = i + 2
        break

extracted_lines = lines[line_number:]
concatenated_lines = []
concatenated_lines.append("From " + "To " + "Steps? ")
current_line = ""

for line in extracted_lines:
    columns = line.split()

    if len(columns) == 11 and columns[2] in ["yes", "no"]:
        if current_line:
            concatenated_lines.append(current_line)
        current_line = " ".join(columns[:3]) + " " + "".join(columns[3:])
    else:
        current_line += "".join(columns)

if current_line:
    concatenated_lines.append(current_line)

with open(genes_path, 'r') as gene_file:
    first_gene_line = gene_file.readline().strip()

first_gene_line = first_gene_line.replace("Species", "").strip()

concatenated_lines[0] += " " + first_gene_line


for i in range(1, len(concatenated_lines)):
    columns = concatenated_lines[i].split()
    if len(columns) > 3:  # Ensure the 4th column exists
        columns[3] = " ".join(columns[3])  # Split the characters in the 4th column
    concatenated_lines[i] = " ".join(columns)  # Reconstruct the line


# print(concatenated_lines[0])
#
for line in concatenated_lines:
    line = line.replace(" ", "\t")
#     if "From" not in line:
#         columns[3] = " ".join(columns[3])
    print(line)


