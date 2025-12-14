import os
from glob import glob
import re
from collections import defaultdict

def read_fasta_file(file_path):
    gene_count = defaultdict(int)
    
    with open(file_path, 'r') as fasta_file:
        for line in fasta_file:
            if line.startswith('>'):
                line = line.lower()
                match = re.search(r'^>[a-z]{3}-([A-Za-z]+-[0-9]+)', line)
                if match:
                    gene = match.group(1)  # Extract gene name from "mir-" to the end of the line
                    gene_count[gene] += 1
    
    return gene_count

def create_frequency_table(files):
    species_gene_count = defaultdict(lambda: defaultdict(int))
    
    for file_path in files:
        species_name = os.path.splitext(os.path.basename(file_path))[0]  # Extract species name from filename
        gene_count = read_fasta_file(file_path)
        
        for gene, count in gene_count.items():
            species_gene_count[species_name][gene] += count
    
    # Get the list of all species and all genes
    species_list = sorted(species_gene_count.keys())
    gene_list = sorted({gene for species in species_gene_count for gene in species_gene_count[species]})
    
    # Print header
    print("\t" + "\t".join(gene_list))
    
    # Print each row
    for species in species_list:
        counts = [str(species_gene_count[species][gene]) for gene in gene_list]
        print(species + "\t" + "\t".join(counts))

# Find all files in the current directory that end with *renamed
fasta_files = glob('*.fa')

# Create the frequency table
create_frequency_table(fasta_files)

