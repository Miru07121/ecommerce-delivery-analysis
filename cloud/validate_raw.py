"""Offline validation of CSV headers, types, row counts, and source hashes."""
import csv
import hashlib
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    'orders': 'olist_orders_dataset.csv',
    'items': 'olist_order_items_dataset.csv',
    'reviews': 'olist_order_reviews_dataset.csv',
    'customers': 'olist_customers_dataset.csv',
    'products': 'olist_products_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
    'translations': 'product_category_name_translation.csv',
}

def main():
    expected = json.loads((ROOT / 'results/quality_report.json').read_text())
    for table, filename in FILES.items():
        path = ROOT / 'data/raw' / filename
        schema = json.loads((ROOT / 'cloud/schemas' / f'{table}.json').read_text())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected['input_sha256'][filename]:
            raise ValueError(f'{table}: source hash changed; review before loading')
        count = 0
        with path.open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.reader(handle)
            if next(reader) != [field['name'] for field in schema]:
                raise ValueError(f'{table}: unexpected CSV header')
            for row in reader:
                count += 1
                if len(row) != len(schema):
                    raise ValueError(f'{table} record {count}: wrong field count')
                for field, value in zip(schema, row):
                    if not value:
                        continue  # all source fields are nullable
                    try:
                        if field['type'] == 'INTEGER':
                            number = Decimal(value)
                            if not number.is_finite() or number != number.to_integral_value():
                                raise ValueError('not integral')
                        elif field['type'] == 'NUMERIC':
                            if not Decimal(value).is_finite():
                                raise ValueError('not finite')
                        elif field['type'] == 'DATETIME':
                            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    except Exception as exc:
                        raise ValueError(f'{table} record {count}: invalid {field["name"]}') from exc
        if count != expected['raw_rows'][table]:
            raise ValueError(f'{table}: row count mismatch')
        print(f'{table}: {count:,} rows; headers, types and SHA-256 PASS')

if __name__ == '__main__':
    main()
