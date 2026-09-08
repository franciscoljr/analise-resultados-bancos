"""Print source passages for a thematic human/model review; never produces conclusions."""
import json,pathlib,re,sys,unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[1]
def canon(s):return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
bank=sys.argv[1]
themes={'Banco_do_Brasil':['agronegocio','guidance','renegocia','capital'], 'Bradesco':['principal','margem de captacao','custo de credito','guidance'], 'Itau':['principalidade','custo de credito','inteligencia artificial','guidance'], 'Santander':['seletividade','margem com clientes','custo de credito','capital'], 'BTG_Pactual':['credito','captacao','pan','pergunta'], 'Caixa':['habitac','inadimpl','poupanca','pergunta']}[bank]
for period in ['1T25','2T25','3T25','4T25','1T26','2T26']:
 folder=ROOT/'data/calls'/bank/period
 p=next((folder/(n+'.txt') for n in ['official','asr','youtube'] if (folder/(n+'.txt')).exists()),None)
 if not p:continue
 s=p.read_text();c=canon(s);positions=[min(1800,len(s)//10)]
 for term in themes:
  matches=list(re.finditer(re.escape(term),c));m=next((m for m in reversed(matches) if m.start()<len(s)-1500),None)
  if m and all(abs(m.start()-k)>1300 for k in positions):positions.append(m.start())
 print('\n###',bank,period,'SOURCE',p.relative_to(ROOT))
 for pos in sorted(positions):
  start=max(0,pos-650);end=min(len(s),pos+1600)
  page=list(re.finditer(r'=== PÁGINA (\d+) ===',s[:pos]));locator='page '+page[-1][1] if page else 'character '+str(pos)
  print('\nLOCATOR',locator,'chars',start,end,'\n',s[start:end])
