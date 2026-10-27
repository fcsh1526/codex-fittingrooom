"""Persist editorial review and M03 still candidate; approvals are never inferred."""
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[5]
run=root/'10_automation/runs/2026-W37'
reels=run/'reels'
folder=run/'generated_images/2026-W37-005/looks/2026-W37-005-L01/reel'
def rel(p): return p.relative_to(root).as_posix()
def write(p,data): p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
v1=folder/'2026-W37-005-L01_M03_A1_full_start_candidate_v1.png'
v2=folder/'2026-W37-005-L01_M03_A1_full_start_candidate_v2.png'
with Image.open(v2) as im: pixels=list(im.size)
record=dict(look_id='2026-W37-005-L01',model_profile_id='M03',date='2026-10-01',status='candidate_pending_user_visual_approval',provider='built_in_imagegen',source_path=rel(v2),pixels=pixels,sha256=hashlib.sha256(v2.read_bytes()).hexdigest(),prompt_path=rel(reels/'prompts/M03_A1_L01_start_v1.md'),correction_prompt_path=rel(reels/'prompts/M03_A1_L01_bag_face_correction_v2.md'),references=['02_brand/reference_models/M03_start_v3_face.png','02_brand/reference_models/M03_start_v3_full.png'],reference_status='Both approved in reference CSV and visually inspected before generation',history=[dict(path=rel(v1),status='superseded_candidate_single_defect_bag_side_orientation'),dict(path=rel(v2),status='candidate_pending_user_visual_approval',edit='One targeted bag orientation edit; broad plain suede panel now more visible')],assistant_still_review=dict(identity='Face, long wavy brown hair and expression are close to approved v3 anchors; final user identity review pending.',wardrobe='Cream sleeveless collared shirt tucked into dark-coffee straight trousers, full black low-heel loafers, silver earrings; caramel suede small shoulder bag beside waistband.',framing='941x1672 native vertical composition; full hair and both shoes visible, free arms do not cover bag. Bag center approximately x63%,y36%.',body='Healthy ordinary proportions close to full anchor; no obvious elongated limb artifact.',scene='Daylit neighborhood cafe wall, bench and paving. Complete shadows and normal ground contact. No text or logos observed.',proof='Broad bag panel clearer after edit; native full-shot bag remains small. Separate proof view must be tested for nap visibility; not yet satisfied.',limitations='Still candidate only, no motion or continuous QA; full-shot does not validate proposed four-shot rhythm.'),user_visual_approval=None,grok_submitted=False,time=dict(active_minutes=None,generation_wait_minutes=None),targeted_corrections=1)
write(folder/'A1_full_start_generation_v2.json',record)

sheet=folder/'review_sheet.csv'
with sheet.open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
for path,status,notes in [(v1,'superseded_single_defect','Bag side gusset faced camera; retained as original, corrected once.'),(v2,'candidate_pending_user_visual_approval','Full hair/shoes and exact outfit retained. Broad suede panel visible after targeted correction. Four-shot style remains untested; no Grok submission.')]:
    if not any(r.get('candidate_file')==path.name for r in rows):
        row=dict.fromkeys(fields,'')
        row.update(carousel_id='2026-W37-005',look_id='2026-W37-005-L01',prompt_id='M03_A1_L01_start_v1',model_profile_id='M03',candidate_file=path.name,tool='built_in_imagegen',publishable='no',status=status,notes=notes)
        if path==v2:
            for field in ['model_consistency','body_proportion_consistency','reader_relatability','outfit_clarity','ai_realism','scene_lighting_integration','outfit_continuity','expression_liveliness','pose_variation','commerce_value']: row[field]='4'
            row['canva_frame_fit']='N/A_reel'
        rows.append(row)
with sheet.open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)

mp=reels/'production_manifest.json'
manifest=json.loads(mp.read_text(encoding='utf-8-sig'))
manifest['editorial_review_2026_10_01']=dict(report_path=rel(reels/'EDITORIAL_REVIEW_2026-10-01.md'),evidence='24 sampled frames from four cuts plus existing user feedback; no new continuous playback or audience-performance claim',decision='Two-shot format is not a mandatory template. M03 proposes four shots for material evidence; hypothesis unvalidated.',latest_ok_scope='Acknowledgment to perform editorial review, not M01 video acceptance')
m=next(r for r in manifest['reels'] if r['model_profile_id']=='M03')
m['audience_problem']='換季仍穿薄衣服，如何用一個麂皮包增加材質差異？'
m['format_variant']='A'
m['status']='storyboard_ready_A1_candidate_pending_visual_approval'
m['visual_theme']='同一咖啡店外廊，先看完整薄衣服，再比較焦糖／奶油白與深棕／淺藍的材質關係，最後回到完整裙裝。'
m['storyboard_path']=rel(reels/'M03_storyboard_v1.md')
m['storyboard']=[dict(shot_id=s,look_id=l,start=a,end=b,framing=f,status='planned_not_generated' if s!='A1' else 'still_candidate_pending_user_approval',new_information=i) for s,l,a,b,f,i in [('A1','2026-W37-005-L01',0,2,'full_person','全身的棉麻衣服與小麂皮包面積關係'),('A2','2026-W37-005-L01',2,4,'faceless_bag_and_cloth_detail','焦糖短絨包與奶油白衣料、深咖啡褲腰'),('B2','2026-W37-005-L02',4,6,'matched_faceless_bag_and_cloth_detail','深棕短絨包與淺藍裙／同布腰帶'),('B1','2026-W37-005-L02',6,8.5,'full_person','完整裙長、黑鞋和小包的搭配')]]
v=next(v for v in m['views'] if v['look_id']=='2026-W37-005-L01' and v['role']=='full')
v.update(source_path=rel(v2),source_type='native_vertical_still',approval='candidate_pending_user_visual_approval',framing_review=record['assistant_still_review']['framing'],clarity_review=record['assistant_still_review']['wardrobe'])
m['identity'].update(face='02_brand/reference_models/M03_start_v3_face.png',full='02_brand/reference_models/M03_start_v3_full.png')
write(mp,manifest)

status=root/'CURRENT_STATUS.md'
text=status.read_text(encoding='utf-8-sig')
entry='''## Editorial review completed; M03 material-detail trial started — 2026-10-01

The user questioned whether two full-person shots are the fixed production mode, then said ok to an editorial review. This ok is **not** M01 video approval. M02/M05/M04 picture approvals remain; M01 is still pending continuous user acceptance. Four cuts were compared through24 sampled frames and their existing records. Recurring front-facing strap-holding poses and low within-shot information are the main editorial limitation; M02/M04 have useful full/detail progression. Report: `reels/EDITORIAL_REVIEW_2026-10-01.md`; board: `reels/qa/editorial_review_2026-10-01/four_reels_comparison.jpg`. No new continuous-playback or audience-performance claim.

Canonical and Reel SOP now explicitly separate technical QA, individual-cut acceptance, account style and measured results. No universal shot-count template. M03 `reels/M03_storyboard_v1.md` proposes ~8.5s full L01 → bag/cloth L01 → matched detail L02 → full L02. The full/detail cuts are a hypothesis requiring actual viewing, not an established cure for scale discomfort.

M03 A1 native941×1672 candidatev2 is under `generated_images/2026-W37-005/looks/2026-W37-005-L01/reel/2026-W37-005-L01_M03_A1_full_start_candidate_v2.png`. Approved v3 face/full anchors were inspected. Cream sleeveless collared shirt, dark-coffee straight trousers, caramel suede small shoulder bag, black low-heel loafers. V1 bag side faced camera; one targeted correction made the broad panel more visible while retaining original scene/body. User visual approval question sent; no Grok upload, A2 derivative or B still yet. Record: `A1_full_start_generation_v2.json`. Proof texture clarity remains open. Proceed after still approval; no new Carousel work or publication.

'''
text=text.replace('## M01 two-look candidate ready;',entry+'## M01 two-look candidate ready;',1)
status.write_text(text,encoding='utf-8')
structure=run/'publishing_structure.md'
text=structure.read_text(encoding='utf-8-sig')
text=text.replace('# W37 Publishing Structure\n','# W37 Publishing Structure\n\n**風格檢視／M03（2026-10-01）：** 已比較四支成片的抽樣畫面；两鏡不是固定量產形式。M03擬試全身→同套包／衣料近景→第二套同景別近景→全身，約8.5秒，接點舒適度尚未驗證。第一套全身v2已生成，包面做一次朝向修正，等待使用者核准；未送Grok。這次ok承接風格檢視，不代表M01成片核准。\n',1)
structure.write_text(text,encoding='utf-8')
gate=reels/'REEL_RELEASE_GATE_2026-09-30.md'
text=gate.read_text(encoding='utf-8-sig')
text=text.replace('| M03／麂皮與皮革一件亮點 | 無雙套成片 | 尚未開始動態驗收 | 同上 |','| M03／麂皮與皮革一件亮點 | 四鏡材質對比分鏡就緒，第一套全身候選v2完成 | A1新圖待視覺核准；動態與四鏡風格均未驗證 | 核准A1、檢查／補齊兩套full與材質proof、動態與完整剪接驗收 |')
gate.write_text(text,encoding='utf-8')
print('Editorial report, M03 storyboard and v2 candidate linked. No new approval or motion submission inferred.')
