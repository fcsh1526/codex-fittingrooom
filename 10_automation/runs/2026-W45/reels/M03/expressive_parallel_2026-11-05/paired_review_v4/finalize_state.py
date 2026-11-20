"""Register the concrete4s candidate; preserve all source/layout acceptance scopes."""
import hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;BR=P.parent;ROOT=BR.parents[5];W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
e=read(P/'edit_receipt.json');assert h(ROOT/e['output'])==e['output_sha256'];e['status']='sampled_review_candidate_not_user_accepted';put(P/'edit_receipt.json',e)
put(P/'visual_review.json',{'date':'2026-11-05','status':'candidate_pending_user_film_quality_review','whole_film_samples_viewed_frames':list(range(0,96,6)),'boundary_samples_viewed_frames':[0,6,12,15,18,21,24,27,30,36,42,48,51,54,57,60,63,66,72,78,84,90,95],'full_resolution_frames_viewed':[12,95],'technical_full_decode':True,'all_96_frames_extracted':True,'continuous_human_native_speed_review':False,'observation':'In sampled views, both heads/shoes remain visible, right hands and skirt flare remain within the revised crop. Left shows turn/bent knee; right side-to-front skirt motion then waist poses. Both use identical scale.','scale_tradeoff':'Approximately50–52% canvas height, smaller than v1 about57–60%; not the original full-frame74%.','join_observation':'Right join0.5–1.25s, left2–2.75s, each0.75s; only one panel dissolves at a time. Face mismatch appears lower in reordered samples, but double outlines of arms/legs remain.','limitations':['4s short edit, not the original planned10.5s','Skirt full back-turn and high V not used; originals retained','No certification of zero physical/anatomical/identity defects','Not a controlled single-variable comparison with v1 after framing and selection changes'],'user_layout_selected':'A parallel','user_film_acceptance':None,'publication_approval':None})
(P/'REVIEW.md').write_text('''# M03 A並排｜4秒修正版

2026-11-05。使用者已選左右並排、選適合欄寬的精彩動作。本片看同件海軍藍西外搭工作直褲／皮鞋與奶油A字裙／球鞋的輪廓和正式感差異。選用既有素材，不新增照片或影片生成。

左：側後轉、回看、屈膝，再接正面叉腰換重心；右：側身回正帶動裙擺，再接叉腰與肩臀變化。左右不強制同步。右側0.5–1.25秒、左側2–2.75秒各0.75秒淡接，避免兩邊同時混影；雙影仍存在。

實際4秒／96格／24fps／720×1280，無音無烙字、原速。每側固定同樣520像素寬裁切、相同縮放；人物約占畫高50–52%，比v1約57–60%小。4秒是既有可用選段的取捨，沒有凍結、重複、變速或光流補長。完整高V／裙裝後轉均保留在原始來源與全幅備選，未宣稱物理已修復。

本輪檢查也更正v1的邊界判讀：裙裝後轉時手指確有被135–585裁切切到。v2僅改順序仍有此問題；v3放寬560像素後仍有一刻手部出邊，且人物較小，均作內部測試保留、不列新待審。v4改選裙裝回正段，另留裙擺空間；已看全片每0.25秒16張、兩處接點密集樣本及0.5秒／末格完整畫面。解碼通過，96格均抽出；未可靠完成連續人工原速驗收。

精確來源與選段見 `edit_receipt.json`，本片SHA256 `'''+e['output_sha256']+'''`。使用者「ok」接續A方向，並非對這支尚未呈現的新修版、裙裝或發布的核准。M01／M02接受與褲裝來源表演接受仍保留。

[觀看4秒原速無音預覽](M03_W45_parallel_selected_review_v4.mp4)
''',encoding='utf-8')
for version,reason in [('paired_review_v2','Order-only test improves face alignment in sampled overlap but repeats skirt rear-turn hand clipping.'),('paired_review_v3','Wider560px crop still clips a hand near0.875s; figures smaller. Not selected for presentation.')]:
    p=BR/version/'edit_receipt.json';v=read(p);v.update(status='internal_test_not_promoted',visual_outcome=reason,latest_candidate=rel(P/'edit_receipt.json'));put(p,v)
v1=BR/'paired_review_v1/visual_review.json';v=read(v1);v['later_boundary_correction']='Later full-resolution review found skirt rear-turn hand clipping in original450px crop, contradicting the earlier sampled safety impression. v1 is retained, not promoted or user-rejected.';v['latest_candidate']=rel(P/'REVIEW.md');put(v1,v)
p=BR/'paired_review_v1/REVIEW.md';t=p.read_text(encoding='utf-8');note='最新：原5.25秒版保留。後續完整畫格發現裙裝後轉手部被欄邊切到；先前安全判讀已更正。現行待看是[4秒並排修正版](../paired_review_v4/REVIEW.md)，並非此v1獲成片核准。\n\n'
if note not in t:t=t.replace('\n\n','\n\n'+note,1);p.write_text(t,encoding='utf-8')
q=read(W/'production_queue.json');q.update(status='M03_parallel_v4_4s_pending_film_review',active_trial=rel(P),active_reviews=[e['output']],latest_edit_receipt=rel(P/'edit_receipt.json'));q['next']={'model':'M03','action':'Review exact4s A parallel candidate for perceived continuity, figure size and action/naturalness; no automatic generation or film/publication approval inferred.'};put(W/'production_queue.json',q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';r=read(rp);s=next(x for x in r['series'] if x['series_id']=='SERIES_W45_M03');s.update(status='layout_A_selected_v4_4s_quality_review_pending',latest_asset_receipt=rel(P/'edit_receipt.json'),current_reassessment=rel(P/'REVIEW.md'))
uid='USE_W45_M03_PARALLEL_SELECTED_V4_20261105';use={'usage_id':uid,'series_id':s['series_id'],'production_date':'2026-11-05','status':'candidate_pending_user_film_quality_review','film_path':e['output'],'film_sha256':e['output_sha256'],'receipt_path':rel(P/'edit_receipt.json'),'feedback_summary':'User selected A parallel layout; new4s complementary-pose edit retains larger figures than wider internal test, fixes sampled crop boundaries and staggers0.75s dissolves. Residual double outlines, shorter duration and smaller-than-v1 figures disclosed; no film/publication approval.','user_acceptance_receipt':None,'publication_url':None}
existing=next((u for u in r['uses'] if u['usage_id']==uid),None)
if existing:existing.update(use)
else:r['uses'].append(use)
if uid not in s['usage_ids']:s['usage_ids'].append(uid)
put(rp,r)
current='W45現況：M01精確10.25秒與M02 trial03已接受，尚無新交接／發布。M03兩張首圖與褲裝trial02表演接受保留，裙裝64c9236b尚待回饋；使用者已選A左右並排方向。現行待看A v4為4秒原速無音、左右錯開0.75秒淡接：左轉身／屈膝，右回正裙擺，最後叉腰比較；人物約畫高50–52%，仍有雙影。原5.25秒v1發現裙裝後轉切手，v2／v3為內部未採試作；B全幅19.333333秒留作備選。沒有新增生成，累計七次靜態／十二支原片／兩支接受成片。技術解碼／抽樣不等於連續人工原速QA，新修版未獲成片／發布核准；M04–M05與proof／Carousel仍缺。詳M03 expressive_parallel_2026-11-05/paired_review_v4/REVIEW.md。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
    p=ROOT/name;lines=p.read_text(encoding='utf-8-sig').splitlines()
    for i,line in enumerate(lines):
        if 'W45現況：' in line:lines[i]=line.split('W45現況：')[0]+current
        elif line.startswith('- 11/5完整換姿：'):lines[i]='- 11/5完整換姿：A並排方向已選，現行[4秒v4修正版](runs/2026-W45/reels/M03/expressive_parallel_2026-11-05/paired_review_v4/REVIEW.md)待品質回饋。舊v1裙裝後轉切手已更正，v2／v3僅內部試作；褲裝來源表演接受不擴成新片／發布。'
        elif line.startswith('2. M01／M02接受保留。'):lines[i]='2. M01／M02接受保留。M03 A排版已選、褲裝來源表演已接受；現行[4秒並排修正版](reels/M03/expressive_parallel_2026-11-05/paired_review_v4/REVIEW.md)待成片品質回饋，非發布核准。'
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(BR/'STATUS.md').write_text('''# M03 換姿研究｜有效狀態

更新：2026-11-05。使用者已選A左右並排方向。現行[4秒v4候選](paired_review_v4/REVIEW.md)待成片品質回饋，沒有發布核准。

- 褲裝trial02 414c5d81：精確來源表演已接受。裙裝64c9236b：已有原片，來源／新成片待回饋。兩張首圖核准有效。
- v1原5.25秒A：保留，後續查到裙裝後轉手部被欄邊切到，原邊界判讀已更正。
- v2重排、v3加寬：內部試作，仍有欄邊問題，未採作待看片，不視為使用者退件。
- v4改用互補選段與錯開接點，4秒／原速／無音／同尺度。人物約畫高50–52%，淡接仍有雙影。B完整依序19.333333秒留存備選。
- 沒有新圖片或影片生成。解碼及樣本檢查不等於連續人工原速驗收。M01／M02接受成片與18份企劃核准快照保持。
''',encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts'];assert all(h(ROOT/a['snapshot_path'])==a['sha256'] for a in snap)
put(P/'state_reconciliation.json',{'date':'2026-11-05','approved_snapshots_unchanged':len(snap),'new_generations':0,'weekly_video_sources':12,'weekly_accepted_finished_reels':2,'user_film_acceptance':None,'original_sources_and_v1_retained':True})
print(json.dumps({'current_review':e['output'],'seconds':4,'source_jobs_unchanged':12,'snapshots_unchanged':len(snap)}))
