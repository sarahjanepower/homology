import pandas as pd
import sys

file_paths = sys.argv[1:4]

dfs = [pd.read_csv(file_path, sep='\t', index_col=0) for file_path in file_paths]

# Start with all genes (columns) from the first file
valid_genes = set(dfs[0].columns)

for df in dfs:
    # Keep only genes where all species (rows) are non-zero
    valid_genes &= set(df.columns[(df != 0).all(axis=0)])

print("Genes present in all species across all files:", sorted(valid_genes))