import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import os
import sys

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

df = pd.read_csv(file_name, sep="\t", header=None)

######
from matplotlib.colors import rgb_to_hsv, to_rgb

def text_color_for_bg(hex_color):
    rgb = np.array(to_rgb(hex_color))
    brightness = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]  # Perceived brightness
    return "black" if brightness > 0.5 else "white"
###############

# Config
focal_col = 6
positions = list(range(-5, 0)) + [0] + list(range(1, 6))
cols_to_keep = list(range(focal_col - 5, focal_col + 6))
col_to_pos = dict(zip(cols_to_keep, positions))

# Melt directly from original df
df_long = (
    df[[0] + cols_to_keep]
    .melt(id_vars=0, var_name="col_index", value_name="gene")
    .assign(pos=lambda d: d["col_index"].map(col_to_pos))
)

# --- Handle colors (case-insensitive, ignoring "_neg") ---
genes_norm = df_long["gene"].str.lower().str.replace("_neg$", "", regex=True)
unique_genes = genes_norm.unique()

df_long["label"] = df_long["gene"].str.replace("_neg$", "", regex=True)

# Use highly distinguishable palettes
palette = list(sns.color_palette("tab20b", min(20, len(unique_genes))))
if len(unique_genes) > 20:
    palette += sns.color_palette("hls", len(unique_genes) - 20)

gene_to_color = dict(zip(unique_genes, palette))
df_long["color"] = genes_norm.map(gene_to_color)

# --- Determine focal gene direction based on _neg suffix ---
df_long["direction"] = np.where(df_long["gene"].str.endswith("_neg"), "neg", "pos")

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, len(df) * 0.4))

for i, species in enumerate(df[0]):
    species_genes = df_long[df_long[0] == species]

    # Draw horizontal baseline first (black, behind boxes)
    ax.hlines(y=i, xmin=-5.5, xmax=5.5, color="black", linewidth=0.5, zorder=0)

    for _, row in species_genes.iterrows():
        if row["pos"] == 0:  # Focal gene → box with arrowhead
            if row["direction"] == "pos":
                ax.add_patch(mpatches.FancyBboxPatch(
                    (row["pos"] - 0.4, i - 0.3),
                    0.8, 0.6,
                    boxstyle="Round,pad=0.02,rounding_size=0.05",
                    facecolor=row["color"], edgecolor="black", zorder=1
                ))
                ax.add_patch(mpatches.Polygon(
                    [[row["pos"]+0.4, i-0.3],
                     [row["pos"]+0.6, i],
                     [row["pos"]+0.4, i+0.3]],
                    closed=True, facecolor=row["color"], edgecolor="black", zorder=1
                ))
            else:  # neg
                ax.add_patch(mpatches.FancyBboxPatch(
                    (row["pos"] - 0.4, i - 0.3),
                    0.8, 0.6,
                    boxstyle="Round,pad=0.02,rounding_size=0.05",
                    facecolor=row["color"], edgecolor="black", zorder=1
                ))
                ax.add_patch(mpatches.Polygon(
                    [[row["pos"]-0.4, i-0.3],
                     [row["pos"]-0.6, i],
                     [row["pos"]-0.4, i+0.3]],
                    closed=True, facecolor=row["color"], edgecolor="black", zorder=1
                ))
        else:  # Normal gene box
            ax.add_patch(mpatches.Rectangle(
                (row["pos"] - 0.4, i - 0.3),
                0.8, 0.6,
                facecolor=row["color"], edgecolor="black", zorder=1
            ))

        # Add text (above boxes in z-order)
        text_col = text_color_for_bg(row["color"])
        ax.text(row["pos"], i, row["label"], ha='center', va='center', fontsize=8,
                zorder=2, fontweight='bold', color=text_col)
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-1, len(df) + 1)
ax.set_yticks(range(len(df[0])))
ax.set_yticklabels(df[0], fontstyle="italic")
ax.invert_yaxis()
ax.set_xlabel("Position relative to focal gene")
ax.set_ylabel("Species")

plt.tight_layout()
plt.savefig(f"{file_name}_plot.png", dpi=300)
#plt.savefig("synteny_plot3.pdf")
