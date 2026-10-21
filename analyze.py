"""Build a validated SQLite order mart and reproducible portfolio outputs."""
from pathlib import Path
import hashlib,json,sqlite3,math
import pandas as pd
ROOT=Path(__file__).resolve().parent
TABLES={'orders':'olist_orders_dataset.csv','items':'olist_order_items_dataset.csv','reviews':'olist_order_reviews_dataset.csv','customers':'olist_customers_dataset.csv','products':'olist_products_dataset.csv','sellers':'olist_sellers_dataset.csv','translations':'product_category_name_translation.csv'}
KEYS={'orders':['order_id'],'items':['order_id','order_item_id'],'customers':['customer_id'],'products':['product_id'],'sellers':['seller_id'],'translations':['product_category_name']}

def wilson(k,n):
 if not n:return (None,None)
 z=1.959963984540054;p=k/n;den=1+z*z/n
 center=(p+z*z/(2*n))/den;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return center-half,center+half

def main():
 out=ROOT/'results';out.mkdir(exist_ok=True)
 data={t:pd.read_csv(ROOT/'data/raw'/f) for t,f in TABLES.items()}
 checks={}
 for t,keys in KEYS.items():
  assert not data[t][keys].isna().any().any(),f'{t}: missing key'
  assert not data[t].duplicated(keys).any(),f'{t}: duplicate key'
 for child,key,parent in [('items','order_id','orders'),('reviews','order_id','orders'),('orders','customer_id','customers'),('items','product_id','products'),('items','seller_id','sellers')]:
  assert data[child][key].isin(data[parent][key]).all(),f'{child}: orphan {key}'
 assert data['reviews'].review_score.between(1,5).all()
 for t,cols in {'orders':['order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date'],'reviews':['review_creation_date','review_answer_timestamp']}.items():
  for col in cols:pd.to_datetime(data[t][col],errors='raise')
 checks['raw_rows']={t:len(d) for t,d in data.items()}
 checks['orders_with_multiple_reviews']=int((data['reviews'].groupby('order_id').size()>1).sum())
 checks['input_sha256']={f:hashlib.sha256((ROOT/'data/raw'/f).read_bytes()).hexdigest() for f in TABLES.values()}
 with sqlite3.connect(out/'analytics.sqlite') as db:
  for t,d in data.items():
   # Review free text and fine geographic details are not needed in the analytical DB.
   d=d.drop(columns=[c for c in d if c.startswith('review_comment') or c.endswith('_city') or 'zip_code' in c or c=='customer_unique_id'])
   d.to_sql(t,db,if_exists='replace',index=False)
  db.execute('DROP TABLE IF EXISTS order_mart')
  db.executescript((ROOT/'sql/order_mart.sql').read_text())
  mart=pd.read_sql_query('SELECT * FROM order_mart',db)
  segments=pd.read_sql_query((ROOT/'sql/segment_performance.sql').read_text(),db)
 assert len(mart)==len(data['orders']) and mart.order_id.is_unique
 assert math.isclose(mart.item_value_brl.sum(),data['items'].price.sum(),abs_tol=.01)
 eligible=mart[mart.delivery_eligible==1].copy()
 # Independent pandas check of SQL's calendar-day late classification.
 expected=pd.to_datetime(eligible.delivered_at).dt.normalize()>pd.to_datetime(eligible.promised_at).dt.normalize()
 assert (expected.astype(int).to_numpy()==eligible.late.to_numpy()).all()
 checks['delivered_status_orders']=int((mart.order_status=='delivered').sum())
 checks['delivery_eligible_orders']=len(eligible)
 checks['delivered_excluded']=checks['delivered_status_orders']-len(eligible)
 checks['eligible_without_items']=int(eligible.item_count.isna().sum())
 checks['eligible_multi_seller_orders']=int((eligible.seller_count>1).sum())
 checks['eligible_without_reviews']=int(eligible.review_score.isna().sum())
 summary={'total_orders':len(mart),'eligible_orders':len(eligible),'late_orders':int(eligible.late.sum()),'late_rate_pct':100*eligible.late.mean(),'median_delivery_days':eligible.delivery_days.median(),'median_late_delay_days':eligible.loc[eligible.late==1,'delay_days'].median(),'purchase_start':mart.purchased_at.min(),'purchase_end':mart.purchased_at.max()}
 rows=[]
 for sample,sub in [('all_reviewed',eligible[eligible.review_score.notna()]),('review_created_on_or_after_delivery',eligible[(eligible.review_after_delivery==1)&eligible.review_score.notna()])]:
  for late,g in sub.groupby('late'):
   k=int(g.poor_review.sum());n=len(g);lo,hi=wilson(k,n)
   rows.append({'sample':sample,'late':int(late),'reviewed_orders':n,'poor_reviews':k,'poor_review_rate_pct':100*k/n,'ci95_low_pct':100*lo,'ci95_high_pct':100*hi,'mean_review_score':g.review_score.mean()})
 comparison=pd.DataFrame(rows)
 monthly=eligible.groupby('purchase_month').agg(orders=('order_id','size'),late_orders=('late','sum'),late_rate=('late','mean')).reset_index()
 for name,df in [('order_mart',mart),('segment_performance',segments),('review_comparison',comparison),('monthly_performance',monthly)]:df.to_csv(out/f'{name}.csv',index=False)
 # Stratification reveals whether the relationship persists within destination states.
 reviewed=eligible[eligible.review_score.notna()]
 strat=reviewed.groupby(['customer_state','late']).agg(n=('order_id','size'),poor_reviews=('poor_review','sum')).reset_index()
 strat['poor_review_rate']=strat.poor_reviews/strat.n;strat.to_csv(out/'review_by_state.csv',index=False)
 for name,obj in [('summary',summary),('quality_report',checks)]:
  (out/f'{name}.json').write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
 print(json.dumps(summary,indent=2));print(comparison.to_string(index=False));print(segments.groupby('dimension').head(3).to_string(index=False))
 return summary
if __name__=='__main__':main()
