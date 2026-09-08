# Mapa da base

Os caminhos abaixo são relativos à raiz do repositório.

| Conteúdo | Caminho | Como usar |
|---|---|---|
| Perfis dos seis especialistas | `specialists/profiles.json` | Mandato específico e erros conhecidos por banco |
| Protocolo comum | `specialists/shared/analytical_protocol.md` | Regras de evidência, comparabilidade e inferência |
| Contrato de guia completo | `specialists/shared/guide_contract.md` | Conteúdo e registros exigidos; no kit o idioma padrão é português |
| Memória dos calls | `specialists/knowledge/<BANK_ID>/latest_calls.json` | Abrir `review` e `sources` apontados; verificar períodos ausentes |
| Memória de concentração | `specialists/knowledge/<BANK_ID>/latest_business_mix.json` | Abrir `review` e `evidence`; manter denominador e eliminações |
| Inventário por banco | `specialists/knowledge/<BANK_ID>/evidence_pack.json` | Orientação para fontes e dados; não é guia concluído |
| Originais e catálogo | `documents/` e `data/index.json` | Consultar caminho, URL, período e versão da fonte |
| Calls adicionais | `data/calls/manifest.json` | Localizar transcrição oficial, legenda ou ASR com status e versão |
| Observações financeiras | `data/normalized.json` | Valores com proveniência; não cobrem todas as notas |
| Pontes de resultado | `data/driver_bridges.json` | Insumos, componentes e resíduos |
| Definições | `reports/methodology.md` e `data/metric_dictionary.csv` | Bases, unidades e quebras de comparabilidade |
| Cobertura e atualização | `reports/coverage.md` e `data/update_status.json` | Lacunas, erros e séries desatualizadas |
| Sínteses recentes | `reports/business_concentration_2T26.md` e `reports/calls_2025_2026.md` | Orientação temática datada |

Identificadores exatos: `Banco_do_Brasil`, `Bradesco`, `BTG_Pactual`, `Caixa`, `Itau`, `Santander`.

Ordem recomendada: instruções → cobertura e ponteiros → memória temática → evidência original → cálculo → conclusão. O contexto de um agente é selecionado por pergunta; não é necessário colocar 3,1 GB no contexto do modelo.

O snapshot de portabilidade é derivado. As fontes canônicas continuam em `specialists/profiles.json`, `specialists/shared/` e nas memórias datadas de cada banco. Caminhos antigos específicos do computador de origem podem aparecer em registros históricos; resolva o arquivo pelo catálogo relativo em vez de assumir que aquele computador está acessível.
