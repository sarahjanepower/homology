import pandas as pd
import numpy as np

# user set this to False if you want end-exclusive (interval [start, end))
END_INCLUSIVE = True

normalised = pd.read_csv("normalised_cleaned.tsv", sep="\t")
mirgenedb = pd.read_csv("mirgenedb_TABLE_FIXED.tsv", sep="\t")

# melt wig into long format
wig_long = normalised.melt(id_vars=["miRNA"], var_name="Pos_", value_name="Score")
wig_long["Pos_"] = wig_long["Pos_"].str.extract(r"(\d+)").astype(int)
wig_long["miRNA_clean"] = wig_long["miRNA"].str.lower()
mirgenedb["mirgenedb_id_clean"] = mirgenedb["mirgenedb_id"].str.lower()

results = []

for mir in wig_long["miRNA_clean"].unique():
    subwig = wig_long[wig_long["miRNA_clean"] == mir]
    wig_len = subwig["Pos_"].max()

    matches = mirgenedb[mirgenedb["mirgenedb_id_clean"].str.contains(mir, case=False, na=False)].copy()
    if matches.empty:
        results.append({"miRNA": mir, "seed_avg": np.nan, "mature_avg": np.nan, "loop_avg": np.nan, "star_avg": np.nan})
        continue

    # choose best match by mature_length; compute according to convention
    if END_INCLUSIVE:
        matches.loc[:, "mature_len"] = matches["mature_end"] - matches["mature_start"] + 1
    else:
        matches.loc[:, "mature_len"] = matches["mature_end"] - matches["mature_start"]

    best = matches.iloc[(matches["mature_len"] - wig_len).abs().argsort().iloc[0]]

    region_means = {}
    for region in ["seed", "mature", "loop", "star"]:
        start_col, end_col = f"{region}_start", f"{region}_end"
        if pd.notna(best[start_col]) and pd.notna(best[end_col]):
            start, end = int(best[start_col]), int(best[end_col])
            if END_INCLUSIVE:
                region_scores = subwig[(subwig["Pos_"] >= start) & (subwig["Pos_"] <= end)]["Score"]
            else:
                region_scores = subwig[(subwig["Pos_"] >= start) & (subwig["Pos_"] < end)]["Score"]

            region_means[f"{region}_avg"] = region_scores.mean() if not region_scores.empty else np.nan
        else:
            region_means[f"{region}_avg"] = np.nan

    results.append({"miRNA": mir, **region_means})

avg_df = pd.DataFrame(results)
avg_df.to_csv("region_avg_scores.tsv", sep="\t", index=False)
print("Saved region_avg_scores.tsv (END_INCLUSIVE={})".format(END_INCLUSIVE))
