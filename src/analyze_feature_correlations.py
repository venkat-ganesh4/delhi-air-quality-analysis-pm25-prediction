import pandas as pd

input_file = "data/processed/delhi_2019_01_wide.csv"

df = pd.read_csv(input_file)

pollutants = [
    "PM2.5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "Ozone"
]

df = df.dropna(subset=pollutants)

features = ["PM10", "NO2", "SO2", "CO", "Ozone"]

correlation_matrix = df[features].corr()

print("\nCorrelation Between Input Features")
print(correlation_matrix.round(3))