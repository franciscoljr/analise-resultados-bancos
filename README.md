# Brazil S1 bank results archive and executive analysis

For reusable CEO/CFO bank specialists and complete-guide workflows, see [Bank specialists](specialists/START_HERE.md).

Start with [Executive comparison](reports/executive_comparison.md), then [Coverage and gaps](reports/coverage.md) and [Metric definitions](reports/methodology.md). The detailed bank reports link each metric to its official source file and page or cell.

The project covers Banco do Brasil, Bradesco, BTG Pactual, Caixa, Itaú and Santander from 2024. The latest reviewed release is **2Q26**. Files are organized under `documents/Bank/Year/Quarter/`; originals are preserved with content hashes. The inventory retains official URLs, document categories, publication information and validation status. Audio/video sources, downloaded recordings and timestamped transcripts are preserved in the archive; see the call coverage report.

## Latest work

- [Business division concentration — 2Q26](reports/business_concentration_2T26.md): official segment definitions, quarterly calculations and cross-bank differences.
- [Earnings calls — 1Q25 through 2Q26](reports/calls_2025_2026.md): downloaded official transcripts, YouTube captions, media transcriptions and explicit Caixa coverage gaps.
- [Six bank specialists](specialists/START_HERE.md): reusable specialist packages and separate persistent knowledge bases.

Current comparisons default to the latest available quarter. The detailed call memories are thematic reviews, not a word-by-word audit or complete bank guides.

## Download the complete archive

This repository uses **Git LFS** for PDFs, spreadsheets, recordings and other large binary files. Install Git LFS before cloning, then run:

```sh
git lfs install
git clone https://github.com/franciscoljr/analise-resultados-bancos.git
cd analise-resultados-bancos
git lfs pull
python3 -m pip install -r requirements.txt
```

A download without Git LFS may contain small pointer files instead of the original documents. The full workspace is approximately 3.1 GB. Original bank disclosures retain their source attribution; no license over those third-party materials is granted by this archive.

The analysis scripts generally resolve the project root from their own location. Specialist installation instructions and some media tools retain paths from the original macOS workspace: update those local paths before installing on another computer. Media transcription additionally requires FFmpeg, yt-dlp and MLX Whisper on a compatible Apple Silicon Mac; existing transcripts can be read without those tools.

## Files to use

- `reports/executive_comparison.md`: cross-bank scorecard, earnings evolution, income bridge and management interpretation.
- `reports/<Bank>.md`: bank-level metrics, historical series and source references.
- `reports/coverage.md`: quarter-by-quarter archive/data coverage and explicit limitations.
- `reports/methodology.md`: units, reporting breaks and comparison rules.
- `data/coverage_index.csv`: source inventory, including partial-run checkpoints where relevant.
- `data/index.csv`: latest completed main collector inventory.
- `data/driver_bridges.csv`: repeatable QoQ/YoY earnings-change decompositions with component sources and an explicit residual.
- `data/metric_dictionary.csv`: coverage, units, period basis and definitions for every bank-metric pair.
- `data/normalized.csv`: analysis-ready financial observations with row-level provenance.
- `data/validation.json`: file integrity and independent release-anchor checks.
- `data/pdf_versions.json`: Caixa comparative observations by source vintage.
- `data/sources.json` and `data/supplements.json`: reviewed official catalog configuration and supplementary links.

## Update when requested

There is no recurring automation. Ask Codex to “update this bank analysis with the latest official results.” The repeatable entry point is:

```sh
python3 scripts/update.py
```

It requires Python with `openpyxl` and `pypdf`, and `curl`. In this Codex workspace, the bundled Python is:

```sh
/Users/francisco/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/update.py
```

Normal incremental refresh discovers new catalog IDs/URLs and verifies existing local hashes before reusing files. To also fetch existing URLs again and detect in-place remote replacements, use `--refresh-existing`; changed bytes receive new filenames, preserving the old files. This costs additional download time.

Use `--offline` to rebuild analysis, validation and reports from the local archive without network access. `--workers 12` controls concurrent downloads. Do not run multiple full updates simultaneously; the entry point takes a workspace lock. The initial historical backfill uses separate checkpoints.

After an update, inspect `data/update_status.json`. A nonzero exit indicates download gaps, mapping failures, stale bank series or validation failures. Do not treat incomplete output as a completed update. Catalog snapshots and prior final indexes are retained under `data/catalogs/<timestamp>/`.

New source layouts require reviewed mapping changes in `data/mappings.json`. `scripts/make_mappings.py` is a bootstrap for the audited 2Q26 workbook layout, not a generic schema-discovery engine; do not rebuild it blindly for a future release. The normal update uses the existing reviewed mapping and verifies the source row labels. Itaú's supplemental historical workbook link must be checked against the official page for each new quarter. Future narrative interpretation requires fresh source review; the 2Q26 interpretation is not silently reused for new quarters.

## Scope and reliability

The normalized series is a decision-support base, not a universal harmonization of different bank reporting models. Quarterly/YTD/trailing ratios, accounting/managerial/prudential scope, legacy/current rules, Stage 3/NPL90 coverage and narrow/broad funding remain distinguishable. Earlier documents are preserved, but a complete quantitative restatement bridge across all archived vintages is not yet implemented. See the coverage report for the actual archive and metric gaps rather than assuming every discovered record has finished downloading.
