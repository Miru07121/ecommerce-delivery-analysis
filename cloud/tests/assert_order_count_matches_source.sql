-- dbt singular test: return failing rows only.
SELECT
 (SELECT COUNT(*) FROM {{ source('olist_raw', 'orders') }}) AS raw_orders,
 (SELECT COUNT(*) FROM {{ ref('fct_delivery_orders') }}) AS mart_orders
WHERE (SELECT COUNT(*) FROM {{ source('olist_raw', 'orders') }})
   != (SELECT COUNT(*) FROM {{ ref('fct_delivery_orders') }})
