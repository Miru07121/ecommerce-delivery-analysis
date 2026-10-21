from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
r=pd.read_csv(ROOT/'results/review_comparison.csv')
s=pd.read_csv(ROOT/'results/segment_performance.csv')
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'font.size':11})
fig,axes=plt.subplots(1,2,figsize=(12,5.5),layout='constrained')
a=axes[0]
for offset,sample,label,color in [(-.18,'all_reviewed','All reviewed orders','#166d8f'),(.18,'review_created_on_or_after_delivery','Review created on/after delivery','#d78b33')]:
 d=r[r['sample']==sample].sort_values('late');v=d.poor_review_rate_pct.to_numpy()
 a.bar([offset,1+offset],v,width=.34,label=label,color=color)
 a.errorbar([offset,1+offset],v,yerr=[v-d.ci95_low_pct.to_numpy(),d.ci95_high_pct.to_numpy()-v],fmt='none',ecolor='#202b35',capsize=3)
 for x,y in zip([offset,1+offset],v):a.text(x,y+2,f'{y:.1f}%',ha='center',fontsize=10)
a.set(xticks=[0,1],xticklabels=['On time','Late'],ylim=(0,76),ylabel='Poor reviews (%)',title='Review timing changes the comparison')
a.legend(loc='upper left',fontsize=8,frameon=False)
d=s[s.dimension=='state'].head(5).iloc[::-1];b=axes[1]
b.barh(d.segment,d.late_orders,color='#166d8f')
for y,(n,rate) in enumerate(zip(d.late_orders,d.late_rate)):b.text(n+20,y,f'{n:,} | {rate:.1%}',va='center',fontsize=10)
b.set(xlim=(0,2400),xlabel='Late orders (labels also show late rate)',title='Where investigation could start')
fig.suptitle('Olist delivery performance | Historical 2016–2018 orders',fontsize=16,fontweight='bold')
fig.supxlabel('Poor review = score 1–2. Error bars: 95% Wilson intervals. Observational associations, not causal effects.',fontsize=9)
fig.savefig(ROOT/'reports/overview.png',dpi=180)
