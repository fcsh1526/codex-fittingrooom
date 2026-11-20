from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;B=P.parent;ROOT=B.parents[5];W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
feedback={'date':'2026-11-05','actor':'user','quote':'之前有看到另一個帳號有好的左右比較，不是kubo，但是你好像沒存到。先暫停左右比較的剪輯。進行下一個剪輯模式','scope':'Pause parallel-comparison editing across the current work; Kubo is not the remembered reference. Continue next nonparallel film. M03 v1 relative preference remains, not accepted or published.','unknown_reference':'The remembered account/reel has not been identified; do not claim Kubo is it.'}
put(P/'user_pause_parallel_2026-11-05.json',feedback)
q=read(W/'production_queue.json');assert q['video_jobs_completed']==16 and q['weekly_reels_user_accepted']==2
q.update(status='M04_single_sequential_preparing_first_still_M03_parallel_paused',active_reviews=[],active_trial=None,latest_performance_feedback=rel(P/'user_pause_parallel_2026-11-05.json'),latest_editorial_proposal='10_automation/runs/2026-W45/planning/M04/production_plan.json',next={'model':'M04','action':'Produce L01 Reel starting image candidate from approved weekly plan; request individual visual approval before motion. M03 parallel editing paused.'});put(W/'production_queue.json',q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(rp)
m03=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M03');m03.update(status='parallel_editing_paused_by_user',latest_performance_feedback=rel(P/'user_pause_parallel_2026-11-05.json'))
m04=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M04');m04.update(status='single_sequential_preparing_first_still');put(rp,reg)
new='W45現況：使用者明確暫停左右比較剪輯；記得的優秀雙欄參考不是Kubo，確切帳號尚未識別。M03的8秒v2退回，9秒v1相對較好但未接受發布，所有原片保留。已轉做原週企劃M04單畫面：先看深底花卉上衣與素色下身，再讀花色與衣料；原核准M04身份與整週分鏡作依據，首圖依規則待個別視覺核准。M01與M02兩支已接受；M04／M05與十套proof／Carousel尚未完成。暫停指示收據：`10_automation/runs/2026-W45/reels/M03/reference_storyboard_2026-11-05/editorial_feedback_2026-11-05/user_pause_parallel_2026-11-05.json`。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
 p=ROOT/name;txt=p.read_text(encoding='utf-8-sig');start=txt.index('W45現況：');end=txt.index('M03未獲成片／發布核准。',start)+len('M03未獲成片／發布核准。');txt=txt[:start]+new+txt[end:]
 txt=txt.replace('目前下一步：依使用者否決8秒v2及對IG感受的回饋，回到共同觀看節奏與表演設計，先評既有素材；9秒v1相對較好但非發布核准。','目前下一步：左右比較剪輯暫停，轉做M04單畫面花卉穿搭，首圖逐張核准後才進影片；記得的參考不是Kubo。')
 txt=txt.replace('4. 先做一支具體片，其他排隊。M05先做短段並排尺度比較；含接點的片先驗完整重疊段。每個相同機制兩次失敗後改設計。','4. 左右比較剪輯暫停，先做M04單畫面花卉穿搭；M05原並排提案亦暫不執行。含接點的片先驗完整重疊段。每個相同機制兩次失敗後改設計。')
 p.write_text(txt,encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for x in snap:assert hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256']
print(json.dumps({'status':q['status'],'protected_snapshots':len(snap)}))
