## This script takes the dollop outfile and formats the changes at each node to have no tab/linebreak. This output is printed to the screen.
#!/usr/bin/env python3

import sys
import os

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

with open(file_name, 'r') as file:
    lines = file.readlines()

# Find the starting point
line_number = None
for i, line in enumerate(lines):
    if "From" in line:
        line_number = i + 2
        break

# Extract lines after the "From" line
extracted_lines = lines[line_number:]

# Prepare for concatenation
concatenated_lines = []
current_line = ""

for line in extracted_lines:
    columns = line.split()

    # If the line starts a new header (with at least "yes" in column 3)
    if len(columns) == 11 and columns[2] in ["yes", "no"]:
        if current_line:  # Append the previous header with its continuation
            concatenated_lines.append(current_line)
        # Start a new header line
        current_line = " ".join(columns[:3]) + " " + "".join(columns[3:])
    else:
        # Append continuation line content without spaces
        current_line += "".join(columns)

# Add the last concatenated line if present
if current_line:
    concatenated_lines.append(current_line)

# Print the results
for line in concatenated_lines:
    print(line)

