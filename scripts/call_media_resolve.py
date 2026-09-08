"""Resolve official call links; retain catalog URLs and redirect evidence."""
import json,pathlib,subprocess,concurrent.futures,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
def resolve(d):
 p=subprocess.run(['curl','-sSIL','--max-time','45',d['url']],capture_output=True,text=True)
 loc=re.findall(r'^location:\s*(.+)',p.stdout,re.I|re.M)
 return dict(d,redirects=loc,resolved_url=loc[-1].strip() if loc else d['url'],resolve_error=p.stderr.strip())
if __name__=='__main__':
 ds=json.loads((ROOT/'data/discovered_calls_refresh.json').read_text())
 ds=[d for d in ds if d['bank']!='BTG_Pactual' and ('video' in d['category'] or 'teleconferencia_de_resultados' in d['category'] or 'video' in d['title'].lower()) and 'transcri' not in d['category']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:out=list(pool.map(resolve,ds))
 (ROOT/'data/calls/media_links.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 for d in out:print(d['bank'],d['period'],d['resolved_url'],d['resolve_error'])
