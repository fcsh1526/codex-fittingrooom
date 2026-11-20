from pathlib import Path
import json,csv,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent
J1=RUN/'generated_images/2026-W44-001/looks/2026-W44-001-L01/reel'
J2=RUN/'generated_images/2026-W44-001/looks/2026-W44-001-L02/reel'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sheet=J1/'review_sheet.csv'
with sheet.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for row in rows:
 if row['candidate_file']=='2026-W44-001-L01_M02_reel_styling_proof_candidate_A.png':row['status']='user_approved_still';row['notes']+=' User ok approved exact independent styling proof; not a route endpoint.'
with sheet.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
outfiles=[('2026-W44-001-L02_M02_outfit_lock_initial_pattern_failed.png','rejected_unwanted_trouser_pattern'),('2026-W44-001-L02_M02_outfit_lock_correction_pattern_failed.png','correction_failed_pattern_retained'),('2026-W44-001-L02_M02_outfit_reference_reset_candidate_A.png','outfit_direction_candidate_pending_user_review')]
outputs=[]
for name,status in outfiles:
 p=J2/name;im=Image.open(p);outputs.append({'file':name,'path':p.relative_to(R).as_posix(),'width':im.width,'height':im.height,'bytes':p.stat().st_size,'sha256':sha(p),'status':status})
current=J2/outfiles[-1][0]
receipt={'date':'2026-10-28','look_id':'2026-W44-001-L02','role':'outfit_reference_only_not_S02_entry','provider':'built-in image_gen','runtime_model':'not surfaced','total_generation_calls':3,'sequence':[{'call':1,'purpose':'New L02 outfit lock using accepted L01 full photo for upper wardrobe/scene plus identity pair','prompt':'hero_A_prompt.md','tool_wall_seconds':31.9,'outcome':'Unwanted ornamental trouser texture; rejected'},{'call':2,'purpose':'One targeted correction to remove trouser ornament','prompt':'denim_surface_correction_prompt.md','tool_wall_seconds':29.9,'outcome':'Pattern retained; rejected, not used for derivatives'},{'call':3,'purpose':'Source reset after failure diagnosis; identity pair only, explicit plain-denim textual outfit specification','prompt':'outfit_source_reset_prompt.md','tool_wall_seconds':57.6,'outcome':'New outfit-direction candidate; not exact shared-world entry'}],'diagnosis':'Possible inherited texture from outfit/photo reference; not established as causal. Source role changed rather than repeating another correction on failed pixels.','actual_inputs':{'calls_1':['L01 accepted full-person framing_v2','M02 v3 face','M02 v3 full'],'call_2':['L02 initial pattern-failed image'],'call_3':['M02 v3 face','M02 v3 full']},'outputs':outputs,'current_review_candidate':current.name,'review':{'viewed':'Full displayed outputs and accepted L01 full source','identity':'Recognizable M02 face, gathered hairstyle and adult proportions; exact identity judgement pending user','outfit_direction':'Purple/white upper layers with chocolate-brown five-pocket straight denim, white-gray sneakers and black bag readable; denim surface still visibly mottled, not a fabric-quality claim','deviations':'Bag switches shoulder; apparent cardigan length/button arrangement, person scale and architecture differ from accepted L01 photo. Not marked exact wardrobe or scene continuity pass.','role_limit':'Candidate may establish L02 dressing direction only after explicit user acceptance. It is not the actual S02 global f150 entry, a verified later-frame projection or a completed connected source.'},'new_still_approved':False,'motion_generated':False,'next':'User review of L02 outfit direction. Build actual entry using an approved/measured S01 boundary or a validated calibrated scene before motion; no unapproved substitution of this reference into S02.'}
write(J2/'outfit_reference_receipt_2026-10-28.json',receipt)
sheet=J2/'review_sheet.csv'
with sheet.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames
rows=[]
for output in outputs:
 row={k:'' for k in fields};row.update({'carousel_id':'2026-W44-001','look_id':'2026-W44-001-L02','prompt_id':'2026-W44-001-L02','model_profile_id':'M02','candidate_file':output['file'],'tool':'Codex built-in image_gen','model_consistency':4,'body_proportion_consistency':4,'reader_relatability':4,'outfit_clarity':4,'ai_realism':4,'scene_lighting_integration':4,'outfit_continuity':2 if 'failed' in output['file'] else 3,'expression_liveliness':4,'pose_variation':4,'canva_frame_fit':'N/A outfit reference','commerce_value':3,'publishable':'no','status':output['status'],'notes':'Not S02 route entry. First two rejected for pattern; source-reset version changes bag side and garment/scene details and needs outfit-direction review. No connected-source approval.'});rows.append(row)
with sheet.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
pp=RUN/'planning/series_01/production_plan.json';plan=read(pp)
plan['assets'].append({'id':'L02_outfit_reference_candidate','kind':'still','path':current.relative_to(R).as_posix(),'sha256':sha(current),'intended_use':'outfit-direction review only; not a shot input'})
plan['status']='L01_full_proof_approved_L02_outfit_reference_pending'
plan['missing_assets']=[x for x in plan['missing_assets'] if not x.startswith('L01 styling proof exists')]
plan['missing_assets']+=['L02 source-reset outfit reference awaits direction approval and is not exact wardrobe/scene continuity pass','Actual S02 f150 entry still and compatible S01/S02 18-frame overlap remain missing; do not substitute outfit-reference-only candidate','Prior shared-space animation generated but no continuous playback review; L01 photoreal site not calibrated to common schematic']
write(pp,plan)
regpath=R/'04_prompts/material_pool/series_registry.json';reg=read(regpath)
for s in reg['series']:
 if s['series_id']=='W44_PROPOSAL_01':s['status']=plan['status'];s['latest_receipt']=str((J2/'outfit_reference_receipt_2026-10-28.json').relative_to(R)).replace('\\','/')
write(regpath,reg)
packet=RUN/'weekly_content_packet.csv'
with packet.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for row in rows:
 if row['carousel_id']=='2026-W44-001':row['status']=plan['status'];row['next_action']='Review L02 outfit direction only; actual route entry/overlap unresolved, no motion submission'
with packet.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
heading='## W44第一套full/proof均已核准；第二套僅造型方向待審 — 2026-10-28'
body='使用者對第一套styling-proof精確SHA b971d913fd7fa9974e3c922dda568b70a939f68b48b720e25233b1ffc293b1c9回「ok」，收據存L01 reel/user_proof_still_approval_2026-10-28.json。L01全身及獨立proof均靜態接受，不推為動態或末幀核准。\n\n核對發現L02 look表誤用S01f0構圖，已修正為S02 globalf150／6.25秒的接入需求；同一shared_space與previs_frames取出L02_entry_f150_camera.png，另輸出13.25秒示意GIF，沒有完整連續目視播放通過宣稱。原照片建築／尺度未校準到示意世界，因此不先宣稱已做出連續下一鏡。\n\n第二套先作outfit_reference：用L01照片＋身份雙參照的一次初圖與一次褲面修正，仍有不應有花紋，兩版退件並保留。診斷後改只用身份雙參照＋文字服裝重建一次，最新 `2026-W44-001-L02_M02_outfit_reference_reset_candidate_A.png`，SHA '+sha(current)+'，'+str(outputs[-1]['width'])+'×'+str(outputs[-1]['height'])+'，位於W44 generated_images/2026-W44-001/looks/2026-W44-001-L02/reel。包換肩、衣長／扣位呈現、尺度和背景均有差；近看褲面仍有斑駁，不記精確材質／服裝連續性通過。只請使用者核對棕丹寧搭配方向，未核准新圖，亦不將此圖填入S02。完整三回合／指令／失敗與限制見outfit_reference_receipt_2026-10-28.json。\n\n下一步：造型方向確認與真正S02接入資料分開。優先取得第一鏡實際可用接點或校準場地後再做接入圖，18幀重疊、原速可用長度、動態身份與接點仍待驗。未新增Grok影片、Carousel、Drive／IG或GitHub同步。'
for name in ['CURRENT_STATUS.md','10_automation/MIRA_EDITORIAL_HANDOFF.md']:
 p=R/name;t=p.read_text(encoding='utf-8-sig')
 if heading not in t:first,rest=t.split('\n',1);p.write_text(first+'\n\n'+heading+'\n\n'+body+'\n'+rest,encoding='utf-8')
p=RUN/'publishing_structure.md';t=p.read_text(encoding='utf-8')
note='## L01 full/proof已核准；L02僅造型參照候選（2026-10-28）\n\n第一套proof已獲「ok」，兩個靜態來源接受。第二套經花紋失敗與身份參照重建，目前只可審outfit_reference_reset候選的搭配方向，包側／衣長／場景與前圖有差，不是精確服裝／世界接續通過。第二鏡應在global f150／6.25秒接入，已修正look表S01f0誤植，取出同模型靜態關鍵視圖；真正接入圖與18幀重疊仍缺。沒有把這張造型圖放進S02或送動態。詳L02 reel/outfit_reference_receipt_2026-10-28.json；以下歷史待proof狀態已取代。\n\n'
if note not in t:first,rest=t.split('\n',1);p.write_text(first+'\n\n'+note+rest,encoding='utf-8')
print(json.dumps(outputs[-1],ensure_ascii=True))
