"""Validate the archive and cross-check normalized amounts against release anchors."""
import pathlib,json,hashlib,zipfile,concurrent.futures
from pypdf import PdfReader
ROOT=pathlib.Path(__file__).resolve().parents[1]
def inspect(p):
 try:
  digest=hashlib.sha256(p.read_bytes()).hexdigest()
  if '__'+digest[:12] not in p.stem:raise ValueError('Content hash differs from filename')
  if p.suffix=='.pdf':
   r=PdfReader(p);n=len(r.pages)
   if not n:raise ValueError('No PDF pages')
   return dict(path=str(p.relative_to(ROOT)),status='passed',pages=n,sha256=digest)
  if p.suffix in ['.xls','.doc','.rtf','.mp3','.mp4']:
   b=p.read_bytes();ok=(p.suffix in ['.xls','.doc'] and b[:8]==bytes.fromhex('d0cf11e0a1b11ae1')) or (p.suffix=='.rtf' and b.startswith(b'{\\rtf')) or (p.suffix=='.mp3' and (b.startswith(b'ID3') or b[:1]==b'\xff')) or (p.suffix=='.mp4' and b[4:8]==b'ftyp')
   if not ok:raise ValueError('Binary format signature mismatch')
   return dict(path=str(p.relative_to(ROOT)),status='passed',sha256=digest,validation='SHA-256 and binary signature')
  with zipfile.ZipFile(p) as z:
   bad=z.testzip()
   if bad:raise ValueError('CRC failure '+bad)
  return dict(path=str(p.relative_to(ROOT)),status='passed',sha256=digest)
 except Exception as e:return dict(path=str(p.relative_to(ROOT)),status='failed',error=str(e))
paths=[p for p in (ROOT/'documents').rglob('*') if p.suffix in ['.pdf','.xlsx','.docx','.pptx','.zip','.xls','.doc','.rtf','.mp3','.mp4']]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:archive=list(pool.map(inspect,paths))
obs=json.loads((ROOT/'data/normalized.json').read_text());lookup={(d['bank'],d['period'],d['metric']):d for d in obs};checks=[]
# Independently read release highlights/key-figure tables, rounded to BRL millions.
anchors={'Banco_do_Brasil':{'net_income_adjusted':3908,'net_income_accounting':3175,'net_interest_income':27483,'credit_cost':18477,'fees':9125,'npl90':5.61},'Bradesco':{'net_income_adjusted':7050,'net_income_accounting':7050,'net_interest_income':20872,'credit_cost':9985,'fees':10486,'npl90':4.3},'BTG_Pactual':{'net_income_adjusted':5142,'net_income_accounting':4901,'revenue':10371,'assets':925219,'roe_adjusted':26.7},'Caixa':{'net_income_adjusted':3899,'net_income_accounting':3899,'fees':7573,'credit_cost':6966,'loans':1448200,'roe_adjusted':9.16,'npl90':3.64},'Santander':{'net_income_adjusted':3014,'net_income_accounting':2667,'fees':5334,'credit_cost':7654,'roe_adjusted':12.5},'Itau':{'cet1':12.3,'net_income_adjusted':12407,'net_income_accounting':12181,'npl90':1.9}}
for b,metrics in anchors.items():
 for m,expected in metrics.items():
  d=lookup.get((b,'2026Q2',m));tol=.11 if m in ['npl90','roe_adjusted','cet1'] else 1
  ok=d is not None and abs(d['value']-expected)<=tol
  checks.append(dict(bank=b,metric=m,expected=expected,actual=d['value'] if d else None,status='passed' if ok else 'failed',type='release_anchor'))
for d in obs:
 err=[]
 if not (ROOT/d['source_path']).exists():err.append('Missing source')
 if not d.get('source_reference') or not d.get('source_url'):err.append('Missing provenance')
 if d['metric'] in ['credit_cost','operating_expenses','fees','assets','loans'] and d['value']<0:err.append('Unexpected sign')
 if d['metric'] in ['npl90','cet1','capital_total'] and not 0<=d['value']<=100:err.append('Percentage scale')
 if d['metric']=='fees' and d['value']<100:err.append('Implausible scale: inspect footnotes/unit')
 if err:checks.append(dict(bank=d['bank'],period=d['period'],metric=d['metric'],status='failed',error=err))
res={'archive':archive,'data_checks':checks,'failed_files':sum(x['status']=='failed' for x in archive),'failed_data_checks':sum(x['status']=='failed' for x in checks)}
(ROOT/'data/validation.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print('Validated',len(archive),'documents;',len(checks),'data checks; failures',res['failed_files'],res['failed_data_checks'])
for x in checks:
 if x['status']=='failed':print(x)
if res['failed_files'] or res['failed_data_checks']:raise SystemExit(1)
