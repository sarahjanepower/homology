import re, sys

fasta_path = sys.argv[1]
synteny_path = sys.argv[2]

fasta_coords = []
fasta_prefixes = []

with open(fasta_path) as fasta_file:
    for line in fasta_file:
        if line.startswith(">"):
            header = line.strip()
            # Extract coordinate pattern like 123-456
            coord_match = re.search(r'([0-9]+-[0-9]+)', header)
            if coord_match:
                fasta_coords.append(coord_match.group(1))
            # Extract the 3-letter prefix (skip '>')
            fasta_prefixes.append(header[1:4].lower())

with open(synteny_path) as synteny_file:
    for line in synteny_file:
        synteny_line = line.strip()

        if any(coord in synteny_line for coord in fasta_coords):
            print(line, end="")

        elif any(synteny_line.lower().startswith(prefix) for prefix in fasta_prefixes):
            print(line, end="")
