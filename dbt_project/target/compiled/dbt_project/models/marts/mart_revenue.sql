WITH orders AS (
    SELECT * FROM "marketpulse360"."analytics"."stg_orders"
),
items AS (
    SELECT * FROM "marketpulse360"."analytics"."stg_order_items"
),
joined AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_date,
        o.year,
        o.month,
        SUM(i.price)           AS revenue,
        SUM(i.freight_value)   AS freight,
        SUM(i.total_item_value) AS total_value,
        COUNT(i.product_id)    AS nb_items
    FROM orders o
    JOIN items i ON o.order_id = i.order_id
    GROUP BY o.order_id, o.customer_id, o.order_date, o.year, o.month
)
SELECT * FROM joined