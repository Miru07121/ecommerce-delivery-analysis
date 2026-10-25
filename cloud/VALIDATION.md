# Validation record — 2026-10-24 (America/Los_Angeles)

Project: `secret-drake-512620-i7`.
Reviewed source commit: `1d23ed972d5a14b3530a30d795d983e1ff473511`.

## Completed locally

- Downloaded the seven CSVs from the official Kaggle endpoint referenced by
  `download_data.py`. All seven SHA-256 hashes match `results/quality_report.json`.
- `python cloud/validate_raw.py`: PASS for every record's field count and type,
  CSV headers, seven row counts and seven source hashes.
- `python analyze.py`: PASS. Source key uniqueness/not-null, foreign keys,
  review score range, date parsing, mart grain, money reconciliation and an
  independent pandas check of calendar-day lateness all passed.
- Regenerated committed `results/` summaries have no Git differences.
- `python -m unittest discover -s tests -v`: **6/6 PASS**. Includes same-day vs
  next-day delivery, missing/reversed dates, canceled orders, latest review
  selection, prevention of item/review join fanout and Wilson edge cases.
- Installed **dbt Core 1.12.0**, **dbt-bigquery 1.12.1** in an isolated environment.
- `dbt parse --no-partial-parse`: PASS after updating accepted-values argument
  syntax. Manifest contains **2 models, 7 sources, 8 tests**. Parsing does not
  execute those tests.
- SQLGlot 30.24.0 parsed all six generated SQL files using its BigQuery dialect.
  This is a local syntax check, not Google's compiler, a dry run or execution.

## Reproduced local baseline

| Source | Rows |
|---|---:|
| orders | 99,441 |
| items | 112,650 |
| reviews | 99,224 |
| customers | 99,441 |
| products | 32,951 |
| sellers | 3,095 |
| translations | 71 |

| Metric | Reproduced value |
|---|---:|
| Order mart rows | 99,441 |
| Eligible delivered orders | 96,470 |
| Late orders | 6,534 |
| Late rate among eligible orders | 6.7730900798175595% |
| Exact median delivery duration | 10 calendar days |
| Exact median delay among late deliveries | 7 calendar days |
| Poor reviews among late reviewed orders | 3,983 / 6,381 = 62.42% |
| Poor reviews among on-time reviewed orders | 8,289 / 89,443 = 9.27% |
| Delivered-status orders excluded by date rules | 8 |
| Eligible deliveries without a review | 646 |

These values were recalculated from the downloaded source CSVs using the
existing SQLite/Python pipeline. They are **not BigQuery results**.

## Cloud work blocked / untested

The project Console URL returned **Site Unavailable / Unable to access this
site** on initial navigation and one reload. No authenticated Console page was
available. The local environment has no Google Application Default Credentials;
`gcloud` and `bq` were not installed. No secrets were requested or exposed.

Consequently:

- Existing project billing/Sandbox status and existing data could not be inspected.
- Neither dataset was created or verified; US location is configured in code only.
- No CSV was uploaded to BigQuery.
- No Google SQL dry run, transformation, row count or warehouse quality test ran.
- dbt warehouse connection/build/test remain untested. Only offline parse ran.
- No billing was activated, account upgraded, existing cloud data modified, or
  billable cloud job submitted.

## Changes prepared for the next cloud session

Explicit seven-table load schemas use STRING identifiers/postal prefixes,
DATETIME local timestamps, NUMERIC money and INTEGER counts. The cloud model
now uses DATE casts and FORMAT_DATE instead of SUBSTR on timestamp columns.

Added first-build SQL that fails if a destination already exists; raw count,
key/relationship/score, monetary reconciliation and delivery baseline checks;
a one-thread dbt profile with US location and a 1 GB per-query byte cap; and
Sandbox-only setup instructions. Existing SQLite code and historical outputs
were preserved.

Before marking deployment complete, inspect billing and existing objects, load
all seven tables, capture job IDs and bytes processed, execute transformations,
and run all eight dbt tests. Record actual cloud results here. If Sandbox rejects
an operation, stop that operation and record the error; do not activate billing.
