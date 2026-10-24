{{ config(materialized='table') }}
WITH item_rollup AS (
 SELECT i.order_id,
 COUNT(*) AS item_count,
 COUNT(DISTINCT i.seller_id) AS seller_count,
 IF(COUNT(DISTINCT i.seller_id)=1, MIN(i.seller_id), 'MULTIPLE') AS seller_id,
 IF(COUNT(DISTINCT COALESCE(t.product_category_name_english,p.product_category_name,'UNKNOWN'))=1,
 MIN(COALESCE(t.product_category_name_english,p.product_category_name,'UNKNOWN')), 'MIXED') AS category,
 SUM(SAFE_CAST(i.price AS NUMERIC)) AS item_value_brl,
 SUM(SAFE_CAST(i.freight_value AS NUMERIC)) AS freight_brl
 FROM {{ source('olist_raw','items') }} i
 LEFT JOIN {{ source('olist_raw','products') }} p USING(product_id)
 LEFT JOIN {{ source('olist_raw','translations') }} t USING(product_category_name)
 GROUP BY 1
), ranked_reviews AS (
 SELECT * EXCEPT(rn) FROM (
 SELECT r.*, ROW_NUMBER() OVER(PARTITION BY order_id ORDER BY review_answer_timestamp DESC, review_creation_date DESC, review_id DESC, review_score DESC) rn
 FROM {{ source('olist_raw','reviews') }} r
 ) WHERE rn=1
), base AS (
 SELECT o.order_id, o.order_status, o.order_purchase_timestamp AS purchased_at,
 SUBSTR(o.order_purchase_timestamp,1,7) AS purchase_month,
 o.order_delivered_customer_date AS delivered_at, o.order_estimated_delivery_date AS promised_at,
 c.customer_state,i.item_count,i.seller_count,i.seller_id,s.seller_state,i.category,i.item_value_brl,i.freight_brl,
 SAFE_CAST(r.review_score AS INT64) AS review_score,r.review_creation_date,r.review_answer_timestamp,
 SAFE_CAST(SUBSTR(o.order_purchase_timestamp,1,10) AS DATE) purchase_date,
 SAFE_CAST(SUBSTR(o.order_delivered_customer_date,1,10) AS DATE) delivery_date,
 SAFE_CAST(SUBSTR(o.order_estimated_delivery_date,1,10) AS DATE) promise_date,
 SAFE_CAST(SUBSTR(r.review_creation_date,1,10) AS DATE) review_date
 FROM {{ source('olist_raw','orders') }} o
 LEFT JOIN {{ source('olist_raw','customers') }} c USING(customer_id)
 LEFT JOIN item_rollup i USING(order_id)
 LEFT JOIN {{ source('olist_raw','sellers') }} s ON i.seller_id=s.seller_id
 LEFT JOIN ranked_reviews r ON o.order_id=r.order_id
)
SELECT * EXCEPT(purchase_date,delivery_date,promise_date,review_date),
 IF(order_status='delivered' AND delivery_date>=purchase_date AND promise_date>=purchase_date,1,0) delivery_eligible,
 IF(delivery_date>promise_date,1,0) late,
 DATE_DIFF(delivery_date,purchase_date,DAY) delivery_days,
 GREATEST(0,DATE_DIFF(delivery_date,promise_date,DAY)) delay_days,
 CASE WHEN review_score<=2 THEN 1 WHEN review_score>=3 THEN 0 END poor_review,
 IF(review_date>=delivery_date,1,0) review_after_delivery
FROM base
