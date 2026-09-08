import json,pathlib,openpyxl
ROOT=pathlib.Path(__file__).resolve().parents[1]; maps=[]
# Row identities are verified against the official workbook when this configuration is built.
def add(bank,sheet,header,items,basis='managerial_adjusted',method='',label_col=1):
 p=ROOT/next(d['path'] for d in json.loads((ROOT/'data/priority.json').read_text()) if d['bank']==bank and d.get('format')=='xlsx')
 w=cache.setdefault(str(p),openpyxl.load_workbook(p,data_only=True,read_only=True)) if str(p) not in cache else cache[str(p)]
 s=w[sheet]; rows={i:r for i,r in enumerate(s.iter_rows(max_row=350,max_col=min(s.max_column,180)),1)}
 for metric,row,unit,mult,frequency in items:
  lc=next(c for c in rows[row][:4] if isinstance(c.value,str) and c.value.strip())
  label=lc.value; actual_col=lc.column
  maps.append(dict(bank=bank,sheet=sheet,header_row=header,label_column=actual_col,label=str(label),row_hint=row,metric=metric,unit=unit,multiplier=mult,frequency=frequency,basis=basis,method=method))
def money(metric,row,mult=1):return(metric,row,'BRL_million',mult,'quarter')
def stock(metric,row,mult=1):return(metric,row,'BRL_million',mult,'end_of_period')
def pct(metric,row,mult=1,freq='end_of_period'):return(metric,row,'percent',mult,freq)
cache={}
add('Banco_do_Brasil','DRE com Realocações',4,[money('net_income_adjusted',33,1e-6),money('net_interest_income',6,1e-6),money('credit_cost',7,-1e-6),money('fees',13,1e-6),money('operating_expenses',14,-1e-6),money('personnel_expenses',15,-1e-6),money('other_operating_result',12,1e-6),money('pretax_income',29,1e-6)],method='CMN 4966 from 2025; BRL cells displayed in millions')
add('Banco_do_Brasil','DRE com Realocações (Res. 4720)',4,[money('net_income_adjusted',54,1e-6),money('net_interest_income',20,1e-6),money('credit_cost',21,-1e-6),money('fees',27,1e-6)],method='Legacy 4720 presentation, discontinued after 2024; credit cost definition differs')
add('Banco_do_Brasil','Despesas Administrativas',4,[money('operating_expenses',6,-1e-6)],method='Expenses include personnel and other administrative costs')
add('Banco_do_Brasil','Desempenho e Eficiência',4,[pct('roe_adjusted',9,1,'quarter_annualized'),pct('roe_accounting',7,1,'quarter_annualized'),pct('efficiency',11,1,'trailing_12m')])
add('Banco_do_Brasil','Carteira de Crédito',4,[stock('loans',6),stock('loans_expanded',18),stock('loans_individuals',8),stock('loans_corporate',9),stock('loans_agriculture',13)],basis='managerial_balance',method='PF and PJ exclude separately classified agribusiness')
add('Banco_do_Brasil','Índices de Atraso',4,[pct('npl90',9),pct('coverage_npl90',24),stock('credit_allowance',22),money('new_npl',27)],basis='managerial_credit',method='CMN 4966 affects write-off and expected-loss accounting from 2025')
add('Banco_do_Brasil','Índice de Basileia',4,[pct('capital_total',56,100),pct('cet1',55,100)],basis='prudential')
add('Banco_do_Brasil','Fontes e Usos',4,[stock('customer_funding',7,1e-6)],basis='managerial_balance',method='Commercial funding: deposits and selected securities; excludes institutional funding')
add('Banco_do_Brasil','BP - Ativo',4,[stock('assets',6,1e-6)],basis='accounting_consolidated')
add('Banco_do_Brasil','BP - Ativo (Res. 4720)',4,[stock('assets',6,1e-6)],basis='accounting_consolidated',method='Legacy 4720 balance presentation')
add('Itau','Sumário_PRO FORMA',2,[money('net_income_adjusted',4),money('revenue',5),money('net_interest_income',6),pct('roe_adjusted',8,100,'quarter_annualized'),pct('npl90',10,100),pct('efficiency',13,100,'quarter'),pct('capital_total',22,100),stock('assets',24),stock('loans_expanded',25),stock('funding_broad',26),stock('equity',28)],basis='managerial_pro_forma',method='Consolidated including LATAM; pro forma series; Avenue consolidated from 2026; assets/equity adopt CMN 4966 prospectively; broad funding includes securities and borrowings',label_col=2)
add('Itau','DRE_MF_PRO FORMA',5,[money('credit_cost',10,-1),money('fees',18),money('operating_expenses',20,-1),money('nii_clients',8),money('nii_market',9),money('pretax_income',23)],basis='managerial_pro_forma',method='Expected-loss expense includes credit-like securities; prior impairment regrouped')
add('BTG_Pactual','InputSite_Highlights',3,[money('revenue',7),money('operating_expenses',9,-1),money('net_income_accounting',16),money('net_income_adjusted',17),stock('equity',23),stock('assets',25),pct('roe_accounting',31,100,'quarter_annualized'),pct('roe_adjusted',32,100,'quarter_annualized'),pct('efficiency',35,100,'quarter'),pct('capital_total',44,100),stock('loans',51),stock('funding_broad',63),stock('aum',39,1000),stock('wum',40,1000)],method='BTG consolidated; Banco Pan fully consolidated from 1Q26 and comparative business-line results adjusted for Consumer Finance & Banking; 4Q24 balance pro forma CMN 4966. Capital ratio applies to Banco BTG Pactual')
# Bradesco legacy and current income statements have different line layouts.
add('Bradesco','4- DRE Recorrente',7,[money('net_income_adjusted',33),money('net_interest_income',10),money('nii_clients',11),money('nii_market',12),money('credit_cost',14,-1),money('fees',19),money('operating_expenses',20,-1),money('personnel_expenses',21,-1),money('insurance_result',18)],method='CMN 4966 from 2025; operating expenses include other net operating income/expenses')
add('Bradesco','DRE Recorrente',7,[money('net_income_adjusted',39),money('net_interest_income',10),money('nii_clients',11),money('nii_market',12),money('credit_cost',14,-1),money('fees',23),money('operating_expenses',25,-1),money('personnel_expenses',26,-1),money('insurance_result',22)],method='Legacy through 2024; labor litigation reclassified into other operating expenses for all historical periods')
add('Bradesco','27- Índice de Desempenho',7,[pct('roe_adjusted',15,1,'ytd_annualized'),pct('capital_total',17),pct('efficiency',20,1,'trailing_12m')],method='ROE footnote specifies accumulated net income in year, annualized; efficiency rolling 12 months')
add('Bradesco','31- Carteira Crédito Indicador ',7,[pct('npl90',10),pct('coverage_npl90',11)],method='NPL loan denominator; coverage uses expanded overdue exposure')
add('Bradesco','13- Carteira Expandida ',7,[stock('loans_expanded',32),stock('loans_individuals',10),stock('loans_corporate',20)],basis='managerial_balance')
add('Bradesco','17- Rec. Captados e Administ.',7,[stock('funding_broad',10)],basis='managerial_balance',method='Broad raised funds includes insurance technical provisions, repos and own capital; not customer deposits')
add('Santander','Sumário Executivo',8,[pct('roe_adjusted',11,100,'quarter_annualized'),pct('efficiency',13,100,'quarter'),pct('npl90',15,100),pct('coverage_stage3',16,100),stock('assets',18),stock('loans_expanded',19),stock('customer_funding',20),stock('equity',21),pct('capital_total',22,100),pct('cet1',23,100)],method='ROAE excludes goodwill; coverage is Stage 3 rather than NPL90',label_col=3)
add('Santander','DRE Gerencial',8,[money('net_income_adjusted',35),money('net_interest_income',10),money('nii_clients',11),money('nii_market',12),money('fees',13),money('revenue',14),money('credit_cost',16,-1),money('operating_expenses',19,-1),money('pretax_income',30)],label_col=2,method='Managerial recurring result; CMN 4966 from 2025')
add('Santander','DRE Gerencial 2023 a 2024',8,[money('net_income_adjusted',29,.001),money('net_interest_income',10,.001),money('nii_clients',11,.001),money('nii_market',12,.001),money('fees',13,.001),money('revenue',14,.001),money('credit_cost',15,-.001),money('operating_expenses',18,-.001),money('pretax_income',26,.001)],label_col=2,method='Legacy discontinued series in BRL thousands; includes 2024 reclassification')
add('Santander','Indicadores Ger. 2023 a 2024',8,[pct('roe_adjusted',10,100,'quarter_annualized'),pct('efficiency',11,100,'quarter'),pct('npl90',17,100),pct('coverage_npl90',19,100)],label_col=2,method='Legacy ratios exclude specified extraordinary provisions, including BRL 1,930m in 2Q24')
add('Bradesco','BP - Dados Selecionados',7,[stock('loans_expanded',16),stock('deposits',18)],basis='managerial_balance',method='Legacy through 2024')
add('Bradesco','Carteira Crédito - Indicadores',7,[pct('npl90',36),pct('coverage_npl90',37)],method='Legacy through 2024')
add('Bradesco','1- BP - Dados Selecionados ',7,[stock('assets',10),stock('equity',28)],basis='managerial_consolidated',method='Managerial consolidated asset total differs from accounting consolidated total')
add('Santander','Balanço Patrimonial até 2024',8,[stock('assets',69,.001),stock('equity',121,.001)],basis='accounting_consolidated',method='Legacy BRL thousands')
add('Santander','Crédito_Segmento 2014 a 2024',8,[stock('loans',15),stock('loans_expanded',19)],basis='managerial_balance',method='Expanded credit includes guarantees')
add('Santander','Captações até 2024',8,[stock('funding_broad',21,.001)],basis='managerial_balance',method='Legacy broad funding BRL thousands')
add('Banco_do_Brasil','DRE Societária',4,[money('net_income_accounting',40,.001)],basis='accounting_consolidated')
add('Banco_do_Brasil','DRE com Realocações (Res. 4720)',4,[money('net_income_accounting',56,1e-6)],basis='accounting_consolidated',method='Legacy accounting profit shown in managerial reconciliation')
add('Banco_do_Brasil','BP - Passivo',4,[stock('equity',21,1e-6)],basis='accounting_consolidated')
add('Bradesco','7- DRE Contábil',7,[money('net_income_accounting',40)],basis='accounting_consolidated')
add('Itau','BRGAAP - DRE',1,[money('net_income_accounting',39)],basis='accounting_consolidated')
add('Santander','DRE Contábil',8,[money('net_income_accounting',51)],basis='accounting_consolidated')
add('BTG_Pactual','InputSite_RegulatoryCapital',3,[stock('rwa',24),stock('cet1_amount',29)],basis='prudential')
(ROOT/'data/mappings.json').write_text(json.dumps(maps,ensure_ascii=False,indent=2));print(len(maps),'mappings')
