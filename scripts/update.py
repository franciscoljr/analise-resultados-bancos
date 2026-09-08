#!/usr/bin/env python3
"""On-demand refresh; no scheduler. Run with Python providing openpyxl and pypdf."""
import argparse,subprocess,sys,pathlib,json,datetime,fcntl
ROOT=pathlib.Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--offline',action='store_true');ap.add_argument('--refresh-existing',action='store_true');ap.add_argument('--workers',type=int,default=12);a=ap.parse_args()
lock=(ROOT/'.update.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
steps=[]
if not a.offline:steps.append(['collect.py','--workers',str(a.workers)]+(['--refresh-existing'] if a.refresh_existing else []))
steps += [['extract_caixa.py'],['extract_itau_capital.py'],['normalize.py'],['driver_bridges.py'],['validate.py'],['charts.py'],['build_reports.py']]
results=[]
for step in steps:
 p=subprocess.run([sys.executable,str(ROOT/'scripts'/step[0]),*step[1:]],cwd=ROOT);results.append({'step':step[0],'exit_code':p.returncode})
ix=json.loads((ROOT/'data/index.json').read_text()) if (ROOT/'data/index.json').exists() else []
missing=[{'bank':d['bank'],'period':d['period'],'title':d['title'],'status':d['status']} for d in ix if d['status'] not in ['downloaded','external_link']]
errors=json.loads((ROOT/'data/normalization_errors.json').read_text())
obs=json.loads((ROOT/'data/normalized.json').read_text());stale=[]
for b in {d['bank'] for d in ix}:
 expected=max((f"{d['year']}Q{d['period'][0]}" for d in ix if d['bank']==b and d['period'][0].isdigit()),default='')
 actual=max((d['period'] for d in obs if d['bank']==b and d['metric']=='net_income_adjusted'),default='')
 if actual<expected:stale.append({'bank':b,'latest_disclosed':expected,'latest_normalized_profit':actual})
report={'date':datetime.datetime.now().isoformat(),'steps':results,'download_gaps':missing,'mapping_errors':errors,'stale_bank_series':stale,'narrative_reviewed_through':'2026Q2','requires_narrative_review':any(d['period']>'2026Q2' for d in obs)}
(ROOT/'data/update_status.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('Update status saved to data/update_status.json')
if missing or errors or stale or any(r['exit_code'] for r in results):sys.exit(1)
