#!/usr/bin/env python

# This script takes the benchmarks spreadsheet and compares the lists of miRNA families found in each pipeline per species
# miRNA families that are uniquely found using the homology method (per species) are listed in the output
# The output can be parsed to individual lists using the "split_unique_lists.sh" script

import pandas as pd

# Load the Excel file
df = pd.read_excel("benchmarks_060425.xlsx")

species_prefixes = sorted(set(col.split('_')[0] for col in df.columns if '_homology' in col))

# Dictionary to hold unique homology IDs for each species
unique_homology_ids = {}

for sp in species_prefixes:
    # Extract relevant columns
    homology = set(df[f"{sp}_homology"].dropna())
    infernal = set(df[f"{sp}_infernal"].dropna())
    mir_machine = set(df[f"{sp}_MirMachine"].dropna())

    # IDs only in homology, not in the other two
    unique = homology - infernal - mir_machine
    unique_homology_ids[sp] = unique



# Print results
#for sp, ids in unique_homology_ids.items():
#    print(f"Unique homology IDs for {sp}:")
#    for mi in sorted(ids):
#        print(f"  {mi}")
#    print()

for sp in unique_homology_ids:
    unique_homology_ids[sp] = sorted(unique_homology_ids[sp])

# Find max number of entries among all species
max_len = max(len(ids) for ids in unique_homology_ids.values())

# Pad each list with None so all are same length
padded_data = {
    sp: ids + [None] * (max_len - len(ids))
    for sp, ids in unique_homology_ids.items()
}

# Create wide-format DataFrame
wide_df = pd.DataFrame(padded_data)

# Save to TSV or print
wide_df.to_csv("wide_unique_homology_ids.tsv", sep='\t', index=False)
print(wide_df.head())
print(wide_df.tail())
