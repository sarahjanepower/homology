import os

benchmark = {'bac','bta','cfa','hsa','laf','mmu','oan','pku','sha','ssc'}
family_set = {line.strip().split()[1] for line in open("fam_ID_dictionary_fixed_060425") if not line.startswith("ID")}
family_to_species = {fam: set() for fam in family_set}

for f in os.listdir():
    if f.endswith("_Mirbase.map.bed_cat"):
        sp = f.split("_")[0]
        for line in open(f):
            fam = line.strip().split('\t')[4]
            if fam in family_to_species:
                family_to_species[fam].add(sp)

with open("benchmark_only_family_support.tsv", "w") as out:
    out.write("family_ID\tspecies_support\n")
    for fam in sorted(family_to_species):
        out.write(f"{fam}\t{','.join(sorted(family_to_species[fam]))}\n")

