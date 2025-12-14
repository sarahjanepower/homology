#!/usr/bin/env python

# This script reverse compliments any sequence that is labelled as "neg" in the sequence ID line of the input multifasta

from Bio import SeqIO
import os
import glob

for input_fasta in sorted(glob.glob("*.fa")):
    with open(input_fasta) as f:

        base, ext = os.path.splitext(input_fasta)
        if ext in [".fa", ".fasta"]:
            output_fasta = base + "_unrevved.fa"
        else:
            output_fasta = input_fasta + "_unrevved.fa"  # fallback

        with open(output_fasta, "w") as out_f:
            for record in SeqIO.parse(input_fasta, "fasta"):
                if 'neg' in record.id:
                    record.seq = record.seq.reverse_complement()
                SeqIO.write(record, out_f, "fasta")
