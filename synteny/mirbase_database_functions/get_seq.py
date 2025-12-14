import pandas as pd
from Bio import SeqIO


df = pd.read_csv("SC_mirbase_IDs", sep="\t", header=None)
df.columns = ["ID", "Fam", "Representative", "accession"]


fasta_path = "mirbase_mammals_filtered_0.9"

# Create {fasta_header: sequence} dictionary
sequence_dict = {record.id: str(record.seq) for record in SeqIO.parse(fasta_path, "fasta")}


df["Sequence"] = df["Representative"].map(sequence_dict)

print(df.head())

df.to_csv("SC_mirbase_with_sequences.tsv", sep="\t", index=False)
