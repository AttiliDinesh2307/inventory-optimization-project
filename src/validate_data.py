import pandas as pd

# Load the dataset
df = pd.read_csv("data/raw/inventory_dataset.csv")

# Display basic information
print("Dataset Loaded Successfully!")
print()

print("Number of Rows:", df.shape[0])
print("Number of Columns:", df.shape[1])

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)