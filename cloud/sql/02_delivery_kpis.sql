-- First build only: fails if destination exists; never replaces existing data.
CREATE TABLE `secret-drake-512620-i7.ecommerce_analytics.delivery_kpis` AS
SELECT purchase_month, customer_state,
 COUNT(*) AS eligible_deliveries,
 SUM(late) AS late_deliveries,
 SAFE_DIVIDE(SUM(late), COUNT(*)) AS late_rate
FROM `secret-drake-512620-i7.ecommerce_analytics.fct_delivery_orders`
WHERE delivery_eligible = 1
GROUP BY purchase_month, customer_state;
