import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("data/raw/inventory_dataset.csv")

print("Dataset Loaded Successfully!")
print(df.head())

print("\nDataset Information:")
df.info()

print("\nDescriptive Statistics:")
print(df.describe())

print("\nTotal Units Sold by Product:")

product_sales = (
    df.groupby("Product")["Units_Sold"]
      .sum()
      .sort_values(ascending=False)
)

print(product_sales)


print("\nTotal Units Sold by Warehouse:")

warehouse_sales = (
    df.groupby("Warehouse")["Units_Sold"]
      .sum()
      .sort_values(ascending=False)
)

print(warehouse_sales)


print("\nTotal Units Sold by Supplier:")

supplier_sales = (
    df.groupby("Supplier")["Units_Sold"]
      .sum()
      .sort_values(ascending=False)
)

print(supplier_sales)


print("\nTotal Revenue by Product:")

df["Revenue"] = df["Units_Sold"] * df["Unit_Price"]

product_revenue = (
    df.groupby("Product")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

print(product_revenue)


print("\nTotal Profit by Product:")

df["Profit"] = df["Units_Sold"] * (df["Unit_Price"] - df["Cost_Price"])

product_profit = (
    df.groupby("Product")["Profit"]
      .sum()
      .sort_values(ascending=False)
)

print(product_profit)


print("\nAverage Units Sold (Promotion vs No Promotion):")

promotion_analysis = (
    df.groupby("Promotion")["Units_Sold"]
      .mean()
)

print(promotion_analysis)


print("\nAverage Units Sold (Weekend vs Weekday):")

weekend_sales = (
    df.groupby("Day")["Units_Sold"]
      .mean()
      .sort_values(ascending=False)
)

print(weekend_sales)

print("\nCreating Product Sales Chart...")

#==== PRODUCT SALES CHART ========print("\nCreating Product Sales Chart...")
plt.figure(figsize=(10, 6))
product_sales.plot(kind="bar", color="#4C72B0")
plt.title("Total Units Sold by Product", fontsize=14, fontweight="bold")
plt.xlabel("Product", fontsize=12)
plt.ylabel("Units Sold", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.xticks(rotation=0, fontsize=10)
plt.tight_layout()
plt.savefig("reports/product_sales_chart.png", dpi=300, bbox_inches="tight")
plt.show()

print("\nCreating Revenue Chart...")
plt.figure(figsize=(10, 6))
product_revenue.plot(kind="bar", color="#55A868")
plt.title("Total Revenue by Product", fontsize=14, fontweight="bold")
plt.xlabel("Product", fontsize=12)
plt.ylabel("Revenue (₹)", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.xticks(rotation=0, fontsize=10)
plt.tight_layout()
plt.savefig("reports/product_revenue_chart.png", dpi=300, bbox_inches="tight")
plt.show()

print("\nCreating Profit Chart...")
plt.figure(figsize=(10, 6))
product_profit.plot(kind="bar", color="#C44E52")
plt.title("Total Profit by Product", fontsize=14, fontweight="bold")
plt.xlabel("Product", fontsize=12)
plt.ylabel("Profit (₹)", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.xticks(rotation=0, fontsize=10)
plt.tight_layout()
plt.savefig("reports/product_profit_chart.png", dpi=300, bbox_inches="tight")
plt.show()

print("\nCreating Warehouse Sales Chart...")
plt.figure(figsize=(10, 6))
warehouse_sales.plot(kind="bar", color="#8172B2")
plt.title("Total Units Sold by Warehouse", fontsize=14, fontweight="bold")
plt.xlabel("Warehouse", fontsize=12)
plt.ylabel("Units Sold", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.xticks(rotation=0, fontsize=10)
plt.tight_layout()
plt.savefig("reports/warehouse_sales_chart.png", dpi=300, bbox_inches="tight")
plt.show()