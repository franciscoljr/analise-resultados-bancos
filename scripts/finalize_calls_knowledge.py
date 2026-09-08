"""Refresh source ledgers and knowledge pointers after the dated thematic reviews exist."""
import json,pathlib,collections,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
BANKS=['Banco_do_Brasil','Bradesco','BTG_Pactual','Caixa','Itau','Santander']
PERIODS=['1T25','2T25','3T25','4T25','1T26','2T26']
RUN='2026-09-07_calls_2025_2026'
m=json.loads((ROOT/'data/calls/manifest.json').read_text())
for bank in BANKS:
 base=ROOT/'specialists/knowledge'/bank;out=base/RUN
 assert (out/'review.md').exists()
 sources=[d for d in m if d['bank']==bank]
 (out/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
 present=[p for p in PERIODS if any(d['period']==p for d in sources)]
 (base/'latest_calls.json').write_text(json.dumps(dict(bank=bank,review_date='2026-09-07',review=str((out/'review.md').relative_to(ROOT)),sources=str((out/'sources.json').relative_to(ROOT)),review_scope='Thematic reading of prepared remarks and selected Q&A; not a full audio audit or complete bank guide',transcript_periods=present,missing_periods=[p for p in PERIODS if p not in present]),ensure_ascii=False,indent=2))
 lines=['# Fontes de calls — '+bank,'','Memória temática: [review.md](review.md). A presença da fonte integral não significa auditoria integral do áudio.','', '| Trimestre | Versão | Texto local | Origem |','|---|---|---|---|']
 for d in sources:
  lines.append(f"| {d['period']} | {d['version']} | [Texto]({ROOT/d['path']}) | [Fonte]({d['url']}) |")
 (out/'sources.md').write_text('\n'.join(lines)+'\n')
counts=collections.Counter(d['version'] for d in m)
lines=['# Calls de resultados — 1T25 a 2T26','','Atualizado em 07/09/2026. Corpus organizado por banco e trimestre, com textos integrais disponíveis, fontes e hashes. As seis bases receberam memórias de leitura temática; não são guias completos nem auditoria de cada palavra do áudio.','','## Cobertura','','| Banco | 1T25 | 2T25 | 3T25 | 4T25 | 1T26 | 2T26 | Memória e fontes |','|---|---|---|---|---|---|---|---|']
labels={'official':'PDF oficial','youtube':'YouTube','asr':'Áudio/vídeo transcrito'}
for bank in BANKS:
 cells=[' + '.join(labels[d['version']] for d in m if d['bank']==bank and d['period']==p) or '**Pendente**' for p in PERIODS]
 base=ROOT/'specialists/knowledge'/bank/RUN
 lines.append('| '+bank.replace('_',' ')+' | '+' | '.join(cells)+f' | [Leitura]({base}/review.md) · [Fontes]({base}/sources.md) |')
lines+=['',f"Cobertura: **{len({(d['bank'],d['period']) for d in m})}/36 combinações banco–trimestre**. {counts['official']} transcrições oficiais, {counts['youtube']} legendas de vídeos YouTube e {counts['asr']} versões transcritas de gravações. Versões alternativas do mesmo trimestre não contam como novos calls.",'','## Pendências e limites','','- **Caixa: 1T25, 2T25, 3T25, 4T25 e 1T26.** As buscas em RI, canal oficial e hospedagem não recuperaram as transcrições. O catálogo Vimeo da produtora identifica CEF 3T25 em português, mas a gravação exigiu autorização. A página atual de divulgação aponta para 2T26. Não se concluiu que os arquivos antigos não existam.','- Caixa 2T26 no YouTube é apresentação institucional/financeira; não contém Q&A identificado. A gravação Vimeo do RI foi baixada e transcrita; reproduz a mesma apresentação com offset diferente e também encerra sem Q&A identificado.','- As memórias registram estratégia, mecanismos, risco, expectativas e mudanças de discurso a partir de leitura temática. A revisão integral, linha por linha, de todas as falas e métricas permanece fora do que foi validado aqui.','- Legendas automáticas e ASR podem errar nomes, percentuais e unidades. Para números usar release/apresentação; para citações preferir a transcrição oficial e conferir o contexto.','- BTG 1T25–3T25: mídia disponível em inglês; versão refeita nesse idioma. Versões anteriores forçadas em português foram isoladas. BTG 1T26 reutiliza o trabalho anterior.','- Santander 4T25: título externo incorreto (3T25) preservado como metadado; identificação pelo conteúdo/data interna de 4T25.','- Um download inicial do BB 2T26 seguiu uma playlist incorreta; arquivos foram isolados em quarantine_wrong_playlist, excluídos do manifesto e substituídos pela legenda do vídeo correto.','','## Uso pelos especialistas','','Cada especialista consulta `latest_calls.json`, a memória datada e seu próprio `sources.json`. `evidence_pack.json` inclui a ligação para a memória. A busca local incorpora o manifesto de calls, isola bancos e devolve páginas de PDF ou blocos de texto com horários. Blocos de texto não são páginas do documento original.','','Corpus: [manifesto]('+str(ROOT/'data/calls/manifest.json')+'). Os arquivos oficiais originais continuam preservados na base documental. As gravações Vimeo baixadas estão em data/calls/Itau/2T26 e data/calls/Caixa/2T26; os áudios/vídeos BTG mantêm os caminhos de origem registrados no manifesto.']
(ROOT/'reports/calls_2025_2026.md').write_text('\n'.join(lines)+'\n')
validation=[]
for d in m:
 p=ROOT/d['path'];assert p.exists() and p.stat().st_size>1000
 assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256']
 assert 'quarantine' not in d['path'] and 'superseded' not in d['path']
 if d['version']=='youtube':
  info=json.loads((p.parent/'youtube.info.json').read_text());assert info['id'] in d['url']
 validation.append({'bank':d['bank'],'period':d['period'],'version':d['version'],'verified_path_hash':True})
(ROOT/'data/calls/validation.json').write_text(json.dumps({'date':'2026-09-07','sources':validation,'scope':'File identity, integrity and bank/period coverage; not semantic validation of every transcript'},ensure_ascii=False,indent=2))
print('Updated six knowledge pointers and source ledgers;',len(m),'source versions')
