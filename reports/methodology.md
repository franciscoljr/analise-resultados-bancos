# Metric definitions and comparison rules

The archive covers the six requested S1 banks and the official results-center categories recorded in `data/sources.json`, from 2024 through the latest disclosed quarter found in those catalogs. The collected material includes releases/performance analyses, BRGAAP and IFRS statements, presentations, historical spreadsheets, available risk/Pillar 3 material, transcripts and related results documents. Webcasts and audio are indexed as official links. Coverage is assessed against the discovered catalogs, not an assumed document count per quarter.

## Units, time and source hierarchy

All normalized monetary amounts are **BRL millions**. Percentage values are on a 0–100 scale: 12.5 means 12.5%, not 0.125. Expense metrics are positive burdens; the original signed value and multiplier remain in the data. Source workbooks take priority for precise series; PDFs supply explicitly labeled table values where needed. Original source files are immutable and named with a SHA-256 prefix.

Quarterly income is extracted only from an explicit quarter header or an exact three-month date range. Annual and YTD columns are excluded. No automatic subtraction of annual or half-year totals is used to manufacture missing quarters. Assets, loans, funding, equity, capital and NPL are end-of-period stocks/ratios. ROE and efficiency retain the source period basis: quarterly, annualized quarterly, YTD annualized or trailing 12 months.

The main normalized series uses the latest mapped workbook vintage, preserving any bank-published restatements. Earlier source files stay in the archive. This does **not** mean all earlier vintages have been reconciled numerically. Caixa comparative PDF versions are separately retained in `pdf_versions.json`. Differences between original and restated reporting are not automatically attributed to economic events.

## Definitions that must remain distinct

| Metric group | Comparison rule |
|---|---|
| Accounting profit | BRGAAP accounting profit is separate from managerial adjusted/recurring profit. IFRS statements are archived but IFRS profit is not substituted into the BRGAAP series. |
| Adjusted profit | A bank-defined measure. The gap to accounting profit can include goodwill, tax, provisions and other exclusions. Equal labels do not guarantee equal adjustments. |
| ROE | BB, Itaú, Santander and BTG mapped ratios are quarterly annualized. Bradesco’s mapped historical series is YTD annualized. Caixa is trailing 12 months. Santander excludes goodwill. Itaú consolidated and Brazil-only ROE differ. |
| NII and revenue | Net interest margins use each bank’s managerial allocations. BTG is analyzed by business-line revenue rather than forcing its revenue into retail-bank NII and fees. Insurance treatment also differs. |
| Credit costs | Positive expense burden. Expanded PDD, net credit cost and expected-loss expense may include different recoveries, discounts, guarantees or credit-like securities. These are not harmonized into a common regulatory loss rate. |
| Operating expenses | BB and Caixa administrative costs, Itaú non-interest costs, Santander general expenses and Bradesco broader operating costs are not identical perimeters. BTG reported expenses include goodwill amortization while adjusted efficiency excludes it. |
| Loans | Retain ordinary and expanded credit separately. Expanded credit can include guarantees and securities. BTG accounting loans differ from its corporate-plus-consumer business portfolio. |
| Funding | Customer/commercial funding and broad raised funds are distinct. Itaú’s currently labeled funding aggregate includes securities and borrowings; BTG also includes broader liability instruments. Avoid a cross-bank loan/deposit ratio from these mismatched totals. |
| Coverage | NPL90 coverage and Stage 3 coverage are different denominators. Santander’s current Stage 3 coverage is explicitly named `coverage_stage3`; it is not spliced into NPL90 coverage. |
| Capital | CET1 and total capital are prudential ratios. Capital is not measured on the same perimeter as every accounting or managerial balance sheet. No regulatory headroom is inferred without bank-specific requirements and buffers. |
| AuM/WuM | Client assets under management/wealth management are not bank balance-sheet assets. They can have overlapping service scopes and must not be added to bank assets. |

## Reporting breaks and current limitations

- **CMN 4,966 / 2025:** expected-credit-loss, write-off and presentation changes affect income and balances. Keep legacy 2024 and current 2025+ labels and methods. Do not describe a reported NPL change as purely economic without the bank’s transition analysis.
- **Banco do Brasil:** legacy Resolution 4,720 sheets coexist with the current presentation. Some raw cells are BRL displayed as millions; others are already millions or thousands. The unit conversion is explicit per mapping.
- **Bradesco:** historical labor-litigation expense has been reclassified. The historical ROE footnote specifies YTD recurring profit annualized. Its managerial and accounting balance-sheet totals differ; the selected balance-summary asset series is managerial consolidated.
- **Itaú:** the latest pro forma series includes managerial regroupings, credit-like securities and 2026 Avenue consolidation. Brazil and consolidated/LATAM ratios must not be mixed. The historical spreadsheet link is a reviewed supplement that must be refreshed for a new release.
- **Santander:** legacy 2024 income/balance tables use thousands where current managerial tables use millions. Certain historical ratios exclude extraordinary provisions, including BRL 1.930bn in 2Q24. The 2026 write-off criteria change also affects interpretation.
- **BTG:** Pan consolidation and comparative Consumer Finance & Banking adjustments require an organic-versus-scope bridge. The capital ratio refers to Banco BTG Pactual. No comparable NPL90 series has yet been normalized.
- **Caixa:** use explicit quarterly table columns; annual/YTD results coexist on the same page. ROE/efficiency are trailing 12 months. Deposits and total raised funds differ substantially.

Each row in `normalized.csv` retains bank, period, metric, value, unit, frequency, reporting basis, scope, method, original source label, URL, local file, sheet/cell or page/column, source vintage, SHA-256, original value and conversion factor. Missing observations remain missing.

## Interpretation and validation

The executive report distinguishes management statements (linked to the release) from analytical conclusions. Its income bridge is arithmetic: change in profit equals selected signed component changes plus an explicitly shown residual. It is not a full accounting reconciliation or proof of causation. The residual must not be described as unexplained operational performance.

Validation checks content hashes, PDF readability/page counts and ZIP integrity, plus independent headline anchors transcribed from official releases. It also checks provenance and obvious unit/sign errors. It is not an audit of the banks’ underlying accounts or every cell in every published workbook. The exact checked files and outcomes are in `data/validation.json`.
