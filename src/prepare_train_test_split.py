import pandas as pd

input_file = "data/processed/delhi_2019_01_wide.csv"

df = pd.read_csv(input_file)

# Required columns for our first ML model
required_columns = [
    "PM2.5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "Ozone"
]

# Convert timestamp into datetime format
df["collected_at"] = pd.to_datetime(df["collected_at"])

# Keep rows with all required pollutant measurements
df = df.dropna(subset=required_columns)

# Get all unique timestamps in chronological order
timestamps = sorted(df["collected_at"].unique())

# Calculate the 80% split point
split_index = int(len(timestamps) * 0.8)

split_timestamp = timestamps[split_index]

# Divide data chronologically
train_df = df[df["collected_at"] < split_timestamp]
test_df = df[df["collected_at"] >= split_timestamp]

# Save both datasets
train_df.to_csv(
    "data/processed/train.csv",
    index=False
)

test_df.to_csv(
    "data/processed/test.csv",
    index=False
)

print("Train-Test Split Completed")

print("\nTraining Data:")
print("Rows:", len(train_df))
print("First timestamp:", train_df["collected_at"].min())
print("Last timestamp:", train_df["collected_at"].max())

print("\nTesting Data:")
print("Rows:", len(test_df))
print("First timestamp:", test_df["collected_at"].min())
print("Last timestamp:", test_df["collected_at"].max())

print("\nTotal rows:", len(train_df) + len(test_df))