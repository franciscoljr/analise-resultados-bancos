"""Extract explicit CET1 columns from Itaú executive-summary tables."""
import pathlib,json,re,hashlib
from pypdf import PdfReader
ROOT=pathlib.Path(__file__).resolve().parents[1];docs=[]
for p in [ROOT/'data/discovered.json',ROOT/'data/index.json']:
 if p.exists():docs+=json.loads(p.read_text())
versions=[]
for p in sorted((ROOT/'documents/Itau').glob('*/*/Analise_gerencial*.pdf')):
 per=p.parent.name;vintage=f'20{per[-2:]}Q{per[0]}';d=next((d for d in docs if d.get('path')==str(p.relative_to(ROOT))),None) or next((d for d in docs if d['bank']=='Itau' and d['period']==per and d['category']=='central_analise_gerencial_da_operacao'),None)
 if not d:continue
 for i,page in enumerate(PdfReader(p).pages[:10]):
  t=page.extract_text()
  if 'Sumário do Resultado Gerencial' not in t:continue
  headers=next((line for line in t.splitlines() if re.search(r'[1-4]T\d{2}.*[1-4]T\d{2}.*[1-4]T\d{2}',line)),None)
  if not headers:continue
  quarters=re.findall(r'([1-4])T(\d{2})',headers)[:3]
  line=next((line for line in t.splitlines() if line.strip().startswith('Índice de Capital Principal') and 'Common Equity' in line),None)
  if not line:continue
  values=re.findall(r'(\d+,\d+)%',line)
  if len(values)<3:continue
  for q,v in zip(quarters,values[:3]):
   period=f'20{q[1]}Q{q[0]}'
   if period<'2024Q1':continue
   versions.append(dict(bank='Itau',period=period,metric='cet1',value=float(v.replace(',','.')),unit='percent',frequency='end_of_period',basis='prudential',scope='prudential',method='Explicit Common Equity Tier I row; values rounded as published in summary',source_label='Índice de Capital Principal (Common Equity Tier I)',source_url=d['url'],source_path=str(p.relative_to(ROOT)),source_reference=f'PDF p. {i+1}; CET1 row; column {q[0]}T{q[1]}',source_vintage=vintage,source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),raw_value=float(v.replace(',','.')),multiplier=1,status='table_extracted'))
unique={}
for d in sorted(versions,key=lambda x:x['source_vintage']):unique[d['period']]=d
(ROOT/'data/itau_capital_observations.json').write_text(json.dumps(list(unique.values()),ensure_ascii=False,indent=2));print('Itaú CET1 quarters',len(unique))
