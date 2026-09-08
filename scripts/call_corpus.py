"""Build clean, timestamped caption text and a bank-isolated source manifest."""
import json,pathlib,re,html,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def captions(p):
 rows=[];last=''
 for block in re.split(r'\n\s*\n',p.read_text()):
  lines=block.splitlines();ti=next((i for i,l in enumerate(lines) if '-->' in l),None)
  if ti is None:continue
  stamp=lines[ti].split(' --> ')[0];clean=html.unescape(re.sub('<[^>]+>','', '\n'.join(lines[ti+1:])))
  for line in clean.splitlines():
   line=line.strip()
   if line and line!=last:rows.append({'timestamp':stamp,'text':line});last=line
 return rows
def main():
 records=[]
 for folder in sorted((ROOT/'data/calls').glob('*/*')):
  if not folder.is_dir():continue
  bank,period=folder.parts[-2:]
  if not re.fullmatch('[1-4]T2[56]',period):continue
  for typ in ['official','asr','youtube']:
   src=folder/(typ+'.json' if typ!='youtube' else 'youtube.info.json')
   if not src.exists():continue
   d=json.loads(src.read_text());p=folder/(typ+'.txt')
   if typ=='youtube':
    v=folder/'youtube.pt-orig.vtt'
    if not v.exists():v=folder/'youtube.pt.vtt'
    if not v.exists():continue
    rows=captions(v);p.write_text('\n'.join(f"[{r['timestamp']}] {r['text']}" for r in rows));(folder/'youtube_segments.json').write_text(json.dumps(rows,ensure_ascii=False))
    url=d['webpage_url'];source_path=str(v.relative_to(ROOT));title=d['title']
   else:
    orig=d['source'] if typ=='official' else d['provenance']['source'];url=orig['url'];source_path=orig['path'];title=orig['title']
   records.append(dict(bank=bank,period=period,version=typ,title=title,url=url,source_path=source_path,path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),characters=len(p.read_text()),status='downloaded',format='txt',category='call_transcript',quality='Official RI transcript' if typ=='official' else 'Automatic transcription; validate numbers and names against primary disclosures'))
 (ROOT/'data/calls/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
 print('Corpus versions',len(records),'bank-periods',len({(d['bank'],d['period']) for d in records}))
if __name__=='__main__':main()
