#!/usr/bin/env python3


import os
import sys

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

def count_and_replace_column(filename, output_filename):
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

    with open(output_filename, 'w') as file:
        file.write('\n'.join(result) + '\n')


# Call the function with your input file and desired output file
count_and_replace_column(file_name, file_name + '_GL_summary')
