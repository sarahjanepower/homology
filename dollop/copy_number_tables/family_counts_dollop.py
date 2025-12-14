import os
import re

# Load miRNA family information
mirna_families = {}
with open('fam_ID_dictionary', 'r') as file:
    next(file)  # Skip header line
    for line in file:
        mirna_id, family = line.strip().split()
        mirna_families[mirna_id] = family

# Directory with FASTA files
fasta_directory = '/home/people/15391131/scratch/NEW_CONCEPT/genomes/0_miRNA_predictions'

# Initialize a dictionary to store species data
species_counts = {}

pattern = r'^>[a-z]{3,5}-(.*?)[_::]'

# Process only files ending in .fa in the directory
for species_file in os.listdir(fasta_directory):
    if species_file.endswith('.fa'):  # Check if file ends with .fa
        species_name = os.path.splitext(species_file)[0]  # Get species name from filename
        species_counts[species_name] = {}
        
        with open(os.path.join(fasta_directory, species_file), 'r') as file:
            for line in file:
                if line.startswith('>'):  # Only process header lines
                    match = re.search(pattern, line)
                    if match:
                        mirna_id = match.group(1)
                        family = mirna_families.get(mirna_id)
                        if family:
                            species_counts[species_name][family] = species_counts[species_name].get(family, 0) + 1
# Write the output TSV file
with open('miRNA_family_counts.tsv', 'w') as out_file:
    # Write the header row
    all_families = sorted({family for counts in species_counts.values() for family in counts})
    out_file.write('Species\t' + '\t'.join(all_families) + '\n')

    # Write the counts for each species
    for species, counts in species_counts.items():
        row = [species] + [str(counts.get(family, 0)) for family in all_families]
        out_file.write('\t'.join(row) + '\n')

print("miRNA family counts saved to 'miRNA_family_counts.tsv'")

