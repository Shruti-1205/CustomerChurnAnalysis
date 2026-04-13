-- Question: Which contract type drives the most recoverable churners, and what is
--           the business case for a contract upgrade campaign?
-- Why it matters: Month-to-month customers churn at 15x the rate of two-year customers.
--                 Quantifying this gap helps size the retention opportunity.
-- Demonstrates: CASE WHEN business labeling, multi-metric aggregation
-- Table: customer_predictions

SELECT
    Contract,
    COUNT(*)                                                  AS total_customers,
    SUM(Churn)                                                AS actual_churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2)                  AS churn_rate_pct,
    SUM(predicted_churn)                                      AS model_predicted_churn,
    ROUND(AVG(churn_probability) * 100, 2)                   AS avg_churn_probability_pct,
    ROUND(SUM(MonthlyCharges), 2)                             AS total_monthly_revenue,
    ROUND(SUM(expected_revenue_at_risk), 2)                   AS revenue_at_risk,
    CASE
        WHEN ROUND(100.0 * SUM(Churn) / COUNT(*), 2) > 30 THEN 'Priority Retention'
        WHEN ROUND(100.0 * SUM(Churn) / COUNT(*), 2) > 10 THEN 'Moderate Risk'
        ELSE 'Low Risk'
    END                                                       AS retention_priority
FROM customer_predictions
GROUP BY Contract
ORDER BY churn_rate_pct DESC;
