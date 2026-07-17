"""
Data Analysis Script for Strategic Product Placement Analysis
==============================================================
This script performs exploratory data analysis (EDA) on the cleaned dataset,
generating insights and summary statistics used in the Tableau visualizations.

Analysis performed:
1. Descriptive statistics
2. Average Sales Volume vs Product Category
3. Average Sales Volume by Product Category by Product Position
4. Average Sales Volume by Product Category by Season
5. Competitor Price vs Price correlation
6. Consumer Demographics vs Sales Volume
7. Foot Traffic vs Average Sales Volume
8. Product Category vs Price
9. Promotion impact on Price and Sales Volume
10. KPI calculations

Author: Data Analysis Team
Date: 2026
"""

import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')


def get_project_root():
    """Get the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_cleaned_data():
    """Load the cleaned dataset."""
    project_root = get_project_root()
    filepath = os.path.join(project_root, 'data', 'cleaned', 'product_positioning_sales_cleaned.csv')
    df = pd.read_csv(filepath)
    print(f"Loaded cleaned dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def descriptive_statistics(df):
    """Generate descriptive statistics."""
    print("\n" + "=" * 60)
    print("1. DESCRIPTIVE STATISTICS")
    print("=" * 60)

    print("\n--- Numeric Summary ---")
    print(df[['Price', 'Competitor_Price', 'Sales_Volume']].describe())

    print("\n--- Categorical Distribution ---")
    for col in ['Product_Position', 'Promotion', 'Foot_Traffic',
                'Consumer_Demographics', 'Product_Category', 'Season']:
        if col in df.columns:
            print(f"\n{col}:")
            print(df[col].value_counts())


def avg_sales_by_category(df):
    """Analysis: Average Sales Volume vs Product Category."""
    print("\n" + "=" * 60)
    print("2. AVG SALES VOLUME vs PRODUCT CATEGORY")
    print("=" * 60)

    result = df.groupby('Product_Category')['Sales_Volume'].agg(['mean', 'median', 'std', 'count'])
    result.columns = ['Avg_Sales', 'Median_Sales', 'Std_Sales', 'Count']
    result = result.round(2)
    print(result)
    return result


def avg_sales_by_category_position(df):
    """Analysis: Average Sales Volume by Product Category by Product Position."""
    print("\n" + "=" * 60)
    print("3. AVG SALES BY CATEGORY × POSITION")
    print("=" * 60)

    result = df.groupby(['Product_Category', 'Product_Position'])['Sales_Volume'].mean().round(2)
    pivot = result.unstack()
    print(pivot)
    return pivot


def avg_sales_by_category_season(df):
    """Analysis: Average Sales Volume by Product Category by Season."""
    print("\n" + "=" * 60)
    print("4. AVG SALES BY CATEGORY × SEASON")
    print("=" * 60)

    result = df.groupby(['Product_Category', 'Season'])['Sales_Volume'].mean().round(2)
    pivot = result.unstack()
    print(pivot)
    return pivot


def price_vs_competitor_price(df):
    """Analysis: Competitor Price vs Price correlation."""
    print("\n" + "=" * 60)
    print("5. COMPETITOR PRICE vs PRICE")
    print("=" * 60)

    correlation = df['Price'].corr(df['Competitor_Price'])
    print(f"  Pearson Correlation: {correlation:.4f}")

    avg_price = df['Price'].mean()
    avg_comp = df['Competitor_Price'].mean()
    print(f"  Average Product Price: ${avg_price:.2f}")
    print(f"  Average Competitor Price: ${avg_comp:.2f}")
    print(f"  Average Price Difference: ${(avg_price - avg_comp):.2f}")

    return correlation


def demographics_vs_sales(df):
    """Analysis: Consumer Demographics vs Sales Volume."""
    print("\n" + "=" * 60)
    print("6. CONSUMER DEMOGRAPHICS vs SALES VOLUME")
    print("=" * 60)

    result = df.groupby('Consumer_Demographics')['Sales_Volume'].agg(['mean', 'median', 'sum', 'count'])
    result.columns = ['Avg_Sales', 'Median_Sales', 'Total_Sales', 'Count']
    result = result.round(2).sort_values('Avg_Sales', ascending=False)
    print(result)
    return result


def foot_traffic_vs_sales(df):
    """Analysis: Foot Traffic vs Average Sales Volume."""
    print("\n" + "=" * 60)
    print("7. FOOT TRAFFIC vs AVG SALES VOLUME")
    print("=" * 60)

    result = df.groupby('Foot_Traffic')['Sales_Volume'].agg(['mean', 'median', 'std', 'count'])
    result.columns = ['Avg_Sales', 'Median_Sales', 'Std_Sales', 'Count']
    result = result.round(2)
    # Reorder
    order = ['High', 'Medium', 'Low']
    result = result.reindex(order)
    print(result)
    return result


def category_vs_price(df):
    """Analysis: Product Category vs Price."""
    print("\n" + "=" * 60)
    print("8. PRODUCT CATEGORY vs PRICE")
    print("=" * 60)

    result = df.groupby('Product_Category')['Price'].agg(['mean', 'median', 'min', 'max', 'std'])
    result.columns = ['Avg_Price', 'Median_Price', 'Min_Price', 'Max_Price', 'Std_Price']
    result = result.round(2)
    print(result)
    return result


def promotion_impact(df):
    """Analysis: Promotion vs Product Category on Price and Sales Volume."""
    print("\n" + "=" * 60)
    print("9. PROMOTION IMPACT ON PRICE & SALES VOLUME")
    print("=" * 60)

    # Sales by Promotion status
    promo_sales = df.groupby('Promotion')['Sales_Volume'].mean().round(2)
    print("\nAvg Sales by Promotion Status:")
    print(promo_sales)

    # Sales by Promotion × Category
    promo_cat = df.groupby(['Promotion', 'Product_Category']).agg({
        'Sales_Volume': 'mean',
        'Price': 'mean'
    }).round(2)
    print("\nAvg Sales & Price by Promotion × Category:")
    print(promo_cat)

    # Promotion lift
    if 'Yes' in promo_sales.index and 'No' in promo_sales.index:
        lift = ((promo_sales['Yes'] - promo_sales['No']) / promo_sales['No']) * 100
        print(f"\nPromotion Sales Lift: {lift:.2f}%")

    return promo_cat


def calculate_kpis(df):
    """Calculate key performance indicators (KPIs)."""
    print("\n" + "=" * 60)
    print("10. KEY PERFORMANCE INDICATORS (KPIs)")
    print("=" * 60)

    kpis = {
        'Total Records': len(df),
        'Total Sales Volume': int(df['Sales_Volume'].sum()),
        'Average Sales Volume': round(df['Sales_Volume'].mean(), 2),
        'Average Price': round(df['Price'].mean(), 2),
        'Average Competitor Price': round(df['Competitor_Price'].mean(), 2),
        'Promotion Rate (%)': round((df['Promotion'] == 'Yes').sum() / len(df) * 100, 2),
        'Top Category (by Avg Sales)': df.groupby('Product_Category')['Sales_Volume'].mean().idxmax(),
        'Best Position (by Avg Sales)': df.groupby('Product_Position')['Sales_Volume'].mean().idxmax(),
        'Top Demographic (by Avg Sales)': df.groupby('Consumer_Demographics')['Sales_Volume'].mean().idxmax(),
    }

    for key, val in kpis.items():
        print(f"  {key}: {val}")

    return kpis


def main():
    """Run complete data analysis pipeline."""
    print("\n" + "=" * 60)
    print(" STRATEGIC PRODUCT PLACEMENT ANALYSIS ")
    print(" EXPLORATORY DATA ANALYSIS ")
    print("=" * 60)

    df = load_cleaned_data()

    descriptive_statistics(df)
    avg_sales_by_category(df)
    avg_sales_by_category_position(df)
    avg_sales_by_category_season(df)
    price_vs_competitor_price(df)
    demographics_vs_sales(df)
    foot_traffic_vs_sales(df)
    category_vs_price(df)
    promotion_impact(df)
    kpis = calculate_kpis(df)

    print("\n" + "=" * 60)
    print(" ANALYSIS COMPLETE! ")
    print("=" * 60)

    return df, kpis


if __name__ == '__main__':
    main()
