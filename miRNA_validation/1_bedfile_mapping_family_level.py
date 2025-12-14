#!/usr/bin/env python
# This script takes a bedfile as input (argument 1) and creates a new column containing the miRNAs gene family
# Output is inout_file_name + "_cat"
# It is assumed that the miRNA to be classified is found in column 4 and the family is inserted as column 5
# Family dictionary is hard coded in and should be updated if needed

import os
import re
import sys

map_path = sys.argv[1]
map_name = os.path.basename(map_path)

mirna_families = {}
with open('fam_ID_dictionary_fixed_060425', 'r') as file:
    next(file)  # Skip header line
    for line in file:
        mirna_id, family = line.strip().split()
        mirna_families[mirna_id] = family

category_count = {}
seen = set()

table_with_fam_val = []

with open(map_name, 'r') as mapping_file:
    for line in mapping_file:
        chrom, start, end, gene, score, strand = line.strip().split('\t')
        mir_id_match = re.search(r'[a-z]{3}-([^\(]+)', gene)
        #support_match = re.search(r'\(([^)]+)\)', gene)

        mir_ID = mir_id_match.group(1).strip()
        #support_cat = support_match.group(1).strip()

        family = mirna_families.get(mir_ID)

        table_with_fam_val.append(f"{chrom}\t{start}\t{end}\t{gene}\t{family}\t{score}\t{strand}")

    # Print results
    # for (support_cat, family), count in sorted(category_count.items()):
    #     print(f"{support_cat}\t{family}\t{count}")

    output_file = map_name + "_cat"

    with open(output_file, 'w') as out_f:
        for line in table_with_fam_val:
            out_f.write(line + "\n")

