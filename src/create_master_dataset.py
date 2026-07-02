import pandas as pd

# -----------------------------
# Load Raw Dataset
# -----------------------------
df = pd.read_csv("data/raw/inventory_dataset.csv")

print("Dataset Loaded Successfully!")

# -----------------------------
# Product Summary
# -----------------------------
product_summary = (
    df.groupby("Product")
      .agg({
          "Category": "first",
          "Warehouse": lambda x: x.mode()[0],
          "Supplier": lambda x: x.mode()[0],
          "Units_Sold": "mean",
          "Current_Stock": "mean",
          "Unit_Price": "mean",
          "Cost_Price": "mean",
          "Lead_Time_Days": "mean"
      })
      .round(2)
      .reset_index()
)

# -----------------------------
# Derived KPIs
# -----------------------------
product_summary["Annual_Demand"] = (
    product_summary["Units_Sold"] * 365
).round()

product_summary["Annual_Revenue"] = (
    product_summary["Annual_Demand"] *
    product_summary["Unit_Price"]
).round()

product_summary["Annual_Profit"] = (
    product_summary["Annual_Demand"] *
    (
        product_summary["Unit_Price"] -
        product_summary["Cost_Price"]
    )
).round()

product_summary["Reorder_Point"] = (
    product_summary["Units_Sold"] *
    product_summary["Lead_Time_Days"]
).round()

product_summary["Safety_Stock"] = (
    product_summary["Units_Sold"] * 2
).round()

product_summary["Final_Reorder_Point"] = (
    product_summary["Reorder_Point"] +
    product_summary["Safety_Stock"]
)

product_summary["Inventory_Status"] = "Normal"

product_summary.loc[
    product_summary["Current_Stock"] <
    product_summary["Final_Reorder_Point"],
    "Inventory_Status"
] = "Low Stock"

product_summary.loc[
    product_summary["Current_Stock"] >
    product_summary["Final_Reorder_Point"] * 2,
    "Inventory_Status"
] = "Overstock"

ORDERING_COST = 500
HOLDING_RATE = 0.20

holding_cost = (
    product_summary["Cost_Price"] *
    HOLDING_RATE
)

product_summary["EOQ"] = (
    (
        (
            2 *
            product_summary["Annual_Demand"] *
            ORDERING_COST
        )
        /
        holding_cost
    ) ** 0.5
).round()

product_summary["Inventory_Value"] = (
    product_summary["Current_Stock"] *
    product_summary["Cost_Price"]
).round()

product_summary["Days_of_Stock"] = (
    product_summary["Current_Stock"] /
    product_summary["Units_Sold"]
).round(1)

# -----------------------------
# Save Dataset
# -----------------------------
product_summary.to_csv(
    "data/processed/master_inventory_dashboard.csv",
    index=False
)

print()
print("Master Dashboard Dataset Created!")
print()
print(product_summary.head())