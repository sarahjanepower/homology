import re, sys

synteny_file = sys.argv[1]
fasta_file = sys.argv[2]

matches = []
with open(synteny_file) as f:
    for line in f:
        line = line.strip()
        m = re.search(r'([0-9]+-[0-9]+)', line)
        if m:
            matches.append(m.group(1))
        else:
            matches.append(line[:3])

# Grab sequences from FASTA whose headers contain any match
with open(fasta_file) as f:
    header = None
    seq_lines = []
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            if header and any(m in header for m in matches):
                print(header)
                print("\n".join(seq_lines))
            header = line
            seq_lines = []
        else:
            seq_lines.append(line)
    # Print last entry if matched
    if header and any(m in header for m in matches):
        print(header)
        print("\n".join(seq_lines))