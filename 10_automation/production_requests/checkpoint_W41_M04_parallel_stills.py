"""Static review and layout diagnostic; never approves stills or moving crop safety."""
import csv, hashlib, json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
week=ROOT/'10_automation/runs/2026-W41';work=week/'reels/M04'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[]
notes=[
 'L01v1 head margin below8%; single framing edit selectedv2. V2 full hair/shoes, complete outfit and cobalt bag clear. Actual left hand is in trouser pocket; animation must extract it naturally before same-side strap touch. No still approval inferred.',
 'L02v1 faint ornamental skirt surface; single material-only edit selectedv2 plain matte cotton. White shirt/black A-line calf skirt, cobalt bag, complete hair/shoes and coherent scene clear. No still approval inferred.'
]
for n, look in enumerate(['L01','L02']):
    lid=f'2026-W41-005-{look}'
    folder=week/f'generated_images/2026-W41-005/looks/{lid}/reel'
    source=folder/f'{lid}_M04_reel_candidate_A_v2.png'
    with Image.open(source) as im: size=im.size
    assert size==(941,1672)
    files.append(dict(look_id=lid,path=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),pixels=list(size),static_review=notes[n],status='candidate_pending_user_visual_approval',user_approval=None))
    p=folder/'review_sheet.csv'
    with p.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f)); fields=list(rows[0])
    row=rows[0];row.update(candidate_file=source.name,tool='Codex built-in imagegen',publishable='pending',status='candidate_pending_user_visual_approval',notes=notes[n])
    for key in ['model_consistency','body_proportion_consistency','reader_relatability','outfit_clarity','ai_realism','scene_lighting_integration','outfit_continuity','expression_liveliness','pose_variation','canva_frame_fit','commerce_value']:row[key]=4
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
canvas=Image.new('RGB',(720,1280),'#e8e2d9')
crop=(220,150,720,1535);panel=(352,975);y=152
for n,r in enumerate(files):
    with Image.open(ROOT/r['path']) as im:
        tile=im.crop(crop).convert('RGB').resize(panel,Image.Resampling.LANCZOS)
        canvas.paste(tile,(4+n*360,y))
target=work/'parallel_layout_static_candidate_v1.png'
if target.exists():raise FileExistsError('Preserve earlier layout diagnostics.')
canvas.save(target)
canvas.resize((360,640),Image.Resampling.LANCZOS).save(work/'parallel_layout_mobile_static_candidate_v1.png')
record=dict(week='2026-W41',model='M04',sources=files,identity_anchors=['02_brand/reference_models/M04_start_v3_face.png','02_brand/reference_models/M04_start_v3_full.png'],generation=dict(tool='Codex built-in imagegen',calls=4,observed_call_seconds=[52.7,73.6,56.5,42.7],active_minutes=None,selected='Bothv2',preserved_prior_variants=True),layout=dict(output=target.relative_to(ROOT).as_posix(),size=[720,1280],left=files[0]['look_id'],right=files[1]['look_id'],fixed_background_only_crop=crop,panel_size=panel,panel_positions=[[4,y],[364,y]],approximate_source_landmarks=dict(A=dict(hair_top=254,waist=662,shoe_bottom=1445),B=dict(hair_top=253,waist=662,shoe_bottom=1445)),landmarks_method='manual visual estimates, not automated exact measurements',source_files_changed=False,aspect_note='975 rounded from977ish proportional height; revise below before rendering film',dynamic_safety='not_started',user_approval=None),proof_and_carousel='incomplete',film='not_generated')
# Keep integer sizing exactly proportional to the reviewed500x1385 window.
# 352/500*1385=975.04, rounded975; no meaningful anisotropic transform.
record['layout']['aspect_note']='352/500*1385=975.04px, rounded975; proportional layout to pixel rounding.'
write(work/'parallel_first_frame_static_review_2026-10-08.json',record)
p=week/'reels/batch_storyboard.json';s=read(p);r=next(x for x in s['films'] if x['reel_id']=='2026-W41-M04-reel')
r['shots'][0]['action_start']='ActualL01v2: right arm relaxed; left hand in trouser pocket, left shoulder bag at image-right. Extract hand naturally before touching short strap.'
r['output_status']='two_first_frame_candidates_static_layout_reviewed_user_approval_pending'
r['first_frame_static_review']='10_automation/runs/2026-W41/reels/M04/parallel_first_frame_static_review_2026-10-08.json'
write(p,s)
p=week/'reels/production_manifest.json';m=read(p);r=next(x for x in m['reels'] if x['model_profile_id']=='M04')
r['status']='parallel_first_frame_pair_candidates_user_approval_pending';r['static_first_frame_candidates']=files;r['static_layout_diagnostic']=record['layout']['output'];write(p,m)
p=ROOT/'10_automation/production_requests/2026-10-08_next_five_reels.json';req=read(p);r=next(x for x in req['slots'] if x['model']=='M04');r['status']='parallel_first_frame_pair_candidates_user_approval_pending';r['still_review']=r'10_automation/runs/2026-W41/reels/M04/parallel_first_frame_static_review_2026-10-08.json';write(p,req)
p=week/'publishing_structure.md';s=p.read_text(encoding='utf-8');s=s.replace('分鏡與窄幅動作範圍已更新，起始圖接續生成。','分鏡與窄幅動作範圍已更新，兩張起始圖v2與左右靜態構圖已備妥並抽查，待使用者視覺核准後才送Grok；第一套實際起姿左手在褲袋，動畫需自然抽出再碰肩帶。')
p.write_text(s,encoding='utf-8')
p=ROOT/'CURRENT_STATUS.md';s=p.read_text(encoding='utf-8');entry='''## W41 M04 parallel first-frame pair ready for visual approval — 2026-10-08

M04 native9:16 first-frame pair prepared with approved v3 face/full anchors and actual pulled-back side-parted hair. Four built-in calls: L01v1 then one framing editv2; L02v1 then one skirt-material editv2. Both selectedv2 files are941×1672 and remain unmodified in their look Reel folders. User approval pending; no Grok submission. L02 uses L01v2 candidate only for porch/camera/bag continuity, not as approved wardrobe or identity. Approximate hair/waist/shoe coordinates match closely; bag, hands and entire skirt fit central narrow crop in static review. A has left hand in pocket; preserve natural hand extraction before touching same-side strap. Independent action timing remains allowed.

Static layout and phone-size diagnostic saved under `10_automation/runs/2026-W41/reels/M04/`, with background-only fixed crop and equal panel rectangles; they do not prove safe moving bounds or constitute a film. Images/QA paths, hashes, generation times and pending approvals in `parallel_first_frame_static_review_2026-10-08.json`. Proof/Carousel remain incomplete. M03/M05 film approvals still pending, M01/M02 pictures accepted, old batch/Drive preserved; later work saved locally.

''';p.write_text(s.replace('# Current Status - Mira AI Fashion Creator\n\n','# Current Status - Mira AI Fashion Creator\n\n'+entry,1),encoding='utf-8')
print(json.dumps({'static_layout':str(target),'first_frames_pending_approval':files},ensure_ascii=False))
