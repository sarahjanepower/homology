import re
import os

fam_dict = {}

with open("fam_ID_dict_SC") as f:
    for line in f:
        columns = line.strip().split()
        mir_id, family = columns
        fam_dict[mir_id] = family

files = [f for f in os.listdir('.') if f.endswith('mirs.fa')]

for fasta_path in files:
    with open(fasta_path) as fasta:
        print(fasta_path)
        lines = fasta.readlines()
        for i in range(len(lines)):
            if lines[i].startswith(">"):
                header = lines[i].strip()
                sequence = lines[i + 1].strip() if i + 1 < len(lines) else ""

                # Extract the miRNA ID up to '::'
                match = re.match(r'^>[^-]+-([^:_]+)', header)
                if match:
                    mir_id = match.group(1)
                    print(mir_id)
                    if mir_id in fam_dict:
                        family = fam_dict[mir_id]
                        print(family)
                        with open(f"{family}.fa", "a") as out:
                            out.write(header + "\n")
                            out.write(sequence + "\n")



