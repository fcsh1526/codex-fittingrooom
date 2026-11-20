from pathlib import Path
import hashlib,json,csv
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=next(x for x in P.parents if (x/'CURRENT_STATUS.md').exists());W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
old=P/'2026-W45-004-L01_M04_reel_candidate_A.png';new=P/'2026-W45-004-L01_M04_reel_candidate_A_face_v2.png'
assert h(old)=='6b0c9691fe0b214a2ae5bbdee103178c125563e1fcfe662f0be20bd7ae7d4b46'
with Image.open(new) as im:pixels=list(im.size)
face=ROOT/'02_brand/reference_models/M04_start_v3_face.png';full=ROOT/'02_brand/reference_models/M04_start_v3_full.png'
assert h(face)=='b9fbb46533782597e255b30a910c2457741aa70f92ddc0aa05060de9fb0b4a91'
assert h(full)=='958dec3949edd2ebaedd7be408bc1ef6cc8a735a9749c11b6e5e73d401fa8241'
receipt={'date':'2026-11-05','status':'face_corrected_candidate_pending_user_visual_approval','generator':'built-in image generation','call_type':'targeted_identity_edit','edit_attempt_for_this_hero':1,'user_feedback_receipt':rel(P/'user_face_feedback_2026-11-05.json'),'input_roles':[{'path':rel(old),'sha256':h(old),'role':'edit target, preserve clothing/body/scene/composition'},{'path':rel(face),'sha256':h(face),'role':'primary identity authority'},{'path':rel(full),'sha256':h(full),'role':'identity and proportion support'}],'prompt_path':rel(P/'face_correction_v2_prompt.txt'),'prompt_sha256':h(P/'face_correction_v2_prompt.txt'),'output_path':rel(new),'output_sha256':h(new),'actual_pixels':pixels,'assistant_visual_review':'Eye/nose/chin appearance adjusted; outfit, floral positions, scene and stance broadly retained visually. Pixel-identical preservation or exact identity not certified. Original tight framing, larger bag and added necklace remain.','user_visual_approval':None,'publishable':None,'new_image_calls':1,'new_video_jobs':0,'publication_action':False}
put(P/'generation_receipt_face_v2.json',receipt)
r=read(P/'generation_receipt.json');r.update(status='user_requested_face_identity_revision',latest_feedback_receipt=rel(P/'user_face_feedback_2026-11-05.json'),superseded_candidate_receipt=rel(P/'generation_receipt_face_v2.json'));put(P/'generation_receipt.json',r)
q=read(W/'production_queue.json');assert q['builtin_image_calls'] in (8,9) and q['video_jobs_completed']==16
q.update(status='M04_L01_face_v2_pending_user_visual_approval_parallel_paused',builtin_image_calls=9,stills_generated=9,active_reviews=[rel(new)],active_trial=None,next={'model':'M04','action':'User checks exact targeted face correction before motion; original rejected face not used.'});put(W/'production_queue.json',q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(rp);series=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M04');series.update(status=q['status'],latest_asset_receipt=rel(P/'generation_receipt_face_v2.json'));put(rp,reg)
sheet=P/'review_sheet.csv'
with sheet.open(encoding='utf-8-sig',newline='') as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
rows[0].update(status='user_requested_face_identity_revision',publishable='no',notes='User: 臉有點飄，再一次. Original kept, not approved for motion.')
if not any(x['candidate_file']==new.name for x in rows):
 row={key:'' for key in fields};row.update(carousel_id='2026-W45-004',look_id='2026-W45-004-L01',prompt_id='2026-W45-004-L01-face-v2',model_profile_id='M04',candidate_file=new.name,tool='Codex',publishable='pending',status='pending_user_visual_approval',notes='One targeted face correction using approved M04 face/full anchors; no motion approval.');rows.append(row)
with sheet.open('w',encoding='utf-8',newline='') as f:writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
old_text='已生成首圖候選；人物約佔畫高89%、留白較少，肩包較計畫大且多項鍊，依規則待個別視覺核准。'
new_text='首圖因使用者回饋「臉有點飄，再一次」完成一次定向臉部修正版face_v2，待個別視覺核准；沿用同套／場景，人物約佔畫高89%、留白較少，包較計畫大及項鍊的既有偏差保留。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
 p=ROOT/name;txt=p.read_text(encoding='utf-8-sig');assert old_text in txt or new_text in txt;txt=txt.replace(old_text,new_text,1).replace('八次靜態／十六支原片，','九次靜態／十六支原片，');p.write_text(txt,encoding='utf-8')
review=P/'REVIEW.md';txt=review.read_text(encoding='utf-8');notice='> 最新進度：使用者回饋「臉有點飄，再一次」，原圖未接受。已用原圖作編輯目標、M04核准臉部作主要身份依據，完成一次face_v2修正；精確版本見`generation_receipt_face_v2.json`，仍待逐張視覺核准。原版保留，下方為初版觀察。\n\n'
if notice not in txt:txt=txt.replace('2026-11-05。',notice+'2026-11-05。',1);review.write_text(txt,encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for item in snap:assert h(ROOT/item['snapshot_path'])==item['sha256']
put(P/'face_v2_verification.json',{'original_preserved':True,'immutable_snapshots_verified':len(snap),'output_sha256':h(new),'new_video_jobs':0,'parallel_editing_still_paused':True,'user_visual_approval':None})
print(json.dumps({'status':q['status'],'output_sha256':h(new),'pixels':pixels,'image_calls':9,'snapshots_unchanged':len(snap)}))
