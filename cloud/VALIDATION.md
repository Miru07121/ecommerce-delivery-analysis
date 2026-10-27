# Cloud validation plan

**Status:** Validation SQL and dbt tests are committed; no claim of execution in BigQuery is made.

## Commands

From `cloud/`, after authentication and loading the seven source tables:

```bash
dbt debug
dbt build
dbt test
```

## Expected reference metrics

The existing local SQLite analysis reports:
- 99,441 raw orders and one-row-per-order mart rows.
- 96,470 eligible delivered orders.
- 6,534 late deliveries (6.77%).
- 547 orders with multiple review records (deduplicated before joining).

These are comparison targets from the local project, **not verified BigQuery results**.

## Reconciliation query

```sql
SELECT
 COUNT(*) AS mart_rows,
 COUNTIF(delivery_eligible = 1) AS eligible_deliveries,
 COUNTIF(delivery_eligible = 1 AND late = 1) AS late_deliveries,
 SAFE_DIVIDE(
   COUNTIF(delivery_eligible = 1 AND late = 1),
   COUNTIF(delivery_eligible = 1)
 ) AS late_rate
FROM `YOUR_PROJECT.ecommerce_analytics.fct_delivery_orders`;
```

The singular dbt tests assert row-count preservation and zero exception rows. If results differ from the local baseline, inspect source schema, timestamp parsing, joins, and review deduplication before changing expected values.

**Important:** The current SQL adaptation uses string timestamp fields. Confirm the imported CSV schemas before executing. Never publish credentials or claim tests passed until they have run.
