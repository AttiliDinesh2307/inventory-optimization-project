import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/inventory_dataset.csv")

print("Dataset Loaded Successfully!")
print(df.head())

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Calculate total daily demand
daily_demand = (
    df.groupby("Date")
      .agg({
          "Units_Sold": "sum",
          "Promotion": "sum"
      })
      .reset_index()
)

# If at least one product had a promotion that day,
# mark the day as a promotion day.
daily_demand["Promotion"] = (
    daily_demand["Promotion"] > 0
).astype(int)

print("\nDaily Demand:")
print(daily_demand.head())

print("\nNumber of Days:", len(daily_demand))

# Create a numerical time feature
daily_demand["Day_Number"] = range(1, len(daily_demand) + 1)

# Additional features for the model
daily_demand["Month"] = daily_demand["Date"].dt.month
daily_demand["Weekday"] = daily_demand["Date"].dt.weekday
daily_demand["Weekend"] = daily_demand["Weekday"].isin([5, 6]).astype(int)

print("\nDataset with Features:")
print(daily_demand.head())

print("\nDaily Demand with Time Feature:")
print(daily_demand.head())

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Prepare features and target
X = daily_demand[[
    "Day_Number",
    "Month",
    "Weekend",
    "Promotion"
]]

y = daily_demand["Units_Sold"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

print("\nLinear Regression model trained successfully!")

# -----------------------------
# Train Random Forest Model
# -----------------------------
print("\nTraining Random Forest Model...")

rf_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

rf_model.fit(X_train, y_train)

print("Random Forest model trained successfully!")

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Make predictions on the test data
# -----------------------------
# Make Predictions
# -----------------------------

# Linear Regression
y_pred_lr = model.predict(X_test)

# Random Forest
y_pred_rf = rf_model.predict(X_test)

print("\nActual vs Predicted Demand:")
comparison = pd.DataFrame({
    "Actual": y_test.values,
    "Linear Regression": y_pred_lr.round(2),
    "Random Forest": y_pred_rf.round(2)
})
print(comparison.head(10))

# -----------------------------
# Evaluate Linear Regression
# -----------------------------
mae_lr = mean_absolute_error(y_test, y_pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
r2_lr = r2_score(y_test, y_pred_lr)

# -----------------------------
# Evaluate Random Forest
# -----------------------------
mae_rf = mean_absolute_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
r2_rf = r2_score(y_test, y_pred_rf)

print("\n========== MODEL COMPARISON ==========")

print("\nLinear Regression")
print(f"MAE  : {mae_lr:.2f}")
print(f"RMSE : {rmse_lr:.2f}")
print(f"R²   : {r2_lr:.4f}")

print("\nRandom Forest")
print(f"MAE  : {mae_rf:.2f}")
print(f"RMSE : {rmse_rf:.2f}")
print(f"R²   : {r2_rf:.4f}")