from pathlib import Path

import pandas as pd

df=pd.read_csv("data/raw/sales.csv")

base_dir = Path(__file__).resolve().parent.parent
raw_path = base_dir/"data/raw"/"sales.csv"

df = pd.read_csv(raw_path)

print("Form (rows,columns):", df.shape)

print("\nMisses:")
print(df.isna().sum())

print("\nFullDoubles:", df.duplicated().sum())

print("\nUniqueCountries:", df["country"].unique())

print("\nUniqueCategories:", df["category"].unique())

print("\nQuantityStatistics:")
print(df["quantity"].describe())

print("\nColumnTypes:")
print(df.dtypes)