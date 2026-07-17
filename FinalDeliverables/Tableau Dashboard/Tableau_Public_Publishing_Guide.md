# Tableau Public Publishing Guide (2026)

## Strategic Product Placement Analysis

Complete instructions for publishing your Tableau Desktop workbook to **Tableau Public 2026** and obtaining **Dashboard** and **Story** embed URLs for the Flask application.

---

## Prerequisites

- [ ] Workbook built in Tableau Desktop / Public Edition 2026 (see `Workbook_Build_Guide.md`)
- [ ] Dashboard named **`Dashboard`**
- [ ] Story named **`Story`**
- [ ] All 5 filters working on the dashboard
- [ ] Free Tableau Public account: https://public.tableau.com/

---

## Step 1: Final Pre-Publish Checklist

Open your saved `.twbx` and verify:

| Check | How to Verify |
|-------|---------------|
| 8+ worksheets render | Click each sheet tab — no errors |
| Dashboard loads | All charts visible, filters on right/bottom |
| Story has 3 scenes | Navigate with story arrows |
| Calculated fields valid | No red error indicators in Data pane |
| Data embedded | Packaged workbook (.twbx) includes Hyper/CSV |

---

## Step 2: Sign In to Tableau Public

### Tableau Public Edition 2026

1. Launch **Tableau Public Edition 2026**.
2. **Help → Settings and Performance → Manage Tableau Public Profile**.
3. Sign in or create a free account.

### Tableau Desktop 2026

1. **Server → Tableau Public → Save to Tableau Public** (first time prompts sign-in).
2. Create account at https://public.tableau.com/ if needed.

---

## Step 3: Publish the Workbook

1. In Tableau Desktop, open your completed workbook.
2. Go to **Server → Tableau Public → Save to Tableau Public As...**
   - *Tableau Public Edition:* **Server → Publish ProductPositioningAnalysis** (or Save to Tableau Public)
3. When prompted for a name, enter:
   ```
   ProductPositioningAnalysis
   ```
4. Wait for the upload progress bar to complete.
5. Tableau opens your workbook in the browser at a URL like:
   ```
   https://public.tableau.com/app/profile/YOUR_USERNAME/viz/ProductPositioningAnalysis/Dashboard
   ```

> **Note:** Your username appears in the URL path. The workbook name and view name determine the embed URL structure.

---

## Step 4: Understand the URL Structure

Tableau Public embed URLs follow this pattern:

```
https://public.tableau.com/views/{WorkbookName}/{ViewName}
```

| Component | Your Value | Example |
|-----------|------------|---------|
| WorkbookName | `ProductPositioningAnalysis` | Set at publish time |
| ViewName (Dashboard) | `Dashboard` | Dashboard tab name |
| ViewName (Story) | `Story` | Story tab name |

Spaces in names become underscores or are URL-encoded. Use the exact name from the **Share** dialog.

---

## Step 5: Get the Dashboard Embed URL

1. Open your published workbook on https://public.tableau.com/
2. Click the **Dashboard** tab (not a worksheet).
3. Click the **Share** icon in the bottom toolbar (or top-right share button).
4. In the Share dialog you will see:
   - **Link** — public page URL (for sharing)
   - **Embed Code** — HTML snippet for websites

### Extract the embed URL from Embed Code

The embed code contains a URL like:

```html
<script type='text/javascript' src='https://public.tableau.com/javascripts/api/viz/v1.js'></script>
<div class='tableauPlaceholder' id='vizProductPositioningAnalysisDashboard' style='position: relative'>
  <object class='tableauViz' style='display:none;'>
    <param name='host_url' value='https://public.tableau.com/' />
    <param name='site_root' value='' />
    <param name='name' value='ProductPositioningAnalysis/Dashboard' />
    ...
  </object>
</div>
```

The **`name`** parameter gives you the view path: `ProductPositioningAnalysis/Dashboard`

Build the embed URL:

```
https://public.tableau.com/views/ProductPositioningAnalysis/Dashboard?:language=en-US&:display_count=y&:origin=viz_share_link&:showVizHome=no&:embed=true
```

### Recommended URL Parameters (2026)

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `:embed=true` | true | Required for iframe/JS embed |
| `:showVizHome=no` | no | Hides Tableau home button |
| `:language=en-US` | en-US | Locale |
| `:display_count=y` | y | Show view count (optional) |
| `:origin=viz_share_link` | — | Analytics tracking (optional) |

---

## Step 6: Get the Story Embed URL

1. On the same published workbook, click the **Story** tab.
2. Click **Share**.
3. Extract the view name — should be `ProductPositioningAnalysis/Story`.

Story embed URL:

```
https://public.tableau.com/views/ProductPositioningAnalysis/Story?:language=en-US&:display_count=y&:origin=viz_share_link&:showVizHome=no&:embed=true
```

---

## Step 7: Update the Flask Application

### Option A — Edit `app.py`

```python
TABLEAU_DASHBOARD_URL = (
    "https://public.tableau.com/views/ProductPositioningAnalysis/Dashboard"
    "?:language=en-US&:display_count=y&:origin=viz_share_link&:showVizHome=no&:embed=true"
)
TABLEAU_STORY_URL = (
    "https://public.tableau.com/views/ProductPositioningAnalysis/Story"
    "?:language=en-US&:display_count=y&:origin=viz_share_link&:showVizHome=no&:embed=true"
)
```

### Option B — Use `.env` file (recommended)

Create `.env` from `.env.example`:

```env
TABLEAU_DASHBOARD_URL=https://public.tableau.com/views/YOUR_USERNAME/ProductPositioningAnalysis/Dashboard?:showVizHome=no&:embed=true
TABLEAU_STORY_URL=https://public.tableau.com/views/YOUR_USERNAME/ProductPositioningAnalysis/Story?:showVizHome=no&:embed=true
```

> If your published URL includes your profile slug (newer Tableau Public URLs), copy the **exact** URL from the Share dialog and replace only the domain portion if needed.

Restart Flask:

```bash
python app.py
```

Test:
- http://127.0.0.1:5000/dashboard
- http://127.0.0.1:5000/story

---

## Step 8: Modern Embed — Tableau Embedding API v3 (Optional Upgrade)

Tableau Public 2026 supports the **Embedding API v3** (recommended over legacy v1 JS API).

Add to `templates/dashboard.html` (inside `{% block scripts %}`):

```html
<script type="module" src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"></script>
<tableau-viz
    id="tableauDashboard"
    src="{{ tableau_url }}"
    width="100%"
    height="750"
    toolbar="bottom"
    hide-tabs>
</tableau-viz>
```

The `src` attribute uses the same URL from Step 5 (without needing `:embed=true` for v3, but it still works if present).

---

## Step 9: Verify Embeds Work

| Test | Expected Result |
|------|-----------------|
| Open embed URL directly in browser | Dashboard/Story renders |
| Flask `/dashboard` page | Tableau viz loads (not placeholder) |
| Flask `/story` page | Story navigation works |
| Apply a filter on dashboard | Charts update |
| "Open in Tableau" link | Opens public.tableau.com page |

The Flask app's `static/js/main.js` auto-embeds when the URL is a real published link (not the default placeholder).

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Blank embed | URL must include `:embed=true` (legacy) or use Embedding API v3 |
| 404 on embed URL | Copy exact URL from Share dialog; check workbook/view names |
| Wrong workbook opens | Verify `ProductPositioningAnalysis` name matches publish name |
| Filters don't apply | Republish; enable "Apply to All Using This Data Source" |
| Data outdated | Edit in Desktop → republish (Public does not auto-refresh) |
| Flask shows placeholder | Default placeholder URLs are detected — replace with your real URLs |
| CORS / iframe blocked | Use official Tableau embed code, not a screenshot |

---

## Updating a Published Workbook

1. Edit workbook in Tableau Desktop.
2. **Server → Tableau Public → Save to Tableau Public** (overwrites existing).
3. Embed URLs stay the same if workbook/view names unchanged.
4. Hard-refresh browser (Ctrl+F5) to see updates.

---

## SmartBridge Submission Checklist

- [ ] Tableau Public profile URL documented in README
- [ ] Live dashboard link works
- [ ] Live story link works
- [ ] Flask app embeds both views
- [ ] Screenshot saved to `docs/screenshots/`
- [ ] Demo script includes live Tableau walkthrough

---

## Security Reminder

Tableau Public workbooks are **world-readable**. Do not publish confidential or PII data. The Kaggle dataset used here is sample FMCG data (Apache 2.0).
