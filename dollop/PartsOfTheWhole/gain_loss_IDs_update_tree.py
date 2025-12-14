import os
import sys
import re

GL_sum_path = sys.argv[1]
GL_sum = os.path.basename(GL_sum_path)

tree_path = sys.argv[2]
tree = os.path.basename(tree_path)

def replace_nodes(GL_sum, tree):

    with open(GL_sum, 'r') as gl_file:
        gl_data = gl_file.readlines()

    with open(tree, 'r') as tree_file:
        tree_data = tree_file.read()


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
    with open('modified_tree.txt', 'w') as modified_tree:
        modified_tree.write(tree_data)


replace_nodes(GL_sum, tree)