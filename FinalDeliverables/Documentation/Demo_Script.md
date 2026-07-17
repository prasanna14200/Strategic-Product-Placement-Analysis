# Demo Script

## Strategic Product Placement Analysis

**Duration:** 10–15 minutes  
**Audience:** SmartBridge evaluators, stakeholders, instructors  
**Presenter:** Data Analysis Team

---

## Pre-Demo Checklist

- [ ] Flask server running (`python app.py`)
- [ ] Browser open to http://127.0.0.1:5000
- [ ] Tableau workbook published to Tableau Public (or use placeholder with build guide)
- [ ] `data/cleaned/product_positioning_sales_cleaned.csv` exists (500 rows)
- [ ] Second browser tab ready for Tableau Public direct link

---

## Scene 1: Introduction (2 minutes)

### Opening

> "Good [morning/afternoon]. Today I'll present the **Strategic Product Placement Analysis** — a data-driven project that investigates how product shelf positioning impacts sales in the FMCG retail sector."

### Context

> "Retailers spend millions on shelf placement, but decisions are often intuition-based. We used the Kaggle dataset 'Impact of Product Positioning on Sales' with 500 records across 9 variables — including product position, pricing, promotions, foot traffic, demographics, and seasonality."

### Show: Home Page (`/`)

1. Point to the **hero section** — project title and value proposition
2. Scroll to **KPI cards**:
   - "We have **500 records** with a total sales volume of **308,542 units**"
   - "Average sales per product is **617 units** with a **50.4% promotion rate**"
3. Highlight **Key Insights**:
   - "Front of Store is the best-performing position"
   - "Food leads in average sales by category"
   - "Seniors are the top consumer demographic"

---

## Scene 2: Data Pipeline (2 minutes)

### Narration

> "Let me walk through our data engineering pipeline."

### Terminal Demo (optional)

```bash
# Show cleaning pipeline
python scripts/data_cleaning.py

# Show analysis output
python scripts/data_analysis.py
```

### Key Points

> "Our cleaning pipeline handled missing values via median/mode imputation, removed 8 duplicate records, standardized categorical values, and capped outliers using the IQR method. We also engineered three derived columns: Price Difference, Price Ratio, and Sales Category."

### Show: About Page (`/about`)

1. Navigate to **About**
2. Point to **Methodology** — 4-step process
3. Scroll to **Dataset Variables** table — all 9 fields documented

---

## Scene 3: Tableau Dashboard (4 minutes)

### Narration

> "The heart of our analysis is an interactive Tableau dashboard with 8 visualizations and 5 filters."

### Show: Dashboard Page (`/dashboard`)

1. Click **Dashboard** in navigation
2. If Tableau embed is live:
   - Demonstrate **Product Category** filter — select "Food"
   - Click **Apply** — charts update
   - Add **Promotion = Yes** filter
   - Reset filters
3. If placeholder shown:
   - "Connect to `tableau/data/product_positioning_sales.hyper` in Tableau Desktop 2026"
   - Follow `tableau/Workbook_Build_Guide.md` to build and publish

### Walk Through Visualizations

| # | Say This |
|---|----------|
| 1 | "Bar chart shows average sales by category — Food leads" |
| 2 | "Grouped bar reveals Front of Store outperforms across categories" |
| 3 | "Seasonal products show distinct patterns by category" |
| 4 | "Scatter plot compares our pricing against competitors" |
| 5 | "Seniors drive the highest sales among demographics" |
| 6 | "High foot traffic areas correlate with higher sales" |
| 7 | "Electronics command the highest prices" |
| 8 | "Promotions deliver an 11% sales lift" |

### Bonus Charts

> "We also included KPI cards, a promotion donut chart, sales histogram, and category treemap for additional context."

---

## Scene 4: Tableau Story (3 minutes)

### Narration

> "We've structured our findings as a 3-scene data story for executive audiences."

### Show: Story Page (`/story`)

1. Click **Story** in navigation
2. Describe each scene:

**Scene 1 — Business Overview:**
> "We open with high-level KPIs, category distribution, and the pricing landscape."

**Scene 2 — Position Analysis:**
> "Scene two dives into shelf position, foot traffic, promotions, and demographic patterns."

**Scene 3 — Recommendations:**
> "We close with actionable recommendations for placement strategy, promotion targeting, and seasonal planning."

3. Scroll to **Key Findings** cards on the page

---

## Scene 5: Technical Architecture (2 minutes)

### Narration

> "The project is built with Python and Flask for the web layer, Pandas for data processing, and Tableau for visualization."

### Show: API Endpoint

Open in browser or terminal:
```
http://127.0.0.1:5000/api/kpis
```

> "We expose KPIs via a REST API for programmatic access."

### Project Structure

Briefly mention:
- `scripts/` — data pipeline
- `tableau/` — workbook and guides
- `templates/` + `static/` — responsive web UI
- `docs/` — complete documentation

---

## Scene 6: Recommendations & Close (2 minutes)

### Business Recommendations

> "Based on our analysis, we recommend five actions:"

1. **Prioritize front-of-store placement** for high-margin products
2. **Deploy promotions strategically** — 11% demonstrated lift
3. **Target high foot-traffic zones** for new launches
4. **Segment by demographics** — Seniors and Families show distinct patterns
5. **Monitor competitor pricing** — especially in Electronics

### Closing

> "This project demonstrates the full analytics lifecycle — from raw Kaggle data through cleaning, analysis, Tableau visualization, and Flask deployment. All code, documentation, and the Tableau workbook are included in the project repository. Thank you — I'm happy to take questions."

---

## Q&A Preparation

| Likely Question | Answer |
|-----------------|--------|
| Why this dataset? | Kaggle FMCG dataset with all required variables for placement analysis |
| How were outliers handled? | IQR method with capping (not removal) to preserve data volume |
| Can filters combine? | Yes — all 5 dashboard filters work together with Apply button |
| Is the app production-ready? | Yes — Gunicorn/Docker/Heroku deployment documented |
| How to update data? | Re-run cleaning pipeline, refresh Tableau extract, republish |

---

## Demo URLs Quick Reference

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:5000/ |
| Dashboard | http://127.0.0.1:5000/dashboard |
| Story | http://127.0.0.1:5000/story |
| About | http://127.0.0.1:5000/about |
| API KPIs | http://127.0.0.1:5000/api/kpis |
| API Data | http://127.0.0.1:5000/api/data |
