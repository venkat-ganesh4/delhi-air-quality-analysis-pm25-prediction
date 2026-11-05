import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


# Load training and testing datasets
train_df = pd.read_csv("data/processed/train.csv")
test_df = pd.read_csv("data/processed/test.csv")


# Define input features
features = ["PM10", "NO2", "SO2", "CO", "Ozone"]

# Define target
target = "PM2.5"


# Separate inputs and target
X_train = train_df[features]
y_train = train_df[target]

X_test = test_df[features]
y_test = test_df[target]


# Train Linear Regression model
model = LinearRegression()

model.fit(X_train, y_train)


# Generate predictions
predictions = model.predict(X_test)


# Calculate evaluation metrics
mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)


# Create a simple baseline model
baseline = DummyRegressor(strategy="mean")

baseline.fit(X_train, y_train)

baseline_predictions = baseline.predict(X_test)


# Calculate baseline metrics
baseline_mae = mean_absolute_error(
    y_test,
    baseline_predictions
)

baseline_rmse = np.sqrt(
    mean_squared_error(y_test, baseline_predictions)
)

baseline_r2 = r2_score(
    y_test,
    baseline_predictions
)


# Display results
print("\nLINEAR REGRESSION RESULTS")

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

print("\nLinear Regression:")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))

print("\nBaseline Model:")
print("MAE:", round(baseline_mae, 2))
print("RMSE:", round(baseline_rmse, 2))
print("R2 Score:", round(baseline_r2, 4))

# Compare actual and predicted PM2.5 values

results = pd.DataFrame({
    "station_id": test_df["station_id"].values,
    "station_name": test_df["station_name"].values,
    "collected_at": test_df["collected_at"].values,

    "PM10": test_df["PM10"].values,
    "NO2": test_df["NO2"].values,
    "SO2": test_df["SO2"].values,
    "CO": test_df["CO"].values,
    "Ozone": test_df["Ozone"].values,

    "Actual_PM2.5": y_test.values,
    "Predicted_PM2.5": predictions
})

results["Error"] = (
    results["Actual_PM2.5"] -
    results["Predicted_PM2.5"]
)

results["Absolute_Error"] = results["Error"].abs()

results["Error"] = (
    results["Actual_PM2.5"] -
    results["Predicted_PM2.5"]
)

results["Absolute_Error"] = results["Error"].abs()

print("\nACTUAL VS PREDICTED VALUES")
print(results.head(15).round(2).to_string(index=False))

print("\nLARGEST PREDICTION ERRORS")

print(
    results.nlargest(10, "Absolute_Error")
    .round(2)
    .to_string(index=False)
)

# Save predictions
results.to_csv(
    "data/processed/linear_regression_predictions.csv",
    index=False
)

print("\nPredictions saved successfully!")