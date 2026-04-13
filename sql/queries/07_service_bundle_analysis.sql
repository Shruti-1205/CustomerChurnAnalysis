-- Question: Do customers with more add-on services churn less? Where is the
--           engagement sweet spot that correlates with retention?
-- Why it matters: Higher service adoption signals deeper product engagement and
--                 increases switching costs — a lever for proactive bundling offers.
-- Demonstrates: GROUP BY on engineered feature, CASE bucketing, multi-metric output
-- Table: customer_predictions

SELECT
    num_services,
    COUNT(*)                                          AS customers,
    SUM(Churn)                                        AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2)          AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                     AS avg_monthly_charge,
    ROUND(AVG(churn_probability) * 100, 2)           AS avg_predicted_churn_pct,
    CASE
        WHEN num_services <= 2 THEN 'Minimal Bundle'
        WHEN num_services <= 4 THEN 'Standard Bundle'
        ELSE 'Full Bundle'
    END                                               AS bundle_tier
FROM customer_predictions
GROUP BY num_services
ORDER BY num_services;
