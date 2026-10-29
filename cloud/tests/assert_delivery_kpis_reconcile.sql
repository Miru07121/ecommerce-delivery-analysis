-- A dbt singular test: return rows only when the monthly/state KPI mart
-- disagrees with an independent aggregation of the order-grain fact table.
-- Null states are compared with IS DISTINCT FROM to avoid silently skipping them.
WITH expected AS (
  SELECT
    purchase_month,
    customer_state,
    COUNT(*) AS eligible_deliveries,
    COUNTIF(late = 1) AS late_deliveries
  FROM {{ ref('fct_delivery_orders') }}
  WHERE delivery_eligible = 1
  GROUP BY 1, 2
),
actual AS (
  SELECT purchase_month, customer_state, eligible_deliveries, late_deliveries
  FROM {{ ref('delivery_kpis') }}
),
discrepancies AS (
  SELECT
    COALESCE(e.purchase_month, a.purchase_month) AS purchase_month,
    COALESCE(e.customer_state, a.customer_state) AS customer_state,
    e.eligible_deliveries AS expected_eligible,
    a.eligible_deliveries AS actual_eligible,
    e.late_deliveries AS expected_late,
    a.late_deliveries AS actual_late
  FROM expected e
  FULL OUTER JOIN actual a
    ON e.purchase_month IS NOT DISTINCT FROM a.purchase_month
   AND e.customer_state IS NOT DISTINCT FROM a.customer_state
)
SELECT *
FROM discrepancies
WHERE expected_eligible IS DISTINCT FROM actual_eligible
   OR expected_late IS DISTINCT FROM actual_late
