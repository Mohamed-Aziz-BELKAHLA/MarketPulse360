
  create view "marketpulse360"."analytics"."stg_customers__dbt_tmp"
    
    
  as (
    SELECT
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state
FROM "marketpulse360"."public"."raw_customers"
  );