"""
Kaggle Dataset Download Script
==============================
Downloads the official Kaggle dataset:
'Impact of Product Positioning on Sales' by Amit V Kulkarni

Dataset URL:
https://www.kaggle.com/datasets/amitvkulkarni/impact-of-product-positioning-on-sales

Prerequisites:
1. Create a Kaggle account at https://www.kaggle.com
2. Go to Account Settings -> API -> Create New Token
3. Save kaggle.json to:
   - Windows: C:\\Users\\<username>\\.kaggle\\kaggle.json
   - Linux/Mac: ~/.kaggle/kaggle.json
4. pip install kaggle

Usage:
    python scripts/download_dataset.py
"""

import os
import shutil
import sys


def get_project_root():
    """Return project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def download_from_kaggle():
    """Download dataset from Kaggle API."""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        print("ERROR: kaggle package not installed.")
        print("Run: pip install kaggle")
        sys.exit(1)

    project_root = get_project_root()
    raw_dir = os.path.join(project_root, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)

    api = KaggleApi()
    api.authenticate()

    dataset = 'amitvkulkarni/impact-of-product-positioning-on-sales'
    print(f"Downloading dataset: {dataset}")
    api.dataset_download_files(dataset, path=raw_dir, unzip=True)

    # Normalize filename to project convention
    for fname in os.listdir(raw_dir):
        if fname.endswith('.csv') and fname != 'product_positioning_sales.csv':
            src = os.path.join(raw_dir, fname)
            dst = os.path.join(raw_dir, 'product_positioning_sales.csv')
            if os.path.exists(dst):
                os.remove(dst)
            shutil.move(src, dst)
            print(f"Renamed to: product_positioning_sales.csv")
            break

    print("Download complete!")
    print(f"Files saved to: {raw_dir}")


def main():
    """Main entry point."""
    print("=" * 60)
    print(" KAGGLE DATASET DOWNLOAD ")
    print(" Impact of Product Positioning on Sales ")
    print("=" * 60)

    kaggle_json = os.path.expanduser('~/.kaggle/kaggle.json')
    if not os.path.exists(kaggle_json):
        print("\nWARNING: kaggle.json not found.")
        print("Manual download steps:")
        print("  1. Visit https://www.kaggle.com/datasets/amitvkulkarni/impact-of-product-positioning-on-sales")
        print("  2. Click Download")
        print("  3. Extract CSV to data/raw/product_positioning_sales.csv")
        print("  4. Run: python scripts/data_cleaning.py")
        sys.exit(1)

    download_from_kaggle()


if __name__ == '__main__':
    main()
