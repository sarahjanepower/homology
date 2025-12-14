#!/usr/bin/env python3

## This script is used to run mirbase validation on one file at once - this allows multiple files to be validated at once rather than one after the other.
## This also flushes after each line is added i.e. the output file is live updated and if the run fails, the progress is saved.

import os
import re
import sys
from urllib.request import urlopen

file_path = sys.argv[1]
# species_file = os.path.basename(file_path)
species_file = file_path

mirbase_page = urlopen('https://www.mirbase.org/download/CURRENT/hairpin.fa').read().decode('utf-8')

sp = species_file.split('_')[0]

with open(species_file, 'r') as mapping, open(f'{species_file}_VAL', 'w') as output:

        print(f"Processing file {species_file}")
        updated_lines = []
        for line in mapping:
            line_parts = line.strip().split('\t')
            whole_mirna_ID = line_parts[3]
            mirna_sp = whole_mirna_ID.split('-')[0]
            mirna_ID = whole_mirna_ID[4:]

            if mirna_sp != sp:
                line_parts[3] += "(2+ sp in data)"

            else:
                pattern = f'[a-z]{{3}}-{mirna_ID}'
                matches = re.findall(pattern, mirbase_page)
                sp_prefixes = []
                for match in matches:
                    prefix = match[:3]
                    if prefix not in sp_prefixes:
                        sp_prefixes.append(prefix)

                line_parts[3] = whole_mirna_ID
                if len(sp_prefixes) > 1:
                    line_parts[3] += "(2+ sp in mirbase)"
                else:
                    line_parts[3] += "(unsupported)"

            new_line = '\t'.join(line_parts)
            output.write(new_line + '\n')
            output.flush()


