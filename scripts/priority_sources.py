import collect, pathlib,json,concurrent.futures
root=collect.ROOT; run=sorted((root/'data/catalogs').glob('20*'))[-1]; jobs=[]
for p in run.glob('*_2026.json'):
 bank=p.stem[:-5]; data=json.loads(p.read_text())
 if 'data' in data: rows=data['data']['document_metas']
 else: rows=[dict(id=d['id'],file_title=d['title'],file_year=2026,file_quarter=2,permalink=d['url'],internal_name=cat,file_url=d['url']) for cat,v in data['categories'].items() if cat=='planilha_series_historicas' for d in v if '2T26' in d['title']]
 for r in rows:
  cat=r['internal_name']; title=r.get('file_title','')
  if (('serie' in cat or (bank=='Caixa' and 'analise-de-desempenho' in cat)) and r.get('file_quarter')==2):
   jobs.append(dict(bank=bank,id=r['id'],year=2026,period='2T26',title=title,type=cat,category=cat,url=r['permalink'],portal=next(c['portal'] for c in json.load(open(root/'data/sources.json')) if c['bank']==bank),status='pending'))
jobs.append(dict(bank='Itau',id='supplement-dd4bec5c',year=2026,period='2T26',title='Planilha de Séries Históricas 2T26',type='historical_series',category='supplement',url='https://api.mziq.com/mzfilemanager/v2/d/42787847-4cf6-4461-94a5-40ed237dca33/dd4bec5c-fb49-759c-fabc-b5db791b0aae?origin=2',portal='https://www.itau.com.br/relacoes-com-investidores/resultados-e-relatorios/central-de-resultados/',status='pending'))
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for d in pool.map(lambda d:collect.download(d,{}),jobs):
  out.append(d);collect.savejson(root/'data/priority.json',out); print(d['bank'],d['status'],d.get('path',d.get('error')),flush=True)
