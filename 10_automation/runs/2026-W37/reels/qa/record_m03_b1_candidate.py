import csv,hashlib,json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[5]
reels=root/'10_automation/runs/2026-W37/reels'
folder=root/'10_automation/runs/2026-W37/generated_images/2026-W37-005/looks/2026-W37-005-L02/reel'
def rel(p):return str(p.relative_to(root)).replace('\\','/')
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[folder/f'2026-W37-005-L02_M03_B1_full_start_candidate_v{v}.png' for v in [1,2]]
attempts=[]
for p,wall,status in zip(files,[43.8,46.5],['rejected_bag_color_too_caramel','candidate_pending_user_visual_approval']):
    with Image.open(p) as im:size=list(im.size)
    attempts.append(dict(path=rel(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),resolution=size,status=status,observed_tool_wall_seconds=wall))
record=dict(week_id='2026-W37',look_id='2026-W37-005-L02',model_profile_id='M03',shot_id='B1',date='2026-10-01',status='candidate_pending_user_visual_approval',tool='built-in image_gen',prompt_path=rel(reels/'prompts/M03_B1_L02_start_v1.md'),correction_prompt_path=rel(reels/'prompts/M03_B1_L02_bag_color_correction_v2.md'),identity_references=['02_brand/reference_models/M03_start_v3_face.png','02_brand/reference_models/M03_start_v3_full.png'],scene_reference='10_automation/runs/2026-W37/generated_images/2026-W37-005/looks/2026-W37-005-L01/reel/2026-W37-005-L01_M03_A1_full_start_candidate_v2.png',selected_path=rel(files[1]),attempts=attempts,assistant_review=dict(framing='Native941x1672 vertical, complete hair and both black closed flats with step room. Same near-frontal identity and cafe perspective as approved A1.',wardrobe='Plain light-blue short-sleeve collared shirt dress, same-fabric tied belt, calf-length A-line hem; small dark chocolate-brown suede bag at viewer-right waist after one color correction.',open_detail='Silver ear decoration reads as a small loop rather than a strict stud. User must see and accept this variation before locking the look.',scene='Cafe window on left, warm-gray wall, wood bench and paving retained. No physical first/last-frame continuity assumption.'),user_approval=None,grok_submitted=False,publishable=False,time=dict(active_minutes=None,generation_wait_minutes=None,observed_tool_wall_seconds_total=90.3,notes='Tool wall includes orchestration; not measured active or pure generation time.'))
save(folder/'B1_full_start_generation_v2.json',record)
p=folder/'review_sheet.csv'
with p.open(encoding='utf-8-sig',newline='') as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
rows[0].update(candidate_file=files[1].name,tool='built-in image_gen',publishable='pending',status='candidate_pending_user_visual_approval',notes='Full native vertical view reviewed; bag v1 color rejected, v2 corrected. Silver ear decoration reads small loop, not strict stud: user review pending. No motion yet.')
with p.open('w',encoding='utf-8',newline='') as f:writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
p=reels/'production_manifest.json';manifest=json.loads(p.read_text(encoding='utf-8-sig'));m=next(x for x in manifest['reels'] if x['model_profile_id']=='M03')
m['status']='L01_transition_075s_accepted_L02_B1_candidate_pending_approval'
v=next(x for x in m['views'] if x['slot_id']=='2026-W37-005-L02_full')
v.update(source_path=rel(files[1]),source_type='native_vertical_still',approval='candidate_pending_user_visual_approval',framing_review='Full hair and both shoes; native941x1672',clarity_review=record['assistant_review']['wardrobe'],review_record_path=rel(folder/'B1_full_start_generation_v2.json'))
for s in m['storyboard']:
    if s['shot_id']=='B1':s['status']='still_candidate_pending_user_visual_approval'
save(p,manifest)
print('M03 B1 candidate saved; visual approval and B2/motion pending.')
