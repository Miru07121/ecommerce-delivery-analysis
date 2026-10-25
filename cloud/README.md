# BigQuery Sandbox + dbt

Target project: `secret-drake-512620-i7`. Datasets: `olist_raw` and
`ecommerce_analytics`, both **US multi-region**.

**Status:** source downloads and the SQLite baseline were validated locally.
BigQuery deployment and warehouse tests are not completed. See
[VALIDATION.md](VALIDATION.md) for the exact evidence and blockers.

## 1. Confirm Sandbox and inspect existing objects

Open [BigQuery Console](https://console.cloud.google.com/bigquery?project=secret-drake-512620-i7).
Confirm the project ID and Sandbox status. Do not activate a free trial, attach
billing, upgrade, use paid services, or create a Cloud Storage bucket.
If billing is already enabled or Sandbox status cannot be verified, stop.

Inspect existing datasets, locations, tables, schemas and row counts before
creating anything. Create only missing datasets using Explorer > project menu >
Create dataset. Enter `olist_raw`, select multi-region **US**, and create it;
repeat for `ecommerce_analytics`. Keep Sandbox expiration defaults. If either
existing dataset is outside US, stop; do not delete or replace it.

[Google's Sandbox documentation](https://docs.cloud.google.com/bigquery/docs/sandbox)
describes free usage limits and automatic 60-day expiration for tables, views
and partitions. DML, streaming and Data Transfer Service are unavailable. This
project uses batch CSV loads and table SELECT transformations. Do not upgrade
to work around an unsupported operation or quota error.

## 2. Download and validate the seven CSVs

From the repository root, in the existing Python analysis environment:

```bash
python download_data.py
python cloud/validate_raw.py
```

The validator checks all CSV records against explicit schemas and the committed
row counts and SHA-256 hashes. A mismatch requires investigation, not an updated
expected value just to make validation pass. The original downloader replaces
local CSV files, so preserve any local data changes before rerunning it.
See `DATA_SOURCES.md` for Olist attribution and license terms.

| File in data/raw | Raw table | Expected rows |
|---|---|---:|
| olist_orders_dataset.csv | orders | 99,441 |
| olist_order_items_dataset.csv | items | 112,650 |
| olist_order_reviews_dataset.csv | reviews | 99,224 |
| olist_customers_dataset.csv | customers | 99,441 |
| olist_products_dataset.csv | products | 32,951 |
| olist_sellers_dataset.csv | sellers | 3,095 |
| product_category_name_translation.csv | translations | 71 |

## 3. Load without schema inference or replacement

For each missing raw table, use Create table > Upload > CSV. Select its source
file, project above, dataset `olist_raw`, and the mapped table name. Turn off
auto-detect. Use Edit as text with the contents of `schemas/<table>.json`.
Set header rows to skip to **1**, encoding **UTF-8**, allow quoted newlines
(needed for review comments), and maximum bad records **0**. Keep unknown-field
ignoring and jagged rows disabled. Create the table, then inspect the load job,
schema and table row count. Do not append or replace if the table already exists.
Instead inspect it and compare its schema/counts before deciding how to proceed.

Identifiers and postal-code prefixes are STRING to preserve leading zeros.
Local date/time values are DATETIME: the source has no timezone, so no UTC
conversion is invented. Prices/freight are NUMERIC; scores, counts and dimensions
are INTEGER. All source fields are nullable; quality checks impose business rules.

## 4. First SQL build through the Console

The checked-in `sql/01_fct_delivery_orders.sql` and `sql/02_delivery_kpis.sql`
are generated from the dbt models with `python cloud/render_sql.py`.
Run them in that order only after validating raw tables. They use CREATE TABLE,
not CREATE OR REPLACE, so they fail if an output table already exists.

Use GoogleSQL, processing location US, and maximum bytes billed **1,000,000,000**
per query in query settings. Inspect each estimate before running. This cap is
an additional per-query guard, not a substitute for keeping billing disabled
or a cumulative quota. Stop if any query exceeds it or requests billing.

Run each `sql/check_*.sql`: each must return **zero rows**. Also verify mart
`order_id` uniqueness/not-null and inspect date exclusions. The full dbt quality
suite below performs additional checks. Save query job IDs, bytes processed,
counts and test results before reporting cloud execution as complete.

## 5. Optional dbt Core (local OAuth; no service-account keys)

Requires a trusted local Python environment, Google Cloud CLI, network access,
and authorized Application Default Credentials. Never paste credentials into
chat or commit them. The profile file contains configuration only.

```bash
python -m venv .venv-dbt
source .venv-dbt/bin/activate
# Windows PowerShell: .venv-dbt\Scripts\Activate.ps1
pip install -r cloud/requirements.txt
export GCP_PROJECT_ID=secret-drake-512620-i7
# PowerShell: $env:GCP_PROJECT_ID='secret-drake-512620-i7'
cp cloud/profiles.example.yml cloud/profiles.yml
# PowerShell: Copy-Item cloud/profiles.example.yml cloud/profiles.yml
gcloud auth application-default login
dbt parse --project-dir cloud --profiles-dir cloud
dbt debug --project-dir cloud --profiles-dir cloud
```

Before building, inspect `ecommerce_analytics`: dbt's table materialization can
replace its existing model tables. Review/back up those objects first; do not
run an unreviewed build over prior work. If neither model exists, run:

```bash
dbt build --project-dir cloud --profiles-dir cloud
```

If using the Console-built tables, run `dbt test` first instead of rebuilding.
Stop on billing requirements, unsupported adapter operations, or quota errors.
No dbt Cloud subscription is needed. `dbt parse` is offline project validation;
it is not a successful warehouse build or SQL execution.

The [dbt BigQuery profile documentation](https://docs.getdbt.com/docs/local/connect-data-platform/bigquery-setup?version=1.12)
describes OAuth, US location and maximum_bytes_billed. Generated artifacts and
local profile files are excluded from Git. Do not upload raw dbt logs without
reviewing them for sensitive contents.

## Acceptance criteria

- Seven raw row counts match, and types match checked-in schemas.
- Raw keys are non-null/unique where expected, foreign keys resolve, reviews
  are 1–5, and mart monetary totals reconcile to raw items.
- Mart has 99,441 unique orders, 96,470 eligible deliveries, 6,534 late orders;
  exact medians are 10 delivery days and 7 late-delay days.
- Late rate is 6.7730900798%; only eligible deliveries enter the denominator.
- All dbt tests pass. Review records are deduplicated before joining;
  multiple reviews per order are valid source data.
- Record local checks and cloud checks separately in VALIDATION.md.
