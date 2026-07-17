# Tableau Workbook Build Guide

## Strategic Product Placement Analysis — Tableau Desktop / Public Edition 2026

This guide walks you through building a **valid** Tableau workbook entirely inside **Tableau Desktop 2026** or **Tableau Public Edition 2026**. Do not use hand-generated `.twb` XML — Tableau must create the workbook file.

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Tableau Public Edition 2026 | Free download: https://public.tableau.com/ |
| OR Tableau Desktop 2026 | With Tableau Public publishing enabled |
| Hyper extract | Run `python scripts/create_tableau_hyper.py` |
| Cleaned CSV (alternative) | `data/cleaned/product_positioning_sales_cleaned.csv` |

---

## Part 0: Generate the Hyper Extract (Recommended)

The Hyper extract is created with the **official Tableau Hyper API** — a supported, valid Tableau data format.

```bash
pip install tableauhyperapi pandas
python scripts/create_tableau_hyper.py
```

Output: `tableau/data/product_positioning_sales.hyper` (500 rows, 12 columns)

> **Why Hyper?** Faster performance in Desktop, portable for packaged workbooks, and fully supported by Tableau Public 2026.

---

## Part 1: Connect Data in Tableau Desktop 2026

### Option A — Connect to Hyper Extract (Recommended)

1. Open **Tableau Public Edition 2026** (or Tableau Desktop 2026).
2. Under **Connect**, click **More... → Hyper**.
3. Browse to:
   ```
   tableau/data/product_positioning_sales.hyper
   ```
4. Drag **ProductPositioningSales** (under Extract schema) to the canvas.
5. At the top, rename the data source: **Product Positioning Sales**.

### Option B — Connect to CSV Directly

1. **Connect → Text file**.
2. Select `data/cleaned/product_positioning_sales_cleaned.csv`.
3. Drag the sheet to the canvas.
4. Rename data source to **Product Positioning Sales**.

### Verify Field Types

Click the **Data Source** tab and confirm:

| Field | Role | Type |
|-------|------|------|
| Product_Position | Dimension | String |
| Price | Measure | Number (decimal) |
| Competitor_Price | Measure | Number (decimal) |
| Promotion | Dimension | String |
| Foot_Traffic | Dimension | String |
| Consumer_Demographics | Dimension | String |
| Product_Category | Dimension | String |
| Season | Dimension | String |
| Sales_Volume | Measure | Number (whole) |
| Price_Difference | Measure | Number (decimal) |
| Price_Ratio | Measure | Number (decimal) |
| Sales_Category | Dimension | String |

Fix any misclassified fields: click the icon (Abc/#) and change to Dimension or Measure.

---

## Part 2: Create Calculated Fields

Right-click in the **Data** pane → **Create Calculated Field**.

Copy formulas from `tableau/Calculated_Fields.md`. Create these minimum fields:

| Name | Formula |
|------|---------|
| Avg Sales Volume | `AVG([Sales_Volume])` |
| Price Difference | `[Price] - [Competitor_Price]` |
| Promotion Rate % | `SUM(IF [Promotion]="Yes" THEN 1 ELSE 0 END) / COUNT([Sales_Volume]) * 100` |
| Foot Traffic Order | `CASE [Foot_Traffic] WHEN "High" THEN 1 WHEN "Medium" THEN 2 ELSE 3 END` |
| Seasonal Label | `IF [Season]="Yes" THEN "Seasonal" ELSE "Non-Seasonal" END` |
| Total Sales Volume | `SUM([Sales_Volume])` |
| Promotion Flag | `IF [Promotion]="Yes" THEN 1 ELSE 0 END` |

---

## Part 3: Build 8 Required Worksheets

For each worksheet: **Worksheet → New Worksheet**, then configure shelves as below.

### WS01 — Avg Sales Volume vs Product Category

1. **Rows:** `Product_Category`
2. **Columns:** `Sales_Volume` → change aggregation to **AVG** (right-click pill → Measure → Average)
3. **Show Me:** Horizontal Bar Chart
4. Sort descending by AVG(Sales_Volume)
5. **Worksheet → Rename:** `WS01_AvgSalesByCategory`
6. **Format → Titles:** "Avg Sales Volume vs Product Category"

### WS02 — Avg Sales by Category × Position

1. **Columns:** `Product_Position`
2. **Rows:** `AVG(Sales_Volume)`
3. **Color:** `Product_Category`
4. **Show Me:** Side-by-side Bar
5. Rename: `WS02_CategoryByPosition`

### WS03 — Avg Sales by Category × Season

1. **Columns:** `Seasonal Label`
2. **Rows:** `AVG(Sales_Volume)`
3. **Color:** `Product_Category`
4. **Show Me:** Stacked Bar
5. Rename: `WS03_CategoryBySeason`

### WS04 — Competitor Price vs Price

1. **Columns:** `Competitor_Price`
2. **Rows:** `Price`
3. **Color:** `Product_Category`
4. **Detail:** `Product_Position`
5. **Show Me:** Circle (Scatter)
6. **Analytics pane → Trend Line → Linear**
7. Rename: `WS04_CompetitorVsPrice`

### WS05 — Consumer Demographics vs Sales Volume

1. **Columns:** `Consumer_Demographics`
2. **Rows:** `AVG(Sales_Volume)`
3. Sort descending
4. Rename: `WS05_DemographicsVsSales`

### WS06 — Foot Traffic vs Avg Sales Volume

1. **Columns:** `Foot_Traffic`
2. **Rows:** `AVG(Sales_Volume)`
3. Click `Foot_Traffic` pill → **Sort → Field → Foot Traffic Order → Ascending**
4. Rename: `WS06_FootTrafficVsSales`

### WS07 — Product Category vs Price

1. **Columns:** `Product_Category`
2. **Rows:** `Price`
3. **Show Me:** Box and Whisker (or Bar with AVG/MIN/MAX)
4. Rename: `WS07_CategoryVsPrice`

### WS08 — Promotion vs Product Category on Price and Sales

1. **Columns:** `Product_Category`, `Promotion`
2. **Rows:** `AVG(Sales_Volume)`
3. Drag `AVG(Price)` to Rows → create **Dual Axis**
4. Right-click axis → **Synchronize Axis** → Off
5. Rename: `WS08_PromotionImpact`

### Bonus Worksheets (Recommended)

| Sheet | Configuration |
|-------|---------------|
| `WS_KPI_Cards` | Text objects: Total Records (500), Total Sales, Avg Sales, Promotion Rate % |
| `WS_Donut_Promotion` | Pie chart: Promotion (Yes/No), mark type Pie, angle = COUNT |
| `WS_Histogram_Sales` | Histogram of Sales_Volume (bin size ~50) |
| `WS_Treemap_Category` | Treemap: Size = SUM(Sales_Volume), Color = Product_Category |

---

## Part 4: Build the Dashboard

1. **Dashboard → New Dashboard**
2. Name it exactly: **`Dashboard`** (required for Flask embed URL)
3. Set size: **Automatic** (or Range: 1000–1400 px width)
4. Drag worksheets onto the canvas in a grid layout:

```
┌──────────────────────────────────────────────────────────┐
│  WS_KPI_Cards (full width)                               │
├────────────────────┬────────────────────┬────────────────┤
│  WS01              │  WS02              │  Filters       │
├────────────────────┼────────────────────┤  (sidebar)     │
│  WS03              │  WS04              │                │
├────────────────────┼────────────────────┤                │
│  WS05              │  WS06              │                │
├────────────────────┼────────────────────┤                │
│  WS07              │  WS08              │                │
├────────────────────┴────────────────────┴────────────────┤
│  WS_Treemap / WS_Donut / WS_Histogram                    │
└──────────────────────────────────────────────────────────┘
```

### Add Filters (Quick Filters)

For each field, drag to the dashboard filter area (or right-click field → **Show Filter**):

| Filter | Settings |
|--------|----------|
| Product_Category | Multi-select dropdown, Apply to: All Using This Data Source |
| Product_Position | Multi-select dropdown, Apply to: All Using This Data Source |
| Promotion | Single/Multi select, Apply to: All Using This Data Source |
| Season | Single select, Apply to: All Using This Data Source |
| Consumer_Demographics | Multi-select dropdown, Apply to: All Using This Data Source |

Enable **Show Apply Button** on each filter (dropdown arrow → Customize → Show Apply Button).

---

## Part 5: Build the Story (3 Scenes)

1. **Story → New Story**
2. Name it exactly: **`Story`**

### Scene 1 — Business Overview

- **Caption:** "Business Overview — KPIs, category sales, and pricing landscape."
- Add: `WS_KPI_Cards`, `WS01_AvgSalesByCategory`, `WS07_CategoryVsPrice`, `WS_Donut_Promotion`

### Scene 2 — Product Position Analysis

- **Caption:** "Product Position Analysis — placement, traffic, promotions, demographics."
- Add: `WS02_CategoryByPosition`, `WS06_FootTrafficVsSales`, `WS05_DemographicsVsSales`, `WS04_CompetitorVsPrice`

### Scene 3 — Recommendations

- **Caption:** "Recommendations — optimize placement, promotions, and seasonal strategy."
- Add: `WS03_CategoryBySeason`, `WS08_PromotionImpact`, `WS_Histogram_Sales`, `WS_Treemap_Category`

---

## Part 6: Formatting for Tableau Public 2026

1. **Format → Workbook → Title Theme** — use consistent colors (blue #6366f1, teal #06b6d4).
2. Remove unnecessary gridlines: **Format → Lines → Grid Lines → None**.
3. Add tooltips with Category, Position, Sales, Price on each chart.
4. **File → Workbook Locale** → English (United States).

---

## Part 7: Save the Workbook

1. **File → Save As**
2. Save to: `tableau/ProductPositioningAnalysis.twbx` (Packaged Workbook — embeds Hyper data)
3. Verify the file opens without errors before publishing.

> The `.twbx` file is created **by Tableau Desktop**, not by this project's Python scripts. That ensures full Tableau Public 2026 compatibility.

---

## Part 8: Validate Against Python Analysis

Compare your Tableau KPI cards with Python output from `python scripts/data_analysis.py`:

| Metric | Expected (~) |
|--------|--------------|
| Total Records | 500 |
| Total Sales Volume | 308,542 |
| Average Sales Volume | 617.08 |
| Promotion Rate | 50.4% |
| Top Category | Food |
| Best Position | Front of Store |
| Promotion Lift | 11.01% |

---

## Next Step

Publish to Tableau Public: **`tableau/Tableau_Public_Publishing_Guide.md`**
