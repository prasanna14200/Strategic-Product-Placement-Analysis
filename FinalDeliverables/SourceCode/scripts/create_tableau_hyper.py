"""
Create Tableau Hyper Extract (.hyper)
======================================
Uses the official Tableau Hyper API to convert the cleaned CSV into a
Tableau-compatible .hyper extract. Connect to this file from Tableau Desktop
2026 / Tableau Public Edition 2026 when building the workbook.

This script does NOT generate workbook XML (.twb). Workbooks must be built
interactively in Tableau Desktop — see tableau/Workbook_Build_Guide.md.

Install:
    pip install tableauhyperapi pandas

Usage:
    python scripts/create_tableau_hyper.py
"""

import os
import sys

import pandas as pd

try:
    from tableauhyperapi import (
        ConnectionContext,
        CreateMode,
        HyperProcess,
        Inserter,
        NOT_NULLABLE,
        NULLABLE,
        SqlType,
        TableDefinition,
        TableName,
        Telemetry,
    )
except ImportError:
    print("ERROR: tableauhyperapi is not installed.")
    print("Run: pip install tableauhyperapi")
    sys.exit(1)


def get_project_root():
    """Return the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_table_definition():
    """Define the Hyper table schema matching the cleaned dataset."""
    return TableDefinition(
        table_name=TableName('Extract', 'ProductPositioningSales'),
        columns=[
            TableDefinition.Column('Product_Position', SqlType.text(), NOT_NULLABLE),
            TableDefinition.Column('Price', SqlType.double(), NOT_NULLABLE),
            TableDefinition.Column('Competitor_Price', SqlType.double(), NOT_NULLABLE),
            TableDefinition.Column('Promotion', SqlType.text(), NOT_NULLABLE),
            TableDefinition.Column('Foot_Traffic', SqlType.text(), NOT_NULLABLE),
            TableDefinition.Column('Consumer_Demographics', SqlType.text(), NOT_NULLABLE),
            TableDefinition.Column('Product_Category', SqlType.text(), NOT_NULLABLE),
            TableDefinition.Column('Season', SqlType.text(), NOT_NULLABLE),
            TableDefinition.Column('Sales_Volume', SqlType.big_int(), NOT_NULLABLE),
            TableDefinition.Column('Price_Difference', SqlType.double(), NOT_NULLABLE),
            TableDefinition.Column('Price_Ratio', SqlType.double(), NOT_NULLABLE),
            TableDefinition.Column('Sales_Category', SqlType.text(), NULLABLE),
        ],
    )


def load_cleaned_dataframe(project_root):
    """Load and validate the cleaned CSV."""
    csv_path = os.path.join(
        project_root, 'data', 'cleaned', 'product_positioning_sales_cleaned.csv'
    )
    if not os.path.exists(csv_path):
        print(f"ERROR: Cleaned CSV not found at {csv_path}")
        print("Run: python scripts/data_cleaning.py")
        sys.exit(1)

    df = pd.read_csv(csv_path)
    df['Sales_Volume'] = df['Sales_Volume'].astype('int64')
    return df, csv_path


def dataframe_to_rows(df):
    """Convert DataFrame rows to tuples for Hyper Inserter."""
    rows = []
    for record in df.itertuples(index=False):
        rows.append(tuple(
            None if (isinstance(value, float) and pd.isna(value)) else value
            for value in record
        ))
    return rows


def create_hyper_extract(df, output_path):
    """Write a valid .hyper file using the Tableau Hyper API."""
    table = build_table_definition()
    rows = dataframe_to_rows(df)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with ConnectionContext(
            hyper.endpoint,
            CreateMode.CREATE_AND_REPLACE,
            database=output_path,
        ) as connection:
            connection.catalog.create_table(table)
            with Inserter(connection, table) as inserter:
                inserter.add_rows(rows)
                inserter.execute()
            count = connection.execute_scalar_query(
                f'SELECT COUNT(*) FROM {table.table_name}'
            )

    return count


def main():
    """Main entry point."""
    print("=" * 60)
    print(" TABLEAU HYPER EXTRACT GENERATOR ")
    print(" Tableau Hyper API (official) ")
    print("=" * 60)

    project_root = get_project_root()
    df, csv_path = load_cleaned_dataframe(project_root)
    output_path = os.path.join(
        project_root, 'tableau', 'data', 'product_positioning_sales.hyper'
    )

    print(f"\n  Source CSV : {csv_path}")
    print(f"  Rows       : {len(df)}")
    print(f"  Columns    : {len(df.columns)}")
    print(f"  Output     : {output_path}\n")

    row_count = create_hyper_extract(df, output_path)

    print("Hyper extract created successfully!")
    print(f"  Verified rows in .hyper: {row_count}")
    print("\nNext steps:")
    print("  1. Open Tableau Desktop 2026 / Tableau Public Edition 2026")
    print("  2. Connect to: tableau/data/product_positioning_sales.hyper")
    print("  3. Follow: tableau/Workbook_Build_Guide.md")


if __name__ == '__main__':
    main()
