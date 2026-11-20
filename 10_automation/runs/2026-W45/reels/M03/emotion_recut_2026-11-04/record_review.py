"""Record user-rejected emotion and the exact new local-only review candidate."""
import csv,hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5];W=ROOT/'10_automation/runs/2026-W45';OLD=HERE.parent/'paired_review_v1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
e=read(HERE/'edit_receipt.json');film=HERE/e['output_file'];assert sha(film)==e['output_sha256']
assert e['output_sha256']=='001ff0dc8fa724c61fd42846689d9877bb0957be296e6c65d8a7dc48795e2022'
assert sha(OLD/'M03_W45_two_looks_review_v1.mp4')==e['old_film_preserved_sha256']
for s in e['sources']:assert sha(ROOT/s['path'])==s['sha256']
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for s in snap:assert sha(ROOT/s['snapshot_path'])==s['sha256']
review={'date':'2026-11-04','status':'emotion_recut_v2_pending_user_review','film':rel(film),'sha256':sha(film),'duration_seconds':7.375,'user_feedback':rel(OLD/'user_emotion_feedback_2026-11-04.json'),'source_interpretation':'The original independent laugh/surprise/talking reactions reset emotion. Source selection now attempts one connected smile/brighten/approach/smile arc; not an objective emotion classifier output.','observed_samples':{'source_selection':'L02 .75–2.5s every .125s; L01 1.5–4s every .25s; L02 5–7s every .25s','whole_film':'0–7s every .5s plus7.333s finalframe','join':'All18overlap frames pluscontext at1.75/2.75/3s, full frame and face diagnostic crops','approach_ending':'4–7.25s every .25s; final native720x1280frame inspected'},'observations':['The surprised rounded-mouth L02 opening no longer appears as a clear shot. The two sides now both progress from a smile toward a wider happy expression.','L01 is cut before its sustained big laugh/head tilt; later L02 speech-like mouth changes are excluded, with an open-eyed smiling last frame.','The0.75s dissolve still has face/body/hand and skirt/trouser double outlines around2–2.75s. No seamless transition claim.','Shorter edit trades away reading time: trousers about2s fully clear; skirt/sneakers about1.25s fully clear after the dissolve before shoe cropping, plus partially overlapped full view. This remains a clothing-readability review issue.','L02 subject steps and framing approach are unchanged; no new physical-gait or camera-only success inferred.'],'technical':{'full_decode':'completed','source_mapping':read(HERE/'source_mapping_check.json'),'native_speed':True,'full_raster':True,'new_generation':False},'continuous_human_visual_review':False,'user_acceptance':None,'publication_approval':None,'next':'Show exact7.375s candidate for native-speed emotional continuity, reading time and transition comfort review. Do not regenerate the same performance mechanism without a new source/design rationale.'}
write(HERE/'visual_review.json',review)
oldreview=read(OLD/'visual_review.json');oldreview.update(status='not_accepted_emotional_continuity_needs_repair',user_feedback=rel(OLD/'user_emotion_feedback_2026-11-04.json'),superseded_by_candidate=rel(film),next='Historical rejected candidate. Do not reopen as pending or publish; see emotion_recut v2.');write(OLD/'visual_review.json',oldreview)
p=OLD/'REVIEW.md';text=p.read_text(encoding='utf-8');p.write_text('> 11/4後續：使用者指出「整體情緒很怪」，此精確10.5秒版未接受，保留作歷史。現行候選為[7.375秒情緒重剪v2](../emotion_recut_2026-11-04/REVIEW.md)。\n\n'+text,encoding='utf-8')
(HERE/'REVIEW.md').write_text('''# M03 情緒重剪 v2

2026-11-04。使用者對原10.5秒版回饋「整體情緒很怪」，該片未接受。現以相同原片另剪7.375秒／177格、720×1280／24fps、原速無音無字候選，沒有新增生成或替換原片。

情緒設計：先帶著笑容看鏡頭，笑容延續到第二套，開心走近，再以微笑收尾。不再將兩次獨立的「認出朋友」反應串成同一場事件，也不以不存在的對話解釋嘴型。

- L01 trial02取[0,66)／0–2.75秒，在持續大笑和抬頭前換裝。
- L02 trial01取[33,162)／1.375–6.75秒，跳過驚訝開頭及說話感尾段。
- 0.75秒疊化保留，全片2–2.75秒；短暫臉／手／裙褲重疊仍存在。
- 代價：完整清晰讀衣約褲裝2秒、裙裝1.25秒；裙裝全身另有部分疊化展示。後半中景約1.75秒。較短的讀衣時間仍須看片判斷，不能單憑情緒改善宣稱整片合格。

技術解碼與159個非疊化來源影格對應通過。已檢視全片抽樣、逐格接點、臉部診斷、靠近與原尺寸末格；未具備助理連續原速觀看證據，使用者本版接受／發布／交接均未取得。不將抽格當作原速全片審查。

原來源、兩張首圖及既有M01／M02接受均保留。W45累計七次內建靜態、八支原片、兩支接受片；本次只重剪，零新生成。新候選精確SHA見edit_receipt.json。
''',encoding='utf-8')
# The same source-native proof frame is still within this edit; change only timeline lineage.
proof=read(OLD/'proof_frame_lineage.json');proof.update(current_film=rel(film),current_film_sha256=sha(film),whole_film_frame=159,whole_film_seconds=6.625,source_proof_record=rel(OLD/'proof_frame_lineage.json'),scope='Same unchanged source f144, medium styling-proof candidate. New timeline correspondence only; not new generation, Carousel or acceptance.')
write(HERE/'proof_frame_lineage.json',proof)
p=W/'asset_requirements.csv'
with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for r in rows:
    if r['look_id']=='2026-W45-003-L02' and r['surface']=='reel' and r['role'] in ['medium_S03','styling_proof']:r['evidence_path']=rel(HERE/'proof_frame_lineage.json')
with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
q=read(W/'production_queue.json');q.update(status='M01_M02_accepted_M03_emotion_recut_v2_pending_user_review',next={'model':'M03','action':'Review exact7.375s emotion recut v2; original10.5s film not accepted for emotional continuity. Judge smile progression, shorter full-skirt reading time and2–2.75s dissolve. No new generation this repair.'},active_reviews=[{'model':'M03','scope':'exact7.375s emotion recut v2, whole film','receipt':'reels/M03/emotion_recut_2026-11-04/visual_review.json','answer':None}]);write(W/'production_queue.json',q)
regp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(regp);uses=reg.get('uses',reg.get('usages'))
for u in uses:
    if u['usage_id']=='USE_W45_M03_PAIRED_V1_20261104':u.update(status='not_accepted_emotional_continuity_needs_repair',feedback_receipt=rel(OLD/'user_emotion_feedback_2026-11-04.json'),feedback_summary='User asks expression purpose, then says overall emotion strange. Exact10.5s film not accepted; not a rejection of approved stills/other films.')
uid='USE_W45_M03_EMOTION_RECUT_V2_20261104'
entry={'usage_id':uid,'series_id':'SERIES_W45_M03','content_week':'2026-W45','source_weeks':['2026-W44','2026-W45'],'production_date':'2026-11-04','model_profile_id':'M03','look_ids':['2026-W45-003-L01','2026-W45-003-L02'],'film_path':rel(film),'film_sha256':sha(film),'receipt_path':rel(HERE/'edit_receipt.json'),'status':'emotion_recut_candidate_pending_user_review','feedback_summary':'Local-only7.375s recut avoids surprise opening and speech-like ending.0.75s ghosting, shorter full-skirt reading interval and continuous dynamic QA gap remain. No new generation.','publication_date':None,'post_url':None,'metrics':None}
existing=next((u for u in uses if u['usage_id']==uid),None)
if existing:existing.update(entry)
else:uses.append(entry)
s=next(s for s in reg['series'] if s['series_id']=='SERIES_W45_M03');s.update(status='emotion_recut_v2_whole_film_pending_user_review',latest_asset_receipt=rel(HERE/'visual_review.json'))
if uid not in s['usage_ids']:s['usage_ids'].append(uid)
write(regp,reg)
summary='W45現況：M01精確10.25秒片與M02 trial03已接受，無新增交接／發布。M03兩張首圖已核准；使用者指出原10.5秒版「整體情緒很怪」，該版未接受。現用相同原片另剪7.375秒情緒v2候選，跳過驚訝開頭與說話感尾段，待原速整片回饋；2–2.75秒短暫疊影、裙裝清楚全身約1.25秒及連續人工動態QA缺項保留。本次零新生成，累計七次內建靜態／八支原片／兩支接受片；M04–M05與十套proof／Carousel仍缺。'
files=[ROOT/'10_automation/CANONICAL_WORKFLOW.md',ROOT/'CURRENT_STATUS.md',ROOT/'10_automation/MIRA_EDITORIAL_HANDOFF.md',W/'publishing_structure.md']
for p in files:
    lines=p.read_text(encoding='utf-8').splitlines()
    for i,line in enumerate(lines):
        if p.name=='CANONICAL_WORKFLOW.md' and line.startswith('現況與交接採短版有效摘要'):lines[i]='現況與交接採短版有效摘要，歷史備份於 `10_automation/history/`。'+summary+'見 `runs/2026-W45/reels/M03/emotion_recut_2026-11-04/REVIEW.md`。'
        elif p.name=='CURRENT_STATUS.md' and line.startswith('- W45現況：'):lines[i]='- '+summary+' [現行M03](10_automation/runs/2026-W45/reels/M03/emotion_recut_2026-11-04/REVIEW.md)。'
        elif p.name=='MIRA_EDITORIAL_HANDOFF.md' and line.startswith('先讀 [主工作流]'):lines[i]='先讀 [主工作流](CANONICAL_WORKFLOW.md)、[CURRENT_STATUS](../CURRENT_STATUS.md)、當週發布結構，再讀本頁與精確收據。'+summary+'最近已交付仍為W44。'
        elif p.name=='MIRA_EDITORIAL_HANDOFF.md' and line.startswith('- 目前下一步：'):lines[i]='- 目前下一步：看[M03精確7.375秒情緒重剪](runs/2026-W45/reels/M03/emotion_recut_2026-11-04/REVIEW.md)的原速整片，確認情緒／讀衣／疊化；原10.5秒版已因情緒回饋退回，不再列待審。兩張首圖及M01／M02不重開；其餘依隊列。'
        elif p.name=='publishing_structure.md' and line.startswith('來源完整W45 v2企劃'):lines[i]='來源完整W45 v2企劃已確認。'+summary+' W44原交付保留。'
        elif p.name=='publishing_structure.md' and line.startswith('2. [M02 trial03]'):lines[i]='2. [M02 trial03](reels/M02/trial_03/REVIEW.md)與[M01 10.25秒片](reels/M01/paired_review_v1/REVIEW.md)已接受。M03原10.5秒版情緒不成立、未接受；現看[7.375秒情緒v2](reels/M03/emotion_recut_2026-11-04/REVIEW.md)，新圖核准保留。'
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=W/'planning/M03/SHOT_CARDS.md';lines=p.read_text(encoding='utf-8').splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('狀態：'));lines[idx]='狀態：兩張首圖核准保留。原10.5秒片被指出「整體情緒很怪」，未接受；現行[7.375秒情緒v2](../../reels/M03/emotion_recut_2026-11-04/REVIEW.md)只用原片重剪。原v2分鏡與下方10.5秒執行為歷史，現行精確時間以下方最新收據為準。';lines+=['','## 11/4情緒回饋後的重剪','','L01[0,66)→L02[33,162)，18格疊化在全片2–2.75秒，177格7.375秒。微笑延續、笑容展開後靠近、微笑收尾；去掉重複驚訝與尾段說話感。完整裙裝閱讀時間縮短，仍待使用者原速觀看；本次零新圖／原片，沒有改變已核准服裝、身份或既有M01／M02接受。'];p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
verification={'date':'2026-11-04','output_sha256':sha(film),'snapshot_count':len(snap),'snapshot_hashes_unchanged':True,'original_film_and_source_hashes_unchanged':True,'new_still_calls':0,'new_video_jobs':0,'complete_decode':'passed','frame_mapping':read(HERE/'source_mapping_check.json'),'continuous_visual_review':False,'user_acceptance':None,'publication_approval':None}
write(HERE/'record_verification.json',verification)
print(json.dumps(verification,ensure_ascii=False))
