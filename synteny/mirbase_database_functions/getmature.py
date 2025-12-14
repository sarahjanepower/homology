#!/usr/bin/env python3

import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys
import os
import re
import csv

base_url = "https://www.mirbase.org/hairpin/"

output = []

with open("SC_mirbase_IDs") as f:
    for line in f:
        mir_id, family, representative, accession, precursor = line.strip().split()

        url = f"{base_url}{accession}"

        response = requests.get(url)
        if response.status_code == 200:
            print(f"Checking {mir_id}")
            content = BeautifulSoup(response.text, 'html.parser')

            row = {
                'ID': mir_id,
                'Family': family,
                'Representative': representative,
                'Precursor': precursor,
                '5p_mature': '-', '5p_start': '-', '5p_end': '-', '5p_seq': '-',
                '3p_mature': '-', '3p_start': '-', '3p_end': '-', '3p_seq': '-',
                'mature_undefined': '-', 'mature_undefined_start': '-', 'mature_undefined_end': '-', 'mature_undefined_seq': '-'
            }

            # Search all mature blocks
            mature_blocks = content.find_all('div', class_='col-lg-6')

            for block in mature_blocks:
                name_tag = block.find('strong', class_='mature-name')
                if not name_tag:
                    continue
                mature_name = name_tag.text.strip()

                sequence_row = block.find('td', string='Sequence')
                if not sequence_row:
                    continue
                sequence_data = sequence_row.find_next_sibling('td')
                if not sequence_data:
                    continue

                match = re.match(r'(\d+)\s*-\s*([AUGCaucg]+)\s*-\s*(\d+)', sequence_data.text.strip())
                if not match:
                    continue

                start, seq, end = match.groups()

                if '5p' in mature_name:
                    row['5p_mature'] = mature_name
                    row['5p_start'] = start
                    row['5p_end'] = end
                    row['5p_seq'] = seq
                elif '3p' in mature_name:
                    row['3p_mature'] = mature_name
                    row['3p_start'] = start
                    row['3p_end'] = end
                    row['3p_seq'] = seq
                else:
                    row['mature_undefined'] = mature_name
                    row['mature_undefined_start'] = start
                    row['mature_undefined_end'] = end
                    row['mature_undefined_seq'] = seq


            output.append([
                row['ID'],
                row['Family'],
                row['Representative'],
                row['Precursor'],
                row['5p_mature'], row['5p_start'], row['5p_end'], row['5p_seq'],
                row['3p_mature'], row['3p_start'], row['3p_end'], row['3p_seq'],
                row['mature_undefined'], row['mature_undefined_start'], row['mature_undefined_end'],
                row['mature_undefined_seq']
            ])

with open("mirbase_mature_precursor_output.tsv", "w", newline="") as out_f:
    writer = csv.writer(out_f, delimiter='\t')
    writer.writerow([
        "ID",
        'Family',
        'Representative',
        'Precursor',
        "5p_mature", "5p_start", "5p_end", "5p_seq",
        "3p_mature", "3p_start", "3p_end", "3p_seq",
        "mature_undefined", "mature_undefined_start", "mature_undefined_end", "mature_undefined_seq"
    ])
    writer.writerows(output)

