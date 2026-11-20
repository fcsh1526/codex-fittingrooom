"""Reconcile one full-source test, technical evidence and unresolved realism review."""
import hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'10_automation/CANONICAL_WORKFLOW.md').is_file());W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
s=read(HERE/'submission.json');tech=read(HERE/'technical_review.json');integrity=read(HERE/'prompt_integrity.json')
assert integrity['prompt_match_whitespace_normalized'] and s['video_asset_id'] in integrity['post_url']
assert any(s['video_asset_id'] in m['src'] for m in integrity['media'])
assert sha(HERE/'source.mp4')==tech['source_sha256']=='5deb6d9d08e89d85a2143493108e7ff87354c7429880fce917ea503f971b2514'
film=HERE/'M03_W45_realism_trial01_silent_review.mp4';assert sha(film)==tech['silent_review_sha256']=='f8d35d777a3f26ebcb7b29f691b816abcfc0d865f2388bb923d5404d78ae75b0'
assert tech['frame_count']==145 and tech['silent_remux_frame_and_timing_hashes_identical']
approval=read(ROOT/s['source_still_approval']);assert sha(ROOT/approval['asset_path'])==approval['target_sha256']==s['source_still_sha256']
feedback={'actor':'user','quote':'已完成驗證','recorded_date':'2026-11-04','scope':'User reports completing Grok Cloudflare site verification; the original Mira canvas was then visibly available. Not approval of a generated video.','actual_agent_challenge_action':'none'}
write(HERE/'site_verification_resolved_2026-11-04.json',feedback)
review={'date':'2026-11-04','status':'full_source_test_pending_realism_and_motion_review_not_usable_master','film_path':rel(film),'film_sha256':sha(film),'duration_seconds':tech['duration_seconds'],'frame_count':145,'fps':24,'raster':[720,1280],'generation_jobs_this_test':1,'new_still_calls':0,'viewer_purpose':'Full work outfit/blazer side line, testing coordinated body/gaze/expression before any outfit join.','observations':['0–about.75s mostly frontal; about1–1.75s hip/shoulder turn with head tilt and smile; about2–3s returns frontal; about3.25–4s turns into near-profile and holds toward6s.','There is more body/head/gaze development than in the previous planted-body source. The generator added a return/front phase and another turn rather than a single small turn; not exact choreography compliance.','Smile remains present through the sampled sequence, with a brief eyes-closed moment around3.25s. Whether it feels natural or uncanny is unresolved; sampled smiling faces do not certify realism.','Foot orientations change during the turns with little visible lift in quarter-second samples. Pivot/sliding concern remains; not a no-slip physical pass.','Bag becomes wider/flap-facing as the body turns and shoes change apparent outline in profile. Unseen bag surfaces/perspective versus generated shape inconsistency are not isolated; no accessory-continuity pass.','Hair and shoes stay in frame; no obvious sampled extreme head enlargement or internal cut. This is not an identity/proportion guarantee.'],'evidence':{'whole_source_samples':'13 frames0–6s at.5s intervals','turn_samples':'15frames.75–4.25s at.25s intervals, face/hands-bag/feet diagnostic crops','native_UI':'Exact post observed playing at1x atabout5.30s; intermittent observation only, no uninterrupted full-source viewing claimed.','prompt_integrity':'Exact URL/mediaUUID/visible prompt matched frozen input; generator internal call not directly visible.'},'technical':{'full_decode':'completed','silent_remux_frames_and_timing_identical':True,'speed':1,'cuts':False,'crop':False,'rescale':False,'freeze':False,'text':False},'continuous_human_visual_review':False,'realism_pass':None,'physical_motion_pass':None,'user_clip_acceptance':None,'whole_film_acceptance':None,'publication_approval':None,'external_delivery':None,'next':'Present exact uncut native6.041667s test for whole-person realism and motion review. Do not auto-retry, trim to conceal concerns or extend L02 before this test is evaluated.','inference_limit':'Several linked performance constraints were redesigned together; this is not a controlled single-variable causal demonstration.'}
write(HERE/'visual_review.json',review)
s.update(status='full_source_test_pending_user_realism_review_not_usable_master',review_file=film.name,source_sha256=tech['source_sha256'],silent_review_sha256=sha(film),actual_new_jobs_completed=1,site_verification='resolved_by_user_canvas_verified',blocker=None);write(HERE/'submission.json',s)
(HERE/'REVIEW.md').write_text('''# M03 真人感單鏡測試01

2026-11-04。使用者完成網站驗證後，原Mira畫布單次生成一支新片。保留全部6.041667秒／145格、720×1280／24fps；無音副本與來源逐格／時序相同，無剪點、換裝、疊化、變速、裁切或停格。

實際表演先小轉肩，再回正面，再轉近側身停住，超出原設計的一次小轉身。比先前有更多身體／頭與視線變化，但笑容仍持續，真人感未判通過。

13個全片抽樣與15個轉身抽樣已檢視。腳在原地轉向、鞋底抬起不清，仍有滑轉疑慮；肩包轉身後顯出更寬的翻蓋面，未釐清透視／未見面與生成形狀變化。手包、步足及自然感均不列通過，不憑臉部抽樣推薦可用。

技術解碼、無音影格等同性與精確網址／媒體UUID／prompt核對完成；原頁1倍速約5.3秒狀態曾觀測，沒有助理連續原速全片觀看證據。本片是待評估測試，未列可用素材／成片／發布，也未延伸L02。保留全長供判斷，不再剪掉不理想區間充數；沒有自動重試。

來源首圖仍是已核准L01 framing_v2，身份M03 v3；零新圖、一支新原片。W45累計七次內建靜態／九支原片／兩支既有接受片，先前兩支M03退件狀態不變。

精確原片／無音片SHA、可用控制與限制見submission.json、technical_review.json及visual_review.json。
''',encoding='utf-8')
q=read(W/'production_queue.json');q.update(status='M03_realism_trial01_full_source_pending_user_review',video_jobs_submitted=9,video_jobs_completed=9,next={'model':'M03','action':'Review exact6.041667s uncut realism trial01 for whole-person naturalness, turn/foot and bag concerns. Not a usable master; no L02 extension or automatic retry.','receipt':rel(HERE/'visual_review.json')},active_reviews=[{'model':'M03','scope':'exact uncut6.041667s realism trial01','receipt':'reels/M03/realism_reset_2026-11-04/trial_01/visual_review.json','answer':None}]);write(W/'production_queue.json',q)
regp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(regp);uses=reg.get('uses',reg.get('usages'));uid='USE_W45_M03_REALISM_TRIAL01_20261104'
entry={'usage_id':uid,'series_id':'SERIES_W45_M03','content_week':'2026-W45','source_weeks':['2026-W44','2026-W45'],'production_date':'2026-11-04','model_profile_id':'M03','look_ids':['2026-W45-003-L01'],'film_path':rel(film),'film_sha256':sha(film),'receipt_path':rel(HERE/'submission.json'),'status':'single_source_realism_test_pending_user_review_not_usable_master','feedback_summary':'Uncut6.04s source, no outfit transition. Body/gaze turn varies from plan; foot pivots, persistent smile and bag outline remain concerns. No realism/physical/publication pass.','publication_date':None,'post_url':None,'metrics':None}
existing=next((u for u in uses if u['usage_id']==uid),None)
if existing:existing.update(entry)
else:uses.append(entry)
series=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M03');series.update(status='single_source_realism_trial01_pending_review_not_usable_master',latest_asset_receipt=rel(HERE/'visual_review.json'))
if uid not in series['usage_ids']:series['usage_ids'].append(uid)
write(regp,reg)
summary='W45現況：M01精確10.25秒與M02 trial03已接受，無新交接／發布。M03兩張首圖核准保留，舊10.5秒／7.375秒均退件，不再重剪。使用者完成Grok真人驗證後，已單次生成真人感重設trial01，完整6.041667秒原速無音測試待評估。實際多一次回正再側轉，笑容持續；原地轉腳與肩包形狀變化有疑慮，未列自然感／物理通過或可用素材，未延伸L02。連續人工原速QA缺項保留。累計七次內建靜態／九支原片／兩支接受片；M04–M05與proof／Carousel仍缺。'
for p in [ROOT/'10_automation/CANONICAL_WORKFLOW.md',ROOT/'CURRENT_STATUS.md',ROOT/'10_automation/MIRA_EDITORIAL_HANDOFF.md',W/'publishing_structure.md']:
    lines=p.read_text(encoding='utf-8').splitlines()
    for i,l in enumerate(lines):
        if p.name=='CANONICAL_WORKFLOW.md' and l.startswith('現況與交接採短版有效摘要'):lines[i]='現況與交接採短版有效摘要，歷史備份於 `10_automation/history/`。'+summary+'見 `runs/2026-W45/reels/M03/realism_reset_2026-11-04/trial_01/REVIEW.md`。'
        elif p.name=='CURRENT_STATUS.md' and l.startswith('- W45現況：'):lines[i]='- '+summary
        elif p.name=='MIRA_EDITORIAL_HANDOFF.md' and l.startswith('先讀 [主工作流]'):lines[i]='先讀 [主工作流](CANONICAL_WORKFLOW.md)、[CURRENT_STATUS](../CURRENT_STATUS.md)、當週發布結構，再讀本頁與精確收據。'+summary+'最近已交付仍為W44。'
        elif p.name=='MIRA_EDITORIAL_HANDOFF.md' and l.startswith('- 目前下一步：'):lines[i]='- 目前下一步：看[M03完整6.04秒單鏡測試](runs/2026-W45/reels/M03/realism_reset_2026-11-04/trial_01/REVIEW.md)的真人感與轉腳／包型，尚非可用主片；不自動重試或接L02。網站驗證已恢復，勿再列阻擋；舊兩支退件片不重開，首圖不重問。'
        elif p.name=='publishing_structure.md' and l.startswith('來源完整W45 v2企劃'):lines[i]='來源完整W45 v2企劃已確認。'+summary+' W44原交付保留。'
        elif p.name=='publishing_structure.md' and l.startswith('2. [M02 trial03]'):lines[i]='2. [M02 trial03](reels/M02/trial_03/REVIEW.md)與[M01 10.25秒片](reels/M01/paired_review_v1/REVIEW.md)已接受。M03兩支舊合片退件；[新6.04秒單鏡測試](reels/M03/realism_reset_2026-11-04/trial_01/REVIEW.md)待真人感與動態回饋，不列可用主片，未接L02；首圖核准保留。'
        elif p.name=='publishing_structure.md' and l.startswith('5. 原速逐鏡'):lines[i]='5. 原速逐鏡／接點／整片、使用者接受、交接與發文分開。七次內建靜態／九支原片，M01／M02共兩支接受片。M03新單鏡仍待評估，連續人工原速QA未補寫；十套proof／Carousel未完成，沒有實際IG發文。'
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=HERE.parent/'REASSESSMENT.md';t=p.read_text(encoding='utf-8');t+='\n## 單鏡測試已完成\n\n使用者完成真人驗證後，trial_01已單次生成／下載完整6.041667秒，精確原片UUID1f291b40-ddb4-423e-ac9a-daf8ea5ca766。單鏡有較多身體轉向，但多次轉向、持續笑容、原地轉腳與包型問題仍待評估，未列真人感通過。詳trial_01/REVIEW.md；驗證不再是阻擋，未自動續做L02或重試。\n';p.write_text(t,encoding='utf-8')
p=W/'planning/M03/SHOT_CARDS.md';lines=p.read_text(encoding='utf-8').splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('狀態：'));lines[idx]='狀態：兩張首圖核准保留，兩支舊合片退件。現有[真人感trial01完整6.04秒測試](../../reels/M03/realism_reset_2026-11-04/trial_01/REVIEW.md)，待自然感與轉腳／包型回饋，非可用主片；未接L02。下方分鏡／舊剪輯為歷史。';p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for a in snap:assert sha(ROOT/a['snapshot_path'])==a['sha256']
write(HERE/'record_verification.json',{'date':'2026-11-04','source_sha256':sha(HERE/'source.mp4'),'review_sha256':sha(film),'full145frames_preserved':True,'source_prompt_URL_UUID_matched':True,'source_still_approval_hash_matched':True,'approved_snapshot_count':len(snap),'approved_snapshot_hashes_unchanged':True,'new_still_calls':0,'new_video_sources':1,'weekly_video_sources':9,'weekly_accepted_films':2,'continuous_full_source_visual_QA':False,'realism_pass':None,'publication_approval':None})
print('One new6.04s source, full145frames preserved; exact input/output matched;18snapshots unchanged. Realism/physical/acceptance pending, noL02 extension.')
