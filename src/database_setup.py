import sqlite3
import pandas as pd

# Connect to SQLite Database
conn = sqlite3.connect("inventory.db")

print("Database Connected Successfully!")

# Load CSV
df = pd.read_csv("data/raw/inventory_dataset.csv")

print("Dataset Loaded!")

# Create Table
df.to_sql(
    "inventory",
    conn,
    if_exists="replace",
    index=False
)

print("Inventory table created!")

# Verify Records
cursor = conn.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM inventory
""")

count = cursor.fetchone()[0]

print("Total Records:", count)

conn.close()

print("Database Saved Successfully!")