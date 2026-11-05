import pandas as pd
import matplotlib.pyplot as plt

input_file = "data/processed/delhi_2019_01_wide.csv"

df = pd.read_csv(input_file)

# Keep rows where all six pollutant measurements are available
pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "Ozone"]

df = df.dropna(subset=pollutants)

# Create five scatter plots
features = ["PM10", "NO2", "SO2", "CO", "Ozone"]

fig, axes = plt.subplots(2, 3, figsize=(15, 9))

axes = axes.flatten()

for i, feature in enumerate(features):

    axes[i].scatter(
        df[feature],
        df["PM2.5"],
        alpha=0.3,
        s=10
    )

    axes[i].set_title(f"PM2.5 vs {feature}")
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel("PM2.5 (µg/m³)")
    axes[i].grid(True, alpha=0.3)

# Remove the unused sixth plot
fig.delaxes(axes[5])

plt.suptitle(
    "Relationships Between PM2.5 and Other Pollutants",
    fontsize=15
)

plt.tight_layout()

plt.savefig(
    "reports/figures/pm25_pollutant_relationships.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()