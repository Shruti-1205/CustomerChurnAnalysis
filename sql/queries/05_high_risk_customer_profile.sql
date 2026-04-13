-- Question: What is the demographic and service profile of Critical-risk customers
--           compared to Low-risk customers?
-- Why it matters: Identifies the archetypal at-risk customer — new, on fiber optic,
--                 month-to-month — enabling surgical retention targeting.
-- Demonstrates: Conditional aggregation with SUM() on 0/1 columns, CASE sort order
-- Table: customer_predictions

SELECT
    risk_band,
    COUNT(*)                                                        AS customers,
    ROUND(100.0 * SUM(SeniorCitizen)      / COUNT(*), 1)           AS pct_senior,
    ROUND(100.0 * SUM(Partner)            / COUNT(*), 1)           AS pct_with_partner,
    ROUND(100.0 * SUM(CASE WHEN InternetService = 'Fiber optic'
                           THEN 1 ELSE 0 END) / COUNT(*), 1)       AS pct_fiber_optic,
    ROUND(100.0 * SUM(is_month_to_month)  / COUNT(*), 1)           AS pct_month_to_month,
    ROUND(100.0 * SUM(is_new_customer)    / COUNT(*), 1)           AS pct_new_customer,
    ROUND(AVG(num_services), 2)                                     AS avg_num_services,
    ROUND(AVG(MonthlyCharges), 2)                                   AS avg_monthly_charge,
    ROUND(AVG(churn_probability) * 100, 2)                         AS avg_churn_prob_pct,
    ROUND(SUM(expected_revenue_at_risk), 2)                        AS total_revenue_at_risk
FROM customer_predictions
GROUP BY risk_band
ORDER BY
    CASE risk_band
        WHEN 'Critical' THEN 1
        WHEN 'High'     THEN 2
        WHEN 'Medium'   THEN 3
        WHEN 'Low'      THEN 4
    END;
