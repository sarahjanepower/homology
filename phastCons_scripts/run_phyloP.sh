#!/usr/bin/env bash
##rename fasta headers
##for file in *.aln; do sed -Ei 's/^(>[a-z]{3}).*/\1/' "$file"; done

for alnfile in *.aln; do
    base="${alnfile%.aln}"
    treefile="${base}_pruned.nwk"

    phyloFit --tree "$treefile" --subst-mod HKY85 --out-root "${base}_neutral" --msa-format FASTA "$alnfile"
    phyloP --mode CONACC --method SCORE --wig-scores --base-by-base "${base}_neutral".mod "$alnfile" > "${base}_phyloP.wig"

done
