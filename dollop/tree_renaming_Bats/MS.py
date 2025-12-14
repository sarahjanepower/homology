## This script takes the dollop outfile and corresponding input gene names (in order) and tabulates which genes were lost at which nodes. This table is printed to the screen and no output file is generated.
#!/usr/bin/env python3

import sys
import os
import re
import tempfile
from Bio import Phylo


dollo_outfile_path = sys.argv[1]
dollo_outfile_name = os.path.basename(dollo_outfile_path)

genes_path = sys.argv[2]
gene_names = os.path.basename(genes_path)

tree_path = sys.argv[3]
tree_file = os.path.basename(tree_path)

with open(dollo_outfile_name, 'r') as file:
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
    print(processed_line)


temp = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
temp_path = temp.name  # Store the file path

# Write data to the temp file
for line in processed_lines:
    new_line = "\t".join(line)
    temp.write(f"{new_line}\n")

temp.close()  # Close the file to ensure it's properly written

GL_sum = temp_path

# This script updates node labels of newick file to match dollop output for easier renaming of node labels to mirNA IDS.
tree = Phylo.read(tree_file, "newick")

node_counter = 1
if tree.root.name is None or tree.root.name == 'Root':
    tree.root.name = f"node_{node_counter}"
    node_counter += 1

# Traverse the rest of the tree and label internal nodes
for clade in tree.find_clades():
    if not clade.is_terminal() and clade.name is None:
        clade.name = f"node_{node_counter}"
        node_counter += 1

with open(f"{tree_file}_updated.newick", "w") as f:
    Phylo.write(tree, f, "newick")

with open(f"{tree_file}_updated.newick", "r+") as f:
    content = f.read()
    content = re.sub(r"(node_\d*)1\.00", r"\1", content)  # Remove '1.00:'

    f.seek(0)  # Move back to the start of the file
    f.write(content)  # Overwrite with modified content
    f.truncate()

Phylo.draw_ascii(tree)

def replace_nodes(GL_sum, tree_file):

    with open(GL_sum, 'r') as gl_file:
        gl_data = gl_file.readlines()
        print(gl_data)

    with open(f"{tree_file}_updated.newick", 'r') as t:
        tree_data = t.read()


    for line in gl_data:
        line = line.replace(", ", "_")
        line = '\t'.join(line.split())
        line = line.split("\t")
        to_node = line[1]
        gains = line[2]
        losses = line[3]
        if to_node.isnumeric():
            to_node = f"node_{to_node}"

        replacement_parts = []
        if gains != "-":
            replacement_parts.append(f"GAINS_{gains}")
        if losses != "-":
            replacement_parts.append(f"LOSSES_{losses}")
        replacement_str = "_".join(replacement_parts)


        # Use regex to replace exact matches of the node name
        to_node_pattern = re.compile(rf"(?<=\)){re.escape(to_node)}(?![a-zA-Z0-9_])")
        tree_data = to_node_pattern.sub(replacement_str, tree_data)

    # Write the modified tree to a new file
    with open(f"modified_{tree_file}", 'w') as modified_tree:
        modified_tree.write(tree_data)

replace_nodes(GL_sum, tree_file)


