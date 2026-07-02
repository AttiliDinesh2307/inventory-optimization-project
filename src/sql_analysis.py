import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("inventory.db")

print("Connected to Database!")

# -----------------------------
# Query 1: Top Selling Products
# -----------------------------
query = """
SELECT
    Product,
    SUM(Units_Sold) AS Total_Units_Sold
FROM inventory
GROUP BY Product
ORDER BY Total_Units_Sold DESC;
"""

result = pd.read_sql(query, conn)

print("\n========== TOP SELLING PRODUCTS ==========")
print(result)


# -----------------------------
# Query 2: Revenue by Product
# -----------------------------
query = """
SELECT
    Product,
    SUM(Units_Sold * Unit_Price) AS Total_Revenue
FROM inventory
GROUP BY Product
ORDER BY Total_Revenue DESC;
"""

result = pd.read_sql(query, conn)

print("\n========== REVENUE BY PRODUCT ==========")
print(result)

# -----------------------------
# Query 3: Profit by Product
# -----------------------------
query = """
SELECT
    Product,
    SUM(Units_Sold * (Unit_Price - Cost_Price)) AS Total_Profit
FROM inventory
GROUP BY Product
ORDER BY Total_Profit DESC;
"""

result = pd.read_sql(query, conn)

print("\n========== PROFIT BY PRODUCT ==========")
print(result)

# -----------------------------
# Query 4: Warehouse Performance
# -----------------------------
query = """
SELECT
    Warehouse,
    SUM(Units_Sold) AS Total_Units_Sold
FROM inventory
GROUP BY Warehouse
ORDER BY Total_Units_Sold DESC;
"""

result = pd.read_sql(query, conn)

print("\n========== WAREHOUSE PERFORMANCE ==========")
print(result)

# -----------------------------
# Query 5: Supplier Performance
# -----------------------------
query = """
SELECT
    Supplier,
    SUM(Units_Sold) AS Total_Units_Sold
FROM inventory
GROUP BY Supplier
ORDER BY Total_Units_Sold DESC;
"""

result = pd.read_sql(query, conn)

print("\n========== SUPPLIER PERFORMANCE ==========")
print(result)

# -----------------------------
# Query 6: Category Performance
# -----------------------------
query = """
SELECT
    Category,
    SUM(Units_Sold) AS Total_Units_Sold,
    SUM(Units_Sold * Unit_Price) AS Total_Revenue
FROM inventory
GROUP BY Category
ORDER BY Total_Revenue DESC;
"""

result = pd.read_sql(query, conn)

print("\n========== CATEGORY PERFORMANCE ==========")
print(result)

# -----------------------------
# Query 7: Promotion Impact
# -----------------------------
query = """
SELECT
    Promotion,
    ROUND(AVG(Units_Sold),2) AS Average_Units_Sold
FROM inventory
GROUP BY Promotion;
"""

result = pd.read_sql(query, conn)

print("\n========== PROMOTION IMPACT ==========")
print(result)

# -----------------------------
# Query 8: Monthly Sales Trend
# -----------------------------
query = """
SELECT
    strftime('%m', Date) AS Month,
    SUM(Units_Sold) AS Total_Units_Sold
FROM inventory
GROUP BY Month
ORDER BY Month;
"""

result = pd.read_sql(query, conn)

print("\n========== MONTHLY SALES TREND ==========")
print(result)

# -----------------------------
# Query 9: Revenue by Warehouse
# -----------------------------
query = """
SELECT
    Warehouse,
    SUM(Units_Sold * Unit_Price) AS Total_Revenue
FROM inventory
GROUP BY Warehouse
ORDER BY Total_Revenue DESC;
"""

result = pd.read_sql(query, conn)

print("\n========== REVENUE BY WAREHOUSE ==========")
print(result)

# -----------------------------
# Query 10: Average Lead Time
# -----------------------------
query = """
SELECT
    Product,
    ROUND(AVG(Lead_Time_Days),2) AS Average_Lead_Time
FROM inventory
GROUP BY Product
ORDER BY Average_Lead_Time DESC;
"""

result = pd.read_sql(query, conn)

print("\n========== AVERAGE LEAD TIME ==========")
print(result)

# -----------------------------
# Query 11: Inventory Value
# -----------------------------
query = """
SELECT
    Product,
    ROUND(AVG(Current_Stock * Cost_Price),2) AS Inventory_Value
FROM inventory
GROUP BY Product
ORDER BY Inventory_Value DESC;
"""

result = pd.read_sql(query, conn)

print("\n========== INVENTORY VALUE ==========")
print(result)

conn.close()