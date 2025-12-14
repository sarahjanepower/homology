#!/usr/bin/env python3

# 26 June 2025
# MIRBASE ONLY
# This script retrieves upstream and downstream 10 protein coding genes for a given input mir-XXX (argument 1)  within gff3 files which has been filtered to just contain CDS entries.
# It is assumed that all ggf3 files are present in the working directory and end in 'mirs_genomic_merged_sorted.bed'
# Unnamed elements and duplicated genes are excluded (i.e. LOC0019209)
# Duplicated miRNA genes will be labelled with genomic coordinates

import re
import sys
import os

fam_dict = {}
with open("mirbase_database_functions/fam_ID_dict_SC") as f:
    for line in f:
        mir_id, family = line.strip().split()
        fam_dict[mir_id] = family

mir_input = sys.argv[1]
output_filename = f'{mir_input}.synteny'

mirnas_in_family = {mir_id for mir_id, fam in fam_dict.items() if fam == mir_input}
mirnas_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(mir) for mir in mirnas_in_family) + r')\b')

file_names = [f for f in os.listdir('.') if f.endswith('mirs_genomic_merged_sorted.bed')]

prefix_pattern = re.compile(r'([a-z]{3})-(?:mir|let)-[0-9]+[a-z]*-?[a-z]*[0-9]*[a-z]*[0-9]*')
gene_pattern = re.compile(r'gene=([^;]+)')
other_mir_pattern = re.compile(r'[a-z]{3}-(?:mir|let)-([0-9]+[a-z]*-?[a-z]*[0-9]*[a-z]*[0-9]*)')

genes_joined = []

for file_name in file_names:
    with open(file_name, "r") as f:
        lines = f.readlines()
        filtered_lines = [line for line in lines if not other_mir_pattern.search(line) or mirnas_pattern.search(line)]

        prefix_counts = {}

        for index, line in enumerate(filtered_lines):

            if mirnas_pattern.search(line):
                prefix = prefix_pattern.search(line).group(1)
                count = prefix_counts.get(prefix, 0)
                prefix_counts[prefix] = count + 1

                if count > 0:
                    cols = line.strip().split()
                    start, end = cols[1], cols[2]
                    prefix = f"{prefix}_({start}-{end})"

                block_lines = [f'{prefix}']
                block = []
                block.append(line.strip())  # center line first

                # get unique upstream genes
                upstream = []
                seen_genes = set()
                i = index - 1
                while i >= 0 and len(upstream) < 10:
                    sub_line = filtered_lines[i]
                    gene_match = gene_pattern.search(sub_line)
                    if gene_match:
                        gene_id = gene_match.group(1)
                        if gene_id not in seen_genes and not gene_id.startswith("LOC"):
                            upstream.insert(0, sub_line.strip())  # insert at beginning
                            seen_genes.add(gene_id)
                    elif mirnas_pattern.search(sub_line):
                        upstream.insert(0, sub_line.strip())  # keep miRs
                    i -= 1

                # get unique downstream genes
                downstream = []
                seen_genes = set()  # reset for downstream
                i = index + 1
                while i < len(filtered_lines) and len(downstream) < 10:
                    sub_line = filtered_lines[i]
                    gene_match = gene_pattern.search(sub_line)
                    if gene_match:
                        gene_id = gene_match.group(1)
                        if gene_id not in seen_genes and not gene_id.startswith("LOC"):
                            downstream.append(sub_line.strip())
                            seen_genes.add(gene_id)
                    elif mirnas_pattern.search(sub_line):
                        downstream.append(sub_line.strip())  # keep miRs
                    i += 1

                block = upstream + block + downstream


                for sub_line in block:
                    if mirnas_pattern.search(sub_line):
                        match_value = other_mir_pattern.search(sub_line).group(0)
                        block_lines.append(match_value)
                    elif gene_pattern.search(sub_line):
                        match_value = gene_pattern.search(sub_line).group(1)
                        block_lines.append(match_value)

                genes_joined.append('\t'.join(block_lines))

with open(output_filename, 'w') as out_f:
    out_f.write('\n'.join(genes_joined) + '\n')
