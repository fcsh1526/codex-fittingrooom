"""Record exact realism rejection; no media generation, re-cut, or provider change."""
import csv,hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5];W=ROOT/'10_automation/runs/2026-W45';M=HERE.parent;V2=M/'emotion_recut_2026-11-04'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
e=read(V2/'edit_receipt.json');film=V2/e['output_file'];assert sha(film)==e['output_sha256']=='001ff0dc8fa724c61fd42846689d9877bb0957be296e6c65d8a7dc48795e2022'
feedback={'actor':'user','recorded_date':'2026-11-04','timezone':'Asia/Taipei','quote':'不行，這有強烈的AI感。我不知道怎麼描述，但是有點恐怖谷效應的感覺','target_file':rel(film),'target_sha256':sha(film),'duration_seconds':7.375,'decision':'rejected_strong_AI_uncanny_feeling','scope':'Exact v2 whole-film realism/viewing discomfort, not rejection of approved stills, identity M03, all expressions/movements or other accepted films.','specific_frame_or_cause_provided':False,'assistant_action':'Stop further recuts of this source pair; reassess performance design and isolate a single-source realism test before rebuilding a film. No new generation in this turn.','publication_approval':None}
write(V2/'user_realism_rejection_2026-11-04.json',feedback)
r=read(V2/'visual_review.json');r.update(status='user_rejected_strong_AI_uncanny_feeling',latest_user_feedback=rel(V2/'user_realism_rejection_2026-11-04.json'),next='Do not re-present as pending or make a third recut from these sources. See realism_reset reassessment.');write(V2/'visual_review.json',r)
p=V2/'REVIEW.md';t=p.read_text(encoding='utf-8');p.write_text('> 最新：使用者以「強烈AI感／恐怖谷」否決此精確v2，停止本組素材重剪。下文保留當時抽樣與技術事實，非現行待審。見[重設](../realism_reset_2026-11-04/REASSESSMENT.md)。\n\n'+t,encoding='utf-8')
for trial in ['L01_trial_02','L02_trial_01']:
    p=M/trial/'submission.json';v=read(p);v.update(status='not_selected_for_current_realism_redesign',latest_whole_film_feedback=rel(V2/'user_realism_rejection_2026-11-04.json'),selection_scope_note='Whole film rejected; individual source cause not isolated. Preserve technical facts, do not infer per-frame user rejection.');write(p,v)
proof=V2/'proof_frame_lineage.json';r=read(proof);r.update(status='withdrawn_from_publish_ready_pending_source_reassessment',latest_whole_film_feedback=rel(V2/'user_realism_rejection_2026-11-04.json'),withdrawal_scope='Assistant withdraws video-derived proof candidate as part of rejected film review; user did not explicitly reject this isolated frame or approved AI stills.');write(proof,r)
p=W/'asset_requirements.csv'
with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for r in rows:
    if r['look_id']=='2026-W45-003-L02' and r['surface']=='reel' and r['role'] in ['medium_S03','styling_proof']:r.update(status='video_derived_candidate_withdrawn_pending_realism_reassessment',evidence_path=rel(proof))
with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
q=read(W/'production_queue.json');q.update(status='M01_M02_accepted_M03_realism_redesign',next={'model':'M03','action':'Use realism_reset reassessment. Existing source pair is no longer selected; no third recut. Next concrete test is one6s existing-approved-L01 full-view body/gaze/expression action, before any outfit join or camera approach. Not yet generated.'},active_reviews=[]);write(W/'production_queue.json',q)
regp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(regp);uses=reg.get('uses',reg.get('usages'))
for u in uses:
    if u['usage_id']=='USE_W45_M03_EMOTION_RECUT_V2_20261104':u.update(status='user_rejected_strong_AI_uncanny_feeling',feedback_receipt=rel(V2/'user_realism_rejection_2026-11-04.json'),feedback_summary='User rejects strongAI/uncanny feeling despite removing surprise. No third recut. Cause unisolated; redesign single-source integrated body/gaze/performance first.')
    if u['usage_id']=='USE_W45_M03_PAIRED_V1_20261104':u['current_reassessment']=rel(HERE/'REASSESSMENT.md')
s=next(s for s in reg['series'] if s['series_id']=='SERIES_W45_M03');s.update(status='realism_redesign_no_current_accepted_film',latest_asset_receipt=rel(V2/'user_realism_rejection_2026-11-04.json'),current_reassessment=rel(HERE/'REASSESSMENT.md'));write(regp,reg)
summary='W45現況：M01精確10.25秒片與M02 trial03已接受，無新增交接／發布。M03兩張首圖核准保留；原10.5秒版情緒被否決，7.375秒v2又因「強烈AI感／恐怖谷」退件，兩版均不列待審或可發布。停止此組來源重剪，轉為單鏡真人感／身體視線表情連動的源頭重設，短測草案已記、尚未生成。回饋未確定單一原因，不泛化為禁用微笑、行走或大動作。本輪零新生成／剪輯，累計七次內建靜態／八支原片／兩支接受片；M04–M05與十套proof／Carousel仍缺。'
for p in [ROOT/'10_automation/CANONICAL_WORKFLOW.md',ROOT/'CURRENT_STATUS.md',ROOT/'10_automation/MIRA_EDITORIAL_HANDOFF.md',W/'publishing_structure.md']:
    lines=p.read_text(encoding='utf-8').splitlines()
    for i,line in enumerate(lines):
        if p.name=='CANONICAL_WORKFLOW.md' and line.startswith('現況與交接採短版有效摘要'):lines[i]='現況與交接採短版有效摘要，歷史備份於 `10_automation/history/`。'+summary+'見 `runs/2026-W45/reels/M03/realism_reset_2026-11-04/REASSESSMENT.md`。'
        elif p.name=='CURRENT_STATUS.md' and line.startswith('- W45現況：'):lines[i]='- '+summary+' [M03重設](10_automation/runs/2026-W45/reels/M03/realism_reset_2026-11-04/REASSESSMENT.md)。'
        elif p.name=='MIRA_EDITORIAL_HANDOFF.md' and line.startswith('先讀 [主工作流]'):lines[i]='先讀 [主工作流](CANONICAL_WORKFLOW.md)、[CURRENT_STATUS](../CURRENT_STATUS.md)、當週發布結構，再讀本頁與精確收據。'+summary+'最近已交付仍為W44。'
        elif p.name=='MIRA_EDITORIAL_HANDOFF.md' and line.startswith('- 目前下一步：'):lines[i]='- 目前下一步：依[M03真人感重設](runs/2026-W45/reels/M03/realism_reset_2026-11-04/REASSESSMENT.md)先驗單鏡整體表演，尚未新生成；不重剪／重貼兩支退件片，也不重開既有首圖或M01／M02接受。沒有待使用者重看片項目。'
        elif p.name=='publishing_structure.md' and line.startswith('來源完整W45 v2企劃'):lines[i]='來源完整W45 v2企劃已確認。'+summary+' W44原交付保留。'
        elif p.name=='publishing_structure.md' and line.startswith('2. [M02 trial03]'):lines[i]='2. [M02 trial03](reels/M02/trial_03/REVIEW.md)與[M01 10.25秒片](reels/M01/paired_review_v1/REVIEW.md)已接受。M03兩版依情緒／強烈AI感退件，停止此組素材重剪，見[源頭重設](reels/M03/realism_reset_2026-11-04/REASSESSMENT.md)；首圖核准保留。'
        elif p.name=='publishing_structure.md' and line.startswith('5. 原速逐鏡'):lines[i]='5. 原速逐鏡／接點／整片、使用者接受、交接與發文分開。七次內建靜態／八支原片；M01與M02共兩支接受片，M03兩版已退件、無現行待審片。完整連續人工原速QA沒有補寫通過，十套proof／Carousel未完成，沒有實際IG發文。'
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=W/'planning/M03/SHOT_CARDS.md';lines=p.read_text(encoding='utf-8').splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('狀態：'));lines[idx]='狀態：兩張首圖核准保留；10.5秒v1與7.375秒v2均退件，停止同組素材剪點修補。現行[單鏡真人感重設](../../reels/M03/realism_reset_2026-11-04/REASSESSMENT.md)尚未生成；下方分鏡／實際剪輯均為歷史，不能再作待審片。';p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for a in snap:assert sha(ROOT/a['snapshot_path'])==a['sha256']
write(HERE/'verification.json',{'date':'2026-11-04','rejected_v2_hash_verified':True,'snapshot_count':len(snap),'approved_snapshot_hashes_unchanged':True,'new_still_calls':0,'new_video_jobs':0,'new_edit_outputs':0,'current_M03_film_accepted':False,'pending_film_reviews':0,'M01_M02_acceptance_retained':True,'cause_is_hypothesis_not_established':True})
print('Exact v2 rejected; current summaries/queue/registry reconciled;18 approved snapshots unchanged; no new media.')
