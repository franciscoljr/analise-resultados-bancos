# Bank specialists for the CEO and CFO

Six reusable specialists connect to the official documents and financial history in this project. Each has its own bank-specific analytical priorities and knowledge directory. They can answer focused questions, generate a full guide, or update a previously reviewed guide with new evidence.

| Bank | Invoke |
|---|---|
| Banco do Brasil | `$banco-do-brasil-specialist` |
| Bradesco | `$bradesco-specialist` |
| BTG Pactual | `$btg-pactual-specialist` |
| Caixa | `$caixa-specialist` |
| Itaú Unibanco | `$itau-specialist` |
| Santander Brasil | `$santander-specialist` |

## First complete guide

Use the relevant specialist name, for example:

> $itau-specialist Create the complete CEO/CFO guide to Itaú from 2024 through the latest verified quarter. Explain how its strategy, products, clients, results and risk evolved. Trace earnings, funding, cash and capital separately. Integrate prepared remarks and analyst Q&A, test management's explanations against subsequent results, and identify strengths, weaknesses and what the numbers imply. Save the guide and supporting evidence, with explicit coverage gaps.

The guide includes the executive thesis; franchise map; strategy timeline; financial statements and reconciliations; sources and uses of money; risk interactions; earnings-call commitments and outcomes; numerical findings and alternative explanations; strengths and weaknesses; and a forward watchlist with questions for management.

Every material conclusion must distinguish disclosed fact, management assertion, calculation and analytical inference. A change in a balance-sheet stock must not be presented as an equivalent cash flow. Inferences require evidence, alternative explanations and indicators that would disprove them.

## Follow-up questions

> $bradesco-specialist Is the improvement in profitability supported by durable operating changes? Separate insurance, credit costs, funding, productivity and nonrecurring effects. Show contrary evidence and what remains unproven.

> $banco-do-brasil-specialist How did the risk of the agribusiness portfolio change, and how did management's explanations evolve? Connect exposures, renegotiations, delinquency, write-offs, provisions and capital over time.

> $btg-pactual-specialist Which earnings streams appear recurring, and which depend on market conditions or transactions? Relate that distinction to funding, liquidity and capital consumption.

## Persistent knowledge and updates

A completed guide is saved under `specialists/knowledge/<bank_id>/runs/<timestamp>/`, together with an evidence ledger, strategy timeline, call ledger and coverage assessment. A reviewed run receives a `latest.json` pointer. Updates preserve previous runs and reassess earlier conclusions and management commitments.

Ask the specialist to update its guide after a new release. Source collection and analysis run when requested; no recurring schedule has been created.

## Current readiness and gaps

The specialists are configured and the evidence inventories are prepared. The six complete analytical guides have **not yet been generated**. The existing bank reports are inputs, not substitutes for that deeper source review.

The financial base spans 1Q24–2Q26, with 1,211 normalized observations. The call update covers 1Q25–2Q26 for BB, Bradesco, BTG, Itaú and Santander, and 2Q26 for Caixa. The five earlier Caixa quarters remain unresolved. See [call coverage and sources](../reports/calls_2025_2026.md).

Each specialist now has a dated thematic call review, source ledger and `latest_calls.json` pointer. These memories distinguish management assertions, analytical inference and open commitments. They do not constitute full bank guides or a word-by-word audit. Official transcripts, downloaded YouTube captions and transcribed media are searchable through the evidence helper; automatic text requires numeric validation.

Package validation, bank/period retrieval isolation and incremental indexing checks passed. Full-guide analytical behavior has not yet been tested through a completed guide. Structural validation does not establish the accuracy of future conclusions.

## Availability and maintenance

The installation registers the six package folders in the personal skill directory through symbolic links. Keep this project at its current location. If the specialist names do not appear, restart Codex; the current session's skill list may predate registration. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

The editable package sources are `profiles.json` and `shared/`; rebuild with `scripts/build_bank_specialists.py` after changing them. `scripts/specialist_evidence.py` prepares bank inventories and retrieves source pages. `validation.json` records checks; `installation.json` records registration paths.
