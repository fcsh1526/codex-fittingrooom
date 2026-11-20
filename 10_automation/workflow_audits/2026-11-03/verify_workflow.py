"""Read-only integrity checks for the reconciled Mira workflow and installed skills."""
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from urllib.parse import unquote

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
INSTALLED=Path('C:/Users/Brandon_ChangChien/.codex/skills')
VALIDATOR=INSTALLED/'.system/skill-creator/scripts/quick_validate.py'
spec=importlib.util.spec_from_file_location('skill_validation',VALIDATOR)
validation=importlib.util.module_from_spec(spec)
spec.loader.exec_module(validation)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

skills={}
for name in ['mira-reel-director','mira-image-daily']:
    source=ROOT/'11_skills'/name
    target=INSTALLED/name
    files=[p for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    entries=[]
    for p in files:
        relative=p.relative_to(source)
        dest=target/relative
        entries.append({'file':relative.as_posix(),'source_sha256':sha(p),
                        'installed_sha256':sha(dest) if dest.is_file() else None,
                        'match':dest.is_file() and sha(p)==sha(dest)})
    sv,sm=validation.validate_skill(source)
    tv,tm=validation.validate_skill(target)
    skills[name]={'source_validation':{'passed':sv,'message':sm},
      'installed_validation':{'passed':tv,'message':tm},'files':entries,
      'package_files_match':all(e['match'] for e in entries)}

docs=['AGENTS.md','CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md',
 '10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W44/publishing_structure.md',
 '09_sops/mira_reel_production_sop.md','09_sops/mira_reel_method_catalog.md',
 '11_skills/mira-reel-director/SKILL.md','11_skills/mira-reel-director/references/production-checkpoints.md',
 '11_skills/mira-reel-director/references/performance-and-reference.md',
 '11_skills/mira-image-daily/SKILL.md','11_skills/mira-image-daily/references/image-standard.md',
 '03_research/reel_method_growth_2026-10-29/QUEUE.md']
missing=[];checked=0
for relative in docs:
    p=ROOT/relative
    for raw in re.findall(r'\[[^\]]*\]\(([^\n)]+)\)',p.read_text(encoding='utf-8-sig')):
        raw=raw.strip().strip('<>')
        if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',raw) or raw.startswith('#'):continue
        raw=unquote(raw.split('#',1)[0])
        checked+=1
        if not (p.parent/raw).exists():missing.append({'document':relative,'target':raw})

archives=json.loads((ROOT/'10_automation/history/workflow_audit_2026-11-03_archives.json').read_text(encoding='utf-8-sig'))
archive_checks=[{'source':a['Source'],'archive':a['Archive'],
 'match':a['OriginalSHA256'].lower()==a['ArchiveSHA256'].lower()==sha(ROOT/a['Archive'])} for a in archives]
result={'date':'2026-11-03','scope':'Local workflow files and two installed Mira skill packages; not GitHub push or new media production.',
 'baseline_issue_fixed':'mira-image-daily had an unsupported frontmatter key; moved the viewer-first instruction into the body.',
 'skills':skills,'local_markdown_links':{'checked':checked,'missing':missing},
 'archives':archive_checks,'current_entry_lines':{r:len((ROOT/r).read_text(encoding='utf-8-sig').splitlines()) for r in docs[:5]},
 'W45_publishing_structure_exists':(ROOT/'10_automation/runs/2026-W45/publishing_structure.md').exists(),
 'manual_review_scope':['A/B preference is not publication or causal proof','A remains a plausible acting variant',
 'M01 duplicate review withdrawn without inventing a new publication approval','Historical W37 pause not reactivated',
 'Weekly inventory and one-model rule preserved','OpenMontage semantic and motion-repair limits explicit']}
result['passed']=not missing and all(a['match'] for a in archive_checks) and all(s['package_files_match'] and s['source_validation']['passed'] and s['installed_validation']['passed'] for s in skills.values())
(HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':result['passed'],'package_files':{n:len(s['files']) for n,s in skills.items()},
                 'links_checked':checked,'missing_links':missing,'archives_match':all(a['match'] for a in archive_checks)},ensure_ascii=False))
raise SystemExit(0 if result['passed'] else 1)
