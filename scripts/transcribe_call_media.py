"""Local MLX Whisper transcription with timestamped provenance and resumable output."""
import os,json,pathlib,hashlib,datetime,argparse
os.environ['TOKENIZERS_PARALLELISM']='false'
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
 import mlx_whisper
 ap=argparse.ArgumentParser();ap.add_argument('--bank',default='BTG_Pactual');ap.add_argument('--input');ap.add_argument('--period');ap.add_argument('--url');ap.add_argument('--language',default='pt');a=ap.parse_args()
 model=str(next(pathlib.Path('/Users/francisco/.cache/huggingface/hub/models--mlx-community--whisper-large-v3-turbo/snapshots').iterdir()))
 ds=[d for d in json.loads((ROOT/'data/index.json').read_text()) if d['bank']==a.bank and d['year']>=2025 and d.get('format') in ('mp3','mp4')]
 if a.input:ds=[{'bank':a.bank,'year':2000+int(a.period[-2:]),'period':a.period,'path':a.input,'url':a.url,'title':'Gravação do call '+a.period}]
 elif a.period:ds=[d for d in ds if d['period'] in a.period.split(',')]
 for d in sorted(ds,key=lambda d:(d['year'],d['period'])):
  out=ROOT/'data/calls'/a.bank/d['period'];out.mkdir(parents=True,exist_ok=True)
  if (out/'asr.json').exists():continue
  if a.bank=='BTG_Pactual' and d['period']=='1T26':
   r=json.loads((ROOT/'data/BTG_1T26_QA_PORT_transcricao.json').read_text());method='Previously generated MLX Whisper transcription; original ASR parameters unavailable'
  else:
   print('START',a.bank,d['period'],flush=True)
   r=mlx_whisper.transcribe(str(ROOT/d['path']),path_or_hf_repo=model,language=a.language,verbose=False,condition_on_previous_text=False)
   method=f'mlx-whisper 0.4.3 / whisper-large-v3-turbo; language {a.language}; condition_on_previous_text=False'
  r['provenance']={'source':d,'method':method,'created_at':datetime.datetime.now().isoformat(),'quality':'Automatic transcript, not audio-verified; names, units and numbers require source checking'}
  (out/'asr.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
  (out/'asr.txt').write_text('\n'.join(f"[{s['start']:.2f}–{s['end']:.2f}s] {s['text'].strip()}" for s in r['segments']))
  print('DONE',a.bank,d['period'],len(r['segments']),flush=True)
if __name__=='__main__':main()
