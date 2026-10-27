import csv,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[2];base=root/'10_automation/runs/2026-W41'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=base/'reels/M03_full_pair_user_approval_2026-10-08.json'
if target.exists():raise SystemExit('Already recorded.')
sources=read(base/'reels/M03_full_pair_static_review_2026-10-08.json')['selected_sources']
for rec in sources:assert hashlib.sha256((root/rec['file']).read_bytes()).hexdigest()==rec['sha256']
approval=dict(date='2026-10-08',user_quote='兩張都可以，沿用',context='Explicit answer identifying M03 L01 v2 and L02 v1 full-person first frames.',sources=sources,scope='Only these exact full-person starting stills. No film/proof/Carousel approval.')
save(target,approval);rel=target.relative_to(root).as_posix()
p=base/'reels/production_manifest.json';manifest=read(p);entry=next(x for x in manifest['reels'] if x['model_profile_id']=='M03')
for rec in sources:
    view=next(x for x in entry['views'] if x['look_id']==rec['look_id'] and x['role']=='full')
    view.update(source_type='native_reel_approved_still',approval=dict(file=rec['file'],sha256=rec['sha256'],user_quote=approval['user_quote'],receipt=rel),framing_review='assistant_static_pass_user_approved',clarity_review='assistant_static_pass_user_approved')
    p=root/rec['file'];rp=p.parent/'review_sheet.csv'
    with rp.open(encoding='utf-8',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
    for row in rows:
        if row['candidate_file']==p.name:row.update(publishable='yes',status='user_approved_reel_first_frame',notes=row['notes']+' Explicit user still approval; video not approved.')
    with rp.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
entry['status']='two_full_first_frames_user_approved_video_generation_next';save(base/'reels/production_manifest.json',manifest)
p=root/'10_automation/production_requests/2026-10-08_next_five_reels.json';req=read(p);slot=next(x for x in req['slots'] if x['model']=='M03');slot['status']=entry['status'];save(p,req)
p=base/'publishing_structure.md';txt=p.read_text(encoding='utf-8');txt=txt.replace('待使用者逐張視覺核准後才送Grok','使用者已明確核准兩張，接續逐鏡Grok生成與驗收',1);p.write_text(txt,encoding='utf-8')
p=root/'CURRENT_STATUS.md';txt=p.read_text(encoding='utf-8');header='# Current Status - Mira AI Fashion Creator\n\n'
new='## W41 M03 exact first-frame pair approved; animate cuff contact — 2026-10-08\n\nUser explicitly approves both M03 full-person sources with `兩張都可以，沿用`. L01v2 and L02v1 hashes verified and bounded approval saved in W41 `reels/M03_full_pair_user_approval_2026-10-08.json`. Static-only approval; proof, Carousel and film remain unapproved/incomplete. Continue separate own-first-frame animations with actual saved identity selection, ordinary-speed cuff contact, fixed full-person framing and clean audio-off output; then check source hands/cloth and0.75s paired dissolve.\n\n'
p.write_text(header+new+txt[len(header):],encoding='utf-8');print('Exact M03 pair approval saved.')
