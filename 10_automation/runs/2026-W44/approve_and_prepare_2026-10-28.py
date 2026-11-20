from pathlib import Path
import csv,json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent;P=RUN/'planning'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvwrite(p,fields,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
series=read(P/'series_proposals.json');approval=RUN/'approvals/user_planning_approval_2026-10-28.json'
receipt={'actor':'user','decision':'approved','scope':'W44 v2 editorial series, ten complete looks, line storyboards and necessary schematic previs; proceed to first starting-image candidate','quote':'ok','recorded_at':'2026-10-28','timezone':'Asia/Taipei','context':'Direct reply to the source-corrected v2 proposal and review.html; original request required confirmation before generating starting images.','artifacts':[],'limits':'Not approval of ungenerated stills, actual camera-path reproduction, dynamic QA, finished films or publication. User continuous-playback self-report unknown.'}
for name in ['review.html','series_proposals.json','shared_space.json']+[f'series_{i:02}_storyboard.png' for i in range(1,6)]:
 file=P/name;receipt['artifacts'].append({'path':file.relative_to(R).as_posix(),'sha256':sha(file)})
write(approval,receipt)
for s in series:
 planpath=P/f"series_{s['id']}/production_plan.json";plan=read(planpath)
 plan['status']='design_approved_stills_pending'
 for a in plan['assets']:
  if a['kind'] in ['storyboard','previs','overhead']:
   normalized=RUN/f"approvals/{s['id']}_{a['kind']}_2026-10-28.json"
   record={'actor':'user','decision':'approved','scope':a['kind'],'target_sha256':a['sha256'],'quote':'ok','recorded_at':'2026-10-28','source_receipt':approval.relative_to(R).as_posix(),'limits':'Schematic design only, not actual generated media or physical/camera adherence.'}
   write(normalized,record)
   plan['approvals'].append({'asset_id':a['id'],'scope':a['kind'],'decision':'approved','target_sha256':a['sha256'],'receipt_path':normalized.relative_to(R).as_posix()})
 plan['missing_assets']=[x for x in plan['missing_assets'] if x not in ['本週企劃及精確線稿待使用者確認','新週服裝需重審連續路線的衣服閱讀價值；沿用幾何不是新企劃核准']]
 plan['design_approval_receipt']=approval.relative_to(R).as_posix();write(planpath,plan)
 s['status']='design_approved_stills_pending';s['planning_approval_receipt']=approval.relative_to(R).as_posix()
# Keep the exact reviewed proposal JSON unchanged: operational state lives separately.
write(P/'planning_approval_state.json',{'date':'2026-10-28','receipt':approval.relative_to(R).as_posix(),'series':series})
packet_fields=next(csv.reader((R/'10_automation/runs/2026-W41/weekly_content_packet.csv').open(encoding='utf-8-sig')))
look_fields=next(csv.reader((R/'10_automation/runs/2026-W41/weekly_look_plan.csv').open(encoding='utf-8-sig')))
packets=[];looks=[]
for s in series:
 cid=f"2026-W44-{int(s['id']):03}"
 action='已踏出自然前進的一步，身體大致面向相機，雙手自然擺動、不遮門襟與腰線' if s['id']=='01' else s['beats'][0]
 scene='台北有遮簷的辦公街廓外側步道，平整淡灰鋪面；中性辦公牆面與簡單窗框、長椅作共同場地地標。首圖取S01 f0近正面視角，詳細幾何只作設計參照，不聲稱照片精確重建。' if s['id']=='01' else s['region']
 packet={k:'' for k in packet_fields};packet.update({'week_id':'2026-W44','carousel_id':cid,'market':'Taiwan Traditional Chinese','creator_name':'Mira','model_profile_id':s['model'],'trend_name':s['title'],'content_bucket':'daily_editorial','audience':'台灣成年女性日常穿搭','occasion':s['region'],'content_engine':'utility_with_immersion','dressing_decision':s['answer'],'visible_action':action,'audience_problem':s['question'],'editorial_answer':s['answer'],'opening_hook':s['title'],'visual_proof':'；'.join(s['proofs']),'practical_rule':s['answer'],'prompt_id':s['source_rows'][0],'clothing_item':s['looks'][0],'color_palette':'依已核准的兩套完整搭配','fabric':'依核准設計；圖片僅示意，不代表商品功能實測','fit':'維持核准身份雙參照的正常比例','styling_rules':s['answer'],'scene':scene,'status':'design_approved_stills_pending','next_action':'Generate first native9:16 Reel full-person candidate; each new still needs individual user visual approval','canva_template_key':s['master']});packets.append(packet)
 for k,lid in enumerate(s['look_ids']):
  look={x:'' for x in look_fields};look.update({'week_id':'2026-W44','carousel_id':cid,'model_profile_id':s['model'],'look_id':lid,'look_order':k+1,'theme_name':s['title'],'opening_hook':s['title'],'look_name':s['looks'][k],'dressing_decision':s['answer'],'occasion':s['region'],'clothing_item':s['looks'][k],'color_palette':'依核准完整搭配','fabric':'輕薄視覺設計；不作商品材質功能主張','fit':'核准人物比例、完整頭鞋、褲腳不遮鞋型','styling_rules':s['answer'],'visual_proof':s['proofs'][k],'practical_rule':s['answer'],'scene':scene,'visible_action':action,'frame_plan':'reel:full_9x16+vertical_styling_proof;carousel:hero_full+scene_application+accessory_detail','required_frames':5,'status':'editorial_approved','next_action':'Prepare both surface jobs; new still visual approval required'});looks.append(look)
csvwrite(RUN/'weekly_content_packet.csv',packet_fields,packets);csvwrite(RUN/'weekly_look_plan.csv',look_fields,looks)
for surface in ['reel','carousel']:
 subprocess.run([sys.executable,str(R/'11_skills/mira-image-daily/scripts/prepare_daily_image_job.py'),'--project-root',str(R),'--run-dir',str(RUN),'--look-id','2026-W44-001-L01','--surface',surface],cwd=R,check=True,capture_output=True)
job=RUN/'generated_images/2026-W44-001/looks/2026-W44-001-L01/reel'
prompt='''Create one photorealistic fashion-magazine starting photograph, composed natively as a vertical 9:16 Reel frame. The dressing decision is one royal-purple lightweight cardigan over neutral workwear. Image 1 supplies facial identity and hairstyle; image 2 supplies the same adult East Asian woman’s normal body proportions only. Preserve her youthful late-20s appearance, soft oval face and loosely gathered dark-brown hair; replace the reference outfit and studio setting.

She is taking one purposeful, natural step toward the camera along a sheltered Taipei office-adjacent walkway, with a gently engaged expression and relaxed arm swing. Keep the ground level, with quiet pale paving and restrained office architecture; the simple window wall and low bench belong to one coherent location. Dress her in an open royal-purple fine-knit V-neck cardigan, white crew-neck short-sleeve cotton T-shirt tucked into charcoal high-waisted straight-leg trousers, white-and-light-gray low-profile sneakers, a small plain black shoulder bag, and delicate silver earrings. The cardigan is the only bright color.

Use soft overcast daylight, matching ambient spill and believable foot contact, lived-in folds, natural skin texture and flyaway hairs. Full-frame mirrorless, 50mm prime, chest-height level optical axis. Keep her full hair, both shoes and entire bag visible, in the lower two-thirds of the frame with generous overhead space and visible ground.

Constraints: no text, logos, watermark, fashion-elongated anatomy, or studio-cutout lighting.'''
(job/'hero_A_prompt.md').write_text('# First Reel A · approved design 2026-10-28\n\n'+prompt+'\n',encoding='utf-8')
write(job/'generation_request.json',{'date':'2026-10-28','look_id':'2026-W44-001-L01','surface':'reel','provider':'built-in image_gen','quantity':1,'prompt':prompt,'references':['02_brand/reference_models/M02_start_v3_face.png','02_brand/reference_models/M02_start_v3_full.png'],'target':'native9:16, intended1080x1920; record actual output dimensions','source_view':'planning/series_01 S01 globalf0; common scene schematic','review_targets':{'person_height_fraction':0.613,'person_center_uv':[0.5,0.602],'top_margin_min':0.08,'central_platform_safe_fraction':0.70},'limits':'The geometric draft is direction, not proof of exact photoreal reconstruction. No image approval or motion submission yet.','approval_receipt':approval.relative_to(R).as_posix()})
print(job)
