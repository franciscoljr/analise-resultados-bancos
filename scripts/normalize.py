#!/usr/bin/env python3
"""Refresh audited series mappings, with explicit units, periods and provenance."""
import json,pathlib,re,datetime as dt,hashlib,csv,collections
import openpyxl
ROOT=pathlib.Path(__file__).resolve().parents[1]
def norm(s):return re.sub(r'\s+',' ',str(s or '')).strip()
def period(v):
 if isinstance(v,dt.datetime):return f'{v.year}Q{(v.month-1)//3+1}'
 s=norm(v)
 m=re.fullmatch(r'01/(01|04|07|10) a (31/03|30/06|30/09|31/12)/(20\d{2})',s)
 if m and {'01':'31/03','04':'30/06','07':'30/09','10':'31/12'}[m[1]]==m[2]:return f'{m[3]}Q{(int(m[1])-1)//3+1}'
 m=re.fullmatch(r'([1-4])\s*[TQ]\s*(?:20)?(\d{2})',s,re.I)
 if m:return f'20{m[2]}Q{m[1]}'
 m=re.fullmatch(r'(Mar|Jun|Set|Sep|Dez|Dec)[/ -]?(?:20)?(\d{2})',s,re.I)
 if m:return f'20{m[2]}Q'+str({'mar':1,'jun':2,'set':3,'sep':3,'dez':4,'dec':4}[m[1].lower()])
 return None
def main():
 mappings=json.loads((ROOT/'data/mappings.json').read_text()); docs=[]
 for p in [ROOT/'data/index.json',ROOT/'data/priority.json']:
  if p.exists():docs+=json.loads(p.read_text())
 # Include collector checkpoints during a first run, without claiming final coverage.
 for p in sorted((ROOT/'data/catalogs').glob('20*/progress.json')):
  docs+=json.loads(p.read_text())
 bypath={d.get('path'):d for d in docs if d.get('path')}; out=[]; errors=[]; cache={}; candidates={}
 for bank in {m['bank'] for m in mappings}:
  ds=[d for d in bypath.values() if d['bank']==bank and 'descontin' not in d.get('title','').lower() and d.get('format')=='xlsx' and any(t in (d['title']+' '+d['category']).lower() for t in ['hist','serie','série'])]
  if not ds:
   errors.append(dict(bank=bank,error='No validated historical workbook'));continue
  ds.sort(key=lambda d:(d['year'],int(d['period'][0]) if d['period'][0].isdigit() else 0,d.get('publication_date') or ''),reverse=True)
  candidates[bank]=ds[0]
 for m in mappings:
  if m['bank'] not in candidates:continue
  d=candidates[m['bank']]; p=ROOT/d['path']
  try:
   if str(p) not in cache:cache[str(p)]=openpyxl.load_workbook(p,data_only=True,read_only=True)
   w=cache[str(p)];s=w[m['sheet']]
   # Bound traversal because published sheets may contain a million formatted blank rows.
   rows=list(s.iter_rows(max_row=350,max_col=min(s.max_column,180)))
   matches=[r for r in rows if norm(r[m['label_column']-1].value)==norm(m['label'])]
   if len(matches)!=1:
    matches=[r for i,r in enumerate(rows,1) if i==m['row_hint'] and norm(r[m['label_column']-1].value)==norm(m['label'])]
   if len(matches)!=1:raise ValueError('Mapped row label absent/ambiguous: '+m['label'])
   row=matches[0];headers=rows[m['header_row']-1]
   for c,h in zip(row,headers):
    per=period(h.value)
    if not per or per<'2024Q1':continue
    raw=c.value
    if not isinstance(raw,(int,float)) or isinstance(raw,bool):
     if raw not in [None,'','-','N/D','n/a']: errors.append(dict(bank=m['bank'],metric=m['metric'],period=per,error='Non-numeric source value '+str(raw)))
     continue
    value=raw*m['multiplier']
    out.append(dict(bank=m['bank'],period=per,metric=m['metric'],value=round(value,6),unit=m['unit'],frequency=m['frequency'],basis=('accounting_consolidated' if m['bank']=='BTG_Pactual' and m['metric'] in ['net_income_accounting','assets','equity','operating_expenses','roe_accounting'] else m['basis']),scope='prudential' if m['metric'] in ['capital_total','cet1','rwa','cet1_amount'] else 'consolidated',method=m['method'],source_label=m['label'],source_url=d['url'],source_path=d['path'],source_reference=m['sheet']+'!'+c.coordinate,source_vintage=f"{d['year']}Q{d['period'][0]}",source_sha256=d.get('sha256') or hashlib.sha256(p.read_bytes()).hexdigest(),raw_value=raw,multiplier=m['multiplier'],status='mapped'))
  except Exception as e:errors.append(dict(bank=m['bank'],metric=m['metric'],error=str(e)))
 # Consolidated identity; duplicate observations with different definitions are retained in versions.
 versions=out.copy(); unique={}
 for d in out:
  key=(d['bank'],d['period'],d['metric'])
  if key not in unique:unique[key]=d
  elif abs(unique[key]['value']-d['value'])>1e-5:errors.append(dict(bank=d['bank'],period=d['period'],metric=d['metric'],error='Conflicting mappings; retained first definition'))
 out=list(unique.values())
 manual=ROOT/'data/pdf_observations.json'
 if manual.exists():out+=json.loads(manual.read_text())
 extra=ROOT/'data/itau_capital_observations.json'
 if extra.exists():out+=json.loads(extra.read_text())
 for d in list(out):
  if d['metric']!='cet1_amount':continue
  denom=next((r for r in out if r['bank']==d['bank'] and r['period']==d['period'] and r['metric']=='rwa'),None)
  if denom and denom['value']>0:out.append({**d,'metric':'cet1','unit':'percent','value':round(100*d['value']/denom['value'],6),'source_reference':d['source_reference']+' / '+denom['source_reference']+' × 100','source_label':'Derived CET1 = Capital Principal / RWA','method':'Derived from prudential capital principal and RWA in the same source workbook','raw_value':d['value'],'multiplier':100/denom['value'],'status':'derived'})
 out.sort(key=lambda d:(d['bank'],d['period'],d['metric']))
 (ROOT/'data/normalized.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 (ROOT/'data/normalization_errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2))
 if out:
  with (ROOT/'data/normalized.csv').open('w',newline='',encoding='utf-8-sig') as f:
   keys=list(dict.fromkeys(k for d in out for k in d));wr=csv.DictWriter(f,keys);wr.writeheader();wr.writerows(out)
 print('Observations',len(out),'errors',len(errors));print(collections.Counter(d['bank'] for d in out));print(errors[:12])
if __name__=='__main__':main()
