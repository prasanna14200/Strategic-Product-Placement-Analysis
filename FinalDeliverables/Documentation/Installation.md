# Installation Guide

## Strategic Product Placement Analysis

Step-by-step instructions to set up the project on your local machine.

---

## Prerequisites

| Requirement | Minimum Version |
|-------------|-----------------|
| Python | 3.10+ |
| pip | 23.0+ |
| Git | 2.30+ (optional) |
| Tableau Desktop | 2024.1+ (for workbook editing) |
| Web Browser | Chrome, Firefox, or Edge (latest) |

---

## Step 1: Clone or Download Project

### Option A: Git Clone
```bash
git clone <repository-url>
cd dataanalyis
```

### Option B: Download ZIP
Extract the project to your desired directory and navigate into it:
```bash
cd dataanalyis
```

---

## Step 2: Create Virtual Environment (Recommended)

### Windows
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Dependencies Installed

| Package | Purpose |
|---------|---------|
| flask | Web framework |
| pandas | Data manipulation |
| numpy | Numerical operations |
| gunicorn | Production WSGI server |
| python-dotenv | Environment variable management |

### Optional: Kaggle API
```bash
pip install kaggle
```

---

## Step 4: Download Dataset

### Option A: Kaggle API (Recommended)

1. Create account at https://www.kaggle.com
2. Go to **Account → API → Create New Token**
3. Save `kaggle.json` to:
   - **Windows:** `C:\Users\<username>\.kaggle\kaggle.json`
   - **macOS/Linux:** `~/.kaggle/kaggle.json`
4. Run:
   ```bash
   python scripts/download_dataset.py
   ```

### Option B: Manual Download

1. Visit https://www.kaggle.com/datasets/amitvkulkarni/impact-of-product-positioning-on-sales
2. Click **Download**
3. Extract CSV to `data/raw/product_positioning_sales.csv`

### Option C: Generate Synthetic Data (Development)
```bash
python scripts/generate_dataset.py
```

---

## Step 5: Run Data Pipeline

```bash
# Clean the data
python scripts/data_cleaning.py

# Run exploratory analysis
python scripts/data_analysis.py
```

Expected output:
- Cleaned CSV at `data/cleaned/product_positioning_sales_cleaned.csv`
- Console output with KPIs and analysis tables

---

## Step 6: Create Tableau Hyper Extract

```bash
python scripts/create_tableau_hyper.py
```

This uses the **official Tableau Hyper API** to create:
- `tableau/data/product_positioning_sales.hyper`

Then build the workbook in Tableau Desktop 2026 — see `tableau/Workbook_Build_Guide.md`.

> Do **not** use hand-generated `.twb` files. Save your workbook from Tableau Desktop as `.twbx` after building.

---

## Step 7: Start Flask Application

```bash
python app.py
```

Output:
```
==================================================
  Strategic Product Placement Analysis
  Flask Web Application
==================================================

  Starting server at http://127.0.0.1:5000
  Press Ctrl+C to stop
```

Open http://127.0.0.1:5000 in your browser.

---

## Step 8: Configure Tableau Embed (After Publishing)

1. Publish workbook to Tableau Public (see `tableau/Tableau_Public_Publishing_Guide.md`)
2. Edit `app.py`:
   ```python
   TABLEAU_DASHBOARD_URL = "your-dashboard-embed-url"
   TABLEAU_STORY_URL = "your-story-embed-url"
   ```
3. Restart Flask server

---

## Environment Variables (Optional)

Create a `.env` file in the project root:

```env
FLASK_SECRET_KEY=your-secret-key
TABLEAU_DASHBOARD_URL=https://public.tableau.com/views/...
TABLEAU_STORY_URL=https://public.tableau.com/views/...
FLASK_DEBUG=True
FLASK_PORT=5000
```

---

## Verify Installation

Run these checks:

```bash
# 1. Data exists
python -c "import pandas as pd; df=pd.read_csv('data/cleaned/product_positioning_sales_cleaned.csv'); print(df.shape)"
# Expected: (500, 12)

# 2. Flask imports
python -c "from app import app; print('Flask OK')"

# 3. API test (with server running)
curl http://127.0.0.1:5000/api/kpis
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `python not found` | Install Python 3.10+ and add to PATH |
| `pip not found` | Use `python -m pip install` |
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| `FileNotFoundError: raw CSV` | Run download or generate_dataset script |
| `Port 5000 in use` | Change port in `app.py` or kill existing process |
| `kaggle.json not found` | Set up Kaggle API credentials |

---

## Directory After Installation

```
dataanalyis/
├── data/
│   ├── raw/product_positioning_sales.csv      ✓
│   └── cleaned/product_positioning_sales_cleaned.csv  ✓
├── tableau/
│   └── data/product_positioning_sales.hyper      ✓
├── static/css/style.css                         ✓
├── static/js/main.js                            ✓
└── venv/                                        ✓ (optional)
```

Installation complete! Proceed to [User_Guide.md](User_Guide.md) or [Deployment_Guide.md](Deployment_Guide.md).
