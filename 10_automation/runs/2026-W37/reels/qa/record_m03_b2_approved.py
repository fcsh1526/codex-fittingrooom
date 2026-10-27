import hashlib,json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[5];reels=root/'10_automation/runs/2026-W37/reels'
folder=root/'10_automation/runs/2026-W37/generated_images/2026-W37-005/looks/2026-W37-005-L02/reel'
def rel(p):return str(p.relative_to(root)).replace('\\','/')
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
still=folder/'2026-W37-005-L02_M03_B2_detail_start_candidate_v1.png'
with Image.open(still) as im:size=list(im.size)
d=dict(week_id='2026-W37',look_id='2026-W37-005-L02',model_profile_id='M03',shot_id='B2',date='2026-10-01',status='user_visual_approved_for_motion',tool='built-in image_gen',selected_path=rel(still),sha256=hashlib.sha256(still.read_bytes()).hexdigest(),resolution=size,prompt_path=rel(reels/'prompts/M03_B2_L02_detail_start_v1.md'),references=[rel(folder/'2026-W37-005-L02_M03_B1_full_start_candidate_v2.png'),'10_automation/runs/2026-W37/generated_images/2026-W37-005/looks/2026-W37-005-L01/reel/2026-W37-005-L01_M03_A2_detail_start_candidate_v4.png'],assistant_review='No face/chin/mouth, collar/short sleeves, plain blue cloth, belt knot, complete chocolate-brown bag/strap and relaxed hands visible. Actual framing extends to below knees. Bag lies somewhat higher/smaller than A2; actual motion/edit matching remains unverified.',user_approval=dict(reply='可以，沿用這張',date='2026-10-01',scope='Displayed B2 v1 still only; no motion approval'),grok_submitted=False,time=dict(active_minutes=None,generation_wait_minutes=None,observed_tool_wall_seconds=48.4))
save(folder/'B2_detail_generation_v1.json',d)
p=reels/'production_manifest.json';manifest=json.loads(p.read_text(encoding='utf-8-sig'));m=next(x for x in manifest['reels'] if x['model_profile_id']=='M03')
m['status']='all_four_stills_approved_L02_motion_preparing'
v=next(x for x in m['views'] if x['slot_id']=='2026-W37-005-L02_proof')
v.update(source_path=rel(still),source_type='native_vertical_generated_detail',approval='user_visual_approved_for_motion_2026-10-01',framing_review='Faceless native941x1672 vertical, complete bag and belt knot; lower hem partly visible',clarity_review='Blue plain poplin and dark-brown bag panel visible',review_record_path=rel(folder/'B2_detail_generation_v1.json'))
for s in m['storyboard']:
    if s['shot_id']=='B2':s['status']='still_approved_motion_preparing'
save(p,manifest);print('B2 explicit approval recorded; both L02 motions authorized.')
