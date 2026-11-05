import pandas as pd

input_file = "data/processed/delhi_2019_01_wide.csv"

df = pd.read_csv(input_file)

df = df.dropna(subset=["PM2.5", "PM10"]).copy()

# Keep only records where PM2.5 exceeds PM10
suspicious = df[df["PM2.5"] > df["PM10"]].copy()

# Calculate the absolute and relative differences
suspicious["Difference"] = (
    suspicious["PM2.5"] - suspicious["PM10"]
)

suspicious["Ratio"] = (
    suspicious["PM2.5"] / suspicious["PM10"]
)

print("\nVIOLATION SUMMARY")
print("Total violations:", len(suspicious))

print("\nDifference statistics (µg/m³):")
print(suspicious["Difference"].describe().round(2))

print("\nRatio statistics:")
print(suspicious["Ratio"].describe().round(3))

print("\nTOP 15 LARGEST DIFFERENCES")

print(
    suspicious[
        [
            "station_id",
            "station_name",
            "collected_at",
            "PM2.5",
            "PM10",
            "Difference",
            "Ratio"
        ]
    ]
    .sort_values("Difference", ascending=False)
    .head(15)
    .round(2)
    .to_string(index=False)
)

print("\nSTATION-WISE AVERAGE DIFFERENCE")

print(
    suspicious.groupby("station_id")["Difference"]
    .agg(["count", "mean", "max"])
    .sort_values("count", ascending=False)
    .round(2)
    .to_string()
)