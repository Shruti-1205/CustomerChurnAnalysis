-- Question: What is the churn rate across all major segmentation dimensions simultaneously?
-- Why it matters: Reveals which combinations of contract type, tenure, and customer value
--                 carry the highest churn risk — enables targeted retention prioritization.
-- Table: customer_predictions

SELECT
    Contract,
    tenure_group,
    customer_value_segment,
    COUNT(*)                                          AS customers,
    SUM(Churn)                                        AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2)           AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                     AS avg_monthly_charge,
    ROUND(AVG(churn_probability) * 100, 2)            AS avg_model_churn_prob_pct
FROM customer_predictions
GROUP BY Contract, tenure_group, customer_value_segment
ORDER BY churn_rate_pct DESC;
