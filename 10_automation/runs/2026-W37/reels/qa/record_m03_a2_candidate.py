"""Record an approved parent and unapproved derivative with retained failed attempts."""
import csv,hashlib,json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[5]
run=root/'10_automation/runs/2026-W37';reels=run/'reels'
folder=run/'generated_images/2026-W37-005/looks/2026-W37-005-L01/reel'
def rel(p):return p.relative_to(root).as_posix()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
paths=[folder/f'2026-W37-005-L01_M03_A2_detail_start_candidate_v{n}.png' for n in range(1,5)]
reasons=['Invented ornamental/scribbled texture on plain clothing.','First local material correction retained visible unwanted texture.','Second local correction still retained the unwanted source texture.','Rebuilt from approved full image; ornament reduced to finer cloth surface. Retained as candidate for user review.']
prompts=['M03_A2_L01_detail_start_v1.md','M03_A2_L01_fabric_correction_v2.md','M03_A2_L01_plain_fabric_correction_v3.md','M03_A2_L01_rebuild_v4.md']
history=[]
for n,(p,reason,prompt) in enumerate(zip(paths,reasons,prompts),1):
    with Image.open(p) as im: size=list(im.size)
    history.append(dict(version=n,path=rel(p),pixels=size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),prompt_path=rel(reels/'prompts'/prompt),status='candidate_pending_user_visual_approval' if n==4 else 'rejected_material_fidelity',review=reason))
record=dict(look_id='2026-W37-005-L01',shot_id='A2',model_profile_id='M03',date='2026-10-01',status='candidate_pending_user_visual_approval',provider='built_in_imagegen',source_path=rel(paths[-1]),approved_parent=rel(folder/'2026-W37-005-L01_M03_A1_full_start_candidate_v2.png'),parent_approval=dict(reply='ok',date='2026-10-01'),history=history,assistant_review=dict(framing='Native941x1672 vertical detail, no face/chin/mouth; complete bag panel, strap/buckle, cream shirt, waist and relaxed hands visible. Actual framing extends toward knees despite upper-thigh request.',outfit='Cream sleeveless collared shirt tucked into dark-coffee trousers; small caramel tapered bag on viewer-right. V4 rebuilding reduced the obvious decorative markings seen in rejected derivatives; fine cloth appearance still subject to user review.',evidence='Bag panel is larger than full source and visibly contrasts with the light shirt; actual product/material performance cannot be inferred.',cut_continuity='Bag center is about76% width/38% height versus approved full about63%/36%. Horizontal shift remains; no successful full-to-detail cut claimed. Must inspect actual A1 ending and A2 starting frames and test framing before accepting edit.',identity='No face is visible by design. Motion must stay a fixed faceless detail, never reveal an unprovided face.'),user_visual_approval=None,grok_submitted=False,production_cost=dict(built_in_calls=4,initial_generation=1,derivative_local_corrections=2,rebuild_from_approved_parent=1,observed_tool_wall_seconds=[45.6,41.2,43.1,36.8],active_minutes=None,generation_wait_minutes=None,note='Wall times include tool overhead, not measured active work or pure generation wait. The approved full Hero was not repeatedly edited.'),motion_prompt_path=rel(reels/'prompts/M03_A2_L01_motion_v1.md'))
save(folder/'A2_detail_generation_v4.json',record)
p=reels/'production_manifest.json';manifest=json.loads(p.read_text(encoding='utf-8-sig'))
m=next(r for r in manifest['reels'] if r['model_profile_id']=='M03');m['status']='A1_approved_A2_v4_pending_visual_approval'
v=next(v for v in m['views'] if v['look_id']=='2026-W37-005-L01' and v['role']=='proof')
v.update(source_path=rel(paths[-1]),source_type='native_vertical_generated_detail',approval='candidate_pending_user_visual_approval',framing_review=record['assistant_review']['framing'],clarity_review=record['assistant_review']['outfit'],review_record_path=rel(folder/'A2_detail_generation_v4.json'))
next(s for s in m['storyboard'] if s['shot_id']=='A2').update(status='still_v4_pending_user_approval',source_still=rel(paths[-1]))
save(p,manifest)
p=folder/'review_sheet.csv'
with p.open(encoding='utf-8-sig',newline='') as f:
    r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for h in history:
    name=Path(h['path']).name
    if any(r['candidate_file']==name for r in rows):continue
    r=dict.fromkeys(fields,'');r.update(carousel_id='2026-W37-005',look_id='2026-W37-005-L01',prompt_id='M03_A2_L01',model_profile_id='M03',candidate_file=name,tool='built_in_imagegen',publishable='no',status=h['status'],notes=h['review']+' No motion generated; cut continuity unverified.')
    rows.append(r)
with p.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

p=root/'CURRENT_STATUS.md';text=p.read_text(encoding='utf-8-sig')
entry='''## M03 A1 approved; A2 detail v4 pending — 2026-10-01

User replied ok directly after the displayed M03 A1 v2 and explicit still-approval question. The full still is now approved for derivatives/motion; no video or account style approval inferred. A2 native941×1672 faceless bag/cloth detail v1 invented patterned fabric. Two derivative-local corrections retained unwanted marks and were rejected. Rebuilding from the approved full still produced v4, with much reduced ornamental marks, visible suede panel and plain-clothing relationship; final user visual approval remains pending. All attempts, prompts, hashes and observed tool wall times are retained in L01/reel `A2_detail_generation_v4.json`. Full Hero was not changed.

Selected pending detail: `generated_images/2026-W37-005/looks/2026-W37-005-L01/reel/2026-W37-005-L01_M03_A2_detail_start_candidate_v4.png`. The detail bag lies farther right (~76%width) than full(~63%); static approval will not establish a comfortable cut. Compare actual A1 end and A2 start and adjust the framing test before accepting four-shot edit. A1/A2 motion prompts prepared under reels/prompts; neither submitted. No B1/B2 generation, Carousel or publication. M01 remains unapproved; previous three selected picture tracks retain acceptance.

'''
text=text.replace('## Editorial review completed;',entry+'## Editorial review completed;',1);p.write_text(text,encoding='utf-8')
p=run/'publishing_structure.md';text=p.read_text(encoding='utf-8-sig');text=text.replace('# W37 Publishing Structure\n','# W37 Publishing Structure\n\n**M03 A1核准／A2候選（2026-10-01）：** 使用者ok核准第一套全身v2。近景初版和兩次局部修正因衣料紋理不符保留退件；由核准全身重做的A2 v4待使用者視覺核准。包面與衣料較清楚，但包水平位置與全身不同，仍須檢查真實動態切點；未送Grok。詳見L01/reel/A2_detail_generation_v4.json。\n',1);p.write_text(text,encoding='utf-8')
p=reels/'M03_storyboard_v1.md';text=p.read_text(encoding='utf-8-sig');text=text.replace('# W37 M03｜薄衣服旁的一個麂皮包\n','# W37 M03｜薄衣服旁的一個麂皮包\n\n**2026-10-01實作更新：** A1 v2已由使用者ok核准。A2三個衍生版本的衣料表面不符，未採用；重新從A1生成A2 v4，待視覺核准。構圖無臉、包面與褲腰可見；包中心約76%寬／38%高，與A1約63%／36%仍有水平位移。不可把靜態完成當切鏡成功；先測實際A1→A2接點，再擴第二套。A1與A2提示詞已準備，未送出影片生成。下方較早候選狀態以本更新為準。\n',1);p.write_text(text,encoding='utf-8')
p=reels/'REEL_RELEASE_GATE_2026-09-30.md';text=p.read_text(encoding='utf-8-sig');text=text.replace('四鏡材質對比分鏡就緒，第一套全身候選v2完成 | A1新圖待視覺核准；動態與四鏡風格均未驗證 | 核准A1、檢查／補齊兩套full與材質proof','四鏡材質對比分鏡就緒，第一套全身v2已核准、近景v4待核准 | A2新圖待視覺核准；動態與四鏡風格均未驗證 | 核准A2、檢查／補齊第二套full與材質proof');p.write_text(text,encoding='utf-8')
print('Approved A1 and pending A2 v4 recorded; rejected derivatives retained. No motion pass or submission inferred.')
