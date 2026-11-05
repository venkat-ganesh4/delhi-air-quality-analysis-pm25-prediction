import pandas as pd

input_file = "data/processed/delhi_2019_01_wide.csv"

df = pd.read_csv(input_file)

stations = ["site_119", "site_1422"]

df = df[df["station_id"].isin(stations)].copy()

# Keep rows where both measurements are available
df = df.dropna(subset=["PM2.5", "PM10"])

# Calculate the ratio
df["PM2.5_PM10_Ratio"] = df["PM2.5"] / df["PM10"]

# Summary for each station
summary = df.groupby(
    ["station_id", "station_name"]
)["PM2.5_PM10_Ratio"].agg(
    ["count", "mean", "median", "min", "max"]
)

print("\nPM2.5 / PM10 RATIO BY STATION")
print(summary.round(3).to_string())

# Compare the two stations with all Delhi stations
all_stations = pd.read_csv(input_file)

all_stations = all_stations.dropna(
    subset=["PM2.5", "PM10"]
)

all_stations["PM2.5_PM10_Ratio"] = (
    all_stations["PM2.5"] / all_stations["PM10"]
)

print("\nDELHI-WIDE RATIO")
print(
    all_stations["PM2.5_PM10_Ratio"]
    .describe()
    .round(3)
)