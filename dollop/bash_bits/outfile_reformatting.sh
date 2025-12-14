sed 's/ \+/,/g' fam_table | sed 's/^,\([.10]\{5\}\)/,,,,\1/'| sed 's/^,//g' | sed 's/,/\t/3;s/,/\t/2;s/,/\t/1' | sed 's/,//g' > fam_processed
