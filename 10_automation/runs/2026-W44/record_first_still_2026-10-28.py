from pathlib import Path
import json,csv,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent
J=RUN/'generated_images/2026-W44-001/looks/2026-W44-001-L01/reel'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
initial=J/'2026-W44-001-L01_M02_reel_candidate_A_initial.png';final=J/'2026-W44-001-L01_M02_reel_candidate_A_framing_v2.png'
correction='''Edit image 1 with ONE targeted correction: widen the existing framing to match the approved full-person starting composition. Keep the canvas natively 9:16. The same woman, from top of hair to shoe soles, should occupy approximately 62% of the image height, with hair top at roughly 29% down and shoe soles near 91% down, centered horizontally. Extend the existing coherent office walkway around her, particularly above her, as a natural wider view from the same chest-height level camera, not borders or an inset. Keep her face, loosely gathered hairstyle, exact purple fine-knit cardigan, white crew-neck T-shirt, charcoal straight trousers, white-gray sneakers, black shoulder bag, silver earrings, existing mid-step pose, expression, light direction and photographic character unchanged. Image 1 is the sole scene and exact wardrobe lock; images 2 and 3 are face and body identity anchors only. Preserve her normal adult proportions. Do not add any new scene landmarks, stairs, doors, extra people, or signs. Match original paving, right-side facade, greenery, and low bench with consistent perspective and soft ambient light. This is a framing correction, not a new outfit or new pose. No text, logos, watermark, borders, or studio-cutout edges.'''
(J/'framing_correction_prompt.md').write_text('# One targeted framing correction\n\n'+correction+'\n',encoding='utf-8')
receipt={'date':'2026-10-28','look_id':'2026-W44-001-L01','model':'M02 v3','surface':'reel','provider':'built-in image_gen','runtime_model_name':'not surfaced','initial_prompt_file':'hero_A_prompt.md','correction_prompt_file':'framing_correction_prompt.md','generation_calls':2,'new_initial_candidates':1,'targeted_corrections':1,'actual_reference_inputs':{'initial':['02_brand/reference_models/M02_start_v3_face.png','02_brand/reference_models/M02_start_v3_full.png'],'correction':[initial.relative_to(R).as_posix(),'02_brand/reference_models/M02_start_v3_face.png','02_brand/reference_models/M02_start_v3_full.png']},'observed_tool_wall_seconds':[58.7,38.5],'timing_limit':'Tool round-trip wall time, not independently measured engine processing or active work time.','outputs':[],'selected_review_file':final.name,'status':'pending_user_visual_approval','approved':False,'motion_generated':False}
for p,st in [(initial,'preserved_initial_needs_framing_revision'),(final,'pending_user_visual_approval')]:
 im=Image.open(p);receipt['outputs'].append({'file':p.name,'path':p.relative_to(R).as_posix(),'width':im.width,'height':im.height,'bytes':p.stat().st_size,'sha256':sha(p),'status':st})
receipt['visual_review']={'reviewed':'Generated full images and identity anchors visually inspected','identity':'Face shape, cheeks, jaw, gathered hairstyle and expression remain close to approved M02v3 anchors; not a quantified biometric result','outfit':'Purple open cardigan/white crew tee/charcoal straight trousers/white-gray low sneakers/black bag/silver earrings visible; no text or visible logo observed','composition':'Corrected figure approx65% frame height, hair top approx21%, shoe bottom approx87%; still larger and higher than schematic approx61%, top29%, bottom91%. Manual visual estimates, not segmentation measurements.','scene':'Office facade, paving, greenery and low bench coherent within still; brighter mottled daylight and more architectural detail than schematic. Not exact world geometry, matched soft-overcast exposure or future camera-route proof.','contact':'Plausible mid-step and floor contact shadows in still; gait/no-slip not established','blocking_defects_observed':'No obvious cropped hair/shoes/bag or gross anatomy collapse in displayed still; user judgement pending'}
write(J/'generation_receipt_2026-10-28.json',receipt)
fields=next(csv.reader((J/'review_sheet.csv').open(encoding='utf-8-sig')))
rows=[]
for p,status in [(initial,'needs_framing_revision_preserved'),(final,'pending_user_visual_approval')]:
 row={k:'' for k in fields};row.update({'carousel_id':'2026-W44-001','look_id':'2026-W44-001-L01','prompt_id':'2026-W44-001-L01','model_profile_id':'M02','candidate_file':p.name,'tool':'Codex built-in image_gen','model_consistency':4,'body_proportion_consistency':4,'reader_relatability':4,'outfit_clarity':4,'ai_realism':4,'scene_lighting_integration':4,'outfit_continuity':4,'expression_liveliness':4,'pose_variation':4,'canva_frame_fit':'N/A Reel','commerce_value':4,'publishable':'pending','status':status,'notes':'Operator still review only, no user approval. See generation_receipt_2026-10-28.json for composition/light/world deviations; no dynamic or Canva fit pass.'});rows.append(row)
with (J/'review_sheet.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
planpath=RUN/'planning/series_01/production_plan.json';plan=read(planpath)
plan['assets'].append({'id':'L01_reel_A_candidate','kind':'still','path':final.relative_to(R).as_posix(),'sha256':sha(final)})
plan['shots'][0]['input_asset_ids']=['L01_reel_A_candidate'];plan['status']='first_still_pending_user_visual_approval';plan['missing_assets'].append('L01 Reel A framing_v2 exists but lacks individual user still approval; no motion submission')
write(planpath,plan)
pack=RUN/'weekly_content_packet.csv'
with pack.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);pf=r.fieldnames;pr=list(r)
pr[0]['status']='first_still_pending_user_visual_approval';pr[0]['next_action']='Review exact L01 Reel A framing_v2; no motion before approval'
with pack.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=pf);w.writeheader();w.writerows(pr)
regpath=R/'04_prompts/material_pool/series_registry.json';reg=read(regpath)
for s in reg['series']:
 if s['series_id'].startswith('W44_PROPOSAL_'):
  s['status']='first_still_pending_user_visual_approval' if s['series_id']=='W44_PROPOSAL_01' else 'design_approved_stills_pending'
  s['planning_approval_receipt']='10_automation/runs/2026-W44/approvals/user_planning_approval_2026-10-28.json'
reg['updated_date']='2026-10-28';write(regpath,reg)
structure=RUN/'publishing_structure.md';text=structure.read_text(encoding='utf-8')
note='## 2026-10-28最新檢查點\n\n使用者回「ok」，確認本v2企劃／分鏡及必要示意預演，授權開始首張候選；不推為新照片、動態或發布核准。精確審閱頁與各線稿hash見approvals/user_planning_approval_2026-10-28.json。五組設計已接受；下方待審描述保留為10/27企劃原始狀態。\n\n第一系列M02／L01已用內建image_gen生成一張原生直式候選，並只做一次拉遠構圖修正；兩張皆保存。最新候選941×1672、SHA '+sha(final)+'，位於generated_images/2026-W44-001/looks/2026-W44-001-L01/reel/。完整頭鞋包可見，人物尺度與上緣仍未精確命中示意，場景光線較亮，未證明精確世界／軌道。等待使用者逐張視覺核准；未生成proof／Carousel圖、影片或外部交付。\n\n'
if '## 2026-10-28最新檢查點' not in text:
 first,rest=text.split('\n',1);structure.write_text(first+'\n\n'+note+rest,encoding='utf-8')
body='使用者對W44來源補正v2回「ok」，記錄企劃、十套搭配、線稿及必要示意預演接受，授權開始首張起始圖；收據 `10_automation/runs/2026-W44/approvals/user_planning_approval_2026-10-28.json` 保存精確hash及範圍。未把這句話當成新照片／動態／發布核准。\n\n第一系列M02紫色薄針織工作日L01，以approved M02v3 face/full雙參照、內建image_gen做一次初圖＋一次針對性拉遠構圖修正。最新候選 `2026-W44-001-L01_M02_reel_candidate_A_framing_v2.png`，941×1672，SHA '+sha(final)+'，存W44 generated_images/2026-W44-001/looks/2026-W44-001-L01/reel。完整紫外搭／白T／炭灰直褲／白灰鞋／黑包可讀；人物約65%高、上緣約21%，仍與示意61%／29%有差，日光比soft-overcast預想更亮，背景不作精確場地或路徑通過。逐項靜態審查與原始／修正prompt見該目錄generation_receipt_2026-10-28.json；圖片未獲使用者視覺核准。\n\n下一步只請使用者確認此精確framing_v2候選。通過後再推導必要proof與後續鏡頭，不自行送動態；Carousel同look規格工作單已備妥但未產圖。其餘四系列設計接受、新照片待做。無新Grok／Drive／IG或GitHub同步。'
for name in ['CURRENT_STATUS.md','10_automation/MIRA_EDITORIAL_HANDOFF.md']:
 p=R/name;t=p.read_text(encoding='utf-8-sig');head='## W44企劃已確認，第一張紫色薄針織候選待審 — 2026-10-28'
 if head not in t:first,rest=t.split('\n',1);p.write_text(first+'\n\n'+head+'\n\n'+body+'\n'+rest,encoding='utf-8')
canonical=R/'10_automation/CANONICAL_WORKFLOW.md';t=canonical.read_text(encoding='utf-8-sig')
note='- W44 planning approved / first still gate,2026-10-28: user reply "ok" accepts source-backed v2 editorial/looks/storyboards/necessary schematic previs and authorizes the first starting-image candidate. Exact scope/hashes in runs/2026-W44/approvals/user_planning_approval_2026-10-28.json. M02 L01 native portrait generated once, then one framing-only correction; latest framing_v2 remains pending individual user still approval. No dynamic generation/publication authority inferred. Earlier proposed/pending-plan wording is superseded within this scope.\n\n'
if note not in t:canonical.write_text(t.replace('## Standard Weekly Production Contract',note+'## Standard Weekly Production Contract'),encoding='utf-8')
print(final.relative_to(R).as_posix());print(sha(final))
