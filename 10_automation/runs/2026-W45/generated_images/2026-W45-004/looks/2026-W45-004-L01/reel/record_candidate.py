from pathlib import Path
import hashlib,json
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=next(x for x in P.parents if (x/'CURRENT_STATUS.md').exists());W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
candidate=P/'2026-W45-004-L01_M04_reel_candidate_A.png';face=ROOT/'02_brand/reference_models/M04_start_v3_face.png';full=ROOT/'02_brand/reference_models/M04_start_v3_full.png'
with Image.open(candidate) as im:width,height=im.size
assert width==941 and height==1672
assert h(face)=='b9fbb46533782597e255b30a910c2457741aa70f92ddc0aa05060de9fb0b4a91';assert h(full)=='958dec3949edd2ebaedd7be408bc1ef6cc8a735a9749c11b6e5e73d401fa8241'
put(P/'generation_receipt.json',{'date':'2026-11-05','status':'candidate_pending_individual_user_visual_approval','generator':'built-in image generation','surface':'reel','model':'M04 v3','look':'2026-W45-004-L01','output_path':rel(candidate),'output_sha256':h(candidate),'actual_pixels':[width,height],'reference_face_path':rel(face),'reference_face_sha256':h(face),'reference_full_path':rel(full),'reference_full_sha256':h(full),'prompt_target_subject_height_percent':'72–78','assistant_approx_subject_height_percent':89,'observed_deviations':['bag appears larger than planned small shoulder bag','additional silver necklace','framing tighter than target, limited head/shoe margin'],'individual_user_approval':None,'film_or_publication_approval':None,'generation_calls':1,'new_video_jobs':0})
q=read(W/'production_queue.json');assert q['video_jobs_completed']==16 and q['weekly_reels_user_accepted']==2
q.update(status='M04_L01_still_candidate_pending_user_visual_approval_parallel_paused',builtin_image_calls=8,stills_generated=8,active_reviews=[rel(candidate)],active_trial=None,next={'model':'M04','action':'User visual approval of exact L01 candidate required before motion; tighter framing and bag size disclosed.'});put(W/'production_queue.json',q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(rp);m04=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M04');m04.update(status=q['status'],latest_asset_receipt=rel(P/'generation_receipt.json'));put(rp,reg)
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
 p=ROOT/name;txt=p.read_text(encoding='utf-8-sig');old='原核准M04身份與整週分鏡作依據，首圖依規則待個別視覺核准。';new='原核准M04身份與整週分鏡作依據，已生成首圖候選；人物約佔畫高89%、留白較少，肩包較計畫大且多項鍊，依規則待個別視覺核准。'
 assert old in txt,name;txt=txt.replace(old,new,1)
 txt=txt.replace('七次靜態／十六支原片，M01／M02共兩支接受成片；','八次靜態／十六支原片，M01／M02共兩支接受成片；')
 p.write_text(txt,encoding='utf-8')
print(json.dumps({'status':q['status'],'sha256':h(candidate),'pixels':[width,height],'image_calls':8}))
