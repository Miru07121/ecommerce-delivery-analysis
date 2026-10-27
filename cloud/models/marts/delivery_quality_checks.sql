{{ config(materialized='view') }}
-- An exception report: zero rows means the checks pass.
WITH mart AS (
  SELECT * FROM {{ ref('fct_delivery_orders') }}
), exceptions AS (
  SELECT 'null_order_id' AS check_name, COUNTIF(order_id IS NULL) AS failing_rows FROM mart
  UNION ALL
  SELECT 'duplicate_order_id', COUNT(*) - COUNT(DISTINCT order_id) FROM mart
  UNION ALL
  SELECT 'invalid_delivery_flag', COUNTIF(delivery_eligible NOT IN (0,1) OR delivery_eligible IS NULL) FROM mart
  UNION ALL
  SELECT 'invalid_late_flag', COUNTIF(late NOT IN (0,1) OR late IS NULL) FROM mart
  UNION ALL
  SELECT 'late_without_eligible_delivery', COUNTIF(delivery_eligible = 0 AND late = 1) FROM mart
  UNION ALL
  SELECT 'negative_eligible_duration', COUNTIF(delivery_eligible = 1 AND delivery_days < 0) FROM mart
  UNION ALL
  SELECT 'invalid_review_score', COUNTIF(review_score IS NOT NULL AND review_score NOT BETWEEN 1 AND 5) FROM mart
)
SELECT * FROM exceptions WHERE failing_rows > 0
