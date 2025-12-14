for file in *_Mirbase.map.bed; do
    prefix=${file:0:3}
    outfile="${file%.bed}_renamed.bed"
    awk -v pre="$prefix" 'BEGIN{OFS="\t"} {$4=pre substr($4, 4); print}' "$file" > "$outfile"
done
