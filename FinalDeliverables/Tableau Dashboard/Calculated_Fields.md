# Tableau Calculated Fields Reference

## Strategic Product Placement Analysis

This document lists all calculated fields to create in **Tableau Desktop 2026** when building the workbook (see `Workbook_Build_Guide.md`).

---

## 1. Avg Sales Volume

**Purpose:** Aggregate measure for all bar charts comparing sales performance.

```
AVG([Sales_Volume])
```

| Property | Value |
|----------|-------|
| Data Type | Number (Decimal) |
| Used In | WS_AvgSalesByCategory, WS_FootTrafficVsSales, WS_DemographicsVsSales |

---

## 2. Price Difference

**Purpose:** Shows pricing gap between product and competitor.

```
[Price] - [Competitor_Price]
```

| Property | Value |
|----------|-------|
| Data Type | Number (Decimal) |
| Used In | WS_CompetitorPriceVsPrice, KPI cards |

---

## 3. Price Ratio

**Purpose:** Relative pricing position vs competitor (1.0 = parity).

```
[Price] / [Competitor_Price]
```

| Property | Value |
|----------|-------|
| Data Type | Number (Decimal) |
| Used In | WS_CompetitorPriceVsPrice tooltip |

---

## 4. Promotion Flag (Numeric)

**Purpose:** Enables numeric aggregation of promotion status.

```
IF [Promotion] = "Yes" THEN 1 ELSE 0 END
```

| Property | Value |
|----------|-------|
| Data Type | Integer |
| Used In | KPI cards, donut chart |

---

## 5. Promotion Rate %

**Purpose:** Percentage of products on promotion.

```
SUM([Promotion Flag (Numeric)]) / COUNT([Sales_Volume]) * 100
```

| Property | Value |
|----------|-------|
| Data Type | Number (Percentage) |
| Used In | Dashboard KPI card |

---

## 6. Sales Above Average

**Purpose:** Classifies records as above or below dataset average.

```
IF [Sales_Volume] > { FIXED : AVG([Sales_Volume]) }
THEN "Above Average"
ELSE "Below Average"
END
```

| Property | Value |
|----------|-------|
| Data Type | String |
| Used In | WS_Histogram, treemap color |

---

## 7. Promotion Sales Lift %

**Purpose:** Measures promotional impact on sales.

```
(
  { FIXED [Promotion] : AVG([Sales_Volume]) }
)
```

Then compute in a separate sheet:
```
(SUM(IF [Promotion]="Yes" THEN [Sales_Volume] END) / COUNT(IF [Promotion]="Yes" THEN 1 END)
-
SUM(IF [Promotion]="No" THEN [Sales_Volume] END) / COUNT(IF [Promotion]="No" THEN 1 END))
/
(SUM(IF [Promotion]="No" THEN [Sales_Volume] END) / COUNT(IF [Promotion]="No" THEN 1 END))
* 100
```

| Property | Value |
|----------|-------|
| Data Type | Number (Percentage) |
| Used In | Story Scene 3, KPI card |

---

## 8. Total Sales Volume

**Purpose:** Sum of all units sold.

```
SUM([Sales_Volume])
```

| Property | Value |
|----------|-------|
| Data Type | Integer |
| Used In | KPI cards, Story Scene 1 |

---

## 9. Avg Price by Category

**Purpose:** Average product price per category.

```
AVG([Price])
```

| Property | Value |
|----------|-------|
| Data Type | Number (Decimal) |
| Used In | WS_CategoryVsPrice, WS_PromotionImpact |

---

## 10. Foot Traffic Order

**Purpose:** Sorts foot traffic levels logically (High → Medium → Low).

```
CASE [Foot_Traffic]
  WHEN "High" THEN 1
  WHEN "Medium" THEN 2
  WHEN "Low" THEN 3
  ELSE 4
END
```

| Property | Value |
|----------|-------|
| Data Type | Integer |
| Used In | WS_FootTrafficVsSales (sort) |

---

## 11. Seasonal Label

**Purpose:** Human-readable seasonal product label.

```
IF [Season] = "Yes" THEN "Seasonal" ELSE "Non-Seasonal" END
```

| Property | Value |
|----------|-------|
| Data Type | String |
| Used In | WS_AvgSalesCategorySeason |

---

## 12. Position Rank

**Purpose:** Ranks product positions by average sales.

```
RANK(AVG([Sales_Volume]), 'desc')
```

| Property | Value |
|----------|-------|
| Data Type | Integer |
| Used In | WS_AvgSalesCategoryPosition tooltip |

---

## Dashboard Filters (Quick Filters)

| Filter Name | Field | Type | Apply To |
|-------------|-------|------|----------|
| Product Category | Product_Category | Multi-select dropdown | All sheets |
| Product Position | Product_Position | Multi-select dropdown | All sheets |
| Promotion | Promotion | Single/Multi select | All sheets |
| Season | Season | Single select | All sheets |
| Consumer Demographics | Consumer_Demographics | Multi-select dropdown | All sheets |

All filters use **Apply to Worksheets → All Using This Data Source** and **Show Apply Button** for responsive dashboard behavior.
