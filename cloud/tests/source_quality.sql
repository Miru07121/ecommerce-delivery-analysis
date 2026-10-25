SELECT 'orders_key' AS check_name, COUNT(*) AS violations FROM (SELECT order_id FROM {{ source('olist_raw','orders') }} GROUP BY order_id HAVING order_id IS NULL OR COUNT(*) > 1) HAVING COUNT(*) > 0
UNION ALL
SELECT 'customers_key' AS check_name, COUNT(*) AS violations FROM (SELECT customer_id FROM {{ source('olist_raw','customers') }} GROUP BY customer_id HAVING customer_id IS NULL OR COUNT(*) > 1) HAVING COUNT(*) > 0
UNION ALL
SELECT 'products_key' AS check_name, COUNT(*) AS violations FROM (SELECT product_id FROM {{ source('olist_raw','products') }} GROUP BY product_id HAVING product_id IS NULL OR COUNT(*) > 1) HAVING COUNT(*) > 0
UNION ALL
SELECT 'sellers_key' AS check_name, COUNT(*) AS violations FROM (SELECT seller_id FROM {{ source('olist_raw','sellers') }} GROUP BY seller_id HAVING seller_id IS NULL OR COUNT(*) > 1) HAVING COUNT(*) > 0
UNION ALL
SELECT 'translations_key' AS check_name, COUNT(*) AS violations FROM (SELECT product_category_name FROM {{ source('olist_raw','translations') }} GROUP BY product_category_name HAVING product_category_name IS NULL OR COUNT(*) > 1) HAVING COUNT(*) > 0
UNION ALL
SELECT 'items_key' AS check_name, COUNT(*) violations FROM (SELECT order_id, order_item_id FROM {{ source('olist_raw','items') }} GROUP BY 1,2 HAVING order_id IS NULL OR order_item_id IS NULL OR COUNT(*)>1) HAVING COUNT(*)>0
UNION ALL
SELECT 'items_order_id_fk' AS check_name, COUNT(*) violations FROM {{ source('olist_raw','items') }} c LEFT JOIN {{ source('olist_raw','orders') }} p USING(order_id) WHERE p.order_id IS NULL HAVING COUNT(*)>0
UNION ALL
SELECT 'reviews_order_id_fk' AS check_name, COUNT(*) violations FROM {{ source('olist_raw','reviews') }} c LEFT JOIN {{ source('olist_raw','orders') }} p USING(order_id) WHERE p.order_id IS NULL HAVING COUNT(*)>0
UNION ALL
SELECT 'orders_customer_id_fk' AS check_name, COUNT(*) violations FROM {{ source('olist_raw','orders') }} c LEFT JOIN {{ source('olist_raw','customers') }} p USING(customer_id) WHERE p.customer_id IS NULL HAVING COUNT(*)>0
UNION ALL
SELECT 'items_product_id_fk' AS check_name, COUNT(*) violations FROM {{ source('olist_raw','items') }} c LEFT JOIN {{ source('olist_raw','products') }} p USING(product_id) WHERE p.product_id IS NULL HAVING COUNT(*)>0
UNION ALL
SELECT 'items_seller_id_fk' AS check_name, COUNT(*) violations FROM {{ source('olist_raw','items') }} c LEFT JOIN {{ source('olist_raw','sellers') }} p USING(seller_id) WHERE p.seller_id IS NULL HAVING COUNT(*)>0
UNION ALL
SELECT 'review_score_range' AS check_name, COUNT(*) violations FROM {{ source('olist_raw','reviews') }} WHERE review_score IS NULL OR review_score NOT BETWEEN 1 AND 5 HAVING COUNT(*)>0
UNION ALL
SELECT 'mart_key' AS check_name, COUNT(*) violations FROM (SELECT order_id FROM {{ ref('fct_delivery_orders') }} GROUP BY 1 HAVING order_id IS NULL OR COUNT(*)>1) HAVING COUNT(*)>0
