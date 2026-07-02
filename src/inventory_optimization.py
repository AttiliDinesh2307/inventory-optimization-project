import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/inventory_dataset.csv")

print("Dataset Loaded Successfully!")
print(df.head())

print("\nAverage Daily Demand Per Product:")

average_demand = (
    df.groupby("Product")["Units_Sold"]
      .mean()
      .round(2)
)

print(average_demand)

print("\nCalculating Reorder Point...")

product_summary = (
    df.groupby("Product")
      .agg({
          "Units_Sold": "mean",
          "Lead_Time_Days": "mean",
          "Current_Stock": "mean",
          "Cost_Price": "mean",
          "Unit_Price": "mean"
      })
      .round(2)
)

product_summary["Reorder_Point"] = (
    product_summary["Units_Sold"] *
    product_summary["Lead_Time_Days"]
).round()

# Calculate Safety Stock
product_summary["Safety_Stock"] = (
    product_summary["Units_Sold"] * 2
).round()

# Final Reorder Point
product_summary["Final_Reorder_Point"] = (
    product_summary["Reorder_Point"] +
    product_summary["Safety_Stock"]
)


# Inventory Status
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

# ---------------------------------
# Economic Order Quantity (EOQ)
# ---------------------------------

ORDERING_COST = 500      # ₹ per order
HOLDING_RATE = 0.20      # 20% of unit cost per year

annual_demand = product_summary["Units_Sold"] * 365

holding_cost = product_summary["Cost_Price"] * HOLDING_RATE

product_summary["EOQ"] = (
    ((2 * annual_demand * ORDERING_COST) / holding_cost) ** 0.5
).round()

# ---------------------------------
# Additional Inventory KPIs
# ---------------------------------

# Annual Demand
product_summary["Annual_Demand"] = annual_demand.round()

# Annual Revenue
product_summary["Annual_Revenue"] = (
    product_summary["Annual_Demand"] *
    product_summary["Unit_Price"]
).round()

# Annual Profit
product_summary["Annual_Profit"] = (
    product_summary["Annual_Demand"] *
    (
        product_summary["Unit_Price"] -
        product_summary["Cost_Price"]
    )
).round()

# Holding Cost per Unit
product_summary["Holding_Cost"] = holding_cost.round()

# Average Inventory Value
product_summary["Inventory_Value"] = (
    product_summary["Current_Stock"] *
    product_summary["Cost_Price"]
).round()

# Days of Stock Available
product_summary["Days_of_Stock"] = (
    product_summary["Current_Stock"] /
    product_summary["Units_Sold"]
).round(1)

product_summary = product_summary.round({
    "Units_Sold": 0,
    "Lead_Time_Days": 0,
    "Current_Stock": 0,
    "Cost_Price": 0,
    "Unit_Price": 0
})

# ---------------------------------
# Replenishment Recommendation
# ---------------------------------

product_summary["Recommended_Order_Qty"] = 0

mask = (
    product_summary["Current_Stock"] <
    product_summary["Final_Reorder_Point"]
)

product_summary.loc[
    mask,
    "Recommended_Order_Qty"
] = product_summary.loc[
    mask,
    "EOQ"
]

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

print("\nInventory Optimization Report")
print(product_summary)

# Save report
product_summary.to_csv(
    "data/processed/inventory_optimization_report.csv",
    index=True
)

print("\nInventory optimization report saved successfully!")