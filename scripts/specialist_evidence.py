#!/usr/bin/env python3
"""Local evidence retrieval for bank specialists; never synthesizes call conclusions."""
import argparse,collections,datetime,hashlib,json,pathlib,re,sqlite3,unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[1]
BANKS=['Banco_do_Brasil','Bradesco','BTG_Pactual','Caixa','Itau','Santander']
def read(name):return json.loads((ROOT/'data'/name).read_text())
def canonical(s):return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
def kind(d):
 s=canonical(d['title']+' '+d['category'])
 if 'transcri' in s:return 'calls'
 if (d.get('format') in ['mp3','mp4'] or d['status']=='external_link') and any(t in s for t in ['video','audio','podcast','webcast','teleconferencia']):return 'call_media'
 if any(t in s for t in ['demonstrac','ifrs','brgaap']):return 'statements'
 if any(t in s for t in ['risco','pilar']):return 'risk'
 return 'results'
def documents(bank):
 ds=read('index.json');p=ROOT/'data/calls/manifest.json'
 if p.exists():ds+=json.loads(p.read_text())
 return [dict(d,evidence_kind=kind(d)) for d in ds if bank=='all' or d['bank']==bank]
def pack(bank):
 ds=documents(bank);obs=[d for d in read('normalized.json') if d['bank']==bank];periods=sorted({d['period'] for d in obs});calls=[d for d in ds if d['evidence_kind']=='calls'];media=[d for d in ds if d['evidence_kind']=='call_media']
 result={'bank':bank,'created_at':datetime.datetime.now().isoformat(),'status':'evidence_inventory_not_a_completed_guide','periods':periods,'observations':obs,'driver_bridges':[d for d in read('driver_bridges.json') if d['bank']==bank],'documents':ds,'call_coverage':{'transcript_periods':sorted({d['period'] for d in calls if d['status']=='downloaded'}),'transcript_count':len(calls),'media_count':len(media),'gap':'No indexed transcript. Locate official call material or record the guide call section as incomplete.' if not calls else 'Presence does not mean reviewed. Read prepared remarks and Q&A across the interval.'},'limitations':['Existing metric normalization does not cover every statement note, cash-flow item or product/client segment.','A guide requires primary-source reading and analysis beyond this generated inventory.']}
 latest=ROOT/'specialists/knowledge'/bank/'latest_calls.json'
 if latest.exists():result['reviewed_calls_knowledge']=json.loads(latest.read_text())
 p=ROOT/'specialists/knowledge'/bank/'evidence_pack.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,ensure_ascii=False,indent=2));return {'bank':bank,'path':str(p),'observations':len(obs),'transcripts':len(calls),'media':len(media)}
def db():
 p=ROOT/'specialists/evidence.sqlite';c=sqlite3.connect(p);c.execute('CREATE TABLE IF NOT EXISTS sources (id TEXT PRIMARY KEY, bank TEXT, period TEXT, kind TEXT, path TEXT, url TEXT, sha256 TEXT)');c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS pages USING fts5(source_id UNINDEXED, page UNINDEXED, text, tokenize='unicode61 remove_diacritics 2')");return c
def index(bank,family):
 from pypdf import PdfReader
 c=db();done=0;errors=[]
 for d in documents(bank):
  if d.get('format') not in ['pdf','txt'] or d['status']!='downloaded' or family!='all' and d['evidence_kind']!=family:continue
  p=ROOT/d['path'];sha=hashlib.sha256(p.read_bytes()).hexdigest();sid=hashlib.sha256((d['bank']+'|'+d['path']+'|'+sha).encode()).hexdigest()
  if c.execute('SELECT 1 FROM sources WHERE id=?',(sid,)).fetchone():continue
  try:
   if d.get('format')=='pdf':texts=[(sid,i+1,page.extract_text() or '') for i,page in enumerate(PdfReader(p).pages)]
   elif d.get('version')=='official':texts=[(sid,int(m[0]),m[1]) for m in re.findall(r'=== PÁGINA (\d+) ===\n(.*?)(?=\n\n=== PÁGINA |\Z)',p.read_text(),re.S)]
   else:
    lines=p.read_text().splitlines();texts=[(sid,i//40+1,'\n'.join(lines[i:i+40])) for i in range(0,len(lines),40)]
   with c:
    c.execute('INSERT INTO sources VALUES (?,?,?,?,?,?,?)',(sid,d['bank'],d['period'],d['evidence_kind'],d['path'],d['url'],sha));c.executemany('INSERT INTO pages VALUES (?,?,?)',texts)
   done+=1
  except Exception as e:errors.append({'path':str(p),'error':str(e)})
 return {'new_sources_indexed':done,'sources_total':c.execute('SELECT count(*) FROM sources').fetchone()[0],'pages_total':c.execute('SELECT count(*) FROM pages').fetchone()[0],'errors':errors}
def search(bank,query,limit,family,period):
 tokens=re.findall(r'\w+',query,flags=re.UNICODE)
 if not tokens:return []
 match=' OR '.join('"'+t+'"' for t in tokens);c=db();sql='SELECT s.bank,s.period,s.kind,s.path,s.url,p.page,snippet(pages,2,"[", "]"," … ",45),p.text FROM pages p JOIN sources s ON p.source_id=s.id WHERE pages MATCH ? AND s.bank=?';params=[match,bank]
 if family!='all':sql+=' AND s.kind=?';params.append(family)
 if period:sql+=' AND s.period=?';params.append(period)
 sql+=' ORDER BY bm25(pages) LIMIT ?';params.append(limit)
 rows=[dict(zip(['bank','period','kind','source_path','source_url','page','snippet','page_text'],r)) for r in c.execute(sql,params)]
 for r in rows:r['locator_type']='pdf_page' if r['source_path'].endswith(('.pdf','official.txt')) else 'text_chunk_with_timestamps'
 return rows
def main():
 ap=argparse.ArgumentParser();ap.add_argument('command',choices=['pack','index','search']);ap.add_argument('--bank',choices=BANKS+['all'],required=True);ap.add_argument('--kind',choices=['calls','statements','risk','results','all'],default='calls');ap.add_argument('--query',default='');ap.add_argument('--period');ap.add_argument('--limit',type=int,default=8);a=ap.parse_args()
 if a.command=='pack':out=[pack(b) for b in (BANKS if a.bank=='all' else [a.bank])]
 elif a.command=='index':out=index(a.bank,a.kind)
 else:
  if a.bank=='all':ap.error('Search requires one bank to avoid cross-bank evidence contamination')
  out=search(a.bank,a.query,a.limit,a.kind,a.period)
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
