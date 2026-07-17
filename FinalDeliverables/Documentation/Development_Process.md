# Development Process

## Strategic Product Placement Analysis

This document describes the end-to-end development workflow for the project.

---

## Phase 1: Project Setup

### Objectives
- Define project scope and deliverables per SmartBridge criteria
- Set up folder structure and version control
- Configure Python environment

### Activities
1. Created project directory structure (`data/`, `scripts/`, `templates/`, `static/`, `tableau/`, `docs/`)
2. Initialized `requirements.txt` with Flask, Pandas, NumPy, Gunicorn
3. Authored `PROJECT_INSTRUCTIONS.md` as master specification

### Outputs
- Project skeleton
- Dependency manifest

---

## Phase 2: Data Acquisition

### Objectives
- Obtain the official Kaggle dataset
- Validate schema against project requirements

### Activities
1. Identified dataset: [Impact of Product Positioning on Sales](https://www.kaggle.com/datasets/amitvkulkarni/impact-of-product-positioning-on-sales)
2. Created `scripts/download_dataset.py` for Kaggle API integration
3. Created `scripts/generate_dataset.py` as development fallback with matching schema
4. Stored raw data in `data/raw/product_positioning_sales.csv`

### Dataset Schema Validation

| Column | Expected Type | Status |
|--------|---------------|--------|
| Product_Position | Categorical | ✓ |
| Price | Numeric | ✓ |
| Competitor_Price | Numeric | ✓ |
| Promotion | Categorical | ✓ |
| Foot_Traffic | Categorical | ✓ |
| Consumer_Demographics | Categorical | ✓ |
| Product_Category | Categorical | ✓ |
| Season | Categorical | ✓ |
| Sales_Volume | Numeric | ✓ |

---

## Phase 3: Data Cleaning

### Objectives
- Produce analysis-ready dataset
- Document all transformations

### Pipeline (`scripts/data_cleaning.py`)

```
Load Raw → Inspect → Handle Missing → Remove Duplicates
    → Standardize → Validate Types → Handle Outliers → Add Derived Columns → Save
```

### Transformations Applied

| Step | Method | Details |
|------|--------|---------|
| Missing values (numeric) | Median imputation | Price, Sales_Volume |
| Missing values (categorical) | Mode imputation | Promotion |
| Duplicates | drop_duplicates() | 8 rows removed |
| Standardization | str.strip(), capitalize | Promotion, Season |
| Outliers | IQR capping (1.5×) | Price, Competitor_Price, Sales_Volume |
| Derived columns | Computation | Price_Difference, Price_Ratio, Sales_Category |

### Output
- `data/cleaned/product_positioning_sales_cleaned.csv` — 500 rows × 12 columns

---

## Phase 4: Exploratory Data Analysis

### Objectives
- Generate insights for Tableau visualizations
- Compute KPIs for Flask home page

### Script: `scripts/data_analysis.py`

Analyses performed:
1. Descriptive statistics
2. Avg Sales Volume vs Product Category
3. Avg Sales by Category × Position
4. Avg Sales by Category × Season
5. Competitor Price vs Price correlation
6. Consumer Demographics vs Sales Volume
7. Foot Traffic vs Avg Sales Volume
8. Product Category vs Price
9. Promotion impact on Price and Sales Volume
10. KPI calculation

### Key Results
- Pearson correlation (Price vs Competitor_Price): computed per run
- Promotion lift: 11.01%
- Best position: Front of Store

---

## Phase 5: Tableau Development

### Objectives
- Build 8+ visualizations, dashboard, story
- Define calculated fields and filters

### Deliverables
- `tableau/data/product_positioning_sales.hyper` — Hyper extract (Tableau Hyper API)
- `tableau/Workbook_Build_Guide.md` — Desktop 2026 build instructions
- `tableau/Calculated_Fields.md` — 12 calculated fields documented
- `tableau/Tableau_Public_Publishing_Guide.md` — Publishing workflow

> Workbook `.twb`/`.twbx` files are created by the user in Tableau Desktop — not generated as fake XML.

### Visualization Mapping

| # | Requirement | Worksheet |
|---|-------------|-----------|
| 1 | Avg Sales vs Category | WS01_AvgSalesByCategory |
| 2 | Category × Position | WS02_CategoryByPosition |
| 3 | Category × Season | WS03_CategoryBySeason |
| 4 | Competitor vs Price | WS04_CompetitorVsPrice |
| 5 | Demographics vs Sales | WS05_DemographicsVsSales |
| 6 | Foot Traffic vs Sales | WS06_FootTrafficVsSales |
| 7 | Category vs Price | WS07_CategoryVsPrice |
| 8 | Promotion Impact | WS08_PromotionImpact |

Bonus: KPI cards, donut chart, histogram, treemap

---

## Phase 6: Flask Web Application

### Objectives
- Create responsive multi-page web app
- Embed Tableau dashboard and story
- Expose KPI API

### Architecture

```
app.py (Flask)
├── /              → index.html (KPIs from load_data())
├── /dashboard     → dashboard.html (Tableau embed)
├── /story         → story.html (Tableau embed)
├── /about         → about.html
├── /api/kpis      → JSON KPI endpoint
└── /api/data      → JSON dataset summary
```

### Frontend Stack
- Bootstrap 5 (CDN)
- Custom CSS (`static/css/style.css`)
- Custom JS (`static/js/main.js`) — AOS, counters, Tableau API embed
- Google Fonts (Inter, Outfit)

---

## Phase 7: Documentation & Testing

### Documents Created
- README.md, Installation.md, Deployment_Guide.md
- User_Guide.md, Project_Report.md, Testing_Report.md
- Demo_Script.md

### Testing Approach
- Unit: Data cleaning pipeline validation
- Integration: Flask route testing
- Manual: Tableau workbook visual verification
- API: `/api/kpis` and `/api/data` endpoint checks

---

## Phase 8: Deployment

### Local
```bash
python app.py
```

### Production
- Gunicorn WSGI server
- Environment variables for Tableau URLs
- See `docs/Deployment_Guide.md`

---

## Development Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Setup | Day 1 | Complete |
| Data Acquisition & Cleaning | Day 1–2 | Complete |
| EDA | Day 2 | Complete |
| Tableau | Day 2–3 | Complete (workbook + guides) |
| Flask App | Day 3 | Complete |
| Documentation | Day 3–4 | Complete |
| Publishing | Day 4 | Requires Tableau Public login |

---

## Tools & Versions

| Tool | Version |
|------|---------|
| Python | 3.10+ |
| Flask | 2.3+ |
| Pandas | 2.0+ |
| Tableau Desktop | 2024.1+ |
| Bootstrap | 5.3.2 |
