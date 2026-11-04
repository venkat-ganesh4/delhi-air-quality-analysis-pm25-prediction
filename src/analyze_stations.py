
import pandas as pd

# Load station metadata
df = pd.read_csv("data/raw/delhi_stations.csv")

# Select useful columns
columns = [
    "station_id",
    "station_name",
    "first_seen",
    "last_seen",
    "n_rows",
    "parameters"
]

summary = df[columns].copy()

# Sort by number of available readings
summary = summary.sort_values(
    by="n_rows",
    ascending=False
)

print("Total stations:", len(summary))

print("\nStation data coverage:\n")
print(summary.to_string(index=False))

# Check repeated station names
duplicates = summary[
    summary["station_name"].duplicated(keep=False)
]

print("\nRepeated station names:\n")
print(duplicates[
    ["station_id", "station_name", "first_seen", "last_seen", "n_rows"]
].to_string(index=False))

print("\nStation metadata columns:")
print(df.columns.tolist())

print("\nLodhi Road and Pusa station details:")

selected_ids = [
    "site_109",
    "site_5395",
    "site_107",
    "site_1563"
]

details = df[df["station_id"].isin(selected_ids)]

print(details.to_string(index=False))