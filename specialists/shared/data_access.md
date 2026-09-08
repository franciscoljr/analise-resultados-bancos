# Evidence access and updates

Project root: `/Users/francisco/Documents/GPT/Analise Bancos`.

Use `data/index.json` for actual source files, `data/normalized.json` for precise values and provenance, `data/driver_bridges.json` for arithmetic changes and `reports/methodology.md` for known definition breaks. Check `data/update_status.json` and `reports/coverage.md`. Sources can be present without being read. Normalized data alone cannot support a complete financial-statement or earnings-call guide.

Bundled Python with pypdf/openpyxl:
`/Users/francisco/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

The local helper is `scripts/specialist_evidence.py`. Run from the project with that Python:

```
scripts/specialist_evidence.py pack --bank BANK_ID
scripts/specialist_evidence.py index --bank BANK_ID --kind calls
scripts/specialist_evidence.py search --bank BANK_ID --kind calls --query "margem captação provisão" --limit 8
```

Optional `--period 2T26` narrows a search. `--kind statements`, `risk`, `results` or `all` selects other PDFs for indexing/search. Indexing is incremental by content hash. Search is lexical (Portuguese terms often work best), not semantic; search misses do not establish absence. It returns the full page plus path/URL/page so you can read context and cite it. It does not identify speakers, summarize calls, transcribe media, interpret tables or validate claims. Inspect original PDF layouts when needed. Restrict search to the specialist's bank; open peer data only for an explicit benchmark and label it.

`pack` generates `specialists/knowledge/BANK_ID/evidence_pack.json`: bank-filtered observations, bridges, inventory and call availability. It is an inventory, not analytical memory or a completed guide. Rebuild it after refreshing data. The 2025–2026 call corpus is in `data/calls/manifest.json`, automatically included by the helper. Read `specialists/knowledge/BANK_ID/latest_calls.json` and its dated review before answering call/strategy questions. These are thematic analytical memories, not complete guides. Coverage and unresolved Caixa periods are in `reports/calls_2025_2026.md`. Prefer official transcripts for precise quotes and PDF pages; automatic transcripts retain timestamps and require number/name validation. English BTG calls require English search terms. Search results marked `text_chunk_with_timestamps` use chunk numbers, not PDF pages. Never index quarantine or superseded transcripts. Do not claim call completeness based on a presentation or an earnings release.

For a full guide review primary sources for every requested quarter; search is a retrieval aid, not a substitute for chronology. Extract additional statement notes, cash-flow or segment tables as the analysis requires. For XLSX use read-only openpyxl and bound traversal: some Santander sheets contain a million formatted blank rows. Detect needed rows/columns before iterating; preserve headers and units.

Refresh downloads/normalization with `scripts/update.py` when the request calls for fresh releases; inspect its status and stale series warnings. Mappings and supplemental Itaú workbook links may need a source-verified update. No recurring job is configured.

For current business concentration, consult `specialists/knowledge/BANK_ID/latest_business_mix.json` and `reports/business_concentration_2T26.md`. Keep official segment definitions and the reported denominator (revenue, pre-tax result or net income); consolidation eliminations must remain visible.
