import pandas as pd
import numpy as np

input_file = "data/processed/delhi_2019_01_wide.csv"

df = pd.read_csv(input_file)

features = ["PM10", "NO2", "SO2", "CO", "Ozone"]

# Use rows with all five input features available
df = df.dropna(subset=features)

# Calculate the feature correlation matrix
correlation_matrix = df[features].corr()

# Calculate VIF using the inverse correlation matrix
vif_values = np.diag(np.linalg.inv(correlation_matrix))

vif_df = pd.DataFrame({
    "Feature": features,
    "VIF": vif_values
})

print("\nVariance Inflation Factor (VIF)")
print(vif_df.round(3).to_string(index=False))