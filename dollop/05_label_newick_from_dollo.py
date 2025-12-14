# This script updates node labels of newick file to match dollop output for easier renaming of node labels to mirNA IDS.
from Bio import Phylo
import os
import sys
import re

tree_path = sys.argv[1]
tree1 = os.path.basename(tree_path)

tree = Phylo.read(tree1, "newick")

node_counter = 1
if tree.root.name is None or tree.root.name == 'Root':
    tree.root.name = f"node_{node_counter}"
    node_counter += 1

# Traverse the rest of the tree and label internal nodes
for clade in tree.find_clades():
    if not clade.is_terminal() and clade.name is None:
        clade.name = f"node_{node_counter}:"
        node_counter += 1

with open(f"{tree1}_updated.newick", "w") as f:
    Phylo.write(tree, f, "newick")

#with open(f"{tree1}_updated.newick", "r+") as f:
#    content = f.read()
#    content = re.sub(r"(node_\d*)1\.00", r"\1", content)  # Remove '1.00:'

#    f.seek(0)  # Move back to the start of the file
#    f.write(content)  # Overwrite with modified content
#    f.truncate()

Phylo.draw_ascii(tree)
