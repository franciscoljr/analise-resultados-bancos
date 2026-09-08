"""Build readable comparisons and coverage from the indexed source archive."""
import json,pathlib,collections,csv,datetime,re,unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[1]; R=ROOT/'reports';R.mkdir(exist_ok=True)
obs=json.loads((ROOT/'data/normalized.json').read_text());ix=json.loads((ROOT/'data/index.json').read_text()) if (ROOT/'data/index.json').exists() else []
dis=json.loads((ROOT/'data/discovered.json').read_text()) if (ROOT/'data/discovered.json').exists() else ix
banks=['Banco_do_Brasil','Bradesco','BTG_Pactual','Caixa','Itau','Santander']; names=dict(zip(banks,['Banco do Brasil','Bradesco','BTG Pactual','Caixa','Itaú','Santander']))
lookup={(d['bank'],d['period'],d['metric']):d for d in obs}; periods=sorted({d['period'] for d in obs});latest=periods[-1]
def mdwrite(p,s):
 s=re.sub(r'\]\((/[^)]+)\)',r'](<\1>)',s);out=[]
 for line in s.splitlines():
  prev=out[-1] if out else ''
  if prev and line and (line.startswith('#') or prev.startswith('#') or (line.startswith('|') and not prev.startswith('|')) or (line.startswith('- ') and not prev.startswith('- ')) or line.startswith('![')):out.append('')
  out.append(line)
 p.write_text('\n'.join(out)+'\n')
def get(b,p,m):return lookup.get((b,p,m))
def val(b,p,m):
 d=get(b,p,m);return d['value'] if d else None
def fmt(v,n=1):return '—' if v is None else f'{v:,.{n}f}'
def pct(a,b):return None if a is None or b in [None,0] else 100*(a/b-1)
def ref(d):return f"[{d['source_reference']}]({ROOT/d['source_path']})"
def value(b,p,m):
 d=get(b,p,m);return '—' if not d else fmt(d['value'],2)+' '+ref(d)
prev=f'{int(latest[:4])-1}Q4' if latest[-1]=='1' else latest[:-1]+str(int(latest[-1])-1); yoy=str(int(latest[:4])-1)+latest[4:]
lines=[f'# Brazil S1 bank results — executive comparison',f'Latest normalized quarter: **{latest}**. Generated {datetime.date.today().isoformat()}. Amounts are BRL millions unless stated. A dash means unavailable, never zero. Read the definition notes before comparing ratios.',
'## Executive scorecard','Adjusted/recurring profit is each bank’s own managerial measure. It is not a standardized accounting measure. ROE bases are deliberately shown in the table.',
'| Bank | Adjusted profit | QoQ | YoY | ROE | ROE period basis | NPL >90d | CET1 |','|---|---:|---:|---:|---:|---|---:|---:|']
for b in banks:
 d=get(b,latest,'roe_adjusted');p=val(b,latest,'net_income_adjusted');lines.append(f"| {names[b]} | {fmt(p)} | {fmt(pct(p,val(b,prev,'net_income_adjusted')))}% | {fmt(pct(p,val(b,yoy,'net_income_adjusted')))}% | {fmt(val(b,latest,'roe_adjusted'),2)}% | {d['frequency'].replace('_',' ') if d else '—'} | {fmt(val(b,latest,'npl90'),2)} | {fmt(val(b,latest,'cet1'),2)} |")
lines+=['','NPL and CET1 are percentages. Missing NPL for BTG is not evidence of zero credit risk. Santander ROE excludes goodwill. Caixa uses a trailing 12-month denominator/numerator window; Bradesco’s mapped ROE is YTD annualized. Bradesco’s 2Q26 release separately reports **quarterly ROAE of 16.2%** (release p. 1), versus 16.0% in the mapped YTD series. No single ROE ranking is asserted.',
'## Earnings evolution',f'![Quarterly recurring earnings]({ROOT}/reports/earnings_trends.png)','| Bank | 1Q24 | 4Q24 | 2Q25 | 4Q25 | 1Q26 | 2Q26 |','|---|---:|---:|---:|---:|---:|---:|']
for b in banks:lines.append('| '+names[b]+' | '+' | '.join(fmt(val(b,p,'net_income_adjusted')) for p in ['2024Q1','2024Q4','2025Q2','2025Q4','2026Q1','2026Q2'])+' |')
lines+=['','The 2024–2025 boundary contains CMN 4,966 and managerial restatement breaks. BTG’s latest historical presentation reflects the inclusion of Consumer Finance & Banking; balance-sheet consolidation changes require separate interpretation. These figures describe the latest disclosed series, not necessarily what was originally published in each quarter.',
'## Accounting versus adjusted profit','| Bank | Accounting profit | Adjusted profit | Adjustment gap |','|---|---:|---:|---:|']
for b in banks:
 a=val(b,latest,'net_income_accounting');j=val(b,latest,'net_income_adjusted');lines.append(f"| {names[b]} | {fmt(a)} | {fmt(j)} | {fmt(j-a if a is not None and j is not None else None)} |")
lines+=['','Adjustment gaps are arithmetic differences, not a common definition of exceptional items. Use each bank’s reconciliation to identify goodwill, tax, provisioning and other adjustments.',
'## Income drivers: change versus the prior-year quarter','Positive NII and fees help earnings; positive increases in credit costs or operating expenses consume earnings. The residual below explicitly absorbs other income, insurance when not shown separately, taxes, minority interests and definition differences. It is an arithmetic decomposition, not a causal attribution.',
'| Bank | Δ NII | Δ fees | −Δ credit cost | −Δ operating expenses | Residual | Δ adjusted profit |','|---|---:|---:|---:|---:|---:|---:|']
for b in banks:
 parts=[]
 for m,sign in [('net_interest_income',1),('fees',1),('credit_cost',-1),('operating_expenses',-1)]:
  a=val(b,latest,m);z=val(b,yoy,m);parts.append(None if a is None or z is None else sign*(a-z))
 a=val(b,latest,'net_income_adjusted');z=val(b,yoy,'net_income_adjusted');delta=None if a is None or z is None else a-z
 residual=None if None in parts or delta is None else delta-sum(parts)
 lines.append('| '+names[b]+' | '+' | '.join(fmt(x) for x in parts+[residual,delta])+' |')
lines+=['','BTG reports a business-line revenue model; a retail-bank NII/fee/provision bridge is not forced onto it. Its total revenue, reported operating expenses and profit series are available in the bank detail.',
'## Sources and interpretation','Every scorecard value and historical observation is reproduced with source sheet/cell or PDF page/column in the bank detail files. The CSV also retains original value, unit multiplier, reporting basis, scope, vintage and SHA-256.',
*['- ['+names[b]+']('+str(R/(b+'.md'))+')' for b in banks],
'- [Coverage and gaps]('+str(R/'coverage.md')+')', '- [Metric definitions and comparability]('+str(R/'methodology.md')+')','- [Normalized data]('+str(ROOT/'data/normalized.csv')+')']
notes=R/'interpretation_2Q26.md'
if latest=='2026Q2' and notes.exists():lines+=['','## Management interpretation — reviewed for 2Q26',notes.read_text()]
mdwrite(R/'executive_comparison.md','\n\n'.join(lines[:3])+'\n\n'+'\n'.join(lines[3:]))
for b in banks:
 out=[f'# {names[b]} — financial history',f'Latest source vintage and definitions are attached to each metric. All money amounts in BRL millions. Latest quarter {latest}.', '## Latest metrics and source references','| Metric | Value | Unit | Period basis | Reporting basis | Source |','|---|---:|---|---|---|---|']
 for d in sorted([d for d in obs if d['bank']==b and d['period']==latest],key=lambda x:x['metric']):out.append(f"| {d['metric'].replace('_',' ')} | {fmt(d['value'],2)} | {d['unit']} | {d['frequency'].replace('_',' ')} | {d['basis'].replace('_',' ')} | {ref(d)} |")
 out+=['','## Quarterly history','| Quarter | Adjusted profit | Accounting profit | ROE | NPL90 |','|---|---|---|---|---|']
 for p in periods:out.append('| '+p+' | '+' | '.join(value(b,p,m) for m in ['net_income_adjusted','net_income_accounting','roe_adjusted','npl90'])+' |')
 for title,metrics in [('Income and costs',['net_interest_income','revenue','fees','credit_cost','operating_expenses']),('Credit and asset quality',['loans','loans_expanded','loans_individuals','loans_corporate','loans_agriculture','npl90']),('Capital and funding',['assets','equity','customer_funding','funding_broad','capital_total','cet1'])]:
  ms=[m for m in metrics if any(d['bank']==b and d['metric']==m for d in obs)]
  if not ms:continue
  out+=['','## '+title,'| Quarter | '+' | '.join(m.replace('_',' ') for m in ms)+' |','|---|'+'---:|'*len(ms)]
  for p in periods:out.append('| '+p+' | '+' | '.join(fmt(val(b,p,m),2) for m in ms)+' |')
 out+=['','Historical source references and definition changes for every displayed cell are in [normalized.csv]('+str(ROOT/'data/normalized.csv')+').']
 bridgepath=ROOT/'data/driver_bridges.json'
 if bridgepath.exists():
  bridges=[d for d in json.loads(bridgepath.read_text()) if d['bank']==b and d['comparison']=='QoQ']
  out+=['','## Quarterly earnings-change bridge','BRL millions. Selected component changes plus a residual; not causal attribution. Positive contributions raise profit. BTG uses total revenue and reported expenses; other banks use NII, fees, credit cost and operating expenses, with insurance included separately for Bradesco.','| Quarter | Profit change | Revenue / NII | Fees | Credit cost effect | Expenses effect | Insurance | Other / tax residual |','|---|---:|---:|---:|---:|---:|---:|---:|']
  for d in bridges:out.append('| '+d['period']+' | '+' | '.join(fmt(d.get(k)) for k in ['profit_change','contribution_revenue' if b=='BTG_Pactual' else 'contribution_net_interest_income','contribution_fees','contribution_credit_cost','contribution_operating_expenses','contribution_insurance_result','other_items_and_tax_residual'])+' |')
  out+=['','[All QoQ and YoY bridges with component sources]('+str(ROOT/'data/driver_bridges.csv')+').']
 out+=['','## Definition notes']
 for method in sorted({d['method'] for d in obs if d['bank']==b and d.get('method')}):out.append('- '+method)
 mdwrite(R/(b+'.md'),'\n'.join(out))
# Join discovery with every completed checkpoint to avoid mistaking in-progress files for gaps.
allrows=[]
for p in [*sorted((ROOT/'data/catalogs').glob('20*/progress.json')),ROOT/'data/index.json',ROOT/'data/backfill2024.json']:
 if p.exists():allrows+=json.loads(p.read_text())
completed={}
for d in allrows:
 k=(d['bank'],d['id'])
 if k not in completed or {'pending':0,'failed':1,'external_link':2,'downloaded':3}.get(d['status'],0)>={'pending':0,'failed':1,'external_link':2,'downloaded':3}.get(completed[k]['status'],0):completed[k]=d
full={ (d['bank'],d['id']):d for d in dis}
for extra in [ROOT/'data/supplements.json',ROOT/'data/supplemental.json']:
 if extra.exists():full.update({(d['bank'],d['id']):d for d in json.loads(extra.read_text())})
full.update(completed); rows=list(full.values())
(ROOT/'data/coverage_index.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with (ROOT/'data/coverage_index.csv').open('w',newline='',encoding='utf-8-sig') as f:
 keys=list(dict.fromkeys(k for d in rows for k in d));w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
c=collections.Counter(d['status'] for d in rows)
coverage=['# Source archive coverage',f'As of {datetime.datetime.now().isoformat(timespec="minutes")}. Catalog records: {len(rows)}. Status counts: {dict(c)}.', 'Coverage means coverage of the selected official results-center categories in data/sources.json, plus explicitly indexed supplements. It is not a claim that every page anywhere on each bank website has been archived. Audio/video and live web pages are indexed as links. Files still pending or failed are not counted as downloaded.', '| Bank | Quarter | Downloaded | Links | Pending/failed | Normalized observations |','|---|---|---:|---:|---:|---:|']
for b in banks:
 for p in periods:
  rs=[d for d in rows if d['bank']==b and d['period']==p[-1]+'T'+p[2:4]];ct=collections.Counter(d['status'] for d in rs)
  coverage.append(f"| {names[b]} | {p} | {ct['downloaded']} | {ct['external_link']} | {len(rs)-ct['downloaded']-ct['external_link']} | {sum(d['bank']==b and d['period']==p for d in obs)} |")
coverage+=['','## Explicit gaps and limitations','- Accounting, credit, funding and capital coverage varies by bank/period; use the metric-level CSV rather than interpreting blanks as zero.','- BTG NPL90 is not normalized; corporate and consumer credit risk require separate definitions.','- Historical workbooks are normalized from the latest available mapped vintage. Earlier documents are archived; their full metric restatement deltas are not yet normalized. Caixa PDF comparative vintages are retained in pdf_versions.json.','- Itaú historical spreadsheet is currently an explicit 2Q26 supplement; a subsequent-quarter refresh must discover and validate its replacement link.','- Same-URL remote replacement detection requires the full recheck option; normal incremental mode checks local hashes and discovers changed/new catalog IDs/URLs.','- Narrative interpretation is reviewed only through 2Q26. Future quarters require a new evidence review.']
coverage+=['','## Core document coverage by quarter','Cells show downloaded / discovered catalog records for each document family. Zero means the selected catalog exposes no matching record; it is not proof that the bank never published the document. Supplemental latest historical workbooks can contain earlier quarters even where no quarterly workbook is exposed.','| Bank | Quarter | Results/analysis | Presentations | Statements | Historical sheets | Transcripts |','|---|---|---:|---:|---:|---:|---:|']
matrix=[]
patterns={'results_analysis':r'release|analise.*(?:desempenho|economica|gerencial)|informe.*resultado|sumario.*resultado','presentation':r'apresenta|coletivas-de-imprensa','statements':r'demonstrac','historical':r'series.*historic|historical','transcript':r'transcri'}
for b in banks:
 for p in periods:
  rs=[d for d in rows if d['bank']==b and d['period']==p[-1]+'T'+p[2:4]];entry={'bank':b,'period':p};cells=[]
  for family,pattern in patterns.items():
   ds=[d for d in rs if not (d['status']=='external_link' and any(x in d['category'].lower() for x in ['gravacao','video','audio','podcast'])) and re.search(pattern,unicodedata.normalize('NFKD',d['title']+' '+d['category']).encode('ascii','ignore').decode().lower())]
   done=sum(d['status']=='downloaded' for d in ds);entry[family+'_downloaded']=done;entry[family+'_discovered']=len(ds);cells.append(str(done)+' / '+str(len(ds)))
  matrix.append(entry);coverage.append('| '+names[b]+' | '+p+' | '+' | '.join(cells)+' |')
with (ROOT/'data/coverage_matrix.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,list(matrix[0]));w.writeheader();w.writerows(matrix)
failed=[d for d in rows if d['status']=='failed']
for d in failed:coverage.append(f"- Download failure: {d['bank']} {d['period']} — {d['title']}: {d.get('error','')} ([official URL]({d['url']})).")
mdwrite(R/'coverage.md','\n'.join(coverage));print('Reports generated',latest,c)
