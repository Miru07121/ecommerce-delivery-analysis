import sqlite3,unittest
from pathlib import Path
import pandas as pd
from analyze import wilson
SQL=(Path(__file__).resolve().parents[1]/'sql/order_mart.sql').read_text()

class SQLTests(unittest.TestCase):
 def build(self,delivered='2018-01-10 23:59:00',status='delivered'):
  data={
   'orders':pd.DataFrame([['o1','c1',status,'2018-01-01 12:00:00',delivered,'2018-01-10 00:00:00']],columns=['order_id','customer_id','order_status','order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date']),
   'customers':pd.DataFrame([['c1','SP']],columns=['customer_id','customer_state']),
   'items':pd.DataFrame([['o1','p1','s1',10,1],['o1','p1','s1',20,2]],columns=['order_id','product_id','seller_id','price','freight_value']),
   'products':pd.DataFrame([['p1','cama']],columns=['product_id','product_category_name']),
   'translations':pd.DataFrame([['cama','bed']],columns=['product_category_name','product_category_name_english']),
   'sellers':pd.DataFrame([['s1','RJ']],columns=['seller_id','seller_state']),
   'reviews':pd.DataFrame([['r1','o1',1,'2018-01-10','2018-01-10'],['r2','o1',5,'2018-01-11','2018-01-12']],columns=['review_id','order_id','review_score','review_creation_date','review_answer_timestamp'])}
  with sqlite3.connect(':memory:') as db:
   for name,d in data.items():d.to_sql(name,db,index=False)
   db.executescript(SQL)
   return pd.read_sql_query('SELECT * FROM order_mart',db)
 def test_no_join_fanout_latest_review(self):
  d=self.build();self.assertEqual(len(d),1)
  self.assertEqual(d.iloc[0].item_value_brl,30)
  self.assertEqual(d.iloc[0].review_score,5)
 def test_same_day_is_on_time(self):self.assertEqual(self.build().iloc[0].late,0)
 def test_next_day_is_late(self):self.assertEqual(self.build('2018-01-11').iloc[0].late,1)
 def test_non_delivered_excluded(self):self.assertEqual(self.build(status='canceled').iloc[0].delivery_eligible,0)
 def test_missing_and_reverse_dates_excluded(self):
  self.assertEqual(self.build(None).iloc[0].delivery_eligible,0)
  self.assertEqual(self.build('2017-12-31').iloc[0].delivery_eligible,0)
 def test_wilson_edge_cases(self):
  self.assertEqual(wilson(0,0),(None,None))
  lo,hi=wilson(0,10);self.assertAlmostEqual(lo,0);self.assertGreater(hi,0)
if __name__=='__main__':unittest.main()
