import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import os
import sys
import re

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

df = pd.read_csv(file_name, sep="\t", header=None)
df[0] = df[0].astype(str).str.replace(r'_(pos|neg)$', '', regex=True)

focal_cols = [11]   # <-- change this list to your 3 focal columns

######
from matplotlib.colors import rgb_to_hsv, to_rgb

def text_color_for_bg(hex_color):
    rgb = np.array(to_rgb(hex_color))
    brightness = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]  # Perceived brightness
    return "black" if brightness > 0.5 else "white"
###############

# Configuration for single gene
#focal_col = 6
#positions = list(range(-5, 0)) + [0] + list(range(1, 6))
#cols_to_keep = list(range(focal_col - 5, focal_col + 6))
#col_to_pos = dict(zip(cols_to_keep, positions))

# Configuration allow multiple focal columns (o-based)


pad = 5
min_focal = min(focal_cols)
max_focal = max(focal_cols)

cols_to_keep = list(range(min_focal - pad, max_focal + pad + 1))
# guard against negative indices and ensure columns exist
cols_to_keep = [c for c in cols_to_keep if c >= 0 and c in df.columns]

# create symmetric plotting positions centered on the focal range
L = (len(cols_to_keep) - 1) // 2
positions = list(range(-L, L + 1))
col_to_pos = dict(zip(cols_to_keep, positions))
focal_set = set(focal_cols)


# Melt directly from original df
df_long = (
    df[[0] + cols_to_keep]
    .melt(id_vars=0, var_name="col_index", value_name="gene")
    .assign(pos=lambda d: d["col_index"].map(col_to_pos))
)
def clean_gene_label(gene):
    # Remove _neg suffix first (if present)
    gene = re.sub(r'_neg$', '', gene)
    # Remove 3-letter prefix if gene starts with mir or let after the dash
    gene = re.sub(r'^[a-z]{3}-(mir|let)', r'\1', gene, flags=re.IGNORECASE)
    return gene.upper()

df_long["label"] = df_long["gene"].apply(clean_gene_label)

# --- Handle colors (case-insensitive, ignoring "_neg") ---
#genes_norm = df_long["gene"].str.lower().str.replace("_neg$", "", regex=True)
#unique_genes = genes_norm.unique()
unique_genes = df_long["label"].unique()


from distinctipy import get_colors
from matplotlib.colors import to_hex

# Get unique cleaned labels
unique_genes = df_long["label"].unique()
n_genes = len(unique_genes)

# Generate n visually distinct colors
colors = get_colors(n_genes, pastel_factor=0.7)  # pastel_factor optional
colors_hex = [to_hex(c) for c in colors]

exclude = "#89FD77"
colors_hex = [c for c in colors_hex if c != exclude]

# Map colors to genes
gene_to_color = dict(zip(unique_genes, colors_hex))
df_long["color"] = df_long["label"].map(gene_to_color)


#focal_color = "#0E18AC"  # or choose any color name/hex, e.g. "orange"
#df_long.loc[df_long["col_index"].isin(focal_set), "color"] = focal_color

# --- Determine focal gene direction based on _neg suffix ---
df_long["direction"] = np.where(df_long["gene"].str.endswith("_neg"), "neg", "pos")

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, len(df) * 0.4))

for i, species in enumerate(df[0]):
    species_genes = df_long[df_long[0] == species]

    # Draw horizontal baseline first (black, behind boxes)
    ax.hlines(y=i, xmin=-6.5, xmax=6.5, color="black", linewidth=0.5, zorder=0)

    for _, row in species_genes.iterrows():
        if row["pos"] == 0:  # Focal gene → box with arrowhead
            if row["direction"] == "pos":
                ax.add_patch(mpatches.FancyBboxPatch(
                    (row["pos"] - 0.4, i - 0.3),
                    0.8, 0.6,
                    boxstyle="Round,pad=0.02,rounding_size=0.05",
                    facecolor=row["color"], edgecolor="black", zorder=1
                ))
                # ax.add_patch(mpatches.Polygon(
                #     [[row["pos"]+0.4, i-0.3],
                #      [row["pos"]+0.6, i],
                #      [row["pos"]+0.4, i+0.3]],
                #     closed=True, facecolor=row["color"], edgecolor="black", zorder=1
                # ))
            else:  # neg
                ax.add_patch(mpatches.FancyBboxPatch(
                    (row["pos"] - 0.4, i - 0.3),
                    0.8, 0.6,
                    boxstyle="Round,pad=0.02,rounding_size=0.05",
                    facecolor=row["color"], edgecolor="black", zorder=1
                ))
                # ax.add_patch(mpatches.Polygon(
                #     [[row["pos"]-0.4, i-0.3],
                #      [row["pos"]-0.6, i],
                #      [row["pos"]-0.4, i+0.3]],
                #     closed=True, facecolor=row["color"], edgecolor="black", zorder=1
                # ))
        else:  # Normal gene box
            ax.add_patch(mpatches.Rectangle(
                (row["pos"] - 0.4, i - 0.3),
                0.8, 0.6,
                facecolor=row["color"], edgecolor="black", zorder=1
            ))

        # Add text (above boxes in z-order)
        text_col = text_color_for_bg(row["color"])
        ax.text(row["pos"], i, row["label"], ha='center', va='center', fontsize=7,
                zorder=2, fontweight='bold', color=text_col)
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-1, len(df) + 0)
ax.set_yticks(range(len(df[0])))
ax.set_yticklabels(df[0], fontstyle="italic")
ax.set_xticklabels([])
ax.invert_yaxis()
ax.set_xlabel("Position relative to focal gene")
ax.set_ylabel("Species")

plt.tight_layout()
plt.savefig(f"{file_name}_plot.png", dpi=300)
plt.savefig(f"{file_name}_plot.pdf")
