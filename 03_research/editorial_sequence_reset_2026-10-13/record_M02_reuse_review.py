from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
approval_path=ROOT/'10_automation/runs/2026-W41/reels/M02_full_pair_user_approval_2026-10-08.json'
approved=read(approval_path)['files'];images=[]
for row in approved:
 assert hashlib.sha256((ROOT/row['file']).read_bytes()).hexdigest()==row['sha256']
 images.append({**row,'reuse_status':'static_suitable_for_this_trial_full_view','review':'Viewed exact native full-person image against approved M02 face and weekly outfit. Full head/shoes, straight brown denim waist/hem and black shoes/bag readable. Same cafe wood-framed glass door at image-right, gray wall, left planter and short wooden stool; native vertical composition. New seated view still missing. Not new user approval or dynamic whole-film pass.'})
motion=[]
for role,name,qa_name,interval in [('first_full','A_attempt_01','QA_A01',[0,60]),('closing_full','B_attempt_01','QA_B01',[24,108])]:
 source=ROOT/f'10_automation/runs/2026-W41/reels/M02/{name}/source.mp4'
 qa=read(ROOT/f'10_automation/runs/2026-W41/reels/M02/{qa_name}/inspection.json')
 actual=hashlib.sha256(source.read_bytes()).hexdigest();assert actual==qa['source_sha256']
 motion.append({'role':role,'file':source.relative_to(ROOT).as_posix(),'sha256':actual,'reuse_status':'sampled_motion_candidate_join_review_required','candidate_frames_end_exclusive':interval,'candidate_seconds':[n/24 for n in interval],'review_method':'Viewed existing25 whole-frame and5 face checkpoint boards per source; read prior native145-lower-body review record. No new continuous assistant playback or all-native-frame inspection claimed.','actual_motion':'Short forward-step/catch-up then stance shifts; no sustained departure. Wardrobe and cafe context broadly stable in checkpoints. No fine hand-cloth action required.','user_accepted_previous_film':'10_automation/runs/2026-W41/reels/M02/review_v2/user_picture_approval_2026-10-08.json','new_combined_film_accepted':False})
review={'date':'2026-10-13','week':'2026-W41','model':'M02','look_ids':[r['look_id'] for r in approved],'old_still_approval':approval_path.relative_to(ROOT).as_posix(),'image_reviews':images,'motion_reviews':motion,'scene_lock_observed':'Cafe exterior: wood-framed glass door at image-right, gray plaster wall, left leafy planter and short wooden stool. Seated sources should derive this place; do not copy M03 window-left/long-bench geometry.','incremental_missing_sources':['L01 seated native9:16 styling-proof still + motion','L02 seated native9:16 styling-proof still + motion'],'planning_reduction':'Two full-person stills and two original full-person clips can be proposed for reuse. Start by generating only two missing seated stills, each with its own exact wardrobe authority; static user approval and motion QA still required. Incremental cost is not from-zero production cost.','limits':'Reuse is a trial source choice. New join comfort, context consistency, complete production/Carousel package and actual reduced generation cost remain unverified.'}
save(BASE/'M02_reuse_review_2026-10-13.json',review)
p=BASE/'next_M02_repeatability_plan.json';plan=read(p)
plan.update(status='existing_full_views_reviewed_two_missing_seated_views_planned',reusable_source_files=review,mising_images=None)
plan.pop('mising_images',None)
plan['missing_images']=review['incremental_missing_sources']
plan['first_action']='Create L01 seated proof candidate using its approved full-person wardrobe and observed cafe doorway/stool scene; inspect exact identity/material/framing, then user visual approval before Grok. Later create L02 proof under its own lock. Existing full clips are reuse candidates; no new full-person generation needed at this stage.'
plan['scene_purpose']='Brief pause outside the existing cafe wood-framed doorway. The actual short wooden stool supports seated layer/waist views, and the same doorway links full-step clips. No added coffee-cup hand interaction or copied M03 bench.'
plan['candidate_source_time_budgets_seconds']=[2.5,3.75,3.75,3.5]
plan['timing_note']='Provisional source budgets only; candidate11.25s after three0.75s overlaps. Recompute from new proof motion and whole-film review; not IG-optimal timing.'
plan['incremental_targets']={'new_still_initial_calls':2,'new_motion_initial_calls':2,'reused_stills':2,'reused_original_clips':2,'source_reuse_qa':'Static/checkpoint review complete; new joins not reviewed.'}
save(p,plan)
p=BASE/'REPEATABILITY_RECIPE.md';p.write_text('> 素材篩選更新2026-10-13：已查看M02兩張核准全身圖與兩段原始動態的25大圖／5臉部檢查板，核對SHA。可作新試片的全身來源候選；目前只需補兩張坐姿重點圖與其動態。咖啡店場景實際為木框玻璃門在右、灰牆、左植栽與矮木凳，應從它規劃坐姿，不能照搬M03長椅。新銜接與增量成本仍待驗證。見`M02_reuse_review_2026-10-13.json`。\n\n'+p.read_text(encoding='utf-8-sig'),encoding='utf-8')
update='''## M03已核准；M02轉用可共用全身來源，補兩張坐姿 — 2026-10-13

精確M03 10.75秒四鏡研究片已由使用者「ok」接受，核准与可重用規格已同步到canonical／SOP／W41研究補記。接著實際查看M02 W41-003兩張核准原生全身圖，以及兩段原始動態各25張大圖／5臉部檢查板，核對圖片／影片SHA與原核准；可作同形式試片的全身來源候選，接點仍需新片評估。場景是右側木框咖啡店玻璃門、灰牆、左植栽與矮木凳，不照搬M03長椅。下一次製作先補L01坐姿重點圖，再補L02；各自使用自己核准的服裝鎖定與人物雙參照，先核准新圖才送Grok。規劃增量2張圖＋2段動態，既有2個全身圖／原片共用；這不是已達效率或从零成本承諾。紀錄：`03_research/editorial_sequence_reset_2026-10-13/M02_reuse_review_2026-10-13.json`、`next_M02_repeatability_plan.json`。本步未生成新媒體／未更新Drive或發布，歷史五支交付保留。下方為歷史進度。

'''
p=ROOT/'CURRENT_STATUS.md';head,rest=p.read_text(encoding='utf-8-sig').split('\n',1);p.write_text(head+'\n\n'+update+rest.lstrip('\n'),encoding='utf-8')
p=BASE/'README.md';p.write_text(update+p.read_text(encoding='utf-8-sig'),encoding='utf-8')
print('M02 existing full images/clips hash-verified and checkpoint reviewed. Two seated proof sources remain; no new generation.')
