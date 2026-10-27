from pathlib import Path
import csv, json, hashlib
ROOT=Path(__file__).resolve().parents[2]; BASE=Path(__file__).resolve().parent
JOB=ROOT/'10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L02/reel/lunch_outing_v1'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=read(BASE/'B1_still_receipt.json'); c=d['candidates'][-1]
assert hashlib.sha256((ROOT/c['file']).read_bytes()).hexdigest()==c['sha256']
a={'date':'2026-10-13','user_quote':'可以，沿用最後這張','question_context':'Explicit reply identifying final M03 L02 B1v4 seated still: face/navy blazer/plain gray tee/cream trousers/black bag/crossed-leg pose for third shot.','file':c['file'],'sha256':c['sha256'],'scope':'Exact B1v4 still only; authorizes next Grok First frame. No motion or whole-film approval.'}
for p in [BASE/'B1_user_approval_2026-10-13.json',JOB/'B1_user_approval_2026-10-13.json']: save(p,a)
d.update(status='v4_user_visual_approved',user_approval=a);d['candidates'][-1]['status']='user_visual_approved'
for p in [BASE/'B1_still_receipt.json',JOB/'B1_generation_receipt.json']:save(p,d)
p=BASE/'B1_reference_plan.json';r=read(p);r.update(status='v4_user_visual_approved',user_approval=a);save(p,r)
sheet=JOB/'review_sheet.csv'
with sheet.open(encoding='utf-8-sig',newline='') as f:
 reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
for row in rows:
 if row['file']==c['file']:row['status']='user_visual_approved';row['notes']+=' Exact v4 user approval recorded; no dynamic pass inferred.'
with sheet.open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
prompt='''Use the selected Mira M03 v3 identity reference and only the exact approved seated First frame. Preserve her open navy lightweight blazer and once-folded cuffs, plain light-gray cotton crewneck tee, cream straight trousers, silver studs and black shoulder bag. Already seated with one leg crossed and hands resting near her knee and bench, she makes one small natural change of attention toward the walkway at image-right, then settles. The head turns only slightly, keeping a recognizable near-frontal face; no shoulder rotation or new hand gesture. Keep hands, crossed legs and bag supported in their original positions. Fixed camera and original head-through-knees framing, no push-in or zoom. Normal everyday movement. Preserve the bench, window frames, wall and left daylight without shifting their geometry. No standing up, outfit changes, ornamental textile patterns, added text or audio.'''
for p in [BASE/'B1_motion_prompt_v1.txt',JOB/'B1_motion_prompt_v1.txt']:p.write_text(prompt+'\n',encoding='utf-8')
p=BASE/'storyboard_candidate.json';s=read(p);s.update(status='all4_stills_approved_B1_motion_next',b1_approval=a,next_action='Animate exact B1v4 once with M03 saved identity/First frame, inspect source, then assemble separate four-shot two-look research trial using reviewed source intervals and0.75s dissolves.');save(p,s)
print('B1v4 exact visual approval saved; all four stills now approved. Motion prompt saved.')
