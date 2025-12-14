#!/usr/bin/env python3

import re
import os
import sys

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

sp = file_path.split('_')[0]
new_file_name = "mirIDupdated_" + file_name

with open(file_name, "r") as f:
    lines = f.readlines()

with open(new_file_name, "w") as f:
    for line in lines:
        line = '\t'.join(line.split())
        line = line.split("\t")
        og_id = line[3].lower()

        matches_per_id_cell = re.findall(r'[a-z]{3}-(?:mir|let|novel)-[0-9]+[a-z]*-?[a-z]*[0-9]*[a-z]*[0-9]*', og_id)
        if len(matches_per_id_cell) == 1:
            suffix_match = re.findall(r'[a-z]{3}-((?:mir|let|novel)-[0-9]+[a-z]*)-?[a-z]*[0-9]*[a-z]*[0-9]*', og_id)
            newID = f"{sp}-{suffix_match[0]}"

        else:
            suffix_matches = re.findall(r'[a-z]{3}-((?:mir|let|novel)-[0-9]+[a-z]*)-?[a-z]*[0-9]*[a-z]*[0-9]*', og_id)

            if len(set(suffix_matches)) == 1:
                newID = f"{sp}-{suffix_matches[0]}"

            elif len(set(suffix_matches)) > 1:
                values = re.findall(r'[a-z]{3}-(?:mir|let|novel)-([0-9]+[a-z]*-?[a-z]*[0-9]*[a-z]*[0-9]*)', og_id)
                concatenated_values = ':'.join(set(values))
                newID = f"{sp}-mir-{concatenated_values}*"

        
        line[3] = newID

        # rejoin all columns and write as a new line
        f.write('\t'.join(line) + '\n')
