#!/usr/bin/env python

# This script averages the wig scores from the different regions of the miRNA based on given coordinates
# File containing coordinates is hard coded.

import pandas as pd
import numpy as np

coords_file = "mirbase_mature_precursor_output.txt"
wig_file = "normalised_all.tsv"

coords_df = pd.read_csv(coords_file, sep="\t", dtype=str)

wig_df = pd.read_csv(wig_file, sep="\t")


def avg_from_coords(row, start_col, end_col, wig_scores):
    try:
        start = row[start_col]
        end = row[end_col]
        if start == "NA" or end == "NA" or pd.isna(start) or pd.isna(end):
            return np.nan
        start = int(start)
        end = int(end)
        # Adjust for 1-based indexing in database vs. 0-based DataFrame index
        cols = [f"pos_{i}" for i in range(start, end + 1)]
        valid_cols = [c for c in cols if c in wig_scores.index]
        if not valid_cols:
            return np.nan
        return wig_scores[valid_cols].mean()
    except Exception:
        return np.nan


# Output list
output_rows = []

for _, coord_row in coords_df.iterrows():
    family = coord_row["Family"]

    wig_match = wig_df[wig_df["miRNA_ID"] == family]
    if wig_match.empty:
        continue
    wig_scores = wig_match.iloc[0]

    out_row = {
        "miRNA_ID": family,
        "5p_mature_avg": avg_from_coords(coord_row, "5p_trimmedaln_start", "5p_trimmedaln_end", wig_scores),
        "5p_seed_avg": avg_from_coords(coord_row, "5p_seed_start", "5p_seed_end", wig_scores),
        "loop_avg": avg_from_coords(coord_row, "aln_loop_start", "aln_loop_end", wig_scores),
        "3p_mature_avg": avg_from_coords(coord_row, "3p_trimmedaln_start", "3p_trimmedaln_end", wig_scores),
        "3p_seed_avg": avg_from_coords(coord_row, "3p_seed_start", "3p_seed_end", wig_scores),
    }

    output_rows.append(out_row)

# Create DataFrame and save
output_df = pd.DataFrame(output_rows)
output_df.to_csv("mirna_wig_averages.tsv", sep="\t", index=False)
print("Results saved to mirna_wig_averages.tsv")
