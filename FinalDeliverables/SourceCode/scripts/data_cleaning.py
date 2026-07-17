"""
Data Cleaning Script for Strategic Product Placement Analysis
==============================================================
This script performs the following data cleaning operations:
1. Load raw dataset
2. Inspect data structure and quality
3. Handle missing values
4. Remove duplicate records
5. Standardize column names and categorical values
6. Validate data types
7. Handle outliers
8. Export cleaned dataset

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


def load_raw_data(filepath):
    """
    Load the raw CSV dataset.

    Args:
        filepath (str): Path to the raw CSV file.

    Returns:
        pd.DataFrame: Raw dataframe.
    """
    print("=" * 60)
    print("STEP 1: LOADING RAW DATA")
    print("=" * 60)
    df = pd.read_csv(filepath)
    print(f"  Loaded {len(df)} records with {len(df.columns)} columns.")
    print(f"  Columns: {list(df.columns)}")
    return df


def inspect_data(df):
    """
    Inspect the dataset for quality issues.

    Args:
        df (pd.DataFrame): The dataframe to inspect.
    """
    print("\n" + "=" * 60)
    print("STEP 2: DATA INSPECTION")
    print("=" * 60)

    print("\n--- Data Types ---")
    print(df.dtypes)

    print("\n--- Missing Values ---")
    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing %': missing_pct.round(2)
    })
    print(missing_df[missing_df['Missing Count'] > 0])

    print("\n--- Duplicate Rows ---")
    dup_count = df.duplicated().sum()
    print(f"  Number of duplicate rows: {dup_count}")

    print("\n--- Descriptive Statistics (Numeric) ---")
    print(df.describe())

    print("\n--- Unique Values (Categorical) ---")
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        print(f"  {col}: {df[col].nunique()} unique -> {df[col].unique()}")

    return missing, dup_count


def handle_missing_values(df):
    """
    Handle missing values using appropriate strategies:
    - Numeric columns: fill with median
    - Categorical columns: fill with mode

    Args:
        df (pd.DataFrame): Dataframe with missing values.

    Returns:
        pd.DataFrame: Dataframe with missing values handled.
    """
    print("\n" + "=" * 60)
    print("STEP 3: HANDLING MISSING VALUES")
    print("=" * 60)

    # Handle numeric missing values with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            count = df[col].isnull().sum()
            df[col].fillna(median_val, inplace=True)
            print(f"  Filled {count} missing values in '{col}' with median: {median_val}")

    # Handle categorical missing values with mode
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            count = df[col].isnull().sum()
            df[col].fillna(mode_val, inplace=True)
            print(f"  Filled {count} missing values in '{col}' with mode: {mode_val}")

    print(f"\n  Remaining missing values: {df.isnull().sum().sum()}")
    return df


def remove_duplicates(df):
    """
    Remove duplicate rows from the dataset.

    Args:
        df (pd.DataFrame): Dataframe with potential duplicates.

    Returns:
        pd.DataFrame: Dataframe without duplicates.
    """
    print("\n" + "=" * 60)
    print("STEP 4: REMOVING DUPLICATES")
    print("=" * 60)

    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    removed = before - after
    print(f"  Removed {removed} duplicate rows.")
    print(f"  Records: {before} -> {after}")
    return df


def standardize_data(df):
    """
    Standardize column names and categorical values.

    Args:
        df (pd.DataFrame): Dataframe to standardize.

    Returns:
        pd.DataFrame: Standardized dataframe.
    """
    print("\n" + "=" * 60)
    print("STEP 5: STANDARDIZING DATA")
    print("=" * 60)

    # Standardize column names (strip whitespace, replace spaces)
    df.columns = df.columns.str.strip()
    print(f"  Standardized column names: {list(df.columns)}")

    # Strip whitespace from string columns
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col] = df[col].str.strip()
        print(f"  Stripped whitespace from '{col}'")

    # Standardize Promotion values
    if 'Promotion' in df.columns:
        df['Promotion'] = df['Promotion'].str.capitalize()

    # Standardize Season values
    if 'Season' in df.columns:
        df['Season'] = df['Season'].str.capitalize()

    return df


def validate_data_types(df):
    """
    Validate and convert data types.

    Args:
        df (pd.DataFrame): Dataframe to validate.

    Returns:
        pd.DataFrame: Dataframe with correct data types.
    """
    print("\n" + "=" * 60)
    print("STEP 6: VALIDATING DATA TYPES")
    print("=" * 60)

    # Ensure numeric columns are numeric
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Competitor_Price'] = pd.to_numeric(df['Competitor_Price'], errors='coerce')
    df['Sales_Volume'] = pd.to_numeric(df['Sales_Volume'], errors='coerce').astype('Int64')

    print(f"  Data types after validation:")
    print(f"  {df.dtypes}")
    return df


def handle_outliers(df):
    """
    Detect and handle outliers using IQR method.
    Rather than removing, we cap outliers at the IQR boundaries.

    Args:
        df (pd.DataFrame): Dataframe to process.

    Returns:
        pd.DataFrame: Dataframe with outliers handled.
    """
    print("\n" + "=" * 60)
    print("STEP 7: HANDLING OUTLIERS (IQR Capping)")
    print("=" * 60)

    numeric_cols = ['Price', 'Competitor_Price', 'Sales_Volume']

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers_below = (df[col] < lower).sum()
        outliers_above = (df[col] > upper).sum()

        df[col] = df[col].clip(lower=lower, upper=upper)

        print(f"  {col}: Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}")
        print(f"    Lower bound={lower:.2f}, Upper bound={upper:.2f}")
        print(f"    Capped {outliers_below} below, {outliers_above} above")

    return df


def add_derived_columns(df):
    """
    Add useful derived columns for analysis.

    Args:
        df (pd.DataFrame): Cleaned dataframe.

    Returns:
        pd.DataFrame: Dataframe with derived columns.
    """
    print("\n" + "=" * 60)
    print("STEP 8: ADDING DERIVED COLUMNS")
    print("=" * 60)

    # Price difference between product and competitor
    df['Price_Difference'] = df['Price'] - df['Competitor_Price']
    df['Price_Difference'] = df['Price_Difference'].round(2)
    print("  Added 'Price_Difference' (Price - Competitor_Price)")

    # Price ratio
    df['Price_Ratio'] = (df['Price'] / df['Competitor_Price']).round(4)
    print("  Added 'Price_Ratio' (Price / Competitor_Price)")

    # Sales volume bins
    df['Sales_Category'] = pd.cut(
        df['Sales_Volume'],
        bins=[0, 300, 600, 900, float('inf')],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    print("  Added 'Sales_Category' (binned Sales_Volume)")

    return df


def save_cleaned_data(df, filepath):
    """
    Save the cleaned dataset to CSV.

    Args:
        df (pd.DataFrame): Cleaned dataframe.
        filepath (str): Output file path.
    """
    print("\n" + "=" * 60)
    print("STEP 9: SAVING CLEANED DATA")
    print("=" * 60)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"  Saved cleaned data to: {filepath}")
    print(f"  Final shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")


def main():
    """Main function to orchestrate data cleaning pipeline."""
    print("\n" + "=" * 60)
    print(" STRATEGIC PRODUCT PLACEMENT ANALYSIS ")
    print(" DATA CLEANING PIPELINE ")
    print("=" * 60)

    project_root = get_project_root()
    raw_path = os.path.join(project_root, 'data', 'raw', 'product_positioning_sales.csv')
    clean_path = os.path.join(project_root, 'data', 'cleaned', 'product_positioning_sales_cleaned.csv')

    # Pipeline
    df = load_raw_data(raw_path)
    inspect_data(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = standardize_data(df)
    df = validate_data_types(df)
    df = handle_outliers(df)
    df = add_derived_columns(df)
    save_cleaned_data(df, clean_path)

    print("\n" + "=" * 60)
    print(" DATA CLEANING COMPLETE! ")
    print("=" * 60)
    print(f"\n  Summary:")
    print(f"    Final records: {len(df)}")
    print(f"    Final columns: {len(df.columns)}")
    print(f"    Missing values: {df.isnull().sum().sum()}")
    print(f"    Duplicate rows: {df.duplicated().sum()}")

    return df


if __name__ == '__main__':
    main()
