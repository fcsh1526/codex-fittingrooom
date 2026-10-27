"""Record the user's explicit contextual ok for the displayed M03 A1 correction."""
import csv,json
from pathlib import Path
root=Path(__file__).resolve().parents[5]
run=root/'10_automation/runs/2026-W37'
folder=run/'generated_images/2026-W37-005/looks/2026-W37-005-L01/reel'
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=folder/'A1_full_start_generation_v2.json'
d=load(p);d['status']='user_visual_approved_for_motion_2026-10-01';d['user_visual_approval']=dict(reply='ok',date='2026-10-01',scope='M03 A1 v2 displayed full still; permits same-look derivatives and motion, not video/style/publication approval')
d['history'][-1]['status']=d['status'];save(p,d)
p=run/'reels/production_manifest.json';m=load(p)
r=next(r for r in m['reels'] if r['model_profile_id']=='M03');r['status']='A1_user_approved_A2_detail_preparing'
v=next(v for v in r['views'] if v['look_id']=='2026-W37-005-L01' and v['role']=='full');v['approval']=d['status']
next(s for s in r['storyboard'] if s['shot_id']=='A1')['status']=d['status'];save(p,m)
p=folder/'review_sheet.csv'
with p.open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
for r in rows:
    if r['candidate_file'].endswith('A1_full_start_candidate_v2.png'):
        r['status']=d['status'];r['notes']+=' User replied ok to the displayed correction and visual approval question. No motion QA yet.'
with p.open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
for ref in ['M03_start_v3_face.png','M03_start_v3_full.png']:
    assert (root/'02_brand/reference_models'/ref).is_file()
print('M03 A1 v2 approval recorded; both approved identity files present.')
