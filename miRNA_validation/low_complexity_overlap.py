#!/usr/bin/env python3

import re
import sys
import os
from collections import defaultdict

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

species_counts = defaultdict(lambda: {'lowercase': 0, 'no_lowercase': 0})

with open(file_name, 'r') as file:
    for line in file:
        line = line.strip()
        if line.startswith('>'):
            seq_species = re.search(r'>([a-z]{3})-', line).group(1)
        elif line.isalpha():
            if any(c.islower() for c in line):
                species_counts[seq_species]['lowercase'] += 1
            else:
                species_counts[seq_species]['no_lowercase'] += 1

print(f"{file_name}")
print(f"{'species':<6} {'lowercase':>10} {'no_lowercase':>13}")

# Collect totals
total_lowercase = 0
total_no_lowercase = 0

# Print per-species data
for species, counts in sorted(species_counts.items()):
    lc = counts['lowercase']
    nlc = counts['no_lowercase']
    total_lowercase += lc
    total_no_lowercase += nlc
    print(f"{species:<8} {lc:>10} {nlc:>13}")

# Print totals
total_all = total_lowercase + total_no_lowercase
print("-" * 33)
print(f"{'TOTAL':<8} {total_lowercase:>10} {total_no_lowercase:>13}")

# Print percentages
if total_all > 0:
    perc_lowercase = (total_lowercase / total_all) * 100
    perc_no_lowercase = (total_no_lowercase / total_all) * 100
    print(f"{'PERCENT':<8} {perc_lowercase:>9.3f}% {perc_no_lowercase:>12.3f}%")

print(f"{file_name} summary:")
print(f"{' ':<6} {'lowercase':>10} {'no_lowercase':>13}")
print(f"{'TOTAL':<8} {total_lowercase:>10} {total_no_lowercase:>13}")
if total_all > 0:
    perc_lowercase = (total_lowercase / total_all) * 100
    perc_no_lowercase = (total_no_lowercase / total_all) * 100
    print(f"{'PERCENT':<8} {perc_lowercase:>9.3f}% {perc_no_lowercase:>12.3f}%")




