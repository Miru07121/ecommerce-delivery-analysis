# BigQuery + dbt cloud extension (implementation scaffold)

This folder adds a **BigQuery-compatible dbt project** for the existing historical Olist e-commerce delivery case study. It is not deployed to a Google Cloud project yet.

## Setup
1. Create a Google Cloud project and enable BigQuery; review billing and free-tier limits before loading data.
2. Download the seven source CSVs using the existing repository's `download_data.py`.
3. Create BigQuery dataset `olist_raw` in the **US** location and load each CSV as a table named `orders`, `customers`, `items`, `products`, `translations`, `sellers`, and `reviews`. Preserve original string identifiers and timestamp text. Inspect inferred schemas; all price fields must be safely convertible to NUMERIC.
4. Install `dbt-bigquery` in a separate virtual environment.
5. Copy `profiles.example.yml` to `~/.dbt/profiles.yml`, replace YOUR_GCP_PROJECT_ID and authenticate with `gcloud auth application-default login` or another approved OAuth method.
6. Set `GCP_PROJECT_ID` to the same project ID, then run `cd cloud && dbt debug && dbt build`.
7. Compare row counts, late deliveries, and poor-review rates to the SQLite baseline documented in the root README. Review differences before publishing.

## Model flow
Raw Olist tables -> `fct_delivery_orders` (one row per order) -> `delivery_kpis` (monthly state-level KPIs).

## Important caveats
- Historical Brazilian marketplace data, not Canadian industry benchmarks.
- No credentials or personal data should be committed.
- BigQuery costs can accrue; configure a budget alert and inspect query estimates.
- The SQL is a portable adaptation of the SQLite project and requires validation against the actual loaded BigQuery schemas.
- **Status: code committed; cloud execution and dbt tests have not been run.** Do not list BigQuery/dbt as hands-on completed experience until validated.
