WITH source AS (
    SELECT * FROM "marketpulse360"."public"."raw_order_items"
)
SELECT
    order_id,
    product_id,
    seller_id,
    price,
    freight_value,
    price + freight_value AS total_item_value
FROM source