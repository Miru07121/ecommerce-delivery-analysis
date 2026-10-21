"""Run locally with streamlit run dashboard.py after analyze.py."""
from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='Delivery & Customer Experience',layout='wide')
st.title('Delivery & Customer Experience')
st.caption('Olist historical orders • Brazil, 2016–2018 • Portfolio analysis')
path=ROOT/'results/order_mart.csv'
if not path.exists():
 st.info('Run python download_data.py, then python analyze.py to build the data.');st.stop()
@st.cache_data
def load(path,modified):return pd.read_csv(path)
df=load(str(path),path.stat().st_mtime)
eligible=df[df.delivery_eligible==1].copy()
months=sorted(eligible.purchase_month.unique())
start,end=st.sidebar.select_slider('Purchase month range',options=months,value=(months[0],months[-1]))
states=sorted(eligible.customer_state.dropna().unique())
selected=st.sidebar.multiselect('Destination states',states,default=states)
d=eligible[eligible.purchase_month.between(start,end)&eligible.customer_state.isin(selected)].copy()
st.sidebar.caption('Only valid delivered orders enter delivery KPIs. Late means delivery calendar date exceeds the promised date.')
if d.empty:st.info('No orders match these filters.');st.stop()
a,b,c,e=st.columns(4)
a.metric('Eligible orders',f'{len(d):,}');b.metric('Late deliveries',f'{d.late.mean():.2%}')
c.metric('Median delivery',f'{d.delivery_days.median():.0f} days');e.metric('Late orders',f'{d.late.sum():,}')
overview,segments,quality=st.tabs(['Delivery & reviews','Investigation queue','Definitions & quality'])
with overview:
 st.subheader('Late-delivery rate by purchase month')
 trend=d.groupby('purchase_month').late.mean().mul(100)
 st.line_chart(trend,y_label='Late orders (%)',x_label='Purchase month')
 conservative=st.checkbox('Restrict to review records created on or after delivery',value=False)
 r=d[d.review_score.notna()]
 if conservative:r=r[r.review_after_delivery==1]
 st.subheader('Poor reviews: scores of 1 or 2 out of 5')
 comp=r.groupby('late').agg(reviewed_orders=('order_id','size'),poor_reviews=('poor_review','sum'))
 comp['poor_review_pct']=100*comp.poor_reviews/comp.reviewed_orders
 comp.index=comp.index.map({0:'On time',1:'Late'})
 st.bar_chart(comp['poor_review_pct'],y_label='Poor reviews (%)')
 st.dataframe(comp,width='stretch')
 st.caption('Association, not a causal effect. The timing restriction changes the sample. Review creation is not necessarily the submission time; response timestamps are retained in the order mart.')
with segments:
 dimension=st.selectbox('Group orders by',['Destination state','Product category','Seller (single-seller orders)'])
 minimum=st.number_input('Minimum eligible orders',min_value=1,value=100,step=25)
 key={'Destination state':'customer_state','Product category':'category','Seller (single-seller orders)':'seller_id'}[dimension]
 x=d[d.seller_count==1] if key=='seller_id' else d
 group=x.groupby(key,dropna=False).agg(orders=('order_id','size'),late_orders=('late','sum'),late_rate=('late','mean')).reset_index()
 group=group[group.orders>=minimum].sort_values(['late_orders','orders'],ascending=False)
 group['late_rate_pct']=100*group.pop('late_rate')
 st.dataframe(group,width='stretch',hide_index=True)
 st.download_button('Download investigation queue',group.to_csv(index=False),'investigation_queue.csv','text/csv')
 st.caption('Ranked by late-order volume. An investigation queue is not proof of seller fault. Mixed-category orders form their own category; multi-seller orders are excluded from seller comparisons.')
with quality:
 st.write('All filters apply to both analysis tabs. Unreviewed orders remain in delivery KPIs but not review denominators. Raw review rows are reduced to the latest answer timestamp per order before joining. Item rows are aggregated before joining to prevent double-counting.')
 st.json(__import__('json').loads((ROOT/'results/quality_report.json').read_text()))
 st.warning('Historical Brazilian marketplace data cannot establish current Canadian operating benchmarks. No savings or causal impact is claimed.')
