-- Grain: one order. Aggregate items and deduplicate reviews BEFORE joining.
CREATE TABLE order_mart AS
WITH item_rollup AS (
 SELECT i.order_id, COUNT(*) AS item_count, COUNT(DISTINCT seller_id) AS seller_count,
 CASE WHEN COUNT(DISTINCT seller_id)=1 THEN MIN(seller_id) ELSE 'MULTIPLE' END AS seller_id,
 CASE WHEN COUNT(DISTINCT COALESCE(t.product_category_name_english,p.product_category_name,'UNKNOWN'))=1
 THEN MIN(COALESCE(t.product_category_name_english,p.product_category_name,'UNKNOWN')) ELSE 'MIXED' END AS category,
 SUM(price) AS item_value_brl, SUM(freight_value) AS freight_brl
 FROM items i LEFT JOIN products p USING(product_id)
 LEFT JOIN translations t USING(product_category_name)
 GROUP BY i.order_id
), ranked_reviews AS (
 SELECT *, ROW_NUMBER() OVER(PARTITION BY order_id ORDER BY review_answer_timestamp DESC,review_creation_date DESC,review_id DESC,review_score DESC) AS rn
 FROM reviews
)
SELECT o.order_id,o.order_status,o.order_purchase_timestamp AS purchased_at,
 substr(o.order_purchase_timestamp,1,7) AS purchase_month,
 o.order_delivered_customer_date AS delivered_at,o.order_estimated_delivery_date AS promised_at,
 c.customer_state,i.item_count,i.seller_count,i.seller_id,s.seller_state,i.category,i.item_value_brl,i.freight_brl,
 r.review_score,r.review_creation_date,r.review_answer_timestamp,
 CASE WHEN o.order_status='delivered' AND date(o.order_delivered_customer_date)>=date(o.order_purchase_timestamp)
 AND date(o.order_estimated_delivery_date)>=date(o.order_purchase_timestamp) THEN 1 ELSE 0 END AS delivery_eligible,
 CASE WHEN date(o.order_delivered_customer_date)>date(o.order_estimated_delivery_date) THEN 1 ELSE 0 END AS late,
 julianday(date(o.order_delivered_customer_date))-julianday(date(o.order_purchase_timestamp)) AS delivery_days,
 MAX(0,julianday(date(o.order_delivered_customer_date))-julianday(date(o.order_estimated_delivery_date))) AS delay_days,
 CASE WHEN r.review_score<=2 THEN 1 WHEN r.review_score>=3 THEN 0 END AS poor_review,
 CASE WHEN date(r.review_creation_date)>=date(o.order_delivered_customer_date) THEN 1 ELSE 0 END AS review_after_delivery
FROM orders o LEFT JOIN customers c USING(customer_id)
LEFT JOIN item_rollup i USING(order_id)
LEFT JOIN sellers s ON i.seller_id=s.seller_id
LEFT JOIN ranked_reviews r ON o.order_id=r.order_id AND r.rn=1;
CREATE UNIQUE INDEX order_mart_pk ON order_mart(order_id);
