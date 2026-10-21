"""Download the official Olist public dataset; keep only seven needed CSVs."""
from pathlib import Path
import io, urllib.request, zipfile
ROOT=Path(__file__).resolve().parent
URL='https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce'
FILES=['olist_orders_dataset.csv','olist_order_items_dataset.csv','olist_order_reviews_dataset.csv','olist_customers_dataset.csv','olist_products_dataset.csv','olist_sellers_dataset.csv','product_category_name_translation.csv']
if __name__=='__main__':
 raw=ROOT/'data/raw';raw.mkdir(parents=True,exist_ok=True)
 with urllib.request.urlopen(URL,timeout=120) as response:payload=response.read()
 with zipfile.ZipFile(io.BytesIO(payload)) as z:
  for name in FILES:(raw/name).write_bytes(z.read(name))
 print('Downloaded seven CSVs. See DATA_SOURCES.md for attribution and terms.')
