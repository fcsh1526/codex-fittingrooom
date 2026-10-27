import csv,json
from pathlib import Path
root=Path(__file__).resolve().parents[5];reels=root/'10_automation/runs/2026-W37/reels'
folder=root/'10_automation/runs/2026-W37/generated_images/2026-W37-005/looks/2026-W37-005-L02/reel'
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=folder/'B1_full_start_generation_v2.json';d=json.loads(p.read_text(encoding='utf-8-sig'))
d['status']='user_visual_approved_for_derivatives_and_motion_2026-10-01'
d['user_approval']=dict(reply='ok',date='2026-10-01',scope='Displayed B1 v2 including explicitly disclosed small silver loop earrings; not video approval.')
d['assistant_review']['open_detail']='Silver small-loop earrings accepted by user after explicit disclosure; retain in derivatives.'
d['attempts'][1]['status']='user_visual_approved_for_derivatives_and_motion';save(p,d)
p=folder/'review_sheet.csv'
with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
rows[0].update(status='user_visual_approved_for_motion',publishable='pending',notes='User ok accepted full B1 v2 and disclosed small silver loop earrings. Motion QA remains separate.')
with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
p=reels/'production_manifest.json';d=json.loads(p.read_text(encoding='utf-8-sig'));m=next(x for x in d['reels'] if x['model_profile_id']=='M03')
m['status']='L02_B1_still_approved_B2_preparing_motion_preparing'
v=next(x for x in m['views'] if x['slot_id']=='2026-W37-005-L02_full');v['approval']='user_visual_approved_for_motion_2026-10-01'
v['approval_evidence']='User ok after full v2 preview and explicit loop-earring disclosure.'
for s in m['storyboard']:
    if s['shot_id']=='B1':s['status']='still_approved_motion_preparing'
save(p,d);print('B1 approved, including ear-decoration variation; motion approval pending.')
