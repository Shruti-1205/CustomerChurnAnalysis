-- Question: How does churn risk evolve over a customer's lifetime, and when is
--           intervention most critical?
-- Why it matters: 48% of new customers (0-12 months) churn vs only 8% after 5 years.
--                 This informs when to deploy onboarding and retention programs.
-- Demonstrates: WITH CTE, LAG window function, period-over-period delta
-- Table: customer_predictions

WITH cohort_stats AS (
    SELECT
        tenure_group,
        COUNT(*)                                         AS customers,
        SUM(Churn)                                       AS churned,
        ROUND(100.0 * SUM(Churn) / COUNT(*), 2)         AS churn_rate_pct,
        ROUND(AVG(MonthlyCharges), 2)                    AS avg_monthly_charge,
        ROUND(AVG(churn_probability) * 100, 2)           AS avg_model_churn_prob_pct
    FROM customer_predictions
    GROUP BY tenure_group
)
SELECT
    tenure_group,
    customers,
    churned,
    churn_rate_pct,
    avg_monthly_charge,
    avg_model_churn_prob_pct,
    LAG(churn_rate_pct) OVER (ORDER BY tenure_group)         AS prev_cohort_churn_rate,
    ROUND(
        churn_rate_pct
        - LAG(churn_rate_pct) OVER (ORDER BY tenure_group),
        2
    )                                                         AS churn_rate_delta_ppt
FROM cohort_stats
ORDER BY tenure_group;
