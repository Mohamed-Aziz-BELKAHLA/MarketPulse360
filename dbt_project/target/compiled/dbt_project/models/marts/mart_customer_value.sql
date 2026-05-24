WITH revenue AS (
    SELECT * FROM "marketpulse360"."analytics"."mart_revenue"
),
customers AS (
    SELECT * FROM "marketpulse360"."analytics"."stg_customers"
),
aggregated AS (
    SELECT
        c.customer_unique_id,
        c.customer_state,
        COUNT(DISTINCT r.order_id)      AS nb_orders,
        SUM(r.revenue)                  AS total_spent,
        AVG(r.revenue)                  AS avg_order_value,
        MIN(r.order_date)               AS first_order,
        MAX(r.order_date)               AS last_order,
        MAX(r.order_date) - MIN(r.order_date) AS customer_lifetime_days
    FROM revenue r
    JOIN customers c ON r.customer_id = c.customer_id
    GROUP BY c.customer_unique_id, c.customer_state
)
SELECT
    *,
    CASE
        WHEN nb_orders >= 3                    THEN 'Champion'
        WHEN total_spent >= 500                THEN 'High Value'
        WHEN nb_orders = 1 AND total_spent < 100 THEN 'One-Time Low'
        ELSE 'Regular'
    END AS customer_segment
FROM aggregated