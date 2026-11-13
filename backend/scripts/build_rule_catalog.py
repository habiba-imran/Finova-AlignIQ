"""Extract the complete corrected/audit catalog, not the unapproved legacy triggers."""
import json
from hashlib import sha256
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
spec=ROOT/'docs/FINOVA_RULE_ENGINE_V2_AUDIT_CORRECTED.md'
audit=ROOT/'docs/Orthodontic_TMT_Independent_Critical_Audit(2).md'
text=spec.read_text(encoding='utf-8'); audit_text=audit.read_text(encoding='utf-8')


def clean(value):
    value=re.sub(r'Finova AlignIQ\s*\|\s*Working specification\s*\|\s*13 Nov 2026','',value)
    value=re.sub(r'\*\*FINOVA.*?SPECIFICATIONS\*\*','',value)
    return ' '.join(value.replace('<br>',' ').replace('**','').replace('_','').split())


cards=list(re.finditer(r'^#### \*\*([GDRTAHL]\d{2}) — (.*?)\*\*\s*$',text,re.M))
records=[]
for i,m in enumerate(cards):
    rid,title=m.groups(); body=text[m.end():cards[i+1].start() if i+1<len(cards) else text.index('## **F.')]
    disposition=re.search(r'\*\*Disposition:\*\* (READY|REVISE|VALIDATE|MORE DATA)',body)[1]
    dependence=re.search(r'\*\*TMT dependence:\*\* (Yes\*?|Metadata|Extra|System|Request|Partial|No)',body)[1]
    row=re.search(r'^\|'+rid+r'\|([^|]*)\|([^|]*)\|([^\n]*)',audit_text,re.M)
    if not row or row[1].strip()!=disposition: raise ValueError('AUDIT_DISPOSITION_MISMATCH:'+rid)
    original=body.split('**Original proposal (trace only):**',1)[1].split('**Audit-required implementation:**',1)[0]
    correction=body.split('**Audit-required implementation:**',1)[1].split('**Engineering migration:**',1)[0]
    migration=body.split('**Engineering migration:**',1)[1]
    refs=sorted(set(re.findall(r'S\d{2}',body.split('**Original proposal',1)[0])+re.findall(r'\bS\d{2}\b',row[3])))
    records.append(dict(rule_id=rid,source_title=clean(title),version='2.0.0',disposition=disposition,tmt_dependence=dependence,
        source_line=text[:m.start()].count('\n')+1,evidence_ids=refs,audit_required=clean(correction),
        audit_assessment=clean(row[3]).rstrip('|'),original_trace=clean(original),migration=clean(migration)))
section=text.split('## **F.',1)[1].split('## **G.',1)[0]
for m in re.finditer(r'\*\*(N\d{2}) — (.*?)\.\*\* ([^\n]+)',section):
    rid,title,correction=m.groups()
    records.append(dict(rule_id=rid,source_title=clean(title),version='2.0.0',disposition='ADDITIONAL',tmt_dependence='System',
        source_line=text[:text.index(m[0])].count('\n')+1,evidence_ids=[],audit_required=clean(correction),audit_assessment=clean(correction),
        original_trace='Additional safeguard, not one of the legacy 82 proposals.',migration=clean(correction)))
expected={f'{p}{i:02}' for p,n in [('G',18),('D',16),('R',16),('T',8),('A',6),('H',12),('L',6),('N',14)] for i in range(1,n+1)}
if {r['rule_id'] for r in records}!=expected or len(records)!=96: raise ValueError('INCOMPLETE_CATALOG')
output={'source_spec_sha256':sha256(spec.read_bytes()).hexdigest(),'source_audit_sha256':sha256(audit.read_bytes()).hexdigest(),
        'original_v1_document':'UNAVAILABLE_STANDALONE; v2 original-trace paragraphs only','rules':sorted(records,key=lambda r:r['rule_id'])}
(ROOT/'backend/app/review/catalog.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('CORRECTED_CATALOG: 96 exact IDs; audit dispositions checked; no clinical policy imported.')
