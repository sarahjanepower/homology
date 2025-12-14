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
        line = line.split()
        to_node = line[1]
        gains = line[3]
        losses = line[4]
        if to_node.isnumeric():
            to_node = f"node_{to_node}"

        replacement_parts = []
        if gains != "0":
            replacement_parts.append(f"gains_{gains}")
        if losses != "0":
            replacement_parts.append(f"losses_{losses}")
        replacement_str = "_".join(replacement_parts)


        # Use regex to replace exact matches of the node name
        to_node_pattern = re.compile(rf"\b{re.escape(to_node)}\b")
        tree_data = to_node_pattern.sub(f"{to_node}_{replacement_str}", tree_data)

    # Write the modified tree to a new file
    with open('modified_tree.txt', 'w') as modified_tree:
        modified_tree.write(tree_data)


replace_nodes(GL_sum, tree)