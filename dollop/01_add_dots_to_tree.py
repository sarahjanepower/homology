import re
import sys
import os

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

# Input and output file paths
input_file = file_name
output_file = f"dots_{file_name}"

# Regex pattern: exactly 3 lowercase letters (surrounded by word boundaries)
pattern = r'\b([a-z]{3})\b'
replacement = r'\g<1>.......'

# Read the file
with open(input_file, 'r') as f:
    text = f.read()

# Replace all matches
modified_text = re.sub(pattern, replacement, text)

# Write to output
with open(output_file, 'w') as f:
    f.write(modified_text)

