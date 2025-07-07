#!/usr/bin/env bash
##rename fasta headers
##sed -E 's/^(>[a-z]{3}).*/\1/' mir-8094.aln

for alnfile in *.aln; do
    base="${alnfile%.aln}"
    treefile="${base}_pruned.nwk"

    phyloFit --tree "$treefile" --subst-mod REV --out-root "${base}_neutral" --msa-format FASTA "$alnfile"
    phastCons "$alnfile" "${base}_neutral.mod" > "${base}_phastcons.wig"

done
