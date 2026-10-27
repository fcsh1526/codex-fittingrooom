from pathlib import Path
import json,hashlib
d=Path(__file__).resolve().parent
base=d.parent.parent
project=next(p for p in d.parents if (p/'CURRENT_STATUS.md').exists())
qa=d/'QA_2026-10-22'
src=d/'cadence_source.mp4'
comp=qa/'original_used_left_trial_right_native_4p5s.mp4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(src)=='9707b42d230466ef2c2088a926ec45745d546d717c0fa9756d1b8e52ac0ab21d'
assert sha(comp)=='bb7cf0ec9cdb7bb5eb3e67aa0a5ff23c2d07768baa9c393f5eb121de74891d0a'
p=d/'submission_receipt.json';r=json.loads(p.read_text(encoding='utf-8'))
r.update(status='one_trial_downloaded_sampled_and_used_interval_comparison_ready',
 actual_parameter_acceptance='Grok agent UI reports requested first/identity accepted, no last or keyframes; internal call not directly observed',
 source='cadence_source.mp4',source_asset_id='192cccdc-1496-4803-95c2-99f6f38a64ac',source_sha256=sha(src),source_bytes=src.stat().st_size,
 actual_fps=24,actual_pixel_dimensions=[720,1280],decoded_source_frames=145,derived_source_duration_seconds=145/24,actual_audio='AAC; silent stream-copy derivative preserved',
 downloaded_via_UI_media_to='C:/Users/Brandon_ChangChien/Downloads/generated_video (62).mp4',
 source_review='source_visual_review.json',comparison='QA_2026-10-22/original_used_left_trial_right_native_4p5s.mp4',
 completion_evidence=['completion_dom.txt','completion_loaded.png','browser_playback_observation.json'],
 next='Exact native-speed comparison pace feedback before selecting gait master or rebuilding necessary original shots; do not insert unmatched sample into five-look film.')
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
visual={'date':'2026-10-22','source_sha256':sha(src),'root_viewed':['QA_2026-10-22/new_checkpoints25.jpg','QA_2026-10-22/new_feet_every3.jpg','QA_2026-10-22/comparison_checkpoints25.jpg','Original F01–F05 three-frame foot boards'],
'independent_review':'/root/gait_cadence_tail_audit_oct22, QA_2026-10-22/CADENCE_COMPARISON_AUDIT.md',
'observations':['Whole person and both shoes in sampled frames through6s, no new costume or push-in','New repeated support-phase centers approx6,21,36,48,60,72,84,96,111,123,135 each±3f; middle repeated12f intervals vs original often15f','Only compare source[0,108) used in actual film: new about8visible phases/originalabout7; not a precise speed or step-count percentage','Opening and around4s includes15f intervals; requested0.5–0.6s not strictly guaranteed throughwhole6s','New later glass doorway/facade revealed, not matched to old route or fifth-look first; not eligible for direct insertion'],
'defects_not_validated':['No world-aligned foot tracking or zero-slip pass','No complete continuous normal-speed visual gait pass','No original film transition or scene continuity pass'],
'technical_only':'Both sources unchanged, all sourceframes decoded. Main comparison108f24fps720x640, native frame order, no text/audio/retime/crop; eachside uniform50percent scaling',
'whole_film_changed':False,'user_pace_approval':False,'automatic_retry':False}
(d/'source_visual_review.json').write_text(json.dumps(visual,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
q='請播放4.5秒左右原速對照：左邊是原片實際採用的格紋段，右邊是新步態樣本。右邊的步伐是否更接近你要的俐落通勤感？這次只選步態方向，沒有換入五套片，場景與接點也尚未核准。'
request={'date':'2026-10-22','artifact':'QA_2026-10-22/original_used_left_trial_right_native_4p5s.mp4','sha256':sha(comp),'bytes':comp.stat().st_size,'frames':108,'fps':24,'duration_seconds':4.5,'size':[720,640],'left':'Original F04 used source[0,108)','right':'One new trial source[0,108)','question':q,'options':['右邊較合適，可作步態基準','右邊仍太慢','右邊太急或不自然'],'answer':None,'status':'awaiting_exact_user_pace_feedback','whole_film_approval':False}
(d/'user_pace_review_request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=project/'CURRENT_STATUS.md';t=p.read_text(encoding='utf-8-sig')
heading='## 運鏡與半身保留；已查步頻差，原速步態對照待選定 — 2026-10-22'
body='''

使用者對精確21.2917秒五套片回「運鏡及半身都可以，但是整體的走路步驟太慢，或這是各鏡的走路步驟不連續，忽快忽慢」。保留運鏡／半身方向，整片步態仍需修正，不推定背景或發布核准。精確回饋在`F05_half_motion_01/five_look_review_2026-10-22/user_film_feedback.json`。

以五來源每3原生幀腳圖與四個接點out/in/composite比對，root及兩個獨立agent發現：J12約2.5–3.25秒incoming較慢，J34約11.54–12.29秒incoming在重疊內逐漸超前；來源本身的步相間隔不一致，並非全是轉場錯覺。J23較接近，J45大致同拍但腳位／裙褲混影。相位標記±3幀，非物理步速或精確落地量測；原速微移接點無法消除不同步頻。方法／限制／來源hash／QA圖在`editorial_reset_2026-10-21/gait_continuity_2026-10-22/`，主摘要`DIAGNOSIS.md`。

只以既有核准格紋全身first＋M03v3身份、無last/keyframe，於原畫布做一次獨立6秒較俐落步態試作。新asset `192cccdc-1496-4803-95c2-99f6f38a64ac`、sourceSHA `9707b42d230466ef2c2088a926ec45745d546d717c0fa9756d1b8e52ac0ab21d`，145幀／24fps／720×1280／6.0417秒／AAC。代理回報控制接受，不代表內部呼叫已觀察。正常原速樣本的中段多次約12幀相位，原格紋多約15幀，支持新較密；開頭／約4秒仍有15幀，不能宣稱恆定0.5–0.6秒或零滑步。新後段門面與原路線未匹配，不能直接替換第四鏡。

主要交付是`gait_continuity_2026-10-22/cadence_master_trial_01/QA_2026-10-22/original_used_left_trial_right_native_4p5s.mp4`，SHA `bb7cf0ec9cdb7bb5eb3e67aa0a5ff23c2d07768baa9c393f5eb121de74891d0a`，2,803,605bytes／108幀／4.5秒／24fps／720×640。左原F04實際採用[0,108)，右新樣本同區間，均原速無字無音，每側只等比50%縮小，不裁切不重複不凍結。兩來源SHA未變、全108幀合成核對在診斷編碼容差內。**6秒對照含原F04[108,144)未採用尾段，只保留內部診斷，不能用來誇大原21.29秒片的慢感。** 原新6秒原片及靜音副本另存。

先請使用者選右側步態是否更合適，再決定必要鏡頭重做與接點相容。沒有重做五支、改速、改半身安排或替換原21.29秒片；Drive／GitHub／IG無異動。精確prompt、單次請求、原片、QA、比較收據與待答問題在`cadence_master_trial_01/`；以下待整片首次回饋為歷史，以上狀態為準。

'''
if heading not in t:
 pos=t.index('\n## ');t=t[:pos]+'\n'+heading+body+t[pos:]
p.write_text(t,encoding='utf-8')
p=project/'10_automation/CANONICAL_WORKFLOW.md';t=p.read_text(encoding='utf-8-sig')
bullet='- Latest gait-feedback diagnostic,2026-10-22: exact21.2917s user accepts camera/half direction but reports slow/discontinuous varying walking; wholefilmNOTaccepted, no backgroundapproval inferred. Exactfeedback in F05_half_motion_01/five_look_review_2026-10-22/user_film_feedback.json. Five-source every3f/paired joins show J12 incoming slower, J34 incoming progressively ahead; J23 nearphase/J45 spatialghosting, approximate±3f phase not physicalspeed. Single first-only approvedcheckedshirt/M03v3identity6s native gait trial, no last/keyframe: asset192cccdc-1496-4803-95c2-99f6f38a64ac/sourceSHA9707b42d230466ef2c2088a926ec45745d546d717c0fa9756d1b8e52ac0ab21d,145f24fps720x1280/AAC. UI-reported controls; no internalcallproof. Newmiddle repeated~12f vsold~15f supports denserwalk, not exact fixedcadence/no-slip. Newfacade unmatched, doNOTdirectinsert. Main4.5s native-left-oldused[0,108)/right-new[0,108) diagnostic in `gait_continuity_2026-10-22/cadence_master_trial_01/QA_2026-10-22/original_used_left_trial_right_native_4p5s.mp4` SHAbb7cf0ec9cdb7bb5eb3e67aa0a5ff23c2d07768baa9c393f5eb121de74891d0a,108f/720x640/silent/no text/no retime, 50%scale eachside.6scomparisoninternalonlyincludesunusedoldtail, not currentfilm attribution. Awaitexactpacefeedback before necessarysource/join redesign, no fullfilmchange/newphotos/retry/Drive/GitHub/publish; formalcontractunchanged. DIAGNOSIS.md and localreceipts recordlimits. Supersedes pendingfinal-firstfeedback status below.\n\n'
if '- Latest gait-feedback diagnostic,2026-10-22:' not in t:t=t.replace('Active rules:\n\n','Active rules:\n\n'+bullet,1)
p.write_text(t,encoding='utf-8')
print(json.dumps({'status':request['status'],'comparison_sha256':sha(comp),'comparison_seconds':4.5,'one_trial_only':True,'whole_film_changed':False},ensure_ascii=False))

