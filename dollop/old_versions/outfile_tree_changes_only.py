#!/usr/bin/env python3

import sys
import os

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

outfile = f"{file_name}.processed"

def append_lines_with_tab(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    result = []
    previous_line = ""

    for line in lines:
        if line.startswith('\t'):
            line = line.replace('\t', '')
            line = line.replace(',', '')
            previous_line += line.rstrip()
        else:
            if previous_line:
                result.append(previous_line)
            previous_line = line.rstrip()

    if previous_line:
        result.append(previous_line)

    with open(outfile, 'w') as file:
        file.write('\n'.join(result) + '\n')

append_lines_with_tab(file_name)

