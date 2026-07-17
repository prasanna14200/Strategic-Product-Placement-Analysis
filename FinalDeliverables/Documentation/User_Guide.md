# User Guide

## Strategic Product Placement Analysis

Welcome to the Strategic Product Placement Analysis web application. This guide explains how to navigate and use all features.

---

## 1. Getting Started

### Access the Application

1. Ensure the Flask server is running (see [Installation.md](Installation.md))
2. Open your browser and go to: **http://127.0.0.1:5000**

### System Requirements

- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection (for Bootstrap CDN, Google Fonts, Tableau embed)
- Screen resolution: 1280×720 minimum recommended

---

## 2. Navigation

The top navigation bar provides access to all pages:

| Link | Page | Description |
|------|------|-------------|
| **Home** | `/` | Project overview, KPIs, key insights |
| **Dashboard** | `/dashboard` | Interactive Tableau dashboard |
| **Story** | `/story` | 3-scene Tableau data story |
| **About** | `/about` | Project details, methodology, dataset info |

On mobile devices, tap the hamburger menu (☰) to expand navigation.

---

## 3. Home Page

### Hero Section
- Project title and description
- **View Dashboard** button — opens the Tableau dashboard page
- **View Story** button — opens the Tableau story page

### KPI Cards
Four key metrics displayed at a glance:

| Card | Metric |
|------|--------|
| Total Records | Number of data records analyzed |
| Total Sales Volume | Sum of all units sold |
| Avg Sales Volume | Average units sold per product |
| Promotion Rate | Percentage of products on promotion |

### Key Insights
- **Best Position** — highest-performing shelf placement
- **Top Category** — category with highest average sales
- **Top Demographic** — consumer segment with highest sales

### Features Section
Overview of project capabilities: data cleaning, visualizations, filters, Tableau Public integration.

---

## 4. Dashboard Page

### Viewing the Dashboard

1. Click **Dashboard** in the navigation
2. The Tableau interactive dashboard loads in the main content area
3. If not yet published, a placeholder with setup instructions appears

### Using Dashboard Filters

The Tableau dashboard includes 5 interactive filters:

| Filter | Options |
|--------|---------|
| Product Category | Food, Electronics, Clothing |
| Product Position | Front of Store, End-cap, Aisle |
| Promotion | Yes, No |
| Season | Yes, No |
| Consumer Demographics | Young adults, Families, Seniors, College students |

**How to filter:**
1. Select values in the filter panel (right side of dashboard)
2. Click **Apply** to update all visualizations
3. Click **Reset** to clear filters

### Open in Tableau
Click **Open in Tableau** (top right) to view the full dashboard on Tableau Public in a new tab.

### Dashboard Visualizations

| # | Chart | What It Shows |
|---|-------|---------------|
| 1 | Bar Chart | Average sales by product category |
| 2 | Grouped Bar | Sales by category and shelf position |
| 3 | Stacked Bar | Seasonal patterns by category |
| 4 | Scatter Plot | Product price vs competitor price |
| 5 | Bar Chart | Sales by consumer demographic |
| 6 | Bar Chart | Sales by foot traffic level |
| 7 | Box Plot | Price distribution by category |
| 8 | Dual Axis | Promotion impact on price and sales |

---

## 5. Story Page

### Viewing the Story

1. Click **Story** in the navigation
2. Use Tableau story navigation arrows to move between scenes

### Story Scenes

| Scene | Title | Content |
|-------|-------|---------|
| 1 | Business Overview | KPIs, category sales, pricing overview |
| 2 | Position Analysis | Placement, traffic, demographics analysis |
| 3 | Recommendations | Strategic recommendations and action items |

### Key Findings Section
Below the story embed, four finding cards summarize the main insights from the analysis.

---

## 6. About Page

Contains:
- **Project Overview** — business context and objectives
- **Methodology** — 4-step approach (Collect → Clean → Analyze → Deploy)
- **Dataset Variables** — table of all 9 variables with types and values
- **Credits** — dataset attribution and program information
- **View Dataset** link — opens the Kaggle dataset page

---

## 7. API Access (Advanced Users)

### KPI Endpoint
```
GET http://127.0.0.1:5000/api/kpis
```

Response:
```json
{
  "status": "success",
  "data": {
    "total_records": 500,
    "total_sales": 308542,
    "avg_sales": 617.08,
    "avg_price": 247.59,
    "promo_rate": 50.4,
    "top_category": "Food",
    "best_position": "Front of Store",
    "top_demographic": "Seniors"
  }
}
```

### Data Summary Endpoint
```
GET http://127.0.0.1:5000/api/data
```

Returns dataset shape, columns, first 10 rows, and data types.

---

## 8. Troubleshooting

| Issue | Solution |
|-------|----------|
| Page won't load | Ensure `python app.py` is running |
| KPIs show 0 | Run `python scripts/data_cleaning.py` first |
| Dashboard blank | Publish to Tableau Public and update URLs in app.py |
| Slow loading | Check internet connection for CDN resources |
| Mobile layout broken | Clear browser cache; use latest browser version |

---

## 9. Tips for Best Experience

- Use **full-screen mode** on the dashboard for detailed chart exploration
- Hover over chart elements for **tooltips** with detailed values
- Use **multiple filters** together to drill into specific segments
- Read the **Story** before the Dashboard for narrative context
- Refer to **About** page for dataset variable definitions

---

## 10. Support

For technical issues, refer to:
- [Installation.md](Installation.md) — setup problems
- [Deployment_Guide.md](Deployment_Guide.md) — hosting issues
- [Tableau_Public_Publishing_Guide.md](../tableau/Tableau_Public_Publishing_Guide.md) — embed issues
