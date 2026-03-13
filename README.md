# Customer Churn Intelligence Platform

An end-to-end machine learning and analytics project focused on **predicting telecom customer churn, identifying high-risk customers, and estimating potential revenue loss**.

The project combines **data analysis, predictive modeling, and business-focused insights** to help organizations proactively retain customers.

This repository demonstrates a full **data science workflow** from raw data exploration to production-style model evaluation and explainability.

---

# Project Objectives

Customer churn significantly impacts revenue for subscription-based businesses.

This project aims to:

• Analyze customer behavior and service usage patterns
• Identify key drivers of churn
• Build predictive models to estimate churn probability
• Segment customers by risk level
• Estimate expected revenue at risk
• Provide actionable insights for retention strategies

---

# Dataset

This project uses the **Telco Customer Churn dataset**, containing customer demographics, service usage, billing information, and churn labels.

Key characteristics:

| Metric    | Value            |
| --------- | ---------------- |
| Customers | 7,043            |
| Features  | 21               |
| Target    | Churn (Yes / No) |

Feature categories include:

**Customer demographics**

* Gender
* Senior citizen status
* Partner / dependents

**Service information**

* Internet service
* Phone service
* Streaming services
* Tech support

**Billing details**

* Contract type
* Payment method
* Monthly charges
* Total charges

---

# Project Structure

```
CustomerChurnAnalysis
│
├── data
│   ├── raw
│   └── processed
│
├── notebooks
│   ├── 01_data_cleaning.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_dashboard_tables.ipynb
│   └── 05_churn_model.ipynb
│
├── reports
│   ├── model_outputs
│   └── feature_importance
│
├── requirements.txt
└── README.md
```

---

# Data Science Workflow

The project follows a structured machine learning pipeline.

## 1 Data Cleaning

Handled:

• missing values
• inconsistent numeric fields
• categorical normalization
• feature formatting

Ensured the dataset was ready for both analysis and modeling.

---

## 2 Feature Engineering

Created several business-relevant features including:

• tenure groups
• service usage counts
• customer value segmentation
• monthly charge categories

These engineered features help capture **customer lifecycle behavior and engagement level**.

---

## 3 Exploratory Data Analysis

EDA explored relationships between churn and:

• contract type
• tenure duration
• pricing tiers
• service adoption

These insights informed feature selection and model design.

---

# Machine Learning Modeling

Multiple models were implemented and evaluated.

## Baseline Model

**Logistic Regression**

Advantages:

• highly interpretable
• strong baseline performance
• easy explanation of churn drivers

Used with:

* class balancing
* feature scaling
* one-hot encoding

---

## Advanced Model

**Histogram Gradient Boosting Classifier**

Enhancements applied:

• hyperparameter tuning with randomized search
• stratified cross-validation
• probability calibration (isotonic regression)
• optimized classification threshold

This approach improves prediction stability and probability quality.

---

# Model Evaluation

Performance was evaluated using metrics suited for imbalanced classification:

| Metric            | Purpose                  |
| ----------------- | ------------------------ |
| ROC-AUC           | overall ranking ability  |
| Average Precision | precision-recall balance |
| F1 Score          | balanced classification  |

Example results:

| Model                   | ROC-AUC | Avg Precision |
| ----------------------- | ------- | ------------- |
| Logistic Regression     | ~0.845  | ~0.651        |
| Tuned Gradient Boosting | ~0.845  | ~0.653        |

These results indicate strong predictive capability while maintaining model interpretability.

---

# Model Explainability

Two explainability approaches were used:

### Logistic Regression Coefficients

Identify features that increase or decrease churn risk.

### Permutation Feature Importance

Measures how model accuracy changes when each feature is randomly shuffled.

This highlights the **most influential drivers of churn**.

Typical drivers include:

• contract type
• tenure length
• monthly charges
• internet service type
• payment method

---

# Customer Risk Scoring

The final model produces **churn probabilities for every customer**.

Customers are categorized into risk bands:

| Risk Band | Probability Range |
| --------- | ----------------- |
| Low       | < 0.25            |
| Medium    | 0.25 – 0.50       |
| High      | 0.50 – 0.75       |
| Critical  | > 0.75            |

This segmentation enables targeted retention campaigns.

---

# Revenue Impact Estimation

For each customer:

```
Expected Revenue at Risk = Churn Probability × Total Charges
```

This allows the business to estimate **potential revenue exposure** due to churn.

---

# Outputs Generated

The modeling pipeline produces datasets for downstream analytics:

• customer-level churn probabilities
• predicted churn labels
• risk band segmentation
• expected revenue at risk

These outputs are designed for integration with **business intelligence dashboards**.

---

# Upcoming Dashboard Layer

The next phase of the project will integrate these predictions into an **interactive Tableau dashboard**.

Planned analytics include:

• churn risk distribution across customer segments
• revenue exposure by risk band
• model driver visualization
• high-risk customer identification

This layer will translate the ML outputs into **actionable business insights**.

---

# Technologies Used

Programming & Data Science:

• Python
• Pandas
• NumPy
• Scikit-learn

Machine Learning:

• Logistic Regression
• Histogram Gradient Boosting
• Probability Calibration
• Permutation Feature Importance

Analytics & Visualization:

• Jupyter Notebooks
• Tableau (planned)

Version Control:

• Git
• GitHub

---

# Business Impact

This project demonstrates how machine learning can support **proactive customer retention strategies**.

Organizations can use these insights to:

• identify customers likely to churn
• prioritize retention efforts
• estimate financial exposure
• understand key drivers of churn behavior

---

# Future Improvements

Potential enhancements include:

• SHAP-based explainability
• customer lifetime value modeling
• retention campaign simulation
• deployment as a REST API service
• real-time scoring pipeline
