-- Return any KPI group with impossible counts or an inconsistent late rate.
-- Tolerance accommodates floating-point division without masking meaningful errors.
SELECT purchase_month, customer_state, eligible_deliveries, late_deliveries, late_rate
FROM {{ ref('delivery_kpis') }}
WHERE eligible_deliveries IS NULL
   OR eligible_deliveries <= 0
   OR late_deliveries IS NULL
   OR late_deliveries < 0
   OR late_deliveries > eligible_deliveries
   OR late_rate IS NULL
   OR ABS(late_rate - SAFE_DIVIDE(late_deliveries, eligible_deliveries)) > 1e-10
