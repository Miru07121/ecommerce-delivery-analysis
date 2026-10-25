-- Exact baseline counts and exact medians; returns zero rows on success.
WITH metrics AS (
 SELECT COUNT(*) total_orders, COUNTIF(delivery_eligible=1) eligible_orders,
 COUNTIF(delivery_eligible=1 AND late=1) late_orders
 FROM {{ ref('fct_delivery_orders') }}
), medians AS (
 SELECT DISTINCT PERCENTILE_CONT(delivery_days,0.5) OVER() median_delivery_days
 FROM {{ ref('fct_delivery_orders') }} WHERE delivery_eligible=1
), delays AS (
 SELECT DISTINCT PERCENTILE_CONT(delay_days,0.5) OVER() median_late_delay_days
 FROM {{ ref('fct_delivery_orders') }} WHERE delivery_eligible=1 AND late=1
)
SELECT * FROM metrics CROSS JOIN medians CROSS JOIN delays
WHERE total_orders != 99441 OR eligible_orders != 96470 OR late_orders != 6534
 OR median_delivery_days != 10 OR median_late_delay_days != 7
