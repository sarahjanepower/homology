import pandas as pd
from scipy.stats import spearmanr

homology_mthd = pd.read_csv("miRNA_family_counts.tsv.sorted", sep="\t", index_col=0)
infernal_mthd = pd.read_csv("infernal_benchmark_copy_numbers", sep="\t", index_col=0)
mirmachine_mthd = pd.read_csv("mirmachine_copy_numbers_2", sep="\t", index_col=0)

homology_mthd.columns = homology_mthd.columns.str.strip()
infernal_mthd.columns = infernal_mthd.columns.str.strip()
mirmachine_mthd.columns = mirmachine_mthd.columns.str.strip()

common_species = homology_mthd.index.intersection(infernal_mthd.index).intersection(mirmachine_mthd.index)
print("Common species after stripping:", common_species)

genes = ['mir-23', 'mir-9', 'mir-375', 'mir-143', 'mir-26', 'mir-455', 'mir-223', 'mir-128', 'mir-101', 'mir-140', 'mir-30', 'mir-551', 'mir-205', 'mir-190', 'mir-24', 'mir-1', 'mir-130', 'mir-135', 'mir-199', 'mir-33', 'mir-186', 'mir-196', 'mir-133', 'mir-96', 'mir-671', 'mir-214', 'mir-124', 'mir-204', 'mir-144', 'mir-221', 'mir-181', 'mir-146', 'mir-218', 'mir-148', 'mir-192', 'mir-22', 'let-7', 'mir-142', 'mir-19', 'mir-21', 'mir-122', 'mir-383', 'mir-193', 'mir-138', 'mir-15', 'mir-103', 'mir-137', 'mir-27', 'mir-92', 'mir-10', 'mir-126', 'mir-29', 'mir-217', 'mir-34', 'mir-17', 'mir-132', 'mir-145', 'mir-187', 'mir-490', 'mir-499', 'mir-129', 'mir-191', 'mir-216', 'mir-139']

homology_mthd_subset = homology_mthd.loc[:, genes]
infernal_mthd_subset = infernal_mthd.loc[:, genes]
mirmachine_mthd_subset = mirmachine_mthd.loc[:, genes]

print("Homology method shape:", homology_mthd_subset.shape)
print("Infernal method shape:", infernal_mthd_subset.shape)
print("MirMachine method shape:", mirmachine_mthd_subset.shape)

species = homology_mthd_subset.index

# Store correlations
correlations_species = {"homology_vs_infernal": [], "homology_vs_mirmachine": [], "infernal_vs_mirmachine": []}
p_values_species = {"homology_vs_infernal": [], "homology_vs_mirmachine": [], "infernal_vs_mirmachine": []}

# Loop over each species (rows)
for sp in species:
    corr_1_2, p_1_2 = spearmanr(homology_mthd_subset.loc[sp], infernal_mthd_subset.loc[sp])
    corr_1_3, p_1_3 = spearmanr(homology_mthd_subset.loc[sp], mirmachine_mthd_subset.loc[sp])
    corr_2_3, p_2_3 = spearmanr(infernal_mthd_subset.loc[sp], mirmachine_mthd_subset.loc[sp])

    correlations_species["homology_vs_infernal"].append(corr_1_2)
    correlations_species["homology_vs_mirmachine"].append(corr_1_3)
    correlations_species["infernal_vs_mirmachine"].append(corr_2_3)

    p_values_species["homology_vs_infernal"].append(p_1_2)
    p_values_species["homology_vs_mirmachine"].append(p_1_3)
    p_values_species["infernal_vs_mirmachine"].append(p_2_3)

# Convert to DataFrames
correlation_species_df = pd.DataFrame(correlations_species, index=species)
p_values_species_df = pd.DataFrame(p_values_species, index=species)

# Print results
print("Spearman Correlations:\n", correlation_species_df)
print("\nP-values:\n", p_values_species_df)

