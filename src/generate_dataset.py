import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

products = [
    "Laptop",
    "Smartphone",
    "Tablet",
    "Keyboard",
    "Mouse",
    "Monitor",
    "Printer",
    "Headphones",
    "Router",
    "Webcam"
]

categories = {
    "Laptop": "Electronics",
    "Smartphone": "Electronics",
    "Tablet": "Electronics",
    "Keyboard": "Accessories",
    "Mouse": "Accessories",
    "Monitor": "Electronics",
    "Printer": "Office",
    "Headphones": "Accessories",
    "Router": "Networking",
    "Webcam": "Accessories"
}

warehouses = [
    "Hyderabad",
    "Bengaluru",
    "Chennai",
    "Mumbai",
    "Delhi"
]

suppliers = [
    "TechSource Pvt Ltd",
    "Global Electronics",
    "Prime Supply Co",
    "Smart Distribution",
    "Rapid Logistics"
]

# Generate date range
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

dates = pd.date_range(start=start_date, end=end_date)

def create_record(date, product):
    warehouse = random.choice(warehouses)
    supplier = random.choice(suppliers)

    min_sales, max_sales = product_demand[product]
    units_sold = random.randint(min_sales, max_sales)

    # Add yearly sales trend
    day_of_year = date.timetuple().tm_yday
    trend_factor = 1 + (day_of_year / 365) * 0.30
    units_sold = int(units_sold * trend_factor)

    # Weekend demand boost
    day_name = date.strftime("%A")
    if day_name in ["Saturday", "Sunday"]:
        units_sold = int(units_sold * 1.20)

    # Festival season boost
    if date.month in [10, 11, 12]:
        units_sold = int(units_sold * 1.25)

    # Promotion effect
    promotion = random.random() < 0.20
    if promotion:
        units_sold = int(units_sold * 1.15)

    # Random daily variation
    noise = random.randint(-5, 5)
    units_sold = max(1, units_sold + noise)

    price = product_info[product]["price"]
    cost = product_info[product]["cost"]
    lead_time = product_info[product]["lead_time"]

    # ------------------------------
    # Generate realistic stock levels
    # ------------------------------

    chance = random.random()

    if chance < 0.15:
        # 15% Low Stock
        current_stock = random.randint(20, 120)
    elif chance < 0.85:
        # 70% Normal Stock
        current_stock = random.randint(150, 350)
    else:
        # 15% Overstock
        current_stock = random.randint(500, 900)

    return {
        "Date": date.date(),
        "Day": day_name,
        "Product": product,
        "Category": categories[product],
        "Warehouse": warehouse,
        "Supplier": supplier,
        "Promotion": promotion,
        "Units_Sold": units_sold,
        "Current_Stock": current_stock,
        "Unit_Price": price,
        "Cost_Price": cost,
        "Lead_Time_Days": lead_time,
    }


product_info = {
    "Laptop": {"price": 65000, "cost": 52000, "lead_time": 7},
    "Smartphone": {"price": 35000, "cost": 28000, "lead_time": 5},
    "Tablet": {"price": 25000, "cost": 20000, "lead_time": 6},
    "Keyboard": {"price": 1500, "cost": 1000, "lead_time": 3},
    "Mouse": {"price": 800, "cost": 500, "lead_time": 2},
    "Monitor": {"price": 12000, "cost": 9000, "lead_time": 5},
    "Printer": {"price": 18000, "cost": 14500, "lead_time": 8},
    "Headphones": {"price": 3000, "cost": 2200, "lead_time": 4},
    "Router": {"price": 4500, "cost": 3200, "lead_time": 4},
    "Webcam": {"price": 2500, "cost": 1800, "lead_time": 3}
}

product_demand = {
    "Laptop": (5, 20),
    "Smartphone": (20, 60),
    "Tablet": (10, 30),
    "Keyboard": (15, 50),
    "Mouse": (30, 80),
    "Monitor": (8, 25),
    "Printer": (3, 12),
    "Headphones": (20, 70),
    "Router": (10, 35),
    "Webcam": (8, 30)
}

#for date in dates:
#   print(date)
records = []

# Generate records for one day
# Generate records for every day and every product
for date in dates:

    for product in products:

        record = create_record(date, product)
        records.append(record)
  # Convert list to DataFrame
df = pd.DataFrame(records)      

# Display the DataFrame
# Save dataset
df.to_csv("data/raw/inventory_dataset.csv", index=False)

print(df.head())
print()
print("Total Records:", len(df))
print()
print("Dataset saved successfully!")