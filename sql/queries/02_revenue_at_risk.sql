-- Question: How much monthly revenue is at risk by predicted risk band, and what
--           percentage of total revenue does each band represent?
-- Why it matters: Converts ML predictions into a financial impact statement that
--                 business stakeholders can act on immediately.
-- Demonstrates: WITH CTE, window-style percentage calculation
-- Table: customer_predictions

WITH total AS (
    SELECT SUM(MonthlyCharges) AS grand_total
    FROM customer_predictions
),
by_band AS (
    SELECT
        risk_band,
        COUNT(*)                                       AS customers,
        ROUND(SUM(MonthlyCharges), 2)                  AS total_monthly_revenue,
        ROUND(SUM(expected_revenue_at_risk), 2)        AS revenue_at_risk
    FROM customer_predictions
    GROUP BY risk_band
)
SELECT
    b.risk_band,
    b.customers,
    b.total_monthly_revenue,
    b.revenue_at_risk,
    ROUND(100.0 * b.revenue_at_risk / t.grand_total, 2)   AS pct_of_total_revenue,
    CASE b.risk_band
        WHEN 'Critical' THEN 1
        WHEN 'High'     THEN 2
        WHEN 'Medium'   THEN 3
        WHEN 'Low'      THEN 4
    END AS sort_order
FROM by_band b, total t
ORDER BY sort_order;
