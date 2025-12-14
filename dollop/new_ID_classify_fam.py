family_map = {}
with open("fam_ID_dictionary_fixed") as f:  # format: mirna_id \t family
    for line in f:
        mirna, family = line.strip().split()
        family_map[mirna.lower()] = family  # lowercase for consistent matching

# Process input miRNA list
with open("NEW_mirs_not_in_mirbase") as f:  # your list of species-prefixed miRNAs
    for line in f:
        full_id = line.strip()
        if '-' in full_id:
            stripped_id = '-'.join(full_id.split('-')[1:])  # remove species prefix
            family = family_map.get(stripped_id.lower(), "Unknown")
            print(f"{full_id}\t{family}")