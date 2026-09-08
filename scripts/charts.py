"""Render a static financial-series figure from normalized observations."""
import json,pathlib
from PIL import Image,ImageDraw,ImageFont
ROOT=pathlib.Path(__file__).resolve().parents[1];r=json.loads((ROOT/'data/normalized.json').read_text());ps=sorted({d['period'] for d in r})
canvas=Image.new('RGB',(1500,880),'#f8fafc');g=ImageDraw.Draw(canvas)
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
def font(s):return ImageFont.truetype(fontpath,s)
def text(x,y,s,size=19,fill='#334155'):g.text((x,y),s,font=font(size),fill=fill)
text(55,28,'Recurring earnings: different paths since 2024',32,'#0f172a');text(55,77,'Bank-defined adjusted / recurring profit • quarterly amounts • BRL billions • shared vertical scale',21)
banks=['Banco_do_Brasil','Bradesco','BTG_Pactual','Caixa','Itau','Santander'];names=['Banco do Brasil','Bradesco','BTG Pactual','Caixa','Itaú','Santander'];colors=['#b77d00','#c93249','#234a78','#0485a8','#dc651e','#da3434']
for k,(b,n,c) in enumerate(zip(banks,names,colors)):
 ox=60+(k%3)*490;oy=140+(k//3)*310;w=395;h=210;text(ox,oy,n,24,'#0f172a');x0=ox+32;y0=oy+45
 for v in [0,4,8,12]:
  y=y0+h-v/14*h;g.line((x0,y,x0+w,y),fill='#dde3ea',width=1);text(ox,y-9,str(v),16)
 points=[]
 for i,p in enumerate(ps):
  x=x0+i*w/(len(ps)-1);d=next((d for d in r if d['bank']==b and d['period']==p and d['metric']=='net_income_adjusted'),None)
  if d:
   y=y0+h-d['value']/1000/14*h;points.append((x,y));g.ellipse((x-4,y-4,x+4,y+4),fill=c)
  if i in [0,3,6,len(ps)-1]:text(x-24,y0+h+12,p[4:]+" '"+p[2:4],15)
 if len(points)>1:g.line(points,fill=c,width=4)
 boundary=x0+3.5*w/(len(ps)-1)
 for y in range(int(y0),int(y0+h),12):g.line((boundary,y,boundary,y+5),fill='#64748b',width=1)
 if points:
  d=next(d for d in r if d['bank']==b and d['period']==ps[-1] and d['metric']=='net_income_adjusted');text(points[-1][0]-40,points[-1][1]-27,f"{d['value']/1000:.2f}",19,c)
text(55,797,'Dashed line: 2025 reporting-rule boundary. Latest disclosed vintage; definitions are not fully harmonized.',18)
text(55,825,'Sources: official historical workbooks and Caixa performance tables. Exact cells/pages: bank reports and normalized.csv.',18)
canvas.save(ROOT/'reports/earnings_trends.png')
