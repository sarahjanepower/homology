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

temp_filename = file_name + "_temp.txt"
with open(temp_filename, 'w') as temp_file:
    temp_file.write('\n'.join(concatenated_lines) + '\n')


def count_and_replace_column(filename):
    with open(filename, 'r') as file:
        result = []
        result.append("From\tTo\tAny Steps?\tGains\tLosses")
        for line in file:
            columns = line.split()  # Use tab as delimiter
            if len(columns) >= 4:
                fourth_column = columns[3].strip()
                count_1 = fourth_column.count('1')
                count_0 = fourth_column.count('0')
                columns[3] = str(count_1)
                columns.append(str(count_0))
            result.append('\t'.join(columns))  # Use tab as delimiter

    output_filename = filename.replace("_temp.txt", "_GL_sum.txt")
    with open(output_filename, 'w') as file:
        file.write('\n'.join(result) + '\n')

# Call the function with the temporary file
count_and_replace_column(temp_filename)

# Clean up (optional): remove the temporary file
os.remove(temp_filename)

