-- dbt singular test fails if the exception report is nonempty.
SELECT * FROM {{ ref('delivery_quality_checks') }}
