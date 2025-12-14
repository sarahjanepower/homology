import re
import sys
import os
import argparse

# mir_pattern_input = sys.argv[1]
# mir_pattern = re.compile(rf'\b{re.escape(mir_pattern_input)}\b')

gene_pattern = re.compile(r'ENST[0-9]+\.([A-Za-z0-9]+)+(?=\.\d)')
other_mir_pattern = re.compile(r'(?:Mir|Let)-([0-9]+[a-z]*-?[a-z]*[0-9]*[a-z]*[0-9]*)')

directory = os.getcwd()
prefix_count = {}
output_file = []


def extract_prefix(file_name):
    match = re.search(r'([A-Z]{1}[a-z]{2}[A-Z]{1}[a-z]{2})', file_name)
    if match:
        return match.group(1)
    return None


def get_synteny(file_name, mir_pattern, output_file, prefix_count, neighbourhood_size):
    with open(file_name, "r") as f:
        prefix = extract_prefix(file_name)
        lines = f.readlines()
        block = []
        filtered_lines = [line for line in lines if not other_mir_pattern.search(line) or mir_pattern.search(line)]


        for index, line in enumerate(filtered_lines):
            if mir_pattern.search(line):
                if prefix in prefix_count:
                    prefix_count[prefix] += 1
                else:
                    prefix_count[prefix] = 1

                if prefix_count[prefix] > 1:
                    numbered_prefix = f"{prefix}_{prefix_count[prefix]}"
                else:
                    numbered_prefix = prefix

                genes_joined = f'{numbered_prefix}\t'

                block = filtered_lines[max(0, index - neighbourhood_size):index + neighbourhood_size + 1]
                for block_line in block:
                    if mir_pattern.search(block_line):
                        match_value = other_mir_pattern.search(block_line).group(0)
                        genes_joined += f'{match_value}\t'
                    elif gene_pattern.search(block_line):
                        match_value = gene_pattern.search(block_line).group(1)
                        genes_joined += f'{match_value}\t'

                output_file.append(genes_joined.strip())


def main():

    usage_message = """
    
    Usage: python Synteny.py -i INPUT miRNA [OPTIONS]

    Description: Identify anchoring proteins (default 10) up and downstream of an input 
                 miRNA of interest for multiple species.
                 
                 Script assumes all genome annotation files of interest species (in .bed
                 format) are present in the current working directory with file name
                 format GenSpe.miRNA_merged_sorted.bed (it will still work if there is 
                 text or numbers before or after GenSpe).
                 
                 Output is in tab separated (.tsv) format with name {input}_synteny.tsv.
                 The first column of the output is the species.
                 
                 Where the input miRNA has multiple copies, they will be labelled in
                 the output file as GenSpe.

    Required arguments:
      -i: INPUT miRNA          miRNA of interest (not case sensitive)

    Optional arguments:
      -n NUMBER OF NEIGHBOUR
         PROTEINS              Number of upstream/downstream anchoring proteins required 
                               (default = 10, integer)
"""

    parser = argparse.ArgumentParser(
        description="Identify anchoring proteins up and downstream of a miRNA of interest",
        usage=usage_message,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-i",
        type=str,
        required=True,
        help="miRNA of interest"
    )

    parser.add_argument(
        "-n",
        type=int,
        default=10,
        help="Number of upstream/downstream anchoring proteins required (default = 10)"
    )

    args = parser.parse_args()
    mir_pattern_input = args.i
    mir_pattern = re.compile(rf'\b{re.escape(mir_pattern_input)}\b', re.IGNORECASE)
    neighbourhood_size = args.n

    for file_name in os.listdir(directory):
        if os.path.isfile(file_name) and file_name.endswith('miRNA_merged_sorted.bed'):
            file = os.path.join(directory, file_name)

            get_synteny(file, mir_pattern, output_file, prefix_count, neighbourhood_size)

    with open(f'{mir_pattern_input}_synteny.tsv', 'w') as f:
        for line in output_file:
            f.write(line + '\n')

if __name__ == "__main__":
    main()
