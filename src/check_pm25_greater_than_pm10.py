import pandas as pd

input_file = "data/processed/delhi_2019_01_wide.csv"

df = pd.read_csv(input_file)

df = df.dropna(subset=["PM2.5", "PM10"])

# PM2.5 should not normally exceed PM10
suspicious = df[df["PM2.5"] > df["PM10"]].copy()

print("\nPM2.5 GREATER THAN PM10")
print("Total records:", len(suspicious))

print("\nStation-wise count:")

print(
    suspicious.groupby("station_id")
    .size()
    .sort_values(ascending=False)
    .to_string()
)

print("\nFirst 15 suspicious records:")

print(
    suspicious[
        [
            "station_id",
            "station_name",
            "collected_at",
            "PM2.5",
            "PM10"
        ]
    ]
    .head(15)
    .to_string(index=False)
)