"""Render these two simple dbt models for a first Console build, without credentials."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parent
PROJECT = 'secret-drake-512620-i7'

def render(sql):
    sql = re.sub(r"\{\{\s*config\(.*?\)\s*\}\}", '', sql)
    sql = re.sub(r"\{\{\s*source\('olist_raw',\s*'([a-z_]+)'\)\s*\}\}", lambda m: f'`{PROJECT}.olist_raw.{m[1]}`', sql)
    sql = re.sub(r"\{\{\s*ref\('([a-z_]+)'\)\s*\}\}", lambda m: f'`{PROJECT}.ecommerce_analytics.{m[1]}`', sql)
    if '{{' in sql or '{%' in sql:
        raise ValueError('Unsupported Jinja; use dbt to compile it')
    return sql.strip()

if __name__ == '__main__':
    dest = ROOT / 'sql'
    dest.mkdir(exist_ok=True)
    for index, name in enumerate(['fct_delivery_orders', 'delivery_kpis'], 1):
        sql = render((ROOT / 'models/marts' / f'{name}.sql').read_text())
        (dest / f'0{index}_{name}.sql').write_text(
            '-- First build only: fails if destination exists; never replaces existing data.\n'
            f'CREATE TABLE `{PROJECT}.ecommerce_analytics.{name}` AS\n{sql};\n')
    for path in (ROOT / 'tests').glob('*.sql'):
        (dest / f'check_{path.stem}.sql').write_text(render(path.read_text())+';\n')
