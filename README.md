# Telecom Customer Churn Analysis

End-to-end churn analysis and prediction for a telecom company with 7,043 customers.
Built to answer: who will leave, when, and what it costs.

---

## Live Demo

| | Link |
|---|---|
| Streamlit App | [Open App](https://telcocustomerchurnanalysis.streamlit.app) |
| Tableau Dashboard | [View Dashboard]([https://public.tableau.com/your-dashboard-link](https://public.tableau.com/app/profile/shruti.liladhar.devlekar/viz/Customer_Churn_and_Revenue_Overview/Dashboard1)) |

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

## Tech Stack

| Layer | Tools |
|-------|-------|
| Data processing | Python, pandas, numpy |
| Machine learning | scikit-learn (HGB, Logistic Regression, calibration, cross-validation) |
| SQL | SQLite |
| Visualisation | matplotlib, seaborn, Altair |
| App | Streamlit |
| BI | Tableau Public |

---

## How to Run

**Prerequisites**

```bash
pip install -r requirements.txt
```

**Train the model**

```bash
python models/train_and_save.py
```

**Build the SQL database**

```bash
python sql/00_setup_database.py
```

**Generate charts**

```bash
python reports/figures/generate_charts.py
```

**Launch the Streamlit app**

```bash
streamlit run app/app.py
```

**Run SQL queries (optional)**

Open `sql/churn.db` in DB Browser for SQLite, or run:

```bash
sqlite3 sql/churn.db < sql/queries/02_revenue_at_risk.sql
```

---

## Key Findings

1. Month-to-month customers churn at 42.71% compared to 2.83% for two-year contracts.
2. 48.28% of customers churn within their first 12 months. This drops to 8.3% after 5 years.
3. Targeted retention for High and Critical risk customers has a positive ROI. See `sql/queries/08_retention_roi_estimate.sql`.
4. The top 3 churn predictors are tenure, contract type, and internet service type.

---

## Project Structure

```
customer-churn-platform/
├── data/
│   ├── raw/
│   │   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│   └── processed/
│       ├── cleaned_churn_data.csv
│       ├── analytics_ready_churn_data.csv
│       └── dashboard_tables/
│           ├── customer_predictions.csv
│           ├── top_50_high_risk_customers.csv
│           ├── kpi_summary.csv
│           ├── churn_by_contract.csv
│           ├── churn_by_tenure.csv
│           ├── churn_by_charge.csv
│           ├── churn_by_value.csv
│           ├── risk_band_summary.csv
│           ├── revenue_summary.csv
│           └── pred_kpis.csv
├── notebooks/
│   ├── 01_data_overview.ipynb
│   ├── 02_clean_and_validate.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_dashboard_tables.ipynb
│   └── 05_churn_model.ipynb
├── models/
│   ├── train_and_save.py
│   └── model_metadata.json
├── sql/
│   ├── 00_setup_database.py
│   └── queries/
│       ├── 01_churn_by_segment.sql
│       ├── 02_revenue_at_risk.sql
│       ├── 03_contract_retention_analysis.sql
│       ├── 04_tenure_cohort_analysis.sql
│       ├── 05_high_risk_customer_profile.sql
│       ├── 06_payment_method_risk.sql
│       ├── 07_service_bundle_analysis.sql
│       └── 08_retention_roi_estimate.sql
├── app/
│   ├── app.py
│   └── utils.py
├── reports/
│   ├── executive_summary.md
│   └── figures/
│       ├── generate_charts.py
│       └── *.png
├── requirements.txt
└── README.md
```

---

## SQL Queries

8 queries covering segmentation, cohort analysis, risk profiling, and retention ROI estimation.
Concepts used: window functions (`LAG`, `ROW_NUMBER`), CTEs, conditional aggregation, and financial modelling.

---

## Analytical Questions

- What factors cause customer churn?
- Which customers are at highest risk right now?
- How much revenue is at risk?
- Which segments need retention strategies, and what is the estimated ROI?
