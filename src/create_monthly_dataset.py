import pandas as pd

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("data/raw/inventory_dataset.csv")

print("Dataset Loaded Successfully!")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Extract Month
df["Month"] = df["Date"].dt.strftime("%B")

# Revenue
df["Revenue"] = (
    df["Units_Sold"] *
    df["Unit_Price"]
)

# Profit
df["Profit"] = (
    df["Units_Sold"] *
    (
        df["Unit_Price"] -
        df["Cost_Price"]
    )
)

# -----------------------------
# Monthly Summary
# -----------------------------

monthly_summary = (
df.groupby(
    [
        "Month",
        "Product",
        "Category"
    ]
)
    .agg(
    Warehouse=("Warehouse", lambda x: x.mode()[0]),
    Supplier=("Supplier", lambda x: x.mode()[0]),
    Units_Sold=("Units_Sold", "sum"),
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Average_Stock=("Current_Stock", "mean"),
    Promotion_Days=("Promotion", "sum"),
    Average_Lead_Time=("Lead_Time_Days", "mean")
)
    .reset_index()
)

# Round values
monthly_summary["Average_Stock"] = (
    monthly_summary["Average_Stock"]
    .round(0)
)

monthly_summary["Average_Lead_Time"] = (
    monthly_summary["Average_Lead_Time"]
    .round(1)
)

# -----------------------------
# Save Dataset
# -----------------------------

monthly_summary.to_csv(
    "data/processed/monthly_sales_dashboard.csv",
    index=False
)

print()
print("Monthly Dashboard Dataset Created!")
print()

print(monthly_summary.head())

print()
print("Rows:", len(monthly_summary))
print("Columns:", len(monthly_summary.columns))