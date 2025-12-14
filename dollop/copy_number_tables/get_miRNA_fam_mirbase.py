#!/usr/bin/env python3

import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys
import os

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

def find_family(df):
    base_url = "https://www.mirbase.org/hairpin/"

    output = []

    for index, row in df.iterrows():
        mir_id = row['mir_ID'].strip('>')
        accession = row['mirbase_accession']

        url = f"{base_url}{accession}"

        response = requests.get(url)
        if response.status_code == 200:
            print(f"Checking {mir_id}")
            content = BeautifulSoup(response.text, 'html.parser')

            # Locate the 'Gene family' section
            gene_family_label = content.find('div', class_='row-title', text="Gene family")
            if gene_family_label:
                # Find the associated row-data div for Gene family
                family_div = gene_family_label.find_next('div', class_='row-data')
                if family_div:
                    # Extract family name from the <a> tag within the row-data div
                    a_tag = family_div.find('a')
                    if a_tag:
                        family_name = a_tag.text.strip()
                        print(f"Family Name: {family_name}")
                    else:
                        family_name = 'NA'
                    
                    # Extract family accession (if present)
                    family_accession = family_div.text.split(';')[0].strip() if family_div.text else 'NA'
                    print(f"Family Accession: {family_accession}")

                    # Append the results to the output
                    output.append([mir_id, accession, family_name, family_accession])
                else:
                    # Handle case where row-data div is not found
                    output.append([mir_id, accession, 'NA', 'NA'])
            else:
                # Handle case where 'Gene family' label is not found
                output.append([mir_id, accession, 'NA', 'NA'])
        else:
            # Handle HTTP request failure
            print(f"Failed to retrieve data for {mir_id}, status code: {response.status_code}")
            output.append([mir_id, accession, 'NA', 'NA'])

    return pd.DataFrame(output, columns=['mir_ID', 'mirbase_accession', 'family_ID', 'family_accession'])

# Read the input file
df = pd.read_csv(file_name, sep=r'\s+', header=None, names=['mir_ID', 'mirbase_accession'])

# Find the family data
family_df = find_family(df)

# Save the output to a TSV file
output_file = f"{file_name}_output.tsv"
family_df.to_csv(output_file, sep='\t', index=False)
print(f"Output written to: {output_file}")

