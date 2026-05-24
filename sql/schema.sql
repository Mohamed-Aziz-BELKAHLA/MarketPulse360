-- ============================================
-- SCHEMA EN ETOILE — MarketPulse 360
-- ============================================

-- Table de faits principale
CREATE TABLE IF NOT EXISTS fact_orders AS
SELECT
    o.order_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,
    o.order_purchase_timestamp::timestamp::date        AS order_date,
    EXTRACT(YEAR  FROM o.order_purchase_timestamp::timestamp)::int AS year,
    EXTRACT(MONTH FROM o.order_purchase_timestamp::timestamp)::int AS month,
    EXTRACT(DOW   FROM o.order_purchase_timestamp::timestamp)::int AS day_of_week,
    oi.price                                AS product_price,
    oi.freight_value,
    oi.price + oi.freight_value             AS total_price,
    p.payment_value,
    o.order_status,
    r.review_score
FROM raw_orders o
LEFT JOIN raw_order_items    oi ON o.order_id   = oi.order_id
LEFT JOIN raw_payments        p ON o.order_id   = p.order_id AND p.payment_sequential = 1
LEFT JOIN raw_reviews         r ON o.order_id   = r.order_id
WHERE o.order_status = 'delivered';

-- Dimension clients
CREATE TABLE IF NOT EXISTS dim_customers AS
SELECT
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state
FROM raw_customers;

-- Dimension produits
CREATE TABLE IF NOT EXISTS dim_products AS
SELECT
    p.product_id,
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
FROM raw_products p
LEFT JOIN raw_category_translation t
       ON p.product_category_name = t.product_category_name;

-- Dimension vendeurs
CREATE TABLE IF NOT EXISTS dim_sellers AS
SELECT
    seller_id,
    seller_city,
    seller_state
FROM raw_sellers;