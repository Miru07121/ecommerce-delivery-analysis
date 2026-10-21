# Data provenance and reuse

**Creator:** Olist. **Dataset:** Brazilian E-Commerce Public Dataset by Olist.

- Official source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- Official download endpoint used: https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce
- Downloaded: October 20, 2026 (America/Vancouver).
- Dataset license shown by Kaggle: Creative Commons Attribution–NonCommercial–ShareAlike 4.0 International (CC BY-NC-SA 4.0).
- Terms: https://creativecommons.org/licenses/by-nc-sa/4.0/
- This project is independent educational portfolio work. No affiliation or endorsement by Olist is implied.

The seven CSVs are orders, order items, order reviews, customers, sellers, products and category translations. Payments and precise geolocation are not used. Raw row counts and SHA-256 hashes are recorded in `results/quality_report.json`; those hashes identify the exact inputs used for the published findings.

## Changes from the source

The order mart aggregates item price/freight totals; replaces multiple categories with MIXED; identifies multi-seller orders; selects one review per order by latest answer timestamp (with deterministic tie-breaks); calculates calendar-day delivery metrics; and joins destination state and translated category. Raw text reviews, city, postal-code details and customer-unique identifiers are excluded from the SQLite analytical database. The downloadable archive contains the derived order mart and aggregate outputs, not the raw dataset or SQLite database. Git excludes raw CSVs and the order mart; both can be regenerated.

The Olist dataset and derived CSVs, figures and analyses are offered under CC BY-NC-SA 4.0 with this attribution and notice of changes. Retain attribution and the license link when sharing adaptations; use the same license for those adaptations. Project code is also offered under CC BY-NC-SA 4.0 for consistency. This license permits only noncommercial reuse; it is not a permissive commercial software license.
