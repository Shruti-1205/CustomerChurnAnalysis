-- Question: Does payment method correlate with churn, and does it add predictive
--           signal beyond contract type?
-- Why it matters: Electronic check users churn at significantly higher rates —
--                 a potential proxy for financial instability or low commitment.
-- Demonstrates: ROW_NUMBER() OVER PARTITION BY, CTE, ranking within a group
-- Table: customer_predictions

WITH payment_contract AS (
    SELECT
        PaymentMethod,
        Contract,
        COUNT(*)                                           AS customers,
        SUM(Churn)                                         AS churned,
        ROUND(100.0 * SUM(Churn) / COUNT(*), 2)           AS churn_rate_pct,
        ROUND(AVG(churn_probability) * 100, 2)            AS avg_churn_prob_pct,
        ROW_NUMBER() OVER (
            PARTITION BY PaymentMethod
            ORDER BY SUM(Churn) DESC
        )                                                  AS rank_within_payment
    FROM customer_predictions
    GROUP BY PaymentMethod, Contract
)
SELECT
    PaymentMethod,
    Contract,
    customers,
    churned,
    churn_rate_pct,
    avg_churn_prob_pct,
    rank_within_payment
FROM payment_contract
ORDER BY PaymentMethod, churn_rate_pct DESC;
