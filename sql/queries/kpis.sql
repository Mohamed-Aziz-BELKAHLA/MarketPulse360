-- ============================================
-- KPI 1 : Chiffre d'affaires mensuel
-- ============================================
SELECT
    year,
    month,
    COUNT(DISTINCT order_id)        AS nb_orders,
    ROUND(SUM(product_price)::numeric, 2)    AS revenue,
    ROUND(AVG(product_price)::numeric, 2)    AS avg_order_value
FROM fact_orders
GROUP BY year, month
ORDER BY year, month;

-- ============================================
-- KPI 2 : Top 10 catégories par revenu
-- ============================================
SELECT
    dp.category,
    COUNT(DISTINCT fo.order_id)             AS nb_orders,
    ROUND(SUM(fo.product_price)::numeric, 2) AS total_revenue,
    ROUND(AVG(fo.product_price)::numeric, 2) AS avg_price,
    ROUND(AVG(fo.review_score)::numeric, 2)  AS avg_review
FROM fact_orders fo
JOIN dim_products dp ON fo.product_id = dp.product_id
GROUP BY dp.category
ORDER BY total_revenue DESC
LIMIT 10;

-- ============================================
-- KPI 3 : Performance par état (région)
-- ============================================
SELECT
    dc.customer_state,
    COUNT(DISTINCT fo.order_id)              AS nb_orders,
    COUNT(DISTINCT fo.customer_id)           AS nb_customers,
    ROUND(SUM(fo.product_price)::numeric, 2)  AS total_revenue,
    ROUND(AVG(fo.product_price)::numeric, 2)  AS avg_order_value
FROM fact_orders fo
JOIN dim_customers dc ON fo.customer_id = dc.customer_id
GROUP BY dc.customer_state
ORDER BY total_revenue DESC;

-- ============================================
-- KPI 4 : Analyse freight (proxy marge)
-- ============================================
SELECT
    dp.category,
    ROUND(AVG(fo.product_price)::numeric, 2)    AS avg_price,
    ROUND(AVG(fo.freight_value)::numeric, 2)    AS avg_freight,
    ROUND(AVG(fo.freight_value / NULLIF(fo.product_price, 0) * 100)::numeric, 2) AS freight_ratio_pct
FROM fact_orders fo
JOIN dim_products dp ON fo.product_id = dp.product_id
GROUP BY dp.category
HAVING AVG(fo.product_price) > 0
ORDER BY freight_ratio_pct DESC;

-- ============================================
-- KPI 5 : Satisfaction client par catégorie
-- ============================================
SELECT
    dp.category,
    COUNT(fo.review_score)                      AS nb_reviews,
    ROUND(AVG(fo.review_score)::numeric, 2)     AS avg_score,
    SUM(CASE WHEN fo.review_score >= 4 THEN 1 ELSE 0 END) AS positive_reviews,
    SUM(CASE WHEN fo.review_score <= 2 THEN 1 ELSE 0 END) AS negative_reviews
FROM fact_orders fo
JOIN dim_products dp ON fo.product_id = dp.product_id
WHERE fo.review_score IS NOT NULL
GROUP BY dp.category
ORDER BY avg_score DESC;

-- ============================================
-- KPI 6 : Valeur client (CLV simple)
-- ============================================
SELECT
    dc.customer_unique_id,
    dc.customer_state,
    COUNT(DISTINCT fo.order_id)              AS nb_orders,
    ROUND(SUM(fo.product_price)::numeric, 2)  AS total_spent,
    ROUND(AVG(fo.product_price)::numeric, 2)  AS avg_order_value,
    MIN(fo.order_date)                        AS first_order,
    MAX(fo.order_date)                        AS last_order
FROM fact_orders fo
JOIN dim_customers dc ON fo.customer_id = dc.customer_id
GROUP BY dc.customer_unique_id, dc.customer_state
ORDER BY total_spent DESC;

-- ============================================
-- KPI 7 : Détection anomalies — orders suspects
-- ============================================
SELECT
    order_id,
    product_price,
    freight_value,
    payment_value,
    ABS(product_price + freight_value - payment_value) AS payment_gap,
    review_score
FROM fact_orders
WHERE ABS(product_price + freight_value - payment_value) > 50
   OR product_price <= 0
   OR freight_value > product_price * 2
ORDER BY payment_gap DESC
LIMIT 100;