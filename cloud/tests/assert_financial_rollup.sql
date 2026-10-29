-- Validate the order-level item and freight totals against raw items.
-- SAFE_CAST mirrors the mart's current conversion behavior.
WITH raw_totals AS (
  SELECT
    order_id,
    SUM(SAFE_CAST(price AS NUMERIC)) AS expected_item_value_brl,
    SUM(SAFE_CAST(freight_value AS NUMERIC)) AS expected_freight_brl
  FROM {{ source('olist_raw', 'items') }}
  GROUP BY order_id
)
SELECT f.order_id,
       f.item_value_brl, r.expected_item_value_brl,
       f.freight_brl, r.expected_freight_brl
FROM {{ ref('fct_delivery_orders') }} f
LEFT JOIN raw_totals r USING (order_id)
WHERE f.item_value_brl IS DISTINCT FROM r.expected_item_value_brl
   OR f.freight_brl IS DISTINCT FROM r.expected_freight_brl
