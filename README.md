# Telecom Customer Churn Intelligence Platform

> End-to-end churn analysis and prediction for a telecom company with 7,043 customers.
> Combines descriptive analytics, SQL, machine learning, and an interactive Streamlit app
> to answer: **who will leave, when, and what it costs.**

---

## Key Results

| Metric | Value |
|--------|-------|
| Overall churn rate | 26.54% |
| Revenue at risk | $2.86M / month (17.83% of total) |
| Month-to-month churn rate | 42.71% vs. 2.83% for two-year contracts |
| First-year churn rate | 48.28% |
| Critical-risk customers | 384 (88.28% actual churn rate) |
| Model ROC-AUC | 0.8448 |
| Optimised threshold | 0.3143 (recall: 77.0%) |

---

## Live Demo

| | Link |
|---|---|
| Streamlit App | [Open App](https://your-app-name.streamlit.app) |
| Tableau Dashboard | [View Dashboard](https://public.tableau.com/your-dashboard-link) |

The app has 5 pages: Executive Overview · Segment Analysis · Risk Intelligence · Customer Lookup · **Live Churn Predictor**

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Data processing | Python, pandas, numpy |
| Machine learning | scikit-learn (HGB, Logistic Regression, calibration, cross-validation) |
| SQL | SQLite — window functions, CTEs, financial modelling |
| Visualisation | matplotlib, seaborn, Altair |
| Dashboard | Streamlit |
| BI tool | Tableau Public |
| Storage | SQLite (`sql/churn.db`), CSV flat files |

---

## How to Run

### Prerequisites

```bash
pip install -r requirements.txt
```

### Step 1 — Train and save the model

```bash
python models/train_and_save.py
```

Produces `models/churn_model.pkl` and `models/model_metadata.json`.

### Step 2 — Build the SQL database

```bash
python sql/00_setup_database.py
```

Loads all 10 processed CSVs into `sql/churn.db`.

### Step 3 — Generate saved charts

```bash
python reports/figures/generate_charts.py
```

Saves 6 PNG charts to `reports/figures/`.

### Step 4 — Launch the Streamlit app

```bash
streamlit run app/app.py
```

### Step 5 — Run SQL queries (optional)

Open `sql/churn.db` in DB Browser for SQLite, or run from the terminal:

```bash
sqlite3 sql/churn.db < sql/queries/02_revenue_at_risk.sql
```

---

## Key Findings

1. **Contract type is the strongest behavioural predictor** — Month-to-month customers churn at 42.71% vs. 2.83% for two-year contracts, a 15× difference
2. **The first 12 months are critical** — 48.28% of new customers churn before their first anniversary; this drops to 8.3% after 5 years
3. **$2.86M/month in revenue is recoverable** — targeted intervention on High + Critical risk customers yields positive ROI (see `sql/queries/08_retention_roi_estimate.sql`)
4. **Fiber optic + no security bundle = red flag** — top 3 features by importance: tenure, month-to-month flag, internet service type

---

## Project Structure

```
customer-churn-platform/
├── data/
│   ├── raw/
│   │   └── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Source: 7,043 customers, 21 features
│   └── processed/
│       ├── cleaned_churn_data.csv                  # After cleaning & type fixes
│       ├── analytics_ready_churn_data.csv          # + 7 engineered features (28 cols)
│       └── dashboard_tables/                       # Aggregated outputs for viz & SQL
│           ├── customer_predictions.csv            # All 7,043 rows + ML scores (32 cols)
│           ├── top_50_high_risk_customers.csv      # Immediate action list
│           ├── kpi_summary.csv
│           ├── churn_by_contract.csv
│           ├── churn_by_tenure.csv
│           ├── churn_by_charge.csv
│           ├── churn_by_value.csv
│           ├── risk_band_summary.csv
│           ├── revenue_summary.csv
│           └── pred_kpis.csv
├── notebooks/
│   ├── 01_data_overview.ipynb                      # EDA & data profiling
│   ├── 02_clean_and_validate.ipynb                 # Cleaning & type correction
│   ├── 03_feature_engineering.ipynb                # 7 engineered features
│   ├── 04_dashboard_tables.ipynb                   # Aggregation for BI
│   └── 05_churn_model.ipynb                        # Model training & evaluation
├── models/
│   ├── train_and_save.py                           # Retrain + save model artifacts
│   ├── churn_model.pkl                             # Saved model (after running script)
│   └── model_metadata.json                         # Threshold, metrics, feature list
├── sql/
│   ├── 00_setup_database.py                        # Build churn.db from CSVs
│   ├── churn.db                                    # SQLite database (after running script)
│   └── queries/
│       ├── 01_churn_by_segment.sql                 # Multi-dimension GROUP BY
│       ├── 02_revenue_at_risk.sql                  # CTE + window percentage
│       ├── 03_contract_retention_analysis.sql      # CASE WHEN business labels
│       ├── 04_tenure_cohort_analysis.sql           # LAG window function
│       ├── 05_high_risk_customer_profile.sql       # Conditional aggregation
│       ├── 06_payment_method_risk.sql              # ROW_NUMBER OVER PARTITION BY
│       ├── 07_service_bundle_analysis.sql          # Engineered feature analysis
│       └── 08_retention_roi_estimate.sql           # Financial modelling in SQL
├── app/
│   ├── app.py                                      # 5-page Streamlit dashboard
│   └── utils.py                                    # Cached data loaders
├── reports/
│   ├── executive_summary.md                        # 1-page business findings
│   ├── 01_data_overview_columns.csv
│   ├── 05_model_compare.csv
│   ├── 05_logreg_top_positive.csv
│   ├── 05_logreg_top_negative.csv
│   ├── 05_perm_importance.csv
│   └── figures/
│       ├── generate_charts.py                      # Produces all 6 PNGs
│       ├── 01_churn_by_contract.png
│       ├── 02_churn_by_tenure.png
│       ├── 03_churn_by_value_segment.png
│       ├── 04_feature_importance.png
│       ├── 05_risk_band_distribution.png
│       └── 06_revenue_at_risk.png
├── dashboards/                                     # Tableau workbook (see link above)
├── requirements.txt
└── README.md
```

---

## SQL Highlights

The 8 queries in `sql/queries/` demonstrate production-level SQL skills:

- **Window functions** — `LAG()` for period-over-period churn delta, `ROW_NUMBER() OVER PARTITION BY` for within-group ranking
- **CTEs** — chained `WITH` clauses for readable multi-step calculations
- **Conditional aggregation** — `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` for cross-tabulated metrics
- **Business financial modelling** — Query 08 estimates the ROI of a retention discount programme entirely in SQL

---

## Analytical Questions Answered

- What factors cause customer churn?
- Which customers are at highest risk right now?
- How much revenue is at risk, and which bands are recoverable?
- Which customer segments need retention strategies, and what is the ROI?
