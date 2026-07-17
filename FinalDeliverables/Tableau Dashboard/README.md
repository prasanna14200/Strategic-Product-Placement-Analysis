# Tableau Assets

## Important: No Pre-Generated Workbook Files

This project **does not** ship a hand-written `.twb` or `.twbx` file. Tableau workbooks contain complex proprietary XML that must be created by **Tableau Desktop** (or Tableau Public Edition). Generating fake workbook XML produces invalid files that Tableau Public 2026 cannot open reliably.

## What We Provide Instead

| Asset | Purpose |
|-------|---------|
| `data/product_positioning_sales.hyper` | Official Tableau Hyper extract (built via Hyper API) |
| `Workbook_Build_Guide.md` | Step-by-step Tableau Desktop 2026 build instructions |
| `Calculated_Fields.md` | All calculated field formulas |
| `Tableau_Public_Publishing_Guide.md` | Publish + embed URL instructions |

## Quick Start

```bash
# 1. Create the Hyper extract (Tableau Hyper API)
pip install tableauhyperapi
python scripts/create_tableau_hyper.py

# 2. Build workbook in Tableau Desktop — follow Workbook_Build_Guide.md

# 3. Publish to Tableau Public — follow Tableau_Public_Publishing_Guide.md
```

## Supported Tools

| Tool | Used For | Creates Valid Workbook? |
|------|----------|-------------------------|
| **Tableau Hyper API** | `.hyper` data extract | N/A (data only) |
| **Tableau Desktop 2026** | Worksheets, dashboard, story | **Yes** |
| **Tableau Public Edition 2026** | Publish to web | **Yes** |
| Tableau Document API | Modify existing `.twb` templates | Only with a real template |
| Hand-written `.twb` XML | — | **No — not used in this project** |

## Tableau Public 2026 Compatibility

- Use **Tableau Public Edition 2026** (free) or **Tableau Desktop 2026** with Public publishing enabled.
- Both can connect to `.hyper` extracts and publish to https://public.tableau.com/
- Published workbooks use **Embedding API v3** for web embeds (documented in publishing guide).
