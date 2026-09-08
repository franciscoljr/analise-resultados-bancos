"""Generate repeatable quarter-on-quarter/year-on-year arithmetic earnings bridges."""
import pathlib,json,csv,collections
ROOT=pathlib.Path(__file__).resolve().parents[1];rows=json.loads((ROOT/'data/normalized.json').read_text());lookup={(d['bank'],d['period'],d['metric']):d for d in rows};out=[]
for bank in sorted({d['bank'] for d in rows}):
 for period in sorted({d['period'] for d in rows if d['bank']==bank}):
  y=int(period[:4]);q=int(period[-1])
  for comparison,base in [('QoQ',f'{y}Q{q-1}' if q>1 else f'{y-1}Q4'),('YoY',f'{y-1}Q{q}')]:
   current=lookup.get((bank,period,'net_income_adjusted'));prior=lookup.get((bank,base,'net_income_adjusted'))
   if not current or not prior:continue
   delta=current['value']-prior['value'];entry={'bank':bank,'period':period,'comparison':comparison,'base_period':base,'unit':'BRL_million','profit_change':delta,'profit_change_percent':100*delta/prior['value'] if prior['value'] else None};refs=[];values=[]
   components=[('revenue',1),('operating_expenses',-1)] if bank=='BTG_Pactual' else [('net_interest_income',1),('fees',1),('credit_cost',-1),('operating_expenses',-1)]+([('insurance_result',1)] if bank=='Bradesco' else [])
   for metric,sign in components:
    a=lookup.get((bank,period,metric));b=lookup.get((bank,base,metric));v=sign*(a['value']-b['value']) if a and b else None;entry['contribution_'+metric]=v;values.append(v)
    if a and b:refs += [{'metric':metric,'period':x['period'],'value':x['value'],'reference':x['source_reference'],'path':x['source_path'],'vintage':x['source_vintage']} for x in [a,b]]
   entry['other_items_and_tax_residual']=delta-sum(values) if None not in values else None
   entry['status']='arithmetic_bridge' if None not in values else 'incomplete_component_coverage';entry['interpretation']='Selected income components plus residual; not causal attribution. Accounting/managerial scope and 2025 rule changes may affect comparability.'
   entry['sources']=json.dumps(refs,ensure_ascii=False);out.append(entry)
with (ROOT/'data/driver_bridges.csv').open('w',newline='',encoding='utf-8-sig') as f:
 keys=list(dict.fromkeys(k for d in out for k in d));w=csv.DictWriter(f,keys);w.writeheader();w.writerows(out)
(ROOT/'data/driver_bridges.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
groups=collections.defaultdict(list)
for d in rows:groups[d['bank'],d['metric']].append(d)
dictionary=[]
for (bank,metric),ds in sorted(groups.items()):
 dictionary.append({'bank':bank,'metric':metric,'units':'; '.join(sorted({d['unit'] for d in ds})),'period_basis':'; '.join(sorted({d['frequency'] for d in ds})),'reporting_basis':'; '.join(sorted({d['basis'] for d in ds})),'scope':'; '.join(sorted({d['scope'] for d in ds})),'first_period':min(d['period'] for d in ds),'last_period':max(d['period'] for d in ds),'observations':len(ds),'source_labels':'; '.join(sorted({d['source_label'] for d in ds})),'methodology':'; '.join(sorted({d['method'] for d in ds if d['method']}))})
with (ROOT/'data/metric_dictionary.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,list(dictionary[0]));w.writeheader();w.writerows(dictionary)
print('Generated',len(out),'earnings bridges;',len(dictionary),'bank-metric dictionary entries')
