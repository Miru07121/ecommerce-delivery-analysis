-- seller rankings use single-seller orders only; outcome belongs to the ORDER.
WITH grouped AS (
 SELECT 'state' AS dimension,customer_state AS segment,COUNT(*) AS orders,SUM(late) AS late_orders FROM order_mart WHERE delivery_eligible=1 GROUP BY customer_state
 UNION ALL
 SELECT 'category',category,COUNT(*),SUM(late) FROM order_mart WHERE delivery_eligible=1 GROUP BY category
 UNION ALL
 SELECT 'seller',seller_id,COUNT(*),SUM(late) FROM order_mart WHERE delivery_eligible=1 AND seller_count=1 GROUP BY seller_id
), rates AS (
 SELECT *,1.0*late_orders/orders AS late_rate FROM grouped WHERE orders>=100
)
SELECT *,ROW_NUMBER() OVER(PARTITION BY dimension ORDER BY late_orders DESC,orders DESC,segment) AS late_volume_rank
FROM rates ORDER BY dimension,late_volume_rank;
