from pathlib import Path
import json,csv,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
JOB=ROOT/'10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L01/reel/lunch_outing_v1'
p=OUT/'A1_still_receipt.json';d=json.loads(p.read_text(encoding='utf-8'));selected=next(r for r in d['candidates'] if r['version']=='v2')
assert hashlib.sha256((ROOT/selected['file']).read_bytes()).hexdigest()==selected['sha256']
approval={'date':'2026-10-13','user_quote':'可以，沿用修正版','question_context':'Explicit reply identifying second displayed M03 L01 walk-start v2 for lunch-outing A1.','file':selected['file'],'sha256':selected['sha256'],'scope':'Only this exact still as A1 source and L01 outfit/scene lock. No approval of A2, motion or whole film.'}
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save(OUT/'A1_user_approval_2026-10-13.json',approval);save(JOB/'A1_user_approval_2026-10-13.json',approval)
d['status']='A1_v2_user_approved';d['user_visual_approval']=approval;selected['status']='user_visual_approved';selected['user_approval']=approval
save(p,d);save(JOB/'A1_generation_receipt.json',d)
p=JOB/'review_sheet.csv'
with p.open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f));fields=list(r[0])
for row in r:
 if row['file']==approval['file']:row['status']='user_visual_approved';row['user_approval']=approval['user_quote']
with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(r)
p=OUT/'storyboard_candidate.json';d=json.loads(p.read_text(encoding='utf-8'));d['status']='A1_approved_A2_still_preparing';d['a1_approval']=approval;d['next_action']='Generate A2 seated candidate from approved A1 and face/full anchors; independently animate exact approved A1. A2 must be visually approved before Grok.';save(p,d)
print('Exact A1 v2 user approval recorded; A2 and film approvals remain separate.')
