## This script takes the dollop outfile and corresponding input gene names (in order) and tabulates which genes were lost at which nodes. This table is printed to the screen and no output file is generated.
#!/usr/bin/env python3

import sys
import os
import csv

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
        current_line = "\t".join(columns[:3]) + "\t" + "".join(columns[3:])
    else:
        current_line += "".join(columns)

if current_line:
    concatenated_lines.append(current_line)

with open(genes_path, 'r') as gene_file:
    first_gene_line = gene_file.readline().strip()

first_gene_line = first_gene_line.replace("Species", "").strip()

concatenated_lines[0] += "\t" + first_gene_line


for i in range(1, len(concatenated_lines)):
    columns = concatenated_lines[i].split()
    if len(columns) > 3:  # Ensure the 4th column exists
        columns[3] = "\t".join(columns[3])  # Split the characters in the 4th column
    concatenated_lines[i] = "\t".join(columns)  # Reconstruct the line


header = concatenated_lines[0].split()
data = concatenated_lines[1:]


new_header = ["from", "to", "gains", "losses"]
processed_lines = [new_header]
for line in data:
    columns = line.split("\t")
    from_node, to_node, steps, *states = columns
    gains = []
    losses = []

    # Compare states to identify gains (1) and losses (0)
    for state, mir in zip(states, header[3:]):  # Start at index 3 for MIR columns
        # print(f"State: {state}, MIR: {mir}")
        if state == "1":
            gains.append(mir)
        elif state == "0":
            losses.append(mir)


    # Construct the output line
    processed_line = [
        from_node,
        to_node,
        ", ".join(gains) if gains else "-",  # Join gains or use "-" if empty
        ", ".join(losses) if losses else "-",  # Join losses or use "-" if empty
    ]
    processed_lines.append(processed_line)

for line in processed_lines:
    print("\t".join(line)) 

