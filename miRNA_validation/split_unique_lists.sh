# Splits table of unique miRNAs per species into lists
# Output file name is "spe_uniq.txt"

input="wide_unique_homology_ids.tsv"

# Read header line into array
IFS=$'\t' read -r -a headers < "$input"

# For each column, extract it skipping header and save as headername.txt
for i in "${!headers[@]}"; do
    # Clean header to safe filename (remove spaces/special chars)
    safe_name=$(echo "${headers[i]}" | tr -cd '[:alnum:]_-')
    # cut columns start at 1, array at 0, so add 1
    cut -f$((i+1)) "$input" | tail -n +2 > "${safe_name}_uniq.txt"
done
