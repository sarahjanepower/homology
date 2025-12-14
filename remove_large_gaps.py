import pandas as pd
import glob
import os

for file in glob.glob("*.aln"):
    headers = []
    seqs = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                headers.append(line)
            else:
                seqs.append(line)

    df = pd.DataFrame([list(s) for s in seqs])

    # Identify mostly-gap columns (>50% gaps)
    gap_fraction = (df == '-').mean()
    cols_mostly_gaps = gap_fraction[gap_fraction > 0.5].index.tolist()

    if not cols_mostly_gaps:
        print(f"Skipping {file} (no columns with >50% gaps)")
        continue

    # Find rows that have letters in these mostly-gap columns
    rows_to_remove = set()
    for col in cols_mostly_gaps:
        rows_with_letters = df.index[df[col] != '-'].tolist()
        rows_to_remove.update(rows_with_letters)

    print(f"{file}: removing rows {sorted(rows_to_remove)}")

    # Remove the offending rows
    df_filtered = df.drop(index=rows_to_remove)
    headers_filtered = [h for i, h in enumerate(headers) if i not in rows_to_remove]

    # === Remove columns that are now all '-' ===
    df_filtered = df_filtered.loc[:, ~(df_filtered == '-').all(axis=0)]

    # Convert back to sequences
    filtered_seqs = [''.join(row) for row in df_filtered.values]

    # Save filtered FASTA
    out_file = os.path.splitext(file)[0] + "_filtered.aln"
    with open(out_file, "w") as f:
        for header, seq in zip(headers_filtered, filtered_seqs):
            f.write(f"{header}\n{seq}\n")
