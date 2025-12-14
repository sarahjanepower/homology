#!/usr/bin/env python
# This script categorises a list of miRNA IDs (including species prefixes) to family level
# Family dictionary file name is hardcoded and should be checked before use

family_map = {}
with open("fam_ID_dictionary_fixed") as f:  # format: mirna_id \t family
    for line in f:
        mirna, family = line.strip().split()
        family_map[mirna.lower()] = family  

# Process input miRNA list
with open("hsa_mirs") as f:
    for line in f:
        full_id = line.strip()
        if '-' in full_id:
            stripped_id = '-'.join(full_id.split('-')[1:])
            family = family_map.get(stripped_id.lower(), "Unknown")
            print(f"{full_id}\t{family}")
