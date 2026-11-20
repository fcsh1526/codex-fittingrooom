"""Keep a CAPTCHA-dependent request unsubmitted; reconcile actual counters."""
import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'10_automation/CANONICAL_WORKFLOW.md').is_file());W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
s=read(HERE/'submission.json');assert s['actual_new_jobs_submitted']==0
write(HERE/'user_test_authorization_2026-11-04.json',{'actor':'user','quote':'好','date':'2026-11-04','timezone':'Asia/Taipei','scope':'Proceed with one redesigned M03 single-source body/gaze/expression realism test from the approved L01 still before rebuilding a two-look film.','limits':'Not approval of an unseen output, publication or new AI still.','prepared_request':rel(HERE/'grok_request.txt')})
q=read(W/'production_queue.json');q.update(status='M03_single_source_test_prepared_site_verification_required',next={'model':'M03','action':'User completes current Grok Cloudflare human verification, then submit existing trial01/grok_request.txt exactly once. It has NOT been sent. Keep7builtin still calls/8video sources until actual submission/result.','prepared_request':rel(HERE/'grok_request.txt'),'submission_record':rel(HERE/'submission.json')},active_reviews=[]);write(W/'production_queue.json',q)
regp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(regp);series=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M03');series.update(status='single_source_test_authorized_prepared_site_human_verification_required',latest_asset_receipt=rel(HERE/'submission.json'));write(regp,reg)
summary='W45現況：M01精確10.25秒與M02 trial03已接受，無新交接／發布。M03兩張首圖核准保留，10.5秒v1與7.375秒v2均退件，不再重剪此組來源。使用者「好」同意改做單鏡身體／視線／表情連動測試；6秒trial01的凍結指令、素材及檢查程式已備妥，但Grok出現Cloudflare真人驗證，請求尚未送出，等待使用者完成網站驗證。沒有點擊／繞過驗證，沒有新生成；累計仍七次內建靜態／八支原片／兩支接受片，M04–M05與proof／Carousel仍缺。'
for p in [ROOT/'10_automation/CANONICAL_WORKFLOW.md',ROOT/'CURRENT_STATUS.md',ROOT/'10_automation/MIRA_EDITORIAL_HANDOFF.md',W/'publishing_structure.md']:
    lines=p.read_text(encoding='utf-8').splitlines()
    for i,l in enumerate(lines):
        if p.name=='CANONICAL_WORKFLOW.md' and l.startswith('現況與交接採短版有效摘要'):lines[i]='現況與交接採短版有效摘要，歷史備份於 `10_automation/history/`。'+summary+'精確狀態見 `runs/2026-W45/reels/M03/realism_reset_2026-11-04/trial_01/submission.json`。'
        elif p.name=='CURRENT_STATUS.md' and l.startswith('- W45現況：'):lines[i]='- '+summary
        elif p.name=='MIRA_EDITORIAL_HANDOFF.md' and l.startswith('先讀 [主工作流]'):lines[i]='先讀 [主工作流](CANONICAL_WORKFLOW.md)、[CURRENT_STATUS](../CURRENT_STATUS.md)、當週發布結構，再讀本頁與精確收據。'+summary+'最近已交付仍為W44。'
        elif p.name=='MIRA_EDITORIAL_HANDOFF.md' and l.startswith('- 目前下一步：'):lines[i]='- 目前下一步：使用者完成Grok網站真人驗證後，按[M03單鏡trial01狀態](runs/2026-W45/reels/M03/realism_reset_2026-11-04/trial_01/submission.json)送出已備妥的一次6秒請求。尚未送出，不得重送當重試；若已恢復，先查當前畫布與精確結果再動作。已核准首圖不重問，兩支退件片不再列待審。'
        elif p.name=='publishing_structure.md' and l.startswith('來源完整W45 v2企劃'):lines[i]='來源完整W45 v2企劃已確認。'+summary+' W44原交付保留。'
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=HERE.parent/'REASSESSMENT.md';t=p.read_text(encoding='utf-8');t+='\n## 使用者同意與執行狀態補記\n\n使用者後續「好」同意推進上述單鏡測試。trial_01凍結prompt／精確輸入與檢查程式已準備；返回原Grok畫布後出現Cloudflare真人驗證。請求尚未送出，沒有新生成或點擊驗證，已請使用者在目前頁面完成。恢復後使用既有grok_request.txt單次送出，毋須重開首圖核准。\n';p.write_text(t,encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for a in snap:assert hashlib.sha256((ROOT/a['snapshot_path']).read_bytes()).hexdigest()==a['sha256']
write(HERE/'pre_submit_verification.json',{'date':'2026-11-04','request_prepared':True,'request_submitted':False,'new_video_jobs':0,'new_still_calls':0,'approved_snapshot_count':len(snap),'snapshot_hashes_unchanged':True,'site_verification':'user_action_requested','challenge_clicked_or_solved':False})
print('Prepared, NOT submitted; site human verification required; counts unchanged;18 approved snapshots preserved.')
