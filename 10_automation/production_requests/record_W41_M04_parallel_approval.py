"""Bound user ok to exact displayed M04 v2 pair and static parallel layout."""
import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
week=ROOT/'10_automation/runs/2026-W41';work=week/'reels/M04'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
review=read(work/'parallel_first_frame_static_review_2026-10-08.json')
for r in review['sources']:
    p=ROOT/r['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
receipt=dict(user_quote='ok',scope='M04 exact two selectedv2 native full-person starting stills and displayed static side-by-side layout. No video approval inferred.',sources=review['sources'],layout=review['layout']['output'],approved_date='2026-10-08',video_user_approval=None)
p=work/'parallel_first_frame_user_approval_2026-10-08.json'
if p.exists():raise FileExistsError('Approval receipt already exists.')
write(p,receipt)
receipt_path=p.relative_to(ROOT).as_posix()
for r in review['sources']:
    p=(ROOT/r['path']).with_name('review_sheet.csv')
    with p.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f));fields=list(rows[0])
    rows[0].update(publishable='yes',status='user_approved_reel_first_frame_only',notes=rows[0]['notes']+' Userok bounds approvedv2 static first frame only; film/proof/Carousel remain separate.')
    with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
p=week/'reels/production_manifest.json';m=read(p);r=next(x for x in m['reels'] if x['model_profile_id']=='M04')
r['status']='parallel_first_frame_pair_user_approved_video_generation_next';r['static_user_approval']=receipt_path
for v in r['static_first_frame_candidates']:v.update(status='user_approved_reel_first_frame_only',user_approval=receipt_path)
write(p,m)
p=week/'reels/batch_storyboard.json';s=read(p);r=next(x for x in s['films'] if x['reel_id']=='2026-W41-M04-reel');r['first_frame_user_approval']=receipt_path;r['output_status']='first_frame_pair_approved_video_generation_next';write(p,s)
p=ROOT/'10_automation/production_requests/2026-10-08_next_five_reels.json';req=read(p);r=next(x for x in req['slots'] if x['model']=='M04');r.update(status='parallel_first_frame_pair_user_approved_video_generation_next',still_user_approval=receipt_path);write(p,req)
p=week/'publishing_structure.md';s=p.read_text(encoding='utf-8');s=s.replace('待使用者視覺核准後才送Grok；第一套','使用者已回覆ok核准兩張起始圖與左右構圖，接續分別送Grok；第一套');p.write_text(s,encoding='utf-8')
p=ROOT/'CURRENT_STATUS.md';s=p.read_text(encoding='utf-8');entry='''## W41 M04 exact v2 pair and parallel layout approved — 2026-10-08

Userok directly answers the displayed left/right first-frame pair. Bothv2 hashes verified; bounded static approval saved in `10_automation/runs/2026-W41/reels/M04/parallel_first_frame_user_approval_2026-10-08.json`. Proceed separate animations with actual M04 identity reference, own first frames, ordinary-speed same-side strap contact; A starts left hand in pocket and extracts it naturally. Then verify moving hand/bag/scene integrity and complete-person panel bounds/scale. No M04 film approval or completed proof/Carousel inferred; M03/M05 film approvals remain pending. Previous batch preserved.

''';p.write_text(s.replace('# Current Status - Mira AI Fashion Creator\n\n','# Current Status - Mira AI Fashion Creator\n\n'+entry,1),encoding='utf-8')
print('M04 exact static pair and layout approval recorded.')
