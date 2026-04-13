# Executive Summary: Telecom Customer Churn Analysis

**Prepared for:** Business Stakeholders
**Date:** April 2026
**Dataset:** 7,043 IBM Telco Customers | 21 Features
**Analyst:** Shrutili12

---

## Business Problem

Customer churn is one of the highest-cost problems in the telecom industry. Acquiring a new customer costs 5–7× more than retaining an existing one. This analysis identifies which customers are at risk of leaving, how much revenue they represent, and what actions can prevent their departure.

## Methodology

- **Data preparation:** 7,043 customer records cleaned, validated, and enriched with 7 engineered features (tenure cohort, service count, value segment, contract flags)
- **Descriptive analytics:** Churn rate segmented across contract type, tenure, pricing tier, and customer lifetime value to identify the highest-risk groups
- **Predictive modelling:** HistGradientBoosting Classifier (calibrated) trained with cross-validation and threshold optimisation, achieving ROC-AUC 0.8448 — each customer scored with a churn probability and risk band (Critical / High / Medium / Low)

---

## Key Findings

### Finding 1: 1 in 4 Customers Are Leaving — Month-to-Month Contracts Are the Primary Driver

- Overall churn rate: **26.54%** (1,869 of 7,043 customers)
- Month-to-month contracts: **42.71% churn** vs. 11.27% (one-year) and 2.83% (two-year)
- 3,875 customers (55% of the base) are currently on month-to-month contracts
- **The gap between month-to-month and two-year contracts is 15×** — the single most actionable lever available

### Finding 2: The First 12 Months Are the Most Dangerous Window

- **48.28% of new customers (0–12 months tenure) churn** — nearly 1 in 2
- This rate drops steadily with tenure: 29.5% at 12–24 months, 8.3% after 60+ months
- Customers who survive year one are dramatically more loyal — the first-year experience defines long-term retention

### Finding 3: $2.86M in Monthly Revenue Is at Risk

- Total monthly revenue: **$16.06M**
- Revenue at risk from churning customers: **$2.86M (17.83%)**
- Critical-risk band (384 customers): **88.28% actual churn rate** — these customers are effectively already leaving
- High-risk band (1,089 customers): **62.81% actual churn rate** — significant but recoverable

### Finding 4: Fiber Optic Internet Without Security Add-Ons Is a Strong Churn Signal

- Internet service type is the #3 most important predictive feature (permutation importance: 0.0363)
- Fiber optic customers with no Online Security show disproportionately high churn
- These customers pay more (higher monthly charges) but feel under-protected — a loyalty gap
- Electronic check payment method also correlates with elevated churn (logistic coefficient: +0.25)

---

## Recommendations

### Recommendation 1: Launch a Contract Upgrade Campaign

**Target:** 3,875 month-to-month customers, prioritised by model risk score
**Action:** Offer a 10–15% monthly discount or added service benefit in exchange for upgrading to a one-year contract
**Estimated impact:** A 10% reduction in month-to-month churn retains ~165 customers/month
**Revenue protected:** ~$1.28M annually at $64.76 average monthly charge

### Recommendation 2: Deploy a First-Year Onboarding Retention Program

**Target:** All customers in months 0–12, especially those with fiber optic and no security services
**Action:** Structured check-ins at months 1, 3, and 6; proactive offer of Online Security at a trial discount
**Rationale:** The model flags 48% of new customers as likely to churn — early intervention is the highest-leverage point
**Cost:** Low (proactive outreach is far cheaper than reacquisition)

### Recommendation 3: Immediate Outreach to 384 Critical-Risk Customers

**Target:** All customers in the Critical risk band (churn probability ≥ 75%)
**Action:** Personalised retention calls with a pre-approved offer (contract upgrade, service bundle, or discount)
**Revenue at stake:** $78,891/month from this cohort alone
**Financial modelling:** A 20% discount offer to Critical + High risk customers costs ~$257K/month but saves ~$537K in at-risk revenue — a net benefit of ~$280K/month (see `sql/queries/08_retention_roi_estimate.sql`)

---

## Model Performance Summary

| Model | ROC-AUC | Avg Precision |
|-------|---------|---------------|
| HGB Calibrated (selected) | **0.8448** | **0.6532** |
| Logistic Regression | 0.8447 | 0.6514 |
| HGB Tuned (uncalibrated) | 0.8437 | 0.6613 |
| HGB Baseline | 0.8229 | 0.6180 |

Decision threshold optimised to **0.3143** (vs. default 0.5) using the precision-recall curve to maximise recall on the minority churn class — recall: 77.0%, precision: 55.6%, F1: 0.646.

---

*Full code, SQL queries, interactive dashboard, and Tableau visualisations available in the project repository.*
