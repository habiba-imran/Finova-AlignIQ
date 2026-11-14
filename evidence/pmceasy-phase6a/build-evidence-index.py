"""Research artifact checks only. No application imports, network or clinical fixtures."""
from hashlib import sha256
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

# Human annotations of the native captures, not OCR or algorithm reconstruction.
annotations = {
    ('iEMJeuOXkq4',150): ('External CAD context','Plan inspection','Dental model and plan/history controls; no PMCEASY output.','No target algorithm or automatic integration can be inferred.'),
    ('iEMJeuOXkq4',180): ('External CAD context','Plan inspection','Another external dental-model/plan view; no PMCEASY output.','Context only, not a new target feature.'),
    ('iEMJeuOXkq4',200): ('Module menu','Tool selection','Adult/growing branches, ordered module links and attachment timing guidance.','Recorded availability is not present-day availability; eligibility logic unknown.'),
    ('iEMJeuOXkq4',210): ('Attachment Interface','Intake and preview','Populated multiline area, display action and rendered TMT.','Clipboard bytes, accepted grammar, source version and semantic mappings unknown.'),
    ('iEMJeuOXkq4',220): ('Attachment Interface','Output','Tooth-indexed rows with geometry/placement labels, named alternatives and absence entries.','No 3D companion renderer, actual-plan input or clinical validity established.'),
    ('iEMJeuOXkq4',240): ('Attachment Interface','Output continuation','Further tooth-indexed option/absence rows.','Literal tooth tokens do not verify notation or indication logic.'),
    ('iEMJeuOXkq4',280): ('Sequencer','Tool selection','Final-pass guidance, adult entry and unavailable growing branch in recording.','Current availability and patient classification unobserved.'),
    ('iEMJeuOXkq4',300): ('Sequencer','Output','Arch/segment strategy rows and anchorage notes.','No numbered stage schedule or proven collision/force model visible; numbers not clinical policies.'),
    ('iEMJeuOXkq4',330): ('Sequencer','Output continuation','Separate lower-arch and right/left anchorage sections, including auxiliary and negative-need assertions.','Off-screen clinical inputs, justification and safety unknown.'),
    ('1GHKNwNkL6Q',90): ('Planning Assistant','Navigation','First-modification menu with assistant and dimensional/manual content links.','Review pass is not an aligner stage; current live selectors unobserved.'),
    ('1GHKNwNkL6Q',100): ('Planning Assistant','Preview and run','Tooth-column/movement-row table and assistant action.','No original clipboard bytes, general parser coverage or verified semantic convention established.'),
    ('1GHKNwNkL6Q',120): ('Planning Assistant','Output','Three dimensional rows with localized CAD-change requests and one predictability reassurance.','Example amounts are not approved rules; hidden context and algorithm unknown.'),
    ('1GHKNwNkL6Q',150): ('External CAD communication','Transfer destination','CAD comment field contains matching earlier output wording; movement table visible.','Transfer mechanism and any clinician edits unobserved; no API/extension inferred.'),
    ('1GHKNwNkL6Q',240): ('External CAD context','Manual plan work','External tooth/feature/plan controls and model, not a PMCEASY analysis view.','Cannot attribute CAD geometry or editing capabilities to the companion.'),
    ('1GHKNwNkL6Q',330): ('Attachment Interface plus external CAD','Review/application context','Companion option table/action beside a separate CAD model/comment field.','Window coexistence does not establish shared geometry, automatic placement or integration.'),
}

frames = []
manifest_paths = [HERE/'videos'/name for name in ('observation-manifest.json','observation-manifest-followup.json','observation-manifest-intake.json')]
for manifest_path in manifest_paths:
    for record in read(manifest_path)['records']:
        for frame in record['frames']:
            if 'path' not in frame:
                continue
            expected = 399.581 if record['id']=='iEMJeuOXkq4' else 371.601
            assert abs(record['playback']['duration']-expected)<2, 'WRONG_MEDIA_IDENTITY'
            assert abs(frame['decoded_media_seconds']-frame['requested_seconds'])<2, 'UNVERIFIED_FRAME_TIME'
            path = HERE/frame['path']
            assert path.is_file(), 'MISSING_CAPTURE'
            module,step,visible,unknown = annotations[(record['id'],frame['requested_seconds'])]
            frames.append(dict(
                evidence_kind='PUBLIC_DEMO_FRAME_NOT_LIVE_PRODUCT',path=frame['path'],
                sha256=sha256(path.read_bytes()).hexdigest(),
                public_source_url=f"https://www.youtube.com/watch?v={record['id']}&t={frame['requested_seconds']}s",
                decoded_media_seconds=frame['decoded_media_seconds'],module=module,workflow_step=step,
                visible_inputs_outputs_controls=visible,
                legible_text='Only limited excerpts are transcribed in PMCEASY_FUNCTIONAL_RESEARCH_REPORT.md; no hidden/cut-off text reconstructed.',
                reasonable_inference='The published recording displayed this surface; no independent product execution or clinical validation follows.',
                cannot_establish=unknown,source_manifest=f'videos/{manifest_path.name}',
                privacy_review='Manually reviewed; native crop excludes browser URL/profile/account header. No patient/account identifiers transcribed. Public tooth tokens/models remain demonstration material.'
            ))

assert len(frames)==15 and len({x['path'] for x in frames})==15
saved_pngs={str(p.relative_to(HERE)).replace('\\','/') for p in (HERE/'videos').glob('*.png')}
assert saved_pngs=={x['path'] for x in frames}, 'UNREGISTERED_OR_EXCLUDED_VIDEO_CAPTURE'
public = read(HERE/'public-capture-manifest.json')
roles = {
    'S01-tmt':('Shared TMT','External table copy'),
    'S02-planning-input':('Planning Assistant','Intake'),
    'S03-planning-comments':('Planning Assistant','Output'),
    'S04-functional':('Functional-treatment promotion','Feature illustration'),
    'S05-attachment-input':('Attachment Interface','Intake'),
    'S06-attachment-output':('Attachment Interface','Output'),
    'S07-sequencer-input':('Sequencer','Intake'),
    'S08-sequencer-output':('Sequencer','Output'),
}
assets=[]
for asset in public['images']:
    module,step=roles[asset['id']]
    assets.append(dict(evidence_id=asset['id'],public_source_url=asset['url'],module=module,workflow_step=step,
        retrieval_status='UNOBSERVED_ASSET_RETRIEVAL_FAILED',diagnostic=asset.get('status'),
        visible_inputs='UNOBSERVED',visible_outputs='UNOBSERVED',controls_ui='UNOBSERVED',legible_text='NONE',
        reasonable_inference='Role inferred only from the official page caption, not image pixels.',
        cannot_establish='Any cell, label, numerical value, control, geometry or behavior within this missing original.'))
assert len(assets)==8
(HERE/'screenshot-observation-register.json').write_text(json.dumps(dict(date='2026-11-14 Asia/Karachi',original_homepage_assets=assets,public_demo_frames=frames),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

reports=[ROOT/name for name in ('PMCEASY_FUNCTIONAL_RESEARCH_REPORT.md','PMCEASY_FEATURE_GAP_MATRIX.md','PMCEASY_RECONSTRUCTION_ROADMAP.md')]
broken=[]
for path in reports:
    text=path.read_text(encoding='utf-8')
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if link.startswith(('https://','http://','#')):
            continue
        target=path.parent/link.split('#',1)[0]
        if not target.exists():
            broken.append(dict(report=path.name,target=link))
assert not broken, broken
matrix=reports[1].read_text(encoding='utf-8')
for i in range(1,24):
    section=matrix.split(f'### GAP{i:02} —',1)[1].split('\n### ',1)[0]
    assert all(re.search(rf'^{n}\. ',section,re.M) for n in range(1,9)),f'INCOMPLETE_GAP_{i}'

inventory=read(HERE/'finova-document-source-inventory.json')
source_checks=[]
def source_records(value):
    if isinstance(value,dict):
        if 'path' in value and 'sha256_bytes' in value:
            yield value
        for child in value.values():
            yield from source_records(child)
    elif isinstance(value,list):
        for child in value:
            yield from source_records(child)
for record in source_records(inventory):
    relative=record['path'].replace('\\','/')
    if not relative.startswith(('backend/app/','frontend/src/','schemas/')):
        continue
    path=(ROOT/relative).resolve()
    assert path.is_relative_to(ROOT.resolve())
    same=sha256(path.read_bytes()).hexdigest()==record['sha256_bytes']
    source_checks.append(dict(path=relative,unchanged=same))
assert source_checks and all(x['unchanged'] for x in source_checks), 'APPLICATION_SOURCE_DRIFT'

check=dict(date='2026-11-14 Asia/Karachi',reports=len(reports),gap_cards=23,required_fields_per_gap=8,
    retained_verified_video_frames=len(frames),unavailable_original_screenshots=len(assets),broken_local_report_links=broken,
    application_source_snapshot_checks=source_checks,
    new_full_test_suite_run=False,new_http_browser_test_success_claim=False,provider_calls_from_local_probes=0,
    note='Artifact/identity/link/completeness checks and source snapshot comparison, not clinical validation or a full application test suite.')
(HERE/'research-artifact-validation.json').write_text(json.dumps(check,indent=2)+'\n',encoding='utf-8')
files=[dict(path=str(p.relative_to(HERE)).replace('\\','/'),bytes=p.stat().st_size,sha256=sha256(p.read_bytes()).hexdigest())
    for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='evidence-files.json' and '__pycache__' not in p.parts]
(HERE/'evidence-files.json').write_text(json.dumps(dict(date='2026-11-14',files=files),indent=2)+'\n',encoding='utf-8')
print(f'RESEARCH_ARTIFACTS_OK: 3 reports; 23 complete gap cards; {len(frames)} verified frames; 8 unavailable originals; {len(source_checks)} unchanged source snapshots; no broken local report links')
