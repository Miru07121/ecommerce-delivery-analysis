# Model and metric dictionary

## Source grains and joins

| Table | Grain/key | Relationship |
|---|---|---|
| orders | order_id | Anchor, 99,441 orders |
| customers | customer_id | Many orders to customer dimension by customer_id |
| items | order_id + order_item_id | Many items per order; aggregate before joining |
| products | product_id | Item product dimension |
| translations | product_category_name | Category English label; original label fallback |
| sellers | seller_id | Seller state; available for single-seller orders |
| reviews | Review records, potentially multiple per order | Latest answer timestamp per order, then creation date, review ID and score tie-breaks |

## Order mart fields

| Fields | Definition |
|---|---|
| order_id, order_status | Source order key and reported final status |
| purchased_at, purchase_month | Purchase timestamp and YYYY-MM cohort |
| delivered_at, promised_at | Recorded customer delivery and estimated delivery timestamps |
| customer_state, seller_state | Brazilian state abbreviations, not geocoded locations |
| item_count, seller_count | Number of item lines and distinct sellers in order |
| seller_id | Single seller identifier; MULTIPLE when more than one |
| category | Single translated product category, MIXED, or UNKNOWN |
| item_value_brl, freight_brl | Sum of source item prices and freight in BRL; not profit or accounting revenue |
| review_score | Selected review score, 1–5; missing if no review |
| review_creation_date, review_answer_timestamp | Source review record creation and response timestamps |
| delivery_eligible | Delivered status, usable delivery/promise dates, both calendar dates on/after purchase |
| late | Delivery calendar date exceeds promised calendar date; meaningful only for eligible orders |
| delivery_days | Delivery calendar date minus purchase calendar date |
| delay_days | Maximum of zero and delivery date minus promised date |
| poor_review | 1 for review score 1–2; 0 for 3–5; missing if unreviewed |
| review_after_delivery | Review record creation date is on/after delivery date; not proof of response timing |

## Denominators and exclusions

- **Late rate:** eligible late orders / all eligible delivered orders. Same-day delivery is on time, even when the estimated timestamp is midnight.
- **Poor-review rate:** selected reviews scoring 1–2 / eligible orders with selected reviews, calculated separately for late/on-time groups. Unreviewed orders are never treated as positive reviews.
- **Sensitivity sample:** eligible reviewed orders whose review record creation date is on/after delivery date. This can select a different population, so differences between samples do not estimate causal effects.
- **Segment queues:** at least 100 eligible orders. Ranked by late-order count, not rate alone. A threshold is a project design choice, not an industry standard.
- **Seller queue:** single-seller orders only. Mixed-category orders remain a separate category to avoid counting an order more than once across categories.
- **Delivery durations:** median over eligible delivered orders; median late delay uses only late orders. Missing means unavailable, never zero.

## Published quality checks

- 99,441 order rows preserved in mart, with unique order keys and reconciled item values.
- 547 orders have more than one raw review; one selected review per order prevents join inflation.
- 96,478 orders have delivered status; 8 fail delivery eligibility, leaving 96,470.
- 646 eligible orders have no selected review and 1,275 have multiple sellers.
- Inputs checked for expected primary keys, foreign-key coverage, review-score range and date parsing.

`results/quality_report.json` records the actual run, including source hashes.
