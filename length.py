#!/usr/bin/env python

import glob

for file in glob.glob("*.aln"):
    print(file)
    lengths = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.isalpha():
                lengths.append(len(line))
        max_len = max(lengths)
        other_values = [l for l in set(lengths) if l != max_len]
        print(f"{file} max length: {max_len}.")
        if other_values:
            print(f"Other values: {sorted(other_values)}")