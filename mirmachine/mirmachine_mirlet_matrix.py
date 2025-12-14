import os
from glob import glob
import re
from collections import defaultdict

def read_fasta_file(file_path):
    gene_count = defaultdict(int)

    with open(file_path, 'r') as mm_file:
        for line in mm_file:
            match = re.search(r"gene_id=(.*)\.PRE", line)
            if match:
                gene = match.group(1)
                gene = gene.lower()
                gene_count[gene] += 1

    return gene_count

def create_frequency_table(files):
    species_gene_count = defaultdict(lambda: defaultdict(int))

    for file_path in files:
        species_name = os.path.basename(file_path).split('_')[0]
        gene_count = read_fasta_file(file_path)

        for gene, count in gene_count.items():
            species_gene_count[species_name][gene] += count

    species_list = sorted(species_gene_count.keys())
    gene_list = sorted({gene for species in species_gene_count for gene in species_gene_count[species]})

    # Print header
    print("\t" + "\t".join(gene_list))

    # Print each row
    for species in species_list:
        counts = [str(species_gene_count[species][gene]) for gene in gene_list]
        print(species + "\t" + "\t".join(counts))

fasta_files = glob('*PRE.gff_mammalfiltered')

# Create the frequency table
create_frequency_table(fasta_files)