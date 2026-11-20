"""Register new natural-performance sources and exact paired candidate without approval inflation."""
import hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent;ROOT=B.parents[5];W=ROOT/'10_automation/runs/2026-W45';P=B/'paired_review_v1'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
e=read(P/'edit_receipt.json');assert h(ROOT/e['output_path'])==e['output_sha256']
put(B/'user_direction_continuation_2026-11-05.json',{'actor':'user','quote':'ok','recorded_at':'2026-11-05','timezone':'Asia/Taipei','scope':'Continue M03 correction after rejecting swaying/dance: natural motivated actions, turns, short steps and responses; retain selected A parallel layout.','context':'Direct reply to assistant stating dance-pose direction was wrong, previous film not adopted, and natural situational performance would replace repeated swaying.','limits':'Not approval of the new specific drawings, generated source quality, finished movie or publication. Existing approved stills and in-scope production authorization retained.'})
for look in ['L01','L02']:
    p=B/(look+'_trial_01');s=read(p/'submission.json');s.update(status='sampled_source_in_paired_review_pending_user',still_approval=f'10_automation/runs/2026-W45/approvals/M03_{look}_still_approval_2026-11-04.json',review_path=rel(P/'REVIEW.md'),user_acceptance=None,publication_approval=None);put(p/'submission.json',s)
    ui=read(p/'native_playback_sampling.json');times=[y['t'] for x in ui['samples'] for y in x['media']]
    put(p/'visual_review.json',{'date':'2026-11-05','status':'sampled_pending_user_performance_review','whole_film_samples_viewed':13,'upper_body_samples_viewed':25,'panel_fit_samples_viewed':25,'additional_full_resolution_source_frames_viewed':[36,108] if look=='L01' else [],'native_UI_samples':len(ui['samples']),'native_UI_sample_range_seconds':[min(times),max(times)],'native_UI_samples_all_playing1x':all(len(x['media'])==1 and not x['media'][0]['paused'] and x['media'][0]['rate']==1 for x in ui['samples']),'continuous_human_native_speed_review':False,'observed':'Initial facial response and brief mouth opening, one side/back turn with low relaxed arms, side hold, then frontal return. Sampled views lack repeated left-right hip/shoulder sway or high arm pose chain.','plan_deviation':'Turn is deeper than the requested45degrees; exact angle unmeasured. Natural-body and face physics not certified.','attention':'Face mostly remains responsive toward camera during turn; friend/photo context is directing intent, not independent evidence of a real off-camera event.','audio':'Original contains AAC. Source sound not reviewed; silent review streamcopies original video and removes audio only.','user_acceptance':None,'publication_approval':None})
e.update(status='sampled_candidate_pending_user_review');put(P/'edit_receipt.json',e)
put(P/'visual_review.json',{'date':'2026-11-05','status':'sampled_candidate_pending_user_review','motion_board_samples_viewed':25,'full_resolution_output_frames_viewed':[0,72],'technical_full_decode':True,'observed':'In samples, full heads/shoes, hands, bag and skirt stay inside the400px crops. Both panels use same scale and show side view then frontal return, no repeated dance-pose sequence.','scale':'Approximate64–67% of canvas height; actual samples compared side by side. Not a guarantee of identical posture heights at all times.','timing':'All145 native frames of each source, no temporal edit join, no retime or duplicate/freeze. Generated motion is not claimed physically perfect.','remaining_limits':['Source turns deeper than planned45degrees','Brief mouth opening/possible speech-like response remains','No uninterrupted human native-speed whole-film review','Source/UI parameter report does not expose internal generation call'],'user_film_acceptance':None,'publication_approval':None})
(P/'REVIEW.md').write_text('''# M03 A並排｜自然回應與單次轉身

2026-11-05。觀眾看同件海軍藍柔肩西外，配工作深褲／皮鞋與休閒淺裙／球鞋的差異。依「我不喜歡搖擺跳舞」及後續ok，改以出發前請朋友拍照為表演動機：短暫回應拍攝者、一次完整轉向、回正站定。

兩套各新生成一次6秒來源，沿用原兩張逐圖核准首圖與M03 v3身份；零張新圖，沒有換服務、加購或額外雲端金鑰。褲裝UUID `95b2f7fe-2b05-4101-88fd-e5367afd784f`，裙裝UUID `d8318fa2-0d21-41fc-b94f-cfffd8111538`。實際各145格／24fps／720×1280／6.041667秒，原片含AAC；原片及原速無音副本保留。

本片將兩支完整連續原片直接並排，保留所有145格，不剪去中段、不改速／凍結／複製補長。兩側同用400像素固定裁切、356像素欄寬及8像素中縫；人物約畫高64–67%，比先前4秒v4大。只有一個合成鏡頭，沒有時間接點，因此沒有新增剪輯淡接；0.75秒規則仍適用於有接點的剪輯，不是改用硬切。

實際可見：開頭微笑／短暫張口回應、手臂低垂近身、側後轉與回眸、回正。抽樣沒有先前連續左右搖擺與高舉擺姿。實際轉向比計畫45度深，精確角度未量測；兩側不強制同步。背景朋友情境是導演意圖，沒有假稱影片證實畫外事件或錄到對話。

兩支來源各看13張全片、25張上身與25張欄寬樣本；本片看25張四分之一秒樣本及首格／3秒完整畫面。來源及合片完整解碼通過。網站原速播放另有褲裝20筆、裙裝42筆動態截圖；不是連續人工全片驗收。手腳、身份、頭身與背景不宣稱零缺陷，原音未審。精確區間／規格／雜湊見 `edit_receipt.json`。

目前是新候選，尚無使用者對此精確片的表演／成片／發布核准。舊4秒v4不採用的回饋保持，不重開待審。M01／M02接受與舊褲裝來源曾接受範圍保留為歷史，不外推為此片核准。

[觀看6.04秒原速無音預覽](M03_W45_natural_parallel_review_v1.mp4)
''',encoding='utf-8')
q=read(W/'production_queue.json');q.update(status='M03_natural_parallel_6s_candidate_pending_user_review',video_jobs_submitted=14,video_jobs_completed=14,active_reviews=[e['output_path']],active_trial=rel(P),latest_edit_receipt=rel(P/'edit_receipt.json'),latest_editorial_proposal=rel(B/'production_plan.json'));q['next']={'model':'M03','action':'Review exact6.04s natural parallel candidate for performance/naturalness, figure scale and pivot contact; no automatic new generation. Previous dance v4 remains not adopted.'};put(W/'production_queue.json',q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';r=read(rp);s=next(x for x in r['series'] if x['series_id']=='SERIES_W45_M03');s.update(status='natural_parallel6s_candidate_pending_user_review',latest_asset_receipt=rel(P/'edit_receipt.json'),current_reassessment=rel(P/'REVIEW.md'),latest_editorial_proposal=rel(B/'production_plan.json'))
for look in ['L01','L02']:
    p=B/(look+'_trial_01');v=read(p/'submission.json');uid=f'USE_W45_M03_NATURAL_{look}_TRIAL01_20261105';u={'usage_id':uid,'series_id':s['series_id'],'production_date':'2026-11-05','status':'source_sampled_pending_user_feedback','film_path':v['silent_path'],'source_asset_id':v['video_asset_id'],'source_sha256':v['source_sha256'],'receipt_path':rel(p/'submission.json'),'feedback_summary':'One new6.04s source after user rejected swaying/dance. Sampled response/one deeper-than45degree turn and return with low arms; no film/publication approval.','user_acceptance_receipt':None,'publication_url':None};existing=next((x for x in r['uses'] if x['usage_id']==uid),None)
    if existing:existing.update(u)
    else:r['uses'].append(u)
    if uid not in s['usage_ids']:s['usage_ids'].append(uid)
uid='USE_W45_M03_NATURAL_PARALLEL_V1_20261105';u={'usage_id':uid,'series_id':s['series_id'],'production_date':'2026-11-05','status':'candidate_pending_user_film_quality_review','film_path':e['output_path'],'film_sha256':e['output_sha256'],'receipt_path':rel(P/'edit_receipt.json'),'feedback_summary':'New6.04s continuous-source parallel after dance rejection; one turn and return, larger figures, no internal temporal join. Pending exact-film user review, not published.','user_acceptance_receipt':None,'publication_url':None};existing=next((x for x in r['uses'] if x['usage_id']==uid),None)
if existing:existing.update(u)
else:r['uses'].append(u)
if uid not in s['usage_ids']:s['usage_ids'].append(uid)
put(rp,r)
current='W45現況：M01精確10.25秒與M02 trial03已接受，尚無新交接／發布。M03舊4秒v4因「我不喜歡搖擺跳舞」不採用，A並排與兩張首圖核准保留。後續ok接續自然表演方向，各單次新製褲裝95b2f7fe與裙裝d8318fa2，均6.041667秒；現行待看natural_parallel_2026-11-05/paired_review_v1，兩支完整原片並排、無時間剪接點／原速無音、人物約畫高64–67%。可見短暫回應、一次側轉與回正；實際轉角比45度深，肢體／真人感未作零瑕疵認證。技術解碼與抽樣不等於連續人工原速QA，這支新片未獲成片／發布核准。累計七次靜態／十四支原片／兩支接受成片，M04–M05與proof／Carousel仍缺；不重開舊v4待審或自動追加生成。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
    p=ROOT/name;lines=p.read_text(encoding='utf-8-sig').splitlines()
    for i,line in enumerate(lines):
        if 'W45現況：' in line:lines[i]=line.split('W45現況：')[0]+current
        elif line.startswith('- 11/5完整換姿：'):lines[i]='- 11/5自然表演：舊v4跳舞方向不採用；兩支各一次新6.04秒來源與[自然並排候選](runs/2026-W45/reels/M03/natural_parallel_2026-11-05/paired_review_v1/REVIEW.md)已完成，待此精確新片回饋。A偏好與原首圖保持，沒有發布核准。'
        elif line.startswith('- 目前下一步：'):lines[i]='- 目前下一步：回看M03自然並排6.04秒候選的表演、尺度與轉身腳掌；舊搖擺v4維持不採用。IG沿用現有頁，本回合未操作IG或新增分頁。'
        elif line.startswith('2. M01／M02接受保留。'):lines[i]='2. M01／M02接受保留。M03 A排版保留；現行[自然並排6.04秒候選](reels/M03/natural_parallel_2026-11-05/paired_review_v1/REVIEW.md)待品質回饋，舊v4跳舞方向不採用。'
        elif line.startswith('5. 原速逐鏡／接點／整片、'):lines[i]='5. 原速逐鏡／接點／整片、使用者接受、交接與發文分開。七次靜態／十四支原片，M01／M02共兩支接受成片；M03自然並排未接受。十套proof／Carousel未完成，無本週IG發文紀錄。'
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
plan=read(B/'production_plan.json');plan.update(status='two_sources_and_parallel_candidate_completed_pending_user_review',latest_review=rel(P/'REVIEW.md'),actual_seconds=145/24,new_video_jobs_submitted=2,new_video_jobs_completed=2,actual_crop_each_source=[160,0,400,1280],actual_deviation='Turn deeper than planned45degrees; crop tightened after actual sampled-envelope inspection, identical scale both sides.');put(B/'production_plan.json',plan)
(B/'STATUS.md').write_text('''# M03 自然並排｜有效狀態

2026-11-05。兩套各一次新6.041667秒來源完成，零張新圖。現行[6.04秒自然並排](paired_review_v1/REVIEW.md)待使用者品質回饋；來源與成片均非發布核准。

舊expressive分支4秒v4因搖擺跳舞不採用，原回饋保持。此版只有一次轉向與回正、手臂低垂，不繼續剪舊擺姿。實際轉角較深，原速全片人工審查缺項如實保留。M01／M02與18份核准快照不變，沒有交接／發布或IG分頁操作。
''',encoding='utf-8')
old=W/'reels/M03/expressive_parallel_2026-11-05'
for f in ['STATUS.md','NATURAL_PERFORMANCE_REPLAN_2026-11-05.md']:
    p=old/f;t=p.read_text(encoding='utf-8');note='接續狀態：本頁保留當時草案／退件範圍。後續已各一次完成兩支自然來源與[6.04秒新並排候選](../natural_parallel_2026-11-05/paired_review_v1/REVIEW.md)，不是重開舊v4或追加搖擺版核准。\n\n'
    if note not in t:t=t.replace('\n\n','\n\n'+note,1);p.write_text(t,encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts'];assert all(h(ROOT/a['snapshot_path'])==a['sha256'] for a in snap)
for file,sha in [('reels/M01/paired_review_v1/M01_W45_two_looks_review_v1.mp4','aa1a657e88480a966226bdbf72ea3e5c46346290df154408d376ebcc2b27a2fb'),('reels/M02/trial_03/M02_W45_trial03_silent_review.mp4','bf1828d34ce61ac76e82d1573a49e85d8403d5a5ae9be9bb8be46c16fa114b67')]:assert h(W/file)==sha
put(P/'state_reconciliation.json',{'date':'2026-11-05','approved_snapshots_unchanged':len(snap),'M01_M02_accepted_files_unchanged':True,'weekly_still_calls':7,'weekly_video_source_jobs':14,'weekly_accepted_finished_reels':2,'new_source_jobs_this_branch':2,'new_still_calls':0,'IG_tabs_created':0,'IG_actions':0,'new_paid_cloud_service_requests':0,'new_film_acceptance':None})
print(json.dumps({'current_candidate':e['output_path'],'source_jobs_completed':14,'accepted_finished_reels':2,'protected_snapshots':len(snap)}))
