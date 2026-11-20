from pathlib import Path
import hashlib, json

ROOT = Path.cwd()
W = ROOT / '10_automation/runs/2026-W45'
P = W / 'reels/M04/production_2026-11-06'
D = W / 'reels/M04/editorial_reset_2026-11-06'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p, obj): p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def rel(p): return p.relative_to(ROOT).as_posix()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

film = P/'M04_W45_floral_single_review_v1.mp4'
assert sha(film) == '4feb9e3016587963605548f5cfcf8dc03d140494b8e25965a0de2a37f7757067'
quote = '不行，做了幾次感覺都是舊做法。前一週的幾個影片還有幾部令人驚豔的'
receipt = D/'user_feedback.json'
assert not receipt.exists(), 'Feedback already recorded; do not overwrite later states.'
status = 'M04_v1_user_rejected_editorial_redesign_required'
put(receipt, {'date':'2026-11-06','actor':'user','quote':quote,'decision':'reject_current_film_return_to_editorial_design',
    'film_path':rel(film),'film_sha256':sha(film),'scope':'Current M04 cut rejected as repetitive old approach; user recalls stronger W44 films without naming exact favorites.',
    'still_approval_retained':True,'prior_accepted_films_retained':True,'parallel_pause_retained':True,
    'analysis':rel(D/'REVIEW.md'),'new_generation_jobs':0,'publication_approval':False})

q = read(W/'production_queue.json')
q.update(status=status,active_reviews=[],active_trial=None,latest_performance_feedback=rel(receipt),latest_editorial_reassessment=rel(D/'REVIEW.md'),
    next={'model':'M04','action':'Rebuild connected performance/storyboard against accepted W44 M02 second-shot benchmark. Current full/detail/full v1 rejected; do not continue cosmetic recuts. Parallel remains paused.'})
q['stills_note']='Nine builtin still calls: prior seven plus M04 initial face-drift candidate and corrected face_v2. Six exact look starting stills approved; proofs/Carousels incomplete. Still approval is not film acceptance.'
put(W/'production_queue.json',q)
for name in ['edit_receipt.json','execution_plan.json']:
    obj=read(P/name)
    obj['status_before_latest_feedback']=obj['status']
    obj.update(status=status,latest_user_feedback=rel(receipt))
    put(P/name,obj)

rp=ROOT/'04_prompts/material_pool/series_registry.json'
reg=read(rp)
s=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M04')
s.update(status=status,current_reassessment=rel(D/'REVIEW.md'),latest_feedback_receipt=rel(receipt))
u=next(x for x in reg['uses'] if x['usage_id']=='USE_W45_M04_FLORAL_SINGLE_V1_20261106')
u.update(status='user_rejected',latest_feedback_receipt=rel(receipt),feedback_summary='User rejects M04 full/detail/full v1 as repetitive old approach and recalls stronger W44 films. Return to viewer hook, performance and connected storyboard; exact approved starting still retained. No new generation or publication.')
put(rp,reg)

new='W45現況：左右比較剪輯仍暫停，記得的優秀雙欄參考不是Kubo，確切帳號未識別。M03的8秒v2退回，9秒v1僅相對較好。11/6使用者否決M04的8.54秒全身→細節→全身初剪，指出反覆沿用舊做法、W44曾有更驚豔成果；M04退回看點與表演企劃，停止同案微調。已回查W44明確肯定的M02第二鏡及M04日常片段，詳 `10_automation/runs/2026-W45/reels/M04/editorial_reset_2026-11-06/REVIEW.md`。M04 face_v2精確首圖核准保留，原片／初剪留存，沒有新生成。累計九次靜態／十七支原片，M01／M02兩支已接受；M05及十套proof／Carousel未完成，無本週新交接或發布。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
    p=ROOT/name
    txt=p.read_text(encoding='utf-8-sig')
    start=txt.index('W45現況：'); end=txt.index('\n',start)
    txt=txt[:start]+new+txt[end:]
    txt=txt.replace('目前下一步：M04 face_v2圖已核准；檢視新8.54秒單畫面初剪的表演、花紋和兩處接點疊影。左右比較仍暫停。','目前下一步：M04初剪已退件；以上週明確獲肯定的M02第二鏡為表演基準，重做觀看吸引點與連接分鏡，再推導必要素材。原首圖核准保留，左右比較仍暫停。')
    txt=txt.replace('| M04 | 深底花卉只放上衣，下身素色；再讀花色 | 1 | 2 | 初剪8.54秒 | [M04初剪](reels/M04/production_2026-11-06/REVIEW.md) |','| M04 | 花卉搭素色主張保留；觀看吸引點與表演退回重設 | 1 | 2 | 待新分鏡 | [退件與對照](reels/M04/editorial_reset_2026-11-06/REVIEW.md) |')
    txt=txt.replace('4. 左右比較剪輯暫停，先做M04單畫面花卉穿搭；M05原並排提案亦暫不執行。含接點的片先驗完整重疊段。每個相同機制兩次失敗後改設計。','4. 左右比較剪輯暫停，M05原並排提案亦暫不執行。M04初剪已否決，退回看點、表演及連接分鏡，先與W44已接受基準具體比較，不延續同案裁切／轉場微調。含接點的片先驗完整重疊段；每個相同機制兩次失敗後改設計。')
    p.write_text(txt,encoding='utf-8')

review=P/'REVIEW.md'
txt=review.read_text(encoding='utf-8-sig')
head,body=txt.split('\n',1)
review.write_text(head+'\n\n最新：此精確初剪已於11/6遭使用者否決，原因為反覆沿用舊做法、缺少上週成果的驚豔感。退回企劃，詳 `../editorial_reset_2026-11-06/REVIEW.md` 與精確回饋收據。下文為當時初剪與審查紀錄，不再是待使用者接受任務。\n'+body,encoding='utf-8')

snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for item in snap: assert sha(ROOT/item['snapshot_path'])==item['sha256']
protected={
    W/'reels/M01/paired_review_v1/M01_W45_two_looks_review_v1.mp4':'aa1a657e88480a966226bdbf72ea3e5c46346290df154408d376ebcc2b27a2fb',
    W/'reels/M02/trial_03/M02_W45_trial03_silent_review.mp4':'bf1828d34ce61ac76e82d1573a49e85d8403d5a5ae9be9bb8be46c16fa114b67',
    ROOT/'10_automation/runs/2026-W44/M02_restart_2026-10-30/M02_restart_review_v2_trim1s.mp4':'e2684e812007df1900fcc89987c7f2d21fa461122b075988e0b153d02c6d6ff3',
}
for path,digest in protected.items(): assert sha(path)==digest
assert (q['builtin_image_calls'],q['video_jobs_completed'],q['weekly_reels_user_accepted'])==(9,17,2)
put(D/'verification.json',{'date':'2026-11-06','protected_snapshots':len(snap),'protected_film_hashes_verified':len(protected),'new_generation_jobs':0,'active_reviews_cleared':True,'counts_unchanged':[9,17,2],'original_M04_film_preserved':sha(film)})
print(json.dumps({'status':status,'protected_snapshots':len(snap),'protected_films':len(protected),'new_generation_jobs':0}))
