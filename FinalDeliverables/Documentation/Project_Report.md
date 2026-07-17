# Project Report

## Strategic Product Placement Analysis

**Program:** SmartBridge Externship — Data Analytics with Tableau  
**Date:** July 2026  
**Dataset:** [Impact of Product Positioning on Sales](https://www.kaggle.com/datasets/amitvkulkarni/impact-of-product-positioning-on-sales) (Amit V Kulkarni)

---

## 1. Executive Summary

This project analyzes how product shelf positioning, pricing, promotions, foot traffic, consumer demographics, and seasonality affect sales volume in the FMCG retail sector. Using a 500-record dataset, we performed data cleaning, exploratory analysis, built 8+ Tableau visualizations with an interactive dashboard and 3-scene story, and deployed a Flask web application for stakeholder access.

**Key finding:** Products at the **Front of Store** with **active promotions** in **high foot-traffic** areas achieve the highest average sales volume, with an 11% promotional lift across all categories.

---

## 2. Business Problem

Retailers invest significantly in shelf placement but often lack data-driven evidence for positioning decisions. This project answers:

1. Which product positions drive the highest sales?
2. How do promotions interact with category and pricing?
3. Which consumer demographics respond most to placement strategies?
4. What is the relationship between foot traffic and sales performance?

---

## 3. Dataset Description

### Source
Kaggle dataset by Amit V Kulkarni — Apache 2.0 license.

### Variables (9 original + 3 derived)

| Variable | Type | Description |
|----------|------|-------------|
| Product_Position | Categorical | Front of Store, End-cap, Aisle |
| Price | Numeric | Product price ($) |
| Competitor_Price | Numeric | Competitor price ($) |
| Promotion | Categorical | Yes / No |
| Foot_Traffic | Categorical | High, Medium, Low |
| Consumer_Demographics | Categorical | Young adults, Families, Seniors, College students |
| Product_Category | Categorical | Food, Electronics, Clothing |
| Season | Categorical | Seasonal flag (Yes/No) |
| Sales_Volume | Numeric | Units sold |
| Price_Difference | Derived | Price − Competitor_Price |
| Price_Ratio | Derived | Price / Competitor_Price |
| Sales_Category | Derived | Low / Medium / High / Very High |

### Data Quality (Post-Cleaning)
- Records: 500
- Missing values: 0
- Duplicates: 0
- Outliers: Capped via IQR method

---

## 4. Methodology

### 4.1 Data Cleaning
- Median imputation for numeric nulls
- Mode imputation for categorical nulls
- Duplicate removal (8 records)
- IQR-based outlier capping
- Derived feature engineering

### 4.2 Exploratory Data Analysis
Python (Pandas) analysis covering all 8 required visualization dimensions plus KPI computation.

### 4.3 Visualization
Tableau Desktop with calculated fields, 5 interactive filters, dashboard layout, and 3-scene story narrative.

### 4.4 Web Deployment
Flask application embedding Tableau Public views with REST API for KPI access.

---

## 5. Analysis Results

### 5.1 Key Performance Indicators

| KPI | Value |
|-----|-------|
| Total Records | 500 |
| Total Sales Volume | 308,542 units |
| Average Sales Volume | 617.08 units |
| Average Price | $247.59 |
| Average Competitor Price | $248.37 |
| Promotion Rate | 50.4% |

### 5.2 Sales by Product Category

| Category | Avg Sales Volume |
|----------|-----------------|
| Food | Highest |
| Electronics | Moderate |
| Clothing | Moderate |

### 5.3 Sales by Product Position

| Position | Performance |
|----------|-------------|
| Front of Store | Highest avg sales |
| End-cap | Moderate |
| Aisle | Lowest |

### 5.4 Foot Traffic Impact

| Foot Traffic | Avg Sales |
|--------------|-----------|
| High | Highest |
| Medium | Moderate |
| Low | Lowest |

### 5.5 Promotion Impact

| Status | Avg Sales |
|--------|-----------|
| Yes | 649.02 |
| No | 584.63 |
| **Lift** | **11.01%** |

### 5.6 Top Demographic
**Seniors** show the highest average sales volume across the dataset.

---

## 6. Visualizations Delivered

| # | Visualization | Chart Type |
|---|---------------|------------|
| 1 | Avg Sales Volume vs Product Category | Bar Chart |
| 2 | Avg Sales by Category × Position | Grouped Bar |
| 3 | Avg Sales by Category × Season | Stacked Bar |
| 4 | Competitor Price vs Price | Scatter Plot |
| 5 | Consumer Demographics vs Sales | Bar Chart |
| 6 | Foot Traffic vs Avg Sales | Bar Chart |
| 7 | Product Category vs Price | Box Plot |
| 8 | Promotion Impact | Dual Axis |
| + | KPI Cards | Text/Shapes |
| + | Promotion Donut | Donut Chart |
| + | Sales Histogram | Histogram |
| + | Category Treemap | Treemap |

---

## 7. Dashboard & Story

### Dashboard
Responsive layout with 5 filters: Product Category, Product Position, Promotion, Season, Consumer Demographics.

### Story Scenes
1. **Business Overview** — KPIs, category sales, pricing landscape
2. **Position Analysis** — Placement, traffic, demographics deep dive
3. **Recommendations** — Seasonal strategy, promotion targeting, placement optimization

---

## 8. Recommendations

1. **Prioritize Front-of-Store placement** for high-margin products to maximize visibility and sales.
2. **Deploy promotions strategically** — 11% lift demonstrated; focus on Electronics and Clothing categories.
3. **Target high foot-traffic zones** for new product launches and seasonal items.
4. **Segment by demographics** — tailor placement and promotions for Seniors (top segment) and Families.
5. **Monitor competitor pricing** — maintain competitive price ratios especially in Electronics.
6. **Plan seasonal assortments** — adjust category mix based on seasonal sales patterns.

---

## 9. Technical Deliverables

| Deliverable | Location |
|-------------|----------|
| Cleaned dataset | `data/cleaned/` |
| Python scripts | `scripts/` |
| Tableau Hyper extract | `tableau/data/product_positioning_sales.hyper` |
| Tableau build guide | `tableau/Workbook_Build_Guide.md` |
| Flask application | `app.py`, `templates/`, `static/` |
| Documentation | `docs/`, `README.md` |

---

## 10. Conclusion

The Strategic Product Placement Analysis demonstrates that product positioning is a significant driver of FMCG sales performance. By combining Python data engineering with Tableau visualization and Flask deployment, this project delivers actionable, interactive insights for retail strategy optimization.

---

## References

1. Kulkarni, A. V. (2024). Impact of Product Positioning on Sales. Kaggle.
2. SmartBridge Externship Curriculum — Data Analytics with Tableau.
3. Tableau Public Documentation — https://help.tableau.com/
