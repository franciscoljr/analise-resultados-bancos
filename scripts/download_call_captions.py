import json,pathlib,subprocess,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1]
def run(d):
 out=ROOT/'data/calls'/d['bank']/d['period'];out.mkdir(parents=True,exist_ok=True)
 url=d['resolved_url'];cmd=['/private/tmp/calls_env/bin/yt-dlp','--no-playlist','--skip-download','--write-subs','--write-auto-subs','--sub-langs','pt-orig,pt','--sub-format','vtt','--write-info-json','--no-warnings','--retries','2','-o',str(out/'youtube.%(ext)s'),url]
 p=subprocess.run(cmd,capture_output=True,text=True);(out/'caption_download.log').write_text(p.stdout+'\n'+p.stderr)
 return {'bank':d['bank'],'period':d['period'],'url':url,'exit_code':p.returncode,'vtt_files':[str(p.relative_to(ROOT)) for p in out.glob('youtube*.vtt')],'log':str((out/'caption_download.log').relative_to(ROOT))}
if __name__=='__main__':
 ds=json.loads((ROOT/'data/calls/media_links.json').read_text());extra=ROOT/'data/calls/caixa_links.json'
 if extra.exists():ds+=json.loads(extra.read_text())
 ds=[d for d in ds if 'youtu' in d['resolved_url']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  rows=[]
  for r in pool.map(run,ds):rows.append(r);print(r,flush=True);(ROOT/'data/calls/caption_status.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
