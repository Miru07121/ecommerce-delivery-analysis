-- Poor review must be 1 for scores 1-2, 0 for scores 3-5,
-- and NULL for missing scores. Return inconsistent orders.
SELECT order_id, review_score, poor_review
FROM {{ ref('fct_delivery_orders') }}
WHERE poor_review IS DISTINCT FROM
  CASE
    WHEN review_score BETWEEN 1 AND 2 THEN 1
    WHEN review_score BETWEEN 3 AND 5 THEN 0
    ELSE NULL
  END
