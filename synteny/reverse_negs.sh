for file in *flank11.tsv; do
  output="${file%.tsv}.reversed.tsv"
  awk -F'\t' 'BEGIN{OFS="\t"}{
    if ($7 ~ /_neg/) {
      printf "%s*", $1;
      for (i=12; i>=2; i--) {
        printf "%s%s", OFS, $i;
      }
      printf "\n";
    } else {
      print;
    }
  }' "$file" > "$output"
done