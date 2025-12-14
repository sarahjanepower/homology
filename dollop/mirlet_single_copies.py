import pandas as pd

file_path = 'mirlet_matrix_060824'
df = pd.read_csv(file_path, sep='\t')

# Identify columns that contain only 1s
columns_with_only_ones = [col for col in df.columns if (df[col] == 1).all()]

columns_with_both = [col for col in df.columns if ((df[col] == 1) | (df[col] == 0)).all() and (df[col] != 1).any() and (df[col] != 0).any()]

minimum_sum = 78  # Replace with your desired minimum sum

columns_with_minimum_sum = [
    col for col in df.columns 
    if ((df[col] == 1) | (df[col] == 0)).all()  # Ensure all values are either 0 or 1
    and (df[col] == 1).any()  # Ensure there is at least one 1
    and df[col].sum() >= minimum_sum  # Check if the sum is at least the minimum sum
]

# Print the results
#print("Single-copy miRNAs:")
#print(columns_with_both)

print(f"Single-copy miRNAs present in at least {minimum_sum} species:")
print(columns_with_minimum_sum)

