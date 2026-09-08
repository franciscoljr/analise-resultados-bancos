import json,pathlib,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
for bank in json.loads((ROOT/'specialists/profiles.json').read_text()):
 p=ROOT/'specialists/packages'/bank['skill'];(p/'references').mkdir(parents=True,exist_ok=True);(p/'agents').mkdir(exist_ok=True)
 desc=f"Analyze {bank['name']} for a CEO/CFO: longitudinal strategy, financial statements, products/clients, earnings calls and risk; create or update its complete evidence-backed bank guide."
 body=f'''---
name: {bank['skill']}
description: {json.dumps(desc,ensure_ascii=False)}
---

# {bank['name']} specialist

You are the dedicated analytical specialist for **{bank['name']}**, bank ID `{bank['id']}`. Serve CEO/CFO decisions with a longitudinal, evidence-backed understanding of this bank. Adapt depth to the request. A full-guide request requires the complete guide workflow; a focused question does not require regenerating the entire guide.

Read [analytical protocol](references/analytical_protocol.md) and [bank focus](references/bank_focus.md). Use [data access](references/data_access.md) to retrieve original disclosures, precise metrics and calls. For a complete guide, read [guide contract](references/guide_contract.md).

Project: `/Users/francisco/Documents/GPT/Analise Bancos`. Build the bank's current evidence pack with `scripts/specialist_evidence.py pack --bank {bank['id']}` using the Python described in data access. Read prior reviewed knowledge under `specialists/knowledge/{bank['id']}/` when present; an evidence inventory or earlier assistant report is not a verified conclusion.

Explain where earnings, funding and cash came from and went as separate mechanisms. Connect strategy and client/product economics to execution, results, capital and risk. Reconcile management's call narrative with subsequent financial evidence and alternative explanations. Assess strengths and weaknesses at the relevant franchise level. Preserve original source locators and distinguish facts, management assertions, calculations and inference.

Work in this bank's knowledge directory. For peer comparisons use compatible definitions and label peer evidence explicitly. Do not create other tasks, delegate work or schedule runs merely because this specialist was invoked. The user's instructions take precedence over this skill.
'''
 (p/'SKILL.md').write_text(body)
 for src in (ROOT/'specialists/shared').glob('*.md'):shutil.copy2(src,p/'references'/src.name)
 focus='# '+bank['name']+' — investigative lens\n\nThese are questions to investigate, not predetermined findings or permanent judgments. Update the analysis as the evidence changes.\n\n## Franchise questions\n\n'+'\n'.join('- '+t for t in bank['focus'])+'\n\n## Known data traps\n\n'+'\n'.join('- '+t for t in bank['traps'])+'\n'
 (p/'references/bank_focus.md').write_text(focus)
 prompt=f"Use ${bank['skill']} to create the complete CEO/CFO guide to {bank['name']} from 2024 through the latest verified quarter, integrating financial statements and earnings calls."
 ui='interface:\n  display_name: '+json.dumps(bank['name']+' specialist',ensure_ascii=False)+'\n  short_description: "CEO/CFO strategy, financials, calls and risk"\n  default_prompt: '+json.dumps(prompt,ensure_ascii=False)+'\npolicy:\n  allow_implicit_invocation: true\n'
 (p/'agents/openai.yaml').write_text(ui)
 print(p)
