import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings("ignore")

# -----------------------------
# LAYER 2 - K-MEANS CLUSTERING
# Goal: Group channels by performance profile to validate
#       and reinforce budget reallocation recommendations
# Algorithm: K-Means | Clusters: 3 | Features: 6 efficiency metrics
# -----------------------------

# -----------------------------
# 1. LOAD & BUILD CHANNEL FEATURES
# -----------------------------
df = pd.read_csv("ecommerce_marketing_growth_2025.csv")
df["date"] = pd.to_datetime(df["date"])

# Aggregate metrics per channel (same logic as Layer 1)
agg = df.groupby("channel").agg(
    spend=("spend", "sum"),
    revenue=("revenue", "sum"),
    clicks=("clicks", "sum"),
    sessions=("sessions", "sum"),
    conversions=("conversions", "sum")
).reset_index()

# Organic Search has no historical spend → assign proposed budget (€50k/year)
# consistent with budget reallocation recommendations
ORGANIC_PROPOSED_SPEND = 50000
agg.loc[agg["channel"] == "Organic Search", "spend"] = ORGANIC_PROPOSED_SPEND

# Compute efficiency metrics
agg["roas"]               = agg["revenue"] / agg["spend"]
agg["cac"]                = agg["spend"] / agg["conversions"]
agg["cpc"]                = agg["spend"] / agg["clicks"]
agg["cvr"]                = agg["conversions"] / agg["sessions"]
agg["revenue_per_session"]= agg["revenue"] / agg["sessions"]
agg["efficiency_gap"]     = (agg["revenue"] / agg["revenue"].sum() -
                              agg["spend"] / agg["spend"].sum()) * 100

print("Channel Feature Matrix:")
print(agg[["channel", "roas", "cac", "cpc", "cvr",
           "revenue_per_session", "efficiency_gap"]].to_string(index=False))
print()


# -----------------------------
# 2. PREPARE FEATURES FOR CLUSTERING
# -----------------------------
# Select the 6 efficiency metrics as clustering features
features = ["roas", "cac", "cpc", "cvr", "revenue_per_session", "efficiency_gap"]
X = agg[features].copy()

# Standardize — critical for K-Means (all metrics on same scale)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# -----------------------------
# 3. K-MEANS CLUSTERING
# -----------------------------
N_CLUSTERS = 3
kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
agg["cluster"] = kmeans.fit_predict(X_scaled)

# Label clusters based on average ROAS per cluster
cluster_roas = agg.groupby("cluster")["roas"].mean().sort_values(ascending=False)
roas_rank    = {c: i for i, c in enumerate(cluster_roas.index)}
label_map    = {0: "🟢 High Efficiency", 1: "🟡 Mid Efficiency", 2: "🔴 Low Efficiency"}
agg["cluster_label"] = agg["cluster"].map(roas_rank).map(label_map)

print("Cluster Assignment:")
print(agg[["channel", "cluster_label"]].to_string(index=False))
print()


# -----------------------------
# 4. CLUSTER PROFILE SUMMARY
# -----------------------------
profile = agg.groupby("cluster_label")[features].mean().round(3)

print("=" * 65)
print("CLUSTER PERFORMANCE PROFILES")
print("=" * 65)
print(profile.to_string())
print()


# -----------------------------
# 5. STRATEGIC INTERPRETATION
# -----------------------------
print("=" * 65)
print("STRATEGIC INTERPRETATION")
print("=" * 65)

for _, row in agg.sort_values("cluster_label").iterrows():
    label = row["cluster_label"]
    channel = row["channel"]

    if "High" in label:
        action = "→ Scale budget — strongest efficiency profile"
    elif "Mid" in label:
        action = "→ Optimize — solid base, room to improve"
    else:
        action = "→ Reduce or restructure — lowest efficiency"

    print(f"  {label} | {channel:<20} {action}")

print()


# -----------------------------
# 6. EXPORT FOR POWER BI
# -----------------------------
agg.to_csv("clustering_results.csv", index=False)
print("📁 clustering_results.csv exported — ready for Power BI\n")


# -----------------------------
# 7. VISUALIZATION
# -----------------------------
# Use PCA to reduce 6 dimensions → 2D for plotting
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
agg["pca_x"] = X_pca[:, 0]
agg["pca_y"] = X_pca[:, 1]

variance_explained = pca.explained_variance_ratio_ * 100

# Color map per cluster label
color_map = {
    "🟢 High Efficiency": "#2ca02c",
    "🟡 Mid Efficiency":  "#ff7f0e",
    "🔴 Low Efficiency":  "#d62728"
}

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# --- Plot 1: PCA Scatter ---
ax1 = axes[0]
for _, row in agg.iterrows():
    color = color_map[row["cluster_label"]]
    ax1.scatter(row["pca_x"], row["pca_y"], color=color, s=300, zorder=3)
    ax1.annotate(row["channel"],
                 xy=(row["pca_x"], row["pca_y"]),
                 xytext=(8, 6), textcoords="offset points",
                 fontsize=10, fontweight="bold")

# Cluster centroids
centroids_pca = pca.transform(kmeans.cluster_centers_)
ax1.scatter(centroids_pca[:, 0], centroids_pca[:, 1],
            marker="X", s=200, color="black", zorder=4, label="Centroid")

centroid_marker = plt.Line2D([0], [0], marker="X", color="w", markerfacecolor="black",
                             markersize=10, label="Cluster centroid (mean profile)")
legend_patches = [mpatches.Patch(color=c, label=l) for l, c in color_map.items()]
ax1.legend(handles=legend_patches + [centroid_marker], fontsize=9, loc="best")
ax1.set_title("Channel Clustering — PCA View\n"
              f"(PC1: {variance_explained[0]:.1f}% | PC2: {variance_explained[1]:.1f}% variance explained)",
              fontsize=11, fontweight="bold")
ax1.set_xlabel("PC1 — Overall Efficiency")
ax1.set_ylabel("PC2 — Cost Structure")
ax1.grid(linestyle="--", alpha=0.4)
ax1.spines[["top", "right"]].set_visible(False)

# --- Plot 2: ROAS vs CAC Bubble Chart ---
ax2 = axes[1]
for _, row in agg.iterrows():
    color = color_map[row["cluster_label"]]
    size  = row["revenue_per_session"] * 300  # bubble size = monetization efficiency
    ax2.scatter(row["cac"], row["roas"], color=color, s=size, alpha=0.8, zorder=3)
    ax2.annotate(row["channel"],
                 xy=(row["cac"], row["roas"]),
                 xytext=(8, 4), textcoords="offset points",
                 fontsize=10, fontweight="bold")

ax2.set_title("ROAS vs CAC by Channel\n(bubble size = Revenue per Session)",
              fontsize=11, fontweight="bold")
ax2.set_xlabel("CAC (€) — lower is better →")
ax2.set_ylabel("ROAS — higher is better ↑")
ax2.legend(handles=legend_patches, fontsize=9, loc="best")
ax2.grid(linestyle="--", alpha=0.4)
ax2.spines[["top", "right"]].set_visible(False)

plt.suptitle("K-Means Channel Clustering — Performance Profile Analysis",
             fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("clustering_by_channel.png", dpi=150, bbox_inches="tight")
plt.show()
print("📊 Chart saved: clustering_by_channel.png")
