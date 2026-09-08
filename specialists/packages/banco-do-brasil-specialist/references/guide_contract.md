# Complete guide deliverable

Write an executive document with a linked contents page and technical evidence appendices. There is no arbitrary page limit: depth follows materiality and evidence. Use concise synthesis in the executive opening and detailed financial/strategic reasoning underneath. Respond in English unless the user requests otherwise; preserve original-language source titles and accurately translate short excerpts.

## Required substance

1. **Executive thesis:** what this bank is, how it makes money, what changed, what is working, what is failing or uncertain, and the main CEO/CFO implications. Date and scope every guide.
2. **Franchise map:** products, clients, geography, distribution, competitive position and the economics of each important business. Identify evidence gaps in segment profitability.
3. **Strategy over time:** phases and turning points, intended mechanisms, resource allocation, trade-offs and outcomes. Include an explicit timeline.
4. **Financial anatomy:** income statement and notes, balance sheet, cash flow and capital. Provide accounting-to-recurring reconciliation and QoQ/YoY/longer-term bridges. Explain interactions, not a list of ratios.
5. **Funding and deployment:** where funding came from, its cost/stickiness/maturity, where balance-sheet capacity went, and how this affected earnings, liquidity and capital.
6. **Risk narrative:** exposure, leading indicators, realized losses, buffers, tail risks and management's perception, including contradictions and unresolved questions.
7. **Earnings calls:** recurring analyst challenges, management explanations, guidance/commitments, later evidence, unanswered questions and strategic changes in emphasis. Prepared remarks and Q&A must remain identifiable. No transcript means an explicit gap, not an invented Q&A summary.
8. **What the numbers reveal:** material calculated findings and inferences, alternatives, confidence and falsification indicators; disagreements between narrative and numbers where supported.
9. **Strengths and weaknesses:** product/client specificity, benchmark, durability, vulnerabilities and counterarguments. Distinguish current results from a sustainable advantage.
10. **Forward watchlist and executive agenda:** indicator, reason, directional trigger or justified threshold, horizon, source, and what it would imply. Scenarios are conditional sensitivities, not forecasts or official guidance. Include the questions a CEO/CFO should put to management and what evidence would resolve them.
11. **Evidence and coverage:** period/document/call coverage, exclusions, reporting breaks, reconciliations, sources and unresolved items. An incomplete call or financial section must be visible in the executive opening; do not title unsupported work a complete verified guide.

## Saved artifacts

Use `specialists/knowledge/<bank_id>/runs/<timestamp>/`:
- `guide.md`: navigable main guide, source links and adjacent page/cell/timestamp references.
- `evidence_ledger.csv`: claim_id, theme, period, evidence_class, claim, source_path, source_url, locator, inputs_or_formula, alternative_explanation, confidence_reason, falsifier, review_status. Multiple supporting sources may occupy separate rows under one claim_id.
- `strategy_timeline.csv`: phase/period, stated_strategy, allocation_or_execution, observed_outcome, evidence_ids, qualification.
- `call_ledger.csv`: call_date, reporting_period, speaker, role, prepared_or_qa, analyst_question, management_response, commitment, definition_and_horizon, later_evidence_ids, assessment, locator. Leave unavailable fields missing rather than reconstructing them.
- `coverage.json`: requested interval, documents actually reviewed, absent/unreadable sources, call coverage, calculation/mapping limitations, material unresolved questions and guide status (`complete_with_stated_limitations` or `partial`). Record source hashes and vintage.

After review, write `specialists/knowledge/<bank_id>/latest.json` containing the run path and status. Do not create empty deliverable shells and claim a completed guide. A focused answer need not produce all five artifacts.

## Release gate

Check that every decisive number and management claim is traceable; bridges reconcile or expose residuals; key contrary evidence is considered; stock/flow, entity, period and accounting perimeters match; conclusions survive obvious alternative explanations; and calls are genuinely reviewed across the requested interval. Review at least the material tables in the original source layout. Report the remaining limitations and explain whether they could change the thesis.
