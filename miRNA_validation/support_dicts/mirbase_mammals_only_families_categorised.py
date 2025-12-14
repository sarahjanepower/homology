from collections import defaultdict

# Load miRNA ID -> family mapping
fam = {}
with open("fam_ID_dictionary_fixed_060425") as f:
    next(f)
    for line in f:
        id, fam_id = line.strip().split()
        fam[id] = fam_id

# Collect species per family
support = defaultdict(set)
with open("all_species_headers.txt") as f:
    for line in f:
        sp, mirna = line.strip().split('-', 1)
        base_id = mirna.split('(')[0]  # In case there are annotations
        family = fam.get(base_id)
        if family:
            support[family].add(sp)

# Write output
with open("mirbase_family_species_support.tsv", "w") as out:
    out.write("family_ID\tspecies_support\n")
    for family, species in sorted(support.items()):
        out.write(f"{family}\t{','.join(sorted(species))}\n")

