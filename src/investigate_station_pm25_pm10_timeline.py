import pandas as pd

input_file = "data/processed/delhi_2019_01_wide.csv"

df = pd.read_csv(input_file)

# Select Jawaharlal Nehru Stadium
df = df[df["station_id"] == "site_1424"].copy()

# Convert timestamp to datetime
df["collected_at"] = pd.to_datetime(df["collected_at"])

# Inspect January 12–14
start_date = "2019-01-12"
end_date = "2019-01-15"

df = df[
    (df["collected_at"] >= start_date)
    & (df["collected_at"] < end_date)
].copy()

# Calculate PM2.5 / PM10 ratio
df["Ratio"] = df["PM2.5"] / df["PM10"]

# Calculate difference
df["Difference"] = df["PM2.5"] - df["PM10"]

print("\nJAWAHARLAL NEHRU STADIUM: JANUARY 12–14, 2019")

print(
    df[
        [
            "collected_at",
            "PM2.5",
            "PM10",
            "Difference",
            "Ratio"
        ]
    ]
    .round(2)
    .to_string(index=False)
)

print("\nVIOLATION COUNTS BY DATE")

df["date"] = df["collected_at"].dt.date

print(
    (df["PM2.5"] > df["PM10"])
    .groupby(df["date"])
    .agg(["sum", "count"])
    .to_string()
)