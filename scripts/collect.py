#!/usr/bin/env python3
"""Incremental collector for official S1 results catalogs; never overwrites source files."""
import argparse, concurrent.futures, csv, datetime as dt, hashlib, json, pathlib, re, subprocess, tempfile, unicodedata, urllib.parse, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def slug(s): return re.sub(r'[^A-Za-z0-9_-]+','_',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()).strip('_')[:130]
def fetch(url,path,payload=None):
 url=urllib.parse.quote(url,safe=':/?=&%+,@')
 cmd=['curl','-sSL','--fail','--retry','2','--max-time','7200','--connect-timeout','20',url,'-o',str(path),'-w','%{http_code}\n%{content_type}\n%{url_effective}']
 if payload is not None: cmd+=['-H','Content-Type: application/json','--data-binary',json.dumps(payload)]
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr.strip()[-400:])
 return p.stdout.splitlines()
def savejson(path,v):
 tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(v,ensure_ascii=False,indent=2)); tmp.replace(path)
def catalog(c,y,run):
 path=run/f"{c['bank']}_{y}.json"
 if c.get('adapter')=='btg':
  url=f"{c['base']}/v2/files/{c['id']}?language=pt&date={y}-01-02"; fetch(url,path)
  data=json.loads(path.read_text()); rows=[]
  for cat,docs in data['categories'].items():
   if cat not in [x['internal_name'] for x in c['categories']]: continue
   for d in docs:
    title=d['title']; date=d['refDate']; yy=int(date[:4]); q=(int(date[5:7])-1)//3+1
    m=re.search(r'([1-4])[TQ]\s*(?:20)?(\d{2})',title,re.I)
    if m: q=int(m[1]); yy=2000+int(m[2])
    else:
     m=re.search(r'(Março|Junho|Setembro|Dezembro)\s+(?:de\s+)?(20\d{2})',title,re.I)
     if m: q={'março':1,'junho':2,'setembro':3,'dezembro':4}[m[1].lower()]; yy=int(m[2])
    rows.append(dict(id=d['id'],file_title=title,file_year=yy,file_quarter=q,permalink=d['url'],internal_name=cat,file_published_date=d.get('deliveryDate'),language_code='pt',file_url=d['url']))
  return c,rows
 url=f"{c['base']}/company/{c['id']}/filter/categories/year/meta"
 fetch(url,path,dict(year=y,categories=[x['internal_name'] for x in c['categories']],language='pt_BR',published=True))
 data=json.loads(path.read_text())
 if not data.get('success'): raise RuntimeError(str(data)[:300])
 return c,data['data']['document_metas']
def download(d,old,refresh=False):
 if d.get('external_link') and re.search(r'\.(pdf|docx?|xlsx?|pptx?|zip)(?:[?#]|$)',d['url'],re.I):d={**d,'external_link':False}
 key=d['bank']+'|'+d['id']; prev=old.get(key)
 if not refresh and prev and prev.get('status')=='downloaded' and (ROOT/prev['path']).exists():
  if hashlib.sha256((ROOT/prev['path']).read_bytes()).hexdigest()==prev['sha256'] and prev['url']==d['url']:
   return {**d,**{k:prev[k] for k in ['path','sha256','bytes','format','status','validated'] if k in prev}}
 folder=ROOT/'documents'/d['bank']/str(d['year'])/d['period']; folder.mkdir(parents=True,exist_ok=True)
 if d.get('external_link') or ('transcri' not in d['category'].lower() and any(t in d['category'].lower() for t in ['audio','podcast','gravacao','video'])):
  p=folder/(slug(d['title'])+'__'+d['id'][:8]+'.url')
  if not p.exists(): p.write_text('[InternetShortcut]\nURL='+d['url']+'\n')
  return {**d,'path':str(p.relative_to(ROOT)),'status':'external_link','validated':'Official catalog link; streaming/page not archived'}
 try:
  for existing in ([] if refresh else folder.glob(slug(d['title'])+'__*')):
   if existing.suffix not in ['.pdf','.xlsx','.docx','.zip','.xls']: continue
   b=existing.read_bytes(); digest=hashlib.sha256(b).hexdigest()
   if digest[:12] in existing.stem:
    return {**d,'path':str(existing.relative_to(ROOT)),'sha256':digest,'bytes':len(b),'format':existing.suffix[1:],'status':'downloaded','validated':'Recovered signature-validated content-addressed download'}
  with tempfile.NamedTemporaryFile(dir=folder,suffix='.part',delete=False) as f: tmp=pathlib.Path(f.name)
  response=fetch(d['url'],tmp); b=tmp.read_bytes(); ext=''; validation='signature'
  if b.startswith(b'%PDF-'): ext='pdf'; validation='PDF signature and EOF' if b'%%EOF' in b[-2048:] else 'PDF signature; EOF not found'
  elif b.startswith(b'PK'):
   with zipfile.ZipFile(tmp) as z:
    bad=z.testzip()
    if bad: raise ValueError('Invalid ZIP member '+bad)
    names=z.namelist(); ext='xlsx' if any(n.startswith('xl/') for n in names) else 'docx' if any(n.startswith('word/') for n in names) else 'pptx' if any(n.startswith('ppt/') for n in names) else 'zip'; validation='ZIP CRC verified'
  elif b[:8]==bytes.fromhex('d0cf11e0a1b11ae1'): ext='xls' if any(x in d['type'].lower() for x in ['serie','série','planilha']) else 'doc'
  elif b.startswith(b'ID3') or (b[:1]==b'\xff' and len(b)>2 and b[1]&0xe0==0xe0): ext='mp3'
  elif b.startswith(b'{\\rtf'): ext='rtf'
  elif len(b)>8 and b[4:8]==b'ftyp': ext='mp4'
  else: raise ValueError('Not a supported document; content-type '+str(response[1:2]))
  digest=hashlib.sha256(b).hexdigest(); path=folder/(slug(d['title'])+'__'+digest[:12]+'.'+ext)
  if not path.exists(): tmp.rename(path)
  else: tmp.unlink()
  return {**d,'path':str(path.relative_to(ROOT)),'sha256':digest,'bytes':len(b),'format':ext,'status':'downloaded','validated':validation}
 except Exception as e:
  if 'tmp' in locals() and tmp.exists(): tmp.unlink()
  return {**d,'status':'failed','error':str(e)}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--from-year',type=int,default=2024); ap.add_argument('--to-year',type=int,default=dt.date.today().year); ap.add_argument('--only-transcripts',action='store_true'); ap.add_argument('--supplements-only',action='store_true'); ap.add_argument('--refresh-existing',action='store_true'); ap.add_argument('--index-name',default='index'); ap.add_argument('--catalog-only',action='store_true'); ap.add_argument('--workers',type=int,default=6); args=ap.parse_args()
 sources=json.loads((ROOT/'data/sources.json').read_text()); run=ROOT/'data/catalogs'/dt.datetime.now().strftime('%Y%m%dT%H%M%S'); run.mkdir(parents=True)
 oldpath=ROOT/('data/'+args.index_name+'.json'); oldlist=[]
 for recovery in [ROOT/'data/priority.json',*sorted((ROOT/'data/catalogs').glob('20*/progress.json')),ROOT/'data/supplemental.json',ROOT/'data/backfill2024.json',ROOT/'data/transcripts.json',ROOT/'data/index.json',oldpath]:
  if recovery.exists(): oldlist+=json.loads(recovery.read_text())
 oldlist=list({d['bank']+'|'+d['id']:d for d in oldlist}.values()); old={d['bank']+'|'+d['id']:d for d in oldlist}; docs={}; errors=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
  futures={} if args.supplements_only else {pool.submit(catalog,c,y,run):(c['bank'],y) for c in sources for y in range(args.from_year,args.to_year+1)}
  for f in concurrent.futures.as_completed(futures):
   bank,y=futures[f]
   try:
    c,rows=f.result(); print('Catalog',bank,y,len(rows),flush=True)
    types={x['internal_name']:x['title'] for x in c['categories']}
    for r in rows:
     yy=int(r.get('file_year') or y); q=int(r.get('file_quarter') or 0)
     if not args.from_year<=yy<=args.to_year: continue
     u=r.get('permalink') or r.get('file_url') or r.get('link_url')
     if not u: continue
     d=dict(bank=bank,id=r['id'],year=yy,period=f'{q}T{str(yy)[2:]}' if q else 'Annual',title=r.get('file_title') or r.get('file_name_original',''),type=types.get(r['internal_name'],r['internal_name']),category=r['internal_name'],url=u,portal=c['portal'],publication_date=r.get('file_published_date'),language=r.get('language_code'),catalog=str(run.relative_to(ROOT)),external_link=not bool(r.get('file_url')),status='pending')
     k=bank+'|'+r['id']
     if k in docs: docs[k]['type']+='; '+d['type']
     else: docs[k]=d
   except Exception as e: errors.append(dict(bank=bank,year=y,error=str(e))); print('Catalog error',bank,y,str(e),flush=True)
 supp=ROOT/'data/supplements.json'
 if supp.exists():
  for d in json.loads(supp.read_text()):
   if args.from_year<=d['year']<=args.to_year:docs[d['bank']+'|'+d['id']]=d
 if args.only_transcripts:docs={k:d for k,d in docs.items() if 'transcri' in d['category'].lower()}
 savejson(run/'errors.json',errors)
 if args.catalog_only: savejson(ROOT/('data/discovered'+('' if args.index_name=='index' else '_'+args.index_name)+'.json'),list(docs.values()));return
 for d in oldlist:
  if not args.only_transcripts and d.get('category')=='supplement' and args.from_year<=d['year']<=args.to_year:docs[d['bank']+'|'+d['id']]=d
 savejson(ROOT/('data/discovered'+('' if args.index_name=='index' else '_'+args.index_name)+'.json'),list(docs.values()))
 results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
  futures=[pool.submit(download,d,old,args.refresh_existing) for d in sorted(docs.values(),key=lambda d:(-d['year'],d['bank'],d['period']))]
  for i,f in enumerate(concurrent.futures.as_completed(futures)):
   d=f.result(); results.append(d)
   if i%15==0 or d['status']=='failed': print('Files',i+1,'/',len(futures),d['bank'],d['period'],d['status'],d.get('error',''),flush=True)
   if i%10==0:
    savejson(run/'progress.json',results)
    savejson(oldpath,results+[x for x in oldlist if x['bank']+'|'+x['id'] not in {r['bank']+'|'+r['id'] for r in results}])
 # Preserve prior records even when an upstream catalog temporarily removes them.
 for d in oldlist:
  if d['bank']+'|'+d['id'] not in docs: results.append({**d,'catalog_presence':'not_seen_this_run'})
 results.sort(key=lambda x:(x['bank'],x['year'],x['period'],x['type'],x['title']))
 savejson(oldpath,results); savejson(run/'index.json',results)
 fields=['bank','year','period','type','title','url','portal','path','status','format','bytes','sha256','validated','publication_date','language','id','category','catalog','error']
 with (ROOT/('data/'+args.index_name+'.csv')).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(results)
 print('COMPLETE',len(results),'records;',sum(d['status']=='downloaded' for d in results),'downloaded;',len(errors),'catalog errors',flush=True)
 if errors or any(d['status']=='failed' for d in results):raise SystemExit(1)
if __name__=='__main__':main()
