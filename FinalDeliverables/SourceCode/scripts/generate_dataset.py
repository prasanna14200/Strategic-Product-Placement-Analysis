"""
Dataset Generator for Strategic Product Placement Analysis
==========================================================
Generates a synthetic dataset matching the Kaggle dataset schema:
'Impact of Product Positioning on Sales' by Amit V Kulkarni.

Columns:
    - Product Position: Front of Store, End-cap, Aisle
    - Price: Numeric product price
    - Competitor_Price: Numeric competitor price
    - Promotion: Yes / No
    - Foot_Traffic: High, Medium, Low
    - Consumer_Demographics: Young adults, Families, Seniors, College students
    - Product_Category: Food, Electronics, Clothing
    - Season: Yes / No (Seasonal product flag)
    - Sales_Volume: Number of units sold
"""

import pandas as pd
import numpy as np
import os

# Seed for reproducibility
np.random.seed(42)

# Number of records
N = 500

# Define categorical values
product_positions = ['Front of Store', 'End-cap', 'Aisle']
promotions = ['Yes', 'No']
foot_traffic_levels = ['High', 'Medium', 'Low']
consumer_demographics = ['Young adults', 'Families', 'Seniors', 'College students']
product_categories = ['Food', 'Electronics', 'Clothing']
seasons = ['Yes', 'No']

# Generate random data
data = {
    'Product_Position': np.random.choice(product_positions, N),
    'Price': np.round(np.random.uniform(5.0, 500.0, N), 2),
    'Competitor_Price': np.round(np.random.uniform(5.0, 500.0, N), 2),
    'Promotion': np.random.choice(promotions, N),
    'Foot_Traffic': np.random.choice(foot_traffic_levels, N),
    'Consumer_Demographics': np.random.choice(consumer_demographics, N),
    'Product_Category': np.random.choice(product_categories, N),
    'Season': np.random.choice(seasons, N),
    'Sales_Volume': np.random.randint(50, 1000, N)
}

df = pd.DataFrame(data)

# Add some realistic correlations:
# Products at Front of Store tend to sell more
front_mask = df['Product_Position'] == 'Front of Store'
df.loc[front_mask, 'Sales_Volume'] = df.loc[front_mask, 'Sales_Volume'] + np.random.randint(50, 150, front_mask.sum())

# Promoted products sell more
promo_mask = df['Promotion'] == 'Yes'
df.loc[promo_mask, 'Sales_Volume'] = df.loc[promo_mask, 'Sales_Volume'] + np.random.randint(30, 120, promo_mask.sum())

# High foot traffic increases sales
high_traffic = df['Foot_Traffic'] == 'High'
df.loc[high_traffic, 'Sales_Volume'] = df.loc[high_traffic, 'Sales_Volume'] + np.random.randint(20, 100, high_traffic.sum())

# Electronics tend to be more expensive
elec_mask = df['Product_Category'] == 'Electronics'
df.loc[elec_mask, 'Price'] = df.loc[elec_mask, 'Price'] + np.random.uniform(50, 200, elec_mask.sum())
df.loc[elec_mask, 'Competitor_Price'] = df.loc[elec_mask, 'Competitor_Price'] + np.random.uniform(40, 180, elec_mask.sum())

# Food tends to be cheaper
food_mask = df['Product_Category'] == 'Food'
df.loc[food_mask, 'Price'] = df.loc[food_mask, 'Price'] * 0.5
df.loc[food_mask, 'Competitor_Price'] = df.loc[food_mask, 'Competitor_Price'] * 0.5

# Round prices
df['Price'] = np.round(df['Price'], 2)
df['Competitor_Price'] = np.round(df['Competitor_Price'], 2)

# Introduce a few NaN values for cleaning purposes (about 2%)
nan_indices_price = np.random.choice(N, 10, replace=False)
nan_indices_sales = np.random.choice(N, 5, replace=False)
nan_indices_promo = np.random.choice(N, 3, replace=False)

df.loc[nan_indices_price, 'Price'] = np.nan
df.loc[nan_indices_sales, 'Sales_Volume'] = np.nan
df.loc[nan_indices_promo, 'Promotion'] = np.nan

# Introduce a few duplicate rows
duplicates = df.sample(8, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# Save raw data
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'raw')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'product_positioning_sales.csv')
df.to_csv(output_path, index=False)

print(f"Dataset generated successfully!")
print(f"Shape: {df.shape}")
print(f"Saved to: {output_path}")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nNull values:\n{df.isnull().sum()}")
print(f"\nFirst 5 rows:\n{df.head()}")
