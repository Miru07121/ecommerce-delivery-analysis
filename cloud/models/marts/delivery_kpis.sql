SELECT purchase_month, customer_state,
 COUNT(*) AS eligible_deliveries,
 SUM(late) AS late_deliveries,
 SAFE_DIVIDE(SUM(late), COUNT(*)) AS late_rate
FROM {{ ref('fct_delivery_orders') }}
WHERE delivery_eligible = 1
GROUP BY purchase_month, customer_state
