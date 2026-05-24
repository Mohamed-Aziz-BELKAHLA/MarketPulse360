WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_orders') }}
),
cleaned AS (
    SELECT
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp::timestamp::date       AS order_date,
        order_delivered_customer_date::timestamp::date  AS delivered_date,
        EXTRACT(YEAR  FROM order_purchase_timestamp::timestamp)::int AS year,
        EXTRACT(MONTH FROM order_purchase_timestamp::timestamp)::int AS month
    FROM source
    WHERE order_status = 'delivered'
      AND order_purchase_timestamp IS NOT NULL
)
SELECT * FROM cleaned