-- Every order's item_count should equal the raw item-row count.
-- Orders with no items should retain a NULL item_count after the left join.
WITH raw_counts AS (
  SELECT order_id, COUNT(*) AS expected_item_count
  FROM {{ source('olist_raw', 'items') }}
  GROUP BY order_id
)
SELECT f.order_id, f.item_count, r.expected_item_count
FROM {{ ref('fct_delivery_orders') }} AS f
LEFT JOIN raw_counts AS r USING (order_id)
WHERE f.item_count IS DISTINCT FROM r.expected_item_count
