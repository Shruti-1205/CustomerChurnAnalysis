-- Question: If we offered a 20% monthly discount to all High and Critical risk
--           customers to retain them, what is the estimated net revenue saved
--           versus the cost of the discount?
-- Why it matters: Translates ML predictions into a financial business case for the
--                 retention program — showing ROI before any budget is committed.
-- Demonstrates: Chained CTEs, financial arithmetic in SQL, conditional ROI verdict
-- Table: customer_predictions

WITH at_risk AS (
    SELECT
        risk_band,
        COUNT(*)                               AS customers,
        ROUND(SUM(MonthlyCharges), 2)          AS total_monthly_revenue,
        ROUND(SUM(expected_revenue_at_risk), 2) AS revenue_at_risk
    FROM customer_predictions
    WHERE risk_band IN ('Critical', 'High')
    GROUP BY risk_band
),
financials AS (
    SELECT
        risk_band,
        customers,
        total_monthly_revenue,
        revenue_at_risk,
        ROUND(total_monthly_revenue * 0.20, 2)                          AS discount_cost,
        ROUND(revenue_at_risk - (total_monthly_revenue * 0.20), 2)      AS net_revenue_saved
    FROM at_risk
),
totals AS (
    SELECT
        'TOTAL'                          AS risk_band,
        SUM(customers)                   AS customers,
        SUM(total_monthly_revenue)       AS total_monthly_revenue,
        SUM(revenue_at_risk)             AS revenue_at_risk,
        SUM(discount_cost)               AS discount_cost,
        SUM(net_revenue_saved)           AS net_revenue_saved
    FROM financials
)
SELECT
    risk_band,
    customers,
    total_monthly_revenue,
    revenue_at_risk,
    discount_cost,
    net_revenue_saved,
    CASE WHEN net_revenue_saved > 0 THEN 'Positive ROI' ELSE 'Negative ROI' END AS roi_verdict
FROM financials
UNION ALL
SELECT * FROM totals
ORDER BY
    CASE risk_band
        WHEN 'Critical' THEN 1
        WHEN 'High'     THEN 2
        ELSE 3
    END;
