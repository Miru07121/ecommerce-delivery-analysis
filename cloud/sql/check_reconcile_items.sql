WITH raw AS (
 SELECT SUM(price) value, SUM(freight_value) freight FROM `secret-drake-512620-i7.olist_raw.items`
), mart AS (
 SELECT SUM(item_value_brl) value, SUM(freight_brl) freight FROM `secret-drake-512620-i7.ecommerce_analytics.fct_delivery_orders`
)
SELECT raw.value AS raw_value, mart.value AS mart_value, raw.freight AS raw_freight, mart.freight AS mart_freight
FROM raw CROSS JOIN mart
WHERE raw.value IS DISTINCT FROM mart.value OR raw.freight IS DISTINCT FROM mart.freight;
