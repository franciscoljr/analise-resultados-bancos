"""Extract explicit quarterly columns from Caixa key-figures tables; retain vintages."""
import pathlib,json,re,hashlib,unicodedata
from pypdf import PdfReader
ROOT=pathlib.Path(__file__).resolve().parents[1]
def simple(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if not unicodedata.combining(c))
def number(s):return float(s.replace('.','').replace(',','.').replace('(','-').replace(')',''))
spec=[('lucro liquido contabil','net_income_accounting','quarter'),('lucro liquido recorrente','net_income_adjusted','quarter'),('resultado operacional','operating_result','quarter'),('margem financeira','net_interest_income','quarter'),('provisao para creditos de liquidacao duvidosa (pcld)','credit_cost','quarter'),('receita com prestacao de servicos','fees','quarter'),('despesas administrativas','operating_expenses','quarter'),('despesas de pessoal','personnel_expenses','quarter'),('ativos caixa','assets','end_of_period'),('credito','loans','end_of_period'),('comercial pf','loans_individuals','end_of_period'),('comercial pj','loans_corporate','end_of_period'),('imobiliario','loans_mortgage','end_of_period'),('agronegocio','loans_agriculture','end_of_period'),('recursos de clientes','customer_funding','end_of_period'),('patrimonio liquido','equity','end_of_period'),('indice de basileia','capital_total','end_of_period'),('indice de capital principal','cet1','end_of_period'),('inadimplencia total (atrasos > 90 dias)','npl90','end_of_period'),('cobertura > 90 dias','coverage_npl90','end_of_period'),('roe contabil','roe_accounting','trailing_12m'),('roe recorrente','roe_adjusted','trailing_12m'),('indice de eficiencia operacional recorrente','efficiency','trailing_12m')]
docs=[]
for p in [ROOT/'data/index.json',ROOT/'data/priority.json',ROOT/'data/discovered.json']:
 if p.exists():docs+=json.loads(p.read_text())
versions=[];issues=[]
for p in sorted((ROOT/'documents/Caixa').glob('*/*/Relatorio_de_Analise*.pdf')):
 per=p.parent.name;vintage=f'20{per[-2:]}Q{per[0]}'
 d=next((d for d in docs if d.get('path')==str(p.relative_to(ROOT))),None) or next((d for d in docs if d['bank']=='Caixa' and d['period']==per and 'analise' in d['category']),{})
 pages=PdfReader(p).pages
 for i,page in enumerate(pages):
  t=page.extract_text(); low=simple(t)
  if 'itens de resultado' not in low and 'indicadores de performance' not in low:continue
  headers=re.search(r'(?:itens de resultado|indicadores de performance)[^\n]*',low)
  quarters=re.findall(r'([1-4])t(\d{2})',headers[0]) if headers else []
  if len(quarters)<3:issues.append({'path':str(p),'page':i+1,'error':'Quarter columns not recognized'});continue
  seen=set();section=''
  for line in t.splitlines():
   l=simple(line).strip()
   if 'itens patrimoniais' in l:section='balance'
   if 'indicadores da carteira' in l:section='credit_ratios'
   for label,metric,freq in spec:
    if (freq=='trailing_12m') != ('indicadores de performance' in low):continue
    if metric in seen or not l.startswith(label):continue
    tail=l[len(label):]
    tail=re.sub(r'^\s*\d{1,2}(?=\s)','',tail)
    # A suffix is only a footnote marker and whitespace, never a different metric label.
    tail=re.sub(r'^\d{1,2}(?=\s)','',tail)
    if tail and not (tail[0].isspace() or tail[0].isdigit() or tail[0]=='('):continue
    tokens=tail.split()
    if len(tokens)<5:continue
    try:values=[number(tokens[k]) for k in [0,1,3]]
    except ValueError:continue
    if metric in ['loans_mortgage','loans_agriculture'] and section=='credit_ratios':continue
    if metric=='credit_cost' and section=='balance':continue
    seen.add(metric)
    for q,val in zip(quarters[:3],values):
     period=f'20{q[1]}Q{q[0]}'
     if period<'2024Q1':continue
     ratio=metric in ['roe_accounting','roe_adjusted','capital_total','cet1','npl90','coverage_npl90','efficiency']
     mult=-1 if metric in ['credit_cost','operating_expenses','personnel_expenses'] else 1
     versions.append(dict(bank='Caixa',period=period,metric=metric,value=val*mult,unit='percent' if ratio else 'BRL_million',frequency=freq,basis='prudential' if metric in ['capital_total','cet1'] else 'accounting' if metric=='net_income_accounting' else 'managerial',scope='prudential' if metric in ['capital_total','cet1'] else 'managerial_consolidated',method='Explicit quarter column; CMN 4966 break from 2025; ROE and efficiency trailing 12 months',source_label=line.split('  ')[0],source_url=d.get('url',''),source_path=str(p.relative_to(ROOT)),source_reference=f'PDF p. {i+1}; column {q[0]}T{q[1]}; row {label}',source_vintage=vintage,source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),raw_value=val,multiplier=mult,status='table_extracted'))
unique={}
for d in sorted(versions,key=lambda x:x['source_vintage']):unique[(d['period'],d['metric'])]=d
(ROOT/'data/pdf_observations.json').write_text(json.dumps(list(unique.values()),ensure_ascii=False,indent=2))
(ROOT/'data/pdf_versions.json').write_text(json.dumps(versions,ensure_ascii=False,indent=2))
(ROOT/'data/pdf_extraction_errors.json').write_text(json.dumps(issues,indent=2))
print('Caixa:',len(unique),'observations;',len(versions),'vintage observations;',issues)
