#!/usr/bin/env python3

from ete3 import Tree
import re
import glob

tree_file = "mammal_tree_GL_nums_1206_ungulatescorrected.txt"

for aln_file in sorted(glob.glob("*.aln")):
    species = set()
    with open(aln_file) as f:
        for line in f:
            if line.startswith('>'):
                sp = re.search(r'^>([a-z]{3})', line).group(1)
                species.add(sp)

    t = Tree(tree_file, format=1)
    t.prune(species, preserve_branch_length=True)

    base = aln_file.replace(".aln", "")
    t.write(outfile=f"{base}_pruned.nwk")
    print(f"{aln_file}: pruned to {len(species)} species.")
