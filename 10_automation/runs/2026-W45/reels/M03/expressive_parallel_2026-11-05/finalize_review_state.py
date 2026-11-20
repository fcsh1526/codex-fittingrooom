"""Reconcile scoped acceptance, new source and actual edit candidates."""
import hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
BR=Path(__file__).resolve().parent;ROOT=BR.parents[5];P=BR/'paired_review_v1';S=BR/'L02_trial_01';L=BR/'trial_02'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=read(P/'edit_receipt.json');tech=read(S/'technical_review.json');native=read(P/'native_frame_verification.json')
assert all(x['decoded_frame_hashes_identical'] for x in native['fps_normalization_checks'])
for o in receipt['outputs']:assert h(ROOT/o['path'])==o['sha256']
sub=read(S/'submission.json');sub.update(status='source_and_edit_candidates_pending_user_review',source_path=rel(S/'source.mp4'),source_sha256=tech['source_sha256'],silent_path=rel(S/'M03_W45_skirt_expressive_trial01_silent_review.mp4'),silent_sha256=tech['silent_sha256'],actual_width=720,actual_height=1280,actual_fps=24,actual_frames=241,actual_seconds=10.041667,source_has_audio=True,user_acceptance=None,publication_approval=None)
put(S/'submission.json',sub)
ui=read(S/'native_playback_sampling.json')
put(S/'visual_review.json',{'date':'2026-11-05','status':'source_pending_user_feedback_used_in_review_edits','whole_film_samples_viewed':21,'upper_body_samples_viewed':23,'additional_full_resolution_frames_viewed':[144,204,216],'native_UI_samples':len(ui['samples']),'uninterrupted_human_visual_review':False,'observed_phrases':['hands on waist, hip and shoulder shifts','high two-arm V','side/rear turn and frontal return, skirt swing','palms near shoulders then hand-on-hip finish'],'attention':'Visible samples mainly address lens; not complete eye tracking.','layout_envelope':'High V and broad arm swing exceed narrow columns. Selected intervals/crop in paired_review_v1/edit_receipt.json; full source retained.','body_feet_bag_anatomy_zero_defect_certification':False,'user_acceptance':None,'publication_approval':None})
(S/'REVIEW.md').write_text('''# M03 裙裝大幅換姿來源

2026-11-05。沿用已逐張核准的L02首圖與M03 v3身份，單次生成10.041667秒／241格／24fps／720×1280。沒有新照片、換服務或額外雲端金鑰。UUID `64c9236b-86e1-4456-82b4-36de7918ec41`。

可見叉腰擺臀、雙臂高V、側後轉帶動裙擺、回正與攤手收姿。鏡頭是展示對象。完整來源保留，並排版只選適合窄欄的段落，不宣稱裁切解決物理瑕疵。

完整解碼通過；21張全片半秒樣本、23張上半身四分之一秒樣本及6／8.5／9秒完整解析度畫格已看。網站1倍播放截圖另存。這些不等於連續人工原速全片驗收；手腳、身份、頭身及包帶不宣稱零缺陷。原片有AAC，無音預覽僅移除音軌、未剪段或變速。

目前來源與兩種剪輯均待使用者回饋。先前「ok」只接受褲裝trial02表演，沒有預先接受本裙裝、新剪輯或發布。

[完整原速無音來源](M03_W45_skirt_expressive_trial01_silent_review.mp4)｜[兩種實片剪輯](../paired_review_v1/REVIEW.md)
''',encoding='utf-8')
put(P/'visual_review.json',{'date':'2026-11-05','status':'review_candidates_not_release_approved','technical_full_decode':[True,True],'native_frame_verification':'native_frame_verification.json','whole_film_contact_samples_viewed':{'A':21,'B':20},'additional_join_and_end_samples_viewed':native['boundary_samples'],'A_observation':'Waist/hip poses, side/rear turn, bent knee and skirt swing visible; sampled head/shoes stay visible and similar scale. Same crop/scale both sides. Broad high-V not included. Last six frames checked for raised-palm panel safety.','A_scale_tradeoff':'Roughly 57–60% canvas height, smaller than full-frame source; no full-height promise.','B_observation':'Full native frames retain high-V and wider gestures, with larger people. Optional sequential alternative.','join_observation':'Both use 18-frame/0.75s dissolve. Overlap has visible double outlines; do not label seamless or ghost-free.','continuous_human_native_speed_review':False,'user_film_acceptance':None,'publication_approval':None,'layout_preference':{'question_pending':True,'default':'A original parallel direction','B':'optional comparison, not substituted'}})
(P/'REVIEW.md').write_text('''# M03 兩套換姿｜實片比較

2026-11-05。觀眾看同件海軍藍柔肩西外，搭深色直褲／皮鞋與奶油A字裙／球鞋的輪廓和正式感差異；人物自在展示衣服，增加叉腰、重心／肩膀變化、轉身、屈膝與裙擺動勢。

| 版本 | 實際內容 | 取捨 |
|---|---|---|
| [A 左右並排](M03_W45_parallel_selected_review_v1.mp4) | 5.25秒、兩側各兩段選材；叉腰、轉側、屈膝／裙擺、收姿 | 原並排方向。窄欄保留頭鞋與手包邊界，人物約占畫高57–60%；不保留雙臂高V |
| [B 依序全畫面](M03_W45_full_frame_sequence_review_v1.mp4) | 19.333333秒、兩支完整10.041667秒來源交疊 | 額外比較候選，保留高V與更大人物，未取代並排方向 |

兩版均720×1280／24fps／無音，18格即0.75秒淡接。未變速、倒放、凍結或額外複製影格補長；來源經fps正規化前後241張解碼影格雜湊逐一相同。淡接有可見雙影，不宣稱無縫／無疊影。剪輯前後原片雜湊保持，精確選段／裁切／尺寸／成片雜湊見 `edit_receipt.json`。

A裁切與選段是版面設計，不是物理修復。完整大幅表演留在來源與B。已看A全片四分之一秒21張、B每秒20張、淡接與A末六格額外樣本；完整解碼通過。仍未可靠完成連續人工原速全片審查，不列可發布。

使用者「ok」精確接受褲裝trial02來源表演與自然感；新裙裝、A/B成片與發布尚無核准。排版偏好問題尚待回覆，先依原並排方向呈現A主候選，B僅供具體比較。新生成：裙裝來源一支；新增靜態圖零張。M01／M02既有接受不變。
''',encoding='utf-8')
lv=read(L/'visual_review.json');lv['parallel_fit_review']='Full V does not fit narrow columns; selected-pose edit candidate reviewed separately in ../paired_review_v1/visual_review.json.';put(L/'visual_review.json',lv)
lp=L/'REVIEW.md';t=lp.read_text(encoding='utf-8');t=t.replace('沒有新照片、右側、合片或額外付費服務。','當時沒有新照片、右側或合片；本次接續另見下方狀態。')
old='目前為`candidate_pending_user_performance_feedback`，不是使用者已接受、正式並排片、交付或發布。保留Grok結果頁方便觀看。此分支已做兩次，若本次仍不符，依具體回饋改設計或研究；沒有自動第三次或右側生成。'
new='最新：使用者直接回覆「ok」，已接受此精確10.04秒來源的表演與自然感，收據為 `user_performance_acceptance_2026-11-05.json`。依既有M03範圍接續一支裙裝來源及[兩種實片剪輯](../paired_review_v1/REVIEW.md)，沒有第三次褲裝重生。來源接受不等於新裙裝、並排完成片或發布核准；連續人工原速QA缺項保留。'
assert old in t or new in t;t=t.replace(old,new);lp.write_text(t,encoding='utf-8')
(BR/'STATUS.md').write_text('''# M03 完整換姿研究｜有效狀態

更新：2026-11-05。

| 精確版本 | 狀態 |
|---|---|
| trial01，a9d31a19，6.041667秒 | 抬臂追手被認為莫名、動作少；未接受，不重開待審 |
| [褲裝trial02，414c5d81，10.041667秒](trial_02/REVIEW.md) | 使用者「ok」接受精確來源表演，非成片／發布 |
| [裙裝L02 trial01，64c9236b，10.041667秒](L02_trial_01/REVIEW.md) | 單次新生成，解碼與動態抽樣完成，待回饋 |
| [A並排選段5.25秒／B完整依序19.333333秒](paired_review_v1/REVIEW.md) | 原速無音剪輯候選；A為原方向，B保留完整高V。排版偏好及成片未核准 |

本次新增一支裙裝影片、零張靜態圖。沿用兩張核准首圖，沒有重生褲裝。兩版淡接皆0.75秒、可見雙影；解碼／抽樣不等於連續人工原速驗收。保留來源完整大動作，並排選段不是物理修復。M01／M02接受與18份企劃核准快照不變，沒有新交接／發布。
''',encoding='utf-8')
weekly=ROOT/'10_automation/runs/2026-W45';q=read(weekly/'production_queue.json');q.update(status='M03_two_edit_candidates_pending_user_review',video_jobs_completed=12,active_reviews=[o['path'] for o in receipt['outputs']],active_trial=rel(P),latest_edit_receipt=rel(P/'edit_receipt.json'));q['next']={'model':'M03','action':'Review concrete A parallel selected poses and optional B full-frame sequence; trousers source performance accepted, new skirt and full film pending. No automatic regeneration.'};put(weekly/'production_queue.json',q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';r=read(rp);r['updated_date']='2026-11-05';series=next(s for s in r['series'] if s['series_id']=='SERIES_W45_M03');series.update(status='trousers_source_performance_accepted_two_edit_candidates_pending',latest_asset_receipt=rel(P/'edit_receipt.json'),current_reassessment=rel(P/'REVIEW.md'),source_performance_acceptance=rel(L/'user_performance_acceptance_2026-11-05.json'))
u=next(x for x in r['uses'] if x['usage_id']=='W45_M03_expressive_trial02_2026-11-05');u.update(status='user_accepted_exact_source_performance',feedback_summary='User ok accepts exact full-frame trousers performance/naturalness; not new skirt, edited film or publication.',user_acceptance_receipt=rel(L/'user_performance_acceptance_2026-11-05.json'))
old_u=next(x for x in r['uses'] if x['usage_id']=='W45_M03_expressive_parallel_trial01_2026-11-05');old_u['feedback_summary']='Arm-following gaze purposeless, larger/more varied poses requested. Not accepted; superseded by accepted-source trial02, not reopened.'
new_uses=[{'usage_id':'W45_M03_skirt_expressive_trial01_20261105','series_id':'SERIES_W45_M03','production_date':'2026-11-05','status':'source_candidate_pending_user_feedback','film_path':rel(S/'M03_W45_skirt_expressive_trial01_silent_review.mp4'),'source_asset_id':sub['video_asset_id'],'source_sha256':tech['source_sha256'],'receipt_path':rel(S/'submission.json'),'user_acceptance_receipt':None,'publication_url':None}]
for tag,o in zip(['PARALLEL_SELECTED','FULL_FRAME_SEQUENCE'],receipt['outputs']):new_uses.append({'usage_id':f'USE_W45_M03_{tag}_V1_20261105','series_id':'SERIES_W45_M03','production_date':'2026-11-05','status':'edited_candidate_pending_user_review','film_path':o['path'],'film_sha256':o['sha256'],'receipt_path':rel(P/'edit_receipt.json'),'user_acceptance_receipt':None,'publication_url':None})
for nu in new_uses:
    nu['feedback_summary']='New skirt/full-film candidate pending user review. Trousers source performance accepted separately; no edited-film or publication approval.'
    existing=next((x for x in r['uses'] if x['usage_id']==nu['usage_id']),None)
    if existing:existing.update(nu)
    else:r['uses'].append(nu)
for uid in [u['usage_id'],old_u['usage_id']]+[x['usage_id'] for x in new_uses]:
    if uid not in series['usage_ids']:series['usage_ids'].append(uid)
put(rp,r)
current='W45現況：M01精確10.25秒與M02 trial03已接受，尚無新交接／發布。M03兩張首圖核准保留；11/4原三版及11/5追手trial01未接受。使用者「ok」已接受褲裝trial02（414c5d81，10.041667秒）的來源表演／自然感；其後單次生成裙裝64c9236b，同為10.041667秒。已完成A左右並排選段5.25秒與B完整依序19.333333秒原速無音候選，待新裙裝／成片回饋及排版偏好，非發布核准。兩版0.75秒淡接可見雙影，解碼與動態抽樣不代表連續人工原速QA。累計七次內建靜態／十二支原片／兩支接受成片；M04–M05與proof／Carousel仍缺。詳M03 expressive_parallel_2026-11-05/paired_review_v1/REVIEW.md；不自動重生。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
    p=ROOT/name;lines=p.read_text(encoding='utf-8-sig').splitlines();matches=[i for i,line in enumerate(lines) if 'W45現況：' in line];assert len(matches)==1
    i=matches[0];lines[i]=lines[i].split('W45現況：')[0]+current;p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=weekly/'publishing_structure.md';t=p.read_text(encoding='utf-8');lines=t.splitlines()
for i,line in enumerate(lines):
    if line.startswith('2. M01與M02精確接受範圍保留。'):lines[i]='2. M01／M02接受保留。M03褲裝trial02來源表演已接受；新裙裝及[A並排／B完整依序實片](reels/M03/expressive_parallel_2026-11-05/paired_review_v1/REVIEW.md)待回饋，非成片／發布核准。'
    if line.startswith('5. 原速逐鏡／接點／整片、'):lines[i]='5. 原速逐鏡／接點／整片、使用者接受、交接與發文分開。七次靜態／十二支原片，M01／M02共兩支接受成片；M03源表演接受未增加成片數。十套proof／Carousel未完成，無本週IG發文紀錄。'
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=ROOT/'10_automation/MIRA_EDITORIAL_HANDOFF.md';lines=p.read_text(encoding='utf-8').splitlines()
for i,line in enumerate(lines):
    if line.startswith('- 11/5完整換姿研究現況見'):lines[i]='- 11/5完整換姿：褲裝trial02表演已獲「ok」，一次新裙裝與A並排5.25秒／B完整依序19.333333秒已完成，見[實片比較](runs/2026-W45/reels/M03/expressive_parallel_2026-11-05/paired_review_v1/REVIEW.md)。排版偏好與新成片待回饋，來源接受不擴成發布；不重開trial01。'
    if line.startswith('- 目前下一步：由'):lines[i]='- 目前下一步：回看M03兩種實片候選與新裙裝，保留原並排方向作主候選。既有IG觀察與退件／接受均保留，不重開舊新頁1/3/5問題；沿用原IG頁、不新增或額外標記分頁。M04–M05與proof／Carousel依後續範圍接續。'
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
ep=weekly/'planning/M03/performance_replan_2026-11-05/EXECUTION_PLAN.md';t=ep.read_text(encoding='utf-8');note='最新執行狀態：下方為最初短測計畫的歷史範圍。使用者後續要求更大更多，trial02來源表演已接受；單次新裙裝與兩種實片已完成，精確選段／版面見 `reels/M03/expressive_parallel_2026-11-05/paired_review_v1/edit_receipt.json`。原9.25秒草案不作實際成片證據，沒有改寫原核准快照。\n\n'
if note not in t:t=t.replace('\n\n','\n\n'+note,1);ep.write_text(t,encoding='utf-8')
approval=read(weekly/'approvals/user_planning_approval_2026-11-03.json');checked=[]
for a in approval['artifacts']:
    path=ROOT/a['snapshot_path'];assert h(path)==a['sha256'];checked.append(a['snapshot_path'])
protected={'M01':'aa1a657e88480a966226bdbf72ea3e5c46346290df154408d376ebcc2b27a2fb','M02':'bf1828d34ce61ac76e82d1573a49e85d8403d5a5ae9be9bb8be46c16fa114b67'}
for model,path in [('M01','reels/M01/paired_review_v1/M01_W45_two_looks_review_v1.mp4'),('M02','reels/M02/trial_03/M02_W45_trial03_silent_review.mp4')]:assert h(weekly/path)==protected[model]
put(P/'state_reconciliation.json',{'date':'2026-11-05','approved_snapshots_unchanged':len(checked),'accepted_M01_M02_unchanged':True,'source_hashes_unchanged':True,'weekly_source_jobs':12,'weekly_accepted_finished_reels':2,'stills_generated':7,'user_accepted_current_source_only':True,'new_skirt_and_edit_user_acceptance':None,'IG_tabs_created_this_turn':0,'new_paid_cloud_provider_requests':0})
print(json.dumps({'state_reconciled':True,'snapshots_unchanged':len(checked),'candidates':len(receipt['outputs'])}))
