#!/usr/bin/env python

# Normalises phyloP output wig scores (z-scores) and outputs each gene as one row of a tsv.
# Input is multiple .wig files in the current directory

import pandas as pd
import glob
import numpy as np
import os

output_tsv_normalised = []

for wig in sorted(glob.glob("*_phyloP.wig")):
    with open(wig, "r") as f:
        lines = f.readlines()
        mirna_id = os.path.basename(wig)
        mirna_id = mirna_id.replace("_cleaned_phyloP.wig", "")
        mirna_id = mirna_id.replace("_phyloP.wig", "")

        scores_str = [line.strip() for line in lines[1:] if line.strip() != ""]

        if not scores_str:
            print(f"WARNING: {wig} has no numeric scores after the header. Skipping.")
            continue

        scores = np.array([float(s) for s in scores_str])

        mean = scores.mean()
        std = scores.std()

        if std == 0:
            z_scores = np.zeros_like(scores)
        else:
            z_scores = (scores - mean) / std

        row = [mirna_id] + z_scores.tolist()
        output_tsv_normalised.append(row)

max_len = max(len(row) for row in output_tsv_normalised) - 1
colnames = ["miRNA_ID"] + [f"pos_{i + 1}" for i in range(max_len)]
df = pd.DataFrame(output_tsv_normalised, columns=colnames)

df.to_csv("normalised_all.tsv", sep="\t", index=False)