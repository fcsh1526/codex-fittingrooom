"""Record story-clarity rejection and return the active task to editorial review."""
import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'10_automation/CANONICAL_WORKFLOW.md').is_file());W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
film=HERE/'M03_W45_realism_trial01_silent_review.mp4';digest=hashlib.sha256(film.read_bytes()).hexdigest();assert digest=='f8d35d777a3f26ebcb7b29f691b816abcfc0d865f2388bb923d5404d78ae75b0'
p=HERE/'user_story_clarity_rejection_2026-11-04.json'
write(p,{'actor':'user','recorded_date':'2026-11-04','timezone':'Asia/Taipei','quote':'不行，在跟我說一次工作流。現在的測試片，情緒不知道要表達啥?','target_film':rel(film),'target_sha256':digest,'video_asset_id':'1f291b40-ddb4-423e-ac9a-daf8ea5ca766','decision':'rejected_emotional_purpose_unclear_return_to_workflow','requested_action':'Explain the current workflow and why this test has no clear readable emotional purpose.','assistant_interpretation':'The written friend-filming-outfit motive and coordinated turn did not create a legible emotional experience. A technical motion test does not substitute for viewer purpose/visible motivation. This is an editorial execution failure; specific physical/uncanny causes were not newly established.','scope':'Exact single-source test; approved stills and accepted M01/M02 remain intact.','new_media_authorized_by_this_reply':False,'publication_approval':None})
v=read(HERE/'visual_review.json');v.update(status='user_rejected_emotional_purpose_unclear',latest_user_feedback=rel(p),next='Explain and audit workflow first. Return to viewer purpose and legible situation/performance; do not auto-generate another gesture/smile variant.');write(HERE/'visual_review.json',v)
v=read(HERE/'submission.json');v.update(status='user_rejected_emotional_purpose_unclear',latest_user_feedback=rel(p));write(HERE/'submission.json',v)
r=HERE/'REVIEW.md';t=r.read_text(encoding='utf-8');r.write_text('> 最新：使用者以「情緒不知道要表達啥」否決此精確單鏡，要求重新說明工作流。回到觀看目的／可見情境的編輯檢討；下方為歷史檢查，非現行待審。\n\n'+t,encoding='utf-8')
q=read(W/'production_queue.json');q.update(status='M03_editorial_workflow_review_after_single_source_rejection',next={'model':'M03','action':'Explain current workflow and diagnose failure of legible emotional purpose. Return to viewer takeaway/situation/visible response before any further source or edit. No automatic test queued.','feedback_receipt':rel(p)},active_reviews=[]);write(W/'production_queue.json',q)
regp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(regp)
for u in reg.get('uses',reg.get('usages')):
    if u['usage_id']=='USE_W45_M03_REALISM_TRIAL01_20261104':u.update(status='user_rejected_emotional_purpose_unclear',feedback_receipt=rel(p),feedback_summary='User rejects unclear emotional meaning and asks workflow explanation. Return to editorial purpose/situation before further generation; no current pending source review.')
s=next(s for s in reg['series'] if s['series_id']=='SERIES_W45_M03');s.update(status='editorial_workflow_review_no_current_accepted_film',latest_asset_receipt=rel(p));write(regp,reg)
summary='W45現況：M01精確10.25秒與M02 trial03已接受，無新交接／發布。M03兩張首圖核准保留；10.5秒／7.375秒合片及6.041667秒真人感單鏡均退件。最新使用者指出單鏡「情緒不知道要表達啥」，要求重新說明工作流；現回到觀眾看點、可見情境／反應的編輯檢討，無排隊新生成、無待看片。網站驗證已恢復。累計仍七次內建靜態／九支原片／兩支接受片，M04–M05與proof／Carousel仍缺；既有動態QA限制保留。'
for f in [ROOT/'10_automation/CANONICAL_WORKFLOW.md',ROOT/'CURRENT_STATUS.md',ROOT/'10_automation/MIRA_EDITORIAL_HANDOFF.md',W/'publishing_structure.md']:
    lines=f.read_text(encoding='utf-8').splitlines()
    for i,l in enumerate(lines):
        if f.name=='CANONICAL_WORKFLOW.md' and l.startswith('現況與交接採短版有效摘要'):lines[i]='現況與交接採短版有效摘要，歷史備份於 `10_automation/history/`。'+summary+'精確回饋見 `runs/2026-W45/reels/M03/realism_reset_2026-11-04/trial_01/user_story_clarity_rejection_2026-11-04.json`。'
        elif f.name=='CURRENT_STATUS.md' and l.startswith('- W45現況：'):lines[i]='- '+summary
        elif f.name=='MIRA_EDITORIAL_HANDOFF.md' and l.startswith('先讀 [主工作流]'):lines[i]='先讀 [主工作流](CANONICAL_WORKFLOW.md)、[CURRENT_STATUS](../CURRENT_STATUS.md)、當週發布結構，再讀本頁與精確收據。'+summary+'最近已交付仍為W44。'
        elif f.name=='MIRA_EDITORIAL_HANDOFF.md' and l.startswith('- 目前下一步：'):lines[i]='- 目前下一步：依使用者要求說明工作流，檢討M03從內容目的到可見情境／情緒的執行落差。單鏡已退件，不再列待審；沒有自動新測試。原圖及M01／M02接受不重開。'
        elif f.name=='publishing_structure.md' and l.startswith('來源完整W45 v2企劃'):lines[i]='來源完整W45 v2企劃已確認。'+summary+' W44原交付保留。'
        elif f.name=='publishing_structure.md' and l.startswith('2. [M02 trial03]'):lines[i]='2. [M02 trial03](reels/M02/trial_03/REVIEW.md)與[M01 10.25秒片](reels/M01/paired_review_v1/REVIEW.md)已接受。M03兩支舊合片與新單鏡均退件；[最新單鏡回饋](reels/M03/realism_reset_2026-11-04/trial_01/user_story_clarity_rejection_2026-11-04.json)要求重新說明工作流，回編輯目的檢討；首圖核准保留。'
        elif f.name=='publishing_structure.md' and l.startswith('5. 原速逐鏡'):lines[i]='5. 原速逐鏡／接點／整片、使用者接受、交接與發文分開。七次內建靜態／九支原片，M01／M02共兩支接受片。M03全部現有候選退件，沒有待審片；連續人工QA缺項保留。十套proof／Carousel未完成，沒有實際IG發文。'
    f.write_text('\n'.join(lines)+'\n',encoding='utf-8')
f=W/'planning/M03/SHOT_CARDS.md';lines=f.read_text(encoding='utf-8').splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('狀態：'));lines[idx]='狀態：兩張首圖核准保留；兩支合片與真人感單鏡均退件。使用者要求重述工作流，現回到觀眾看點與可見情境／情緒檢討，無現行待審片或新生成排程。下方分鏡與剪輯資料為歷史。';f.write_text('\n'.join(lines)+'\n',encoding='utf-8')
f=HERE.parent/'REASSESSMENT.md';t=f.read_text(encoding='utf-8');t+='\n## 單鏡退件與工作流檢討\n\n最新使用者否決trial01，指出情緒目的不可讀，要求重述工作流。前述單鏡測試沒有通過，不能只歸因於身體／臉或腳步；文字動機與流暢動作並不自動讓觀眾讀懂。回到觀眾看點／可見情境／反應設計，沒有自動新生成或待審片。\n';f.write_text(t,encoding='utf-8')
print('Exact6.04s test rejected; workflow review active; no new media queued; counts and still approvals retained.')
