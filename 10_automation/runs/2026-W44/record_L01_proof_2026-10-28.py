from pathlib import Path
import json,csv,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent
J=RUN/'generated_images/2026-W44-001/looks/2026-W44-001-L01/reel'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
full=J/'2026-W44-001-L01_M02_reel_candidate_A_framing_v2.png';proof=J/'2026-W44-001-L01_M02_reel_styling_proof_candidate_A.png'
assert sha(full)=='e4f2e8b1e4aba05d295d21f3987d01d65ccdf94a263de096317732ae7a55a3c7'
approval=J/'user_A_still_approval_2026-10-28.json';a=read(approval);assert a['target_sha256']==sha(full)
im=Image.open(proof)
receipt={'date':'2026-10-28','look_id':'2026-W44-001-L01','role':'reel_styling_proof','provider':'built-in image_gen','runtime_model':'not surfaced','generation_calls':1,'corrections':0,'tool_wall_seconds':54.4,'timing_limit':'Observed round trip, not separate engine or active production measurement','input_roles':[{'path':full.relative_to(R).as_posix(),'role':'user-approved exact outfit and scene lock','sha256':sha(full),'approval_receipt':approval.relative_to(R).as_posix()},{'path':'02_brand/reference_models/M02_start_v3_face.png','role':'face identity'},{'path':'02_brand/reference_models/M02_start_v3_full.png','role':'body proportion identity'}],'prompt':'styling_proof_prompt.md','output':{'path':proof.relative_to(R).as_posix(),'width':im.width,'height':im.height,'bytes':proof.stat().st_size,'sha256':sha(proof)},'status':'pending_user_visual_approval','review':{'viewed':'Full generated output and approved full-person source','framing':'Full hair/face, open cardigan, white crew neck, charcoal waistband and whole black shoulder bag visible; lower legs intentionally out of frame','identity':'Face, gathered hairstyle, expression close to M02v3/source; not quantified biometric evidence','wardrobe':'Same purple-white-charcoal-black grouping; close view makes knit and trouser surface detail more pronounced, user wardrobe-continuity check pending','physical_limit':'Closer independent styling-proof composition only; not an approved later frame, continuous dolly endpoint or exact world/camera match','lighting':'Preserves bright available daylight treatment of accepted full still; not relabeled overcast exposure','blocking_defects_observed':'No obvious cropped hair/bag or gross hand collapse in displayed proof; no dynamic review performed'},'motion_generated':False,'new_still_approved':False}
write(J/'styling_proof_receipt_2026-10-28.json',receipt)
g=read(J/'generation_receipt_2026-10-28.json');g['status']='user_approved_full_still';g['approved']=True;g['approval_receipt']=approval.name
for o in g['outputs']:
 if o['file']==full.name:o['status']='user_approved_still'
write(J/'generation_receipt_2026-10-28.json',g)
sheet=J/'review_sheet.csv'
with sheet.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for row in rows:
 if row['candidate_file']==full.name:row['status']='user_approved_still';row['notes']+=' User ok approved this exact full still; proof and motion approvals separate.'
if not any(x['candidate_file']==proof.name for x in rows):
 row={k:'' for k in fields};row.update({'carousel_id':'2026-W44-001','look_id':'2026-W44-001-L01','prompt_id':'2026-W44-001-L01','model_profile_id':'M02','candidate_file':proof.name,'tool':'Codex built-in image_gen','model_consistency':4,'body_proportion_consistency':4,'reader_relatability':4,'outfit_clarity':4,'ai_realism':4,'scene_lighting_integration':4,'outfit_continuity':4,'expression_liveliness':4,'pose_variation':4,'canva_frame_fit':'N/A Reel','commerce_value':4,'publishable':'pending','status':'pending_user_visual_approval','notes':'Operator still review only; verify knit/trouser surface continuity in close view. Independent proof, not a camera-route endpoint.'});rows.append(row)
with sheet.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
pp=RUN/'planning/series_01/production_plan.json';plan=read(pp)
plan['approvals'].append({'asset_id':'L01_reel_A_candidate','scope':'still','decision':'approved','target_sha256':sha(full),'receipt_path':approval.relative_to(R).as_posix()})
plan['assets'].append({'id':'L01_styling_proof_candidate','kind':'still','path':proof.relative_to(R).as_posix(),'sha256':sha(proof)})
plan['status']='L01_full_approved_proof_pending'
plan['missing_assets']=[s for s in plan['missing_assets'] if s!='L01 Reel A framing_v2 exists but lacks individual user still approval; no motion submission']
plan['missing_assets'].append('L01 styling proof exists but awaits its own user visual approval; L02 and later world-time guides remain missing.');write(pp,plan)
packet=RUN/'weekly_content_packet.csv'
with packet.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for row in rows:
 if row['carousel_id']=='2026-W44-001':row['status']='L01_full_approved_proof_pending';row['next_action']='Review exact L01 styling proof, then prepare remaining look/scene inputs; no motion yet'
with packet.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
heading='## W44第一套全身已核准，穿搭重點圖待審 — 2026-10-28'
body='使用者對精確L01全身framing_v2回「ok」，接受人物、穿搭與已披露的構圖／日光差異；SHA '+sha(full)+'，收據 `10_automation/runs/2026-W44/generated_images/2026-W44-001/looks/2026-W44-001-L01/reel/user_A_still_approval_2026-10-28.json`。這是該張靜態圖核准，不是動態／路徑／精確場地或發布核准。\n\n用此全身圖作服裝與場景鎖，加M02v3 face/full雙參照，內建image_gen單次生成直式styling-proof（未修正），'+str(im.width)+'×'+str(im.height)+'，檔名 `2026-W44-001-L01_M02_reel_styling_proof_candidate_A.png`，SHA '+sha(proof)+'，與全身圖同資料夾。完整頭臉、紫色門襟、白T、炭灰腰線及完整黑包可見；近景衣料表面更明顯，仍待使用者核對服裝連續性。它是獨立穿搭proof，不指定為同世界時間末幀或連續推近端點。精確指令／回合／靜態審查見styling_proof_prompt.md及styling_proof_receipt_2026-10-28.json。\n\n下一步審此proof；其後補第二套與必要場地時序素材。未送動態、未產Carousel圖或外部交付，所有舊圖與影片保留。'
for name in ['CURRENT_STATUS.md','10_automation/MIRA_EDITORIAL_HANDOFF.md']:
 p=R/name;t=p.read_text(encoding='utf-8-sig')
 if heading not in t:first,rest=t.split('\n',1);p.write_text(first+'\n\n'+heading+'\n\n'+body+'\n'+rest,encoding='utf-8')
p=RUN/'publishing_structure.md';t=p.read_text(encoding='utf-8')
note='## L01全身核准／proof待審（2026-10-28）\n\n全身framing_v2已獲使用者「ok」核准，精確收據與hash在該look reel資料夾。由它單次衍生的styling_proof_candidate_A仍待逐張視覺核准；它是獨立穿搭驗證構圖，不是路線影片的實際末幀。尚未生成動態或Carousel；下方先前待全身核准狀態已取代。\n\n'
if note not in t:first,rest=t.split('\n',1);p.write_text(first+'\n\n'+note+rest,encoding='utf-8')
print(json.dumps(receipt['output'],ensure_ascii=True))
