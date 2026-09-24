import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Make the generated data reproducible
random.seed(42)
np.random.seed(42)

# Sample values
restaurants = [
    "Pizza Hut",
    "KFC",
    "Burger King",
    "Dominos",
    "Subway"
]

categories = [
    "Fast Food",
    "Pizza",
    "Burger",
    "Sandwich"
]

countries = [
    "Sri Lanka",
    "India",
    "Australia",
    "Singapore"
]

records = []

start_date = datetime(2024, 1, 1)

# Generate 10,500 records
for i in range(1, 10501):

    date = start_date + timedelta(
        days=random.randint(0, 900)
    )

    record = {
        "transaction_id": i,
        "customer_name": f"Customer_{random.randint(1, 3000)}",
        "restaurant": random.choice(restaurants),
        "category": random.choice(categories),
        "country": random.choice(countries),
        "quantity": random.randint(1, 10),
        "unit_price": round(random.uniform(500, 5000), 2),
        "rating": round(random.uniform(1, 5), 1),
        "transaction_date": date.strftime("%Y-%m-%d")
    }

    records.append(record)

# Convert to DataFrame
df = pd.DataFrame(records)

# --------------------------------
# Introduce dirty data
# --------------------------------

# Missing values
df.loc[10, "customer_name"] = None
df.loc[100, "country"] = None
df.loc[500, "rating"] = None

# Inconsistent formatting
df.loc[20, "country"] = "sri lanka"
df.loc[21, "country"] = "SRI LANKA"
df.loc[22, "category"] = "fast food"

# Invalid values
df.loc[30, "unit_price"] = -500
df.loc[40, "rating"] = 6

# Add duplicate records
df = pd.concat([
    df,
    df.iloc[100:120]
])

# Make sure the output directory exists
os.makedirs("data/raw", exist_ok=True)

# Save dataset
file_path = "data/raw/restaurant_sales.csv"

df.to_csv(
    file_path,
    index=False
)

print("Dataset generated successfully!")
print(f"Total records: {len(df)}")
print(f"File: {file_path}")