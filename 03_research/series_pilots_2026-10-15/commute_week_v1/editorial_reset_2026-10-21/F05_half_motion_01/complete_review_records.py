from pathlib import Path
import json,hashlib
d=Path(__file__).resolve().parent
base=d.parent
project=next(p for p in d.parents if (p/'CURRENT_STATUS.md').exists())
five=d/'five_look_review_2026-10-22'
out=five/'v1/review.mp4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(d/'F05_half_source.mp4')=='c2d9f0442ea0d9b9c50674fb959b96ae53a8264c3947c509aa91f05e4bec9aa9'
assert sha(out)=='e4ed855809463e9c8421c5c7d4292f62bdf3f12f1c5f30af8f5c0e0a4edd32dc'
p=d/'submission_receipt.json';r=json.loads(p.read_text(encoding='utf-8'))
r.update(status='unique_source_downloaded_sampled_review_and_five_look_append_done_pending_user_visual_review',
 actual_parameter_acceptance='Grok agent UI reports all requested first/5⅓skeyframe/M03v3identity controls accepted, last absent, no fallback. Internal model call not directly observed.',
 source_asset_id='e785251a-279e-4c71-8538-1f45d5ef0c47',
 source_sha256=sha(d/'F05_half_source.mp4'),source_bytes=(d/'F05_half_source.mp4').stat().st_size,
 fully_decoded_frames=145,actual_fps=24,actual_pixel_dimensions=[720,1280],
 actual_audio_track='AAC, approximately6s; source retained, separate stream-copy silent preview',
 downloaded_via_UI_media_to='C:/Users/Brandon_ChangChien/Downloads/generated_video (61).mp4',
 workspace_source='F05_half_source.mp4',outcome='source_visual_review.json',
 completion_evidence=['completion_dom.txt','completion_loaded.png','browser_playback_observation.json'],
 next='Exact21.2917s final preview user visual feedback on five-look focus/rhythm/new J45 ghosting, early tightening and additional right-side stairs; no automatic retry or publishing.')
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=d/'preflight.json';r=json.loads(p.read_text(encoding='utf-8'));r.update(status='single_trial_completed_source_inspected_five_look_review_ready',F05_motion_generated=True,actual_parameter_acceptance='See submission_receipt.json; UI agent-reported, not internal-call observation')
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for sub in ['F05_full_start_01','F05_half_late_01']:
 p=base/sub/'generation_receipt.json';r=json.loads(p.read_text(encoding='utf-8'));r.update(Grok_uploaded=True,F05_motion_generated=True,motion_receipt='../F05_half_motion_01/submission_receipt.json');p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
source_review={
 'date':'2026-10-22','source':'F05_half_source.mp4','sha256':sha(d/'F05_half_source.mp4'),
 'root_viewed':['QA_2026-10-22/checkpoints_25.jpg','QA_2026-10-22/pushin_dense_f060_to144.jpg','QA_2026-10-22/first18.jpg','QA_2026-10-22/frame_000090.png','QA_2026-10-22/frame_000128.png'],
 'findings':['Full head/skirt hem/both shoes readable approximately source0–3s; by~3.25s shoe crop begins, earlier than requested constantfull to3.75s','Continuous tighter framing develops, about5.33s reaches approved head-to-thigh family with complete blue bag','Sampled face/hair/shirt/skirt/bag consistent, near hand waist and far arm swinging; no blocking still-visible anatomy issue observed','Additional short stairs reveal from right edge around1.5–1.75s then pass behind/toleft; relationship to initial left stairs unverified; no sampled central spontaneous growth shown'],
 'independent_review':{'agent':'/root/half_shot_reuse_audit_oct22','scope':'Named QA sheets plus native90/128, no complete normal-speed visual playback','eligible_for_research_append':True,'limits':'No measured zero-slide, literal keyframe pin or exact world/route claim'},
 'source_eligible_for_research_append':True,'source_eligible_is_user_approval':False,
 'background_validated':False,'measured_zero_slide':False,'full_continuous_visual_review':False,
 'browser_playback':'Original source UI loop-play observed muted at1x; screenshots/time metadata only, see browser_playback_observation.json',
 'automatic_regeneration':False,'user_video_approval':False,'publishing_approval':False}
(d/'source_visual_review.json').write_text(json.dumps(source_review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
q='請完整播放21.29秒五套預覽：最後一套先全身、再推近半身的觀看重點與整體節奏是否可以保留？約15.3–16秒仍有臉、手臂與腿鞋重影，約17秒右側另露出台階；推近比草案稍早。這次只確認研究片，原發布影片保留。'
review={'date':'2026-10-22','artifact':'v1/review.mp4','sha256':sha(out),'bytes':out.stat().st_size,'frames':511,'fps':24,'duration_seconds':511/24,'question':q,'options':['可以保留這版','節奏或半身位置需調整','接點或背景需修正'],'answer':None,'status':'awaiting_exact_user_film_visual_feedback','publishing_approval':False}
(five/'user_review_request.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
full_review={'date':'2026-10-22','output_sha256':sha(out),'root_viewed':['v1/QA/full25.png','v1/QA/J45_dense.png','v1/QA/F05_progress.png'],'independent_reviewer':'/root/half_shot_reuse_audit_oct22','sampled_observations':['No sudden scale jump or disappearing person observed at J45','Output15.5–15.8s visible face/arm/leg/shoe double edges and skirt/trouser overlap; not an invisible join','Full fifth outfit pure after dissolve~16.04–18.3s, then tighter at~18.5s, head-to-thigh by~20.6–21.25s','Additional right stairs at~17s, unvalidated spatial relation to existing stairs'],'technical_fidelity':'All511decoded frames within intended-composite codec tolerance, per v1/edit_receipt.json; protectedsource hashes unchanged','continuous_normal_speed_full_film_visual_review':False,'user_accepted':False,'no_retime_crop_text_audio':True,'status':'sampled_review_complete_ready_for_exact_user_feedback','review_request':'user_review_request.json'}
(five/'root_visual_review.json').write_text(json.dumps(full_review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=five/'README.md';t=p.read_text(encoding='utf-8');t=t.replace('# Fifth-look full-to-half research append — prepared, not rendered','# Fifth-look full-to-half research append — v1 rendered, awaiting user feedback',1)
t=t.replace('Only run after root inspects','2026-10-22: v1/review.mp4 rendered and sampled by root;511f/21.2917s, SHA '+sha(out)+'. See root_visual_review.json and user_review_request.json. Original full-normal-speed visual/user approval remains pending.\n\nOnly run after root inspects',1);p.write_text(t,encoding='utf-8')
heading='## 21.29秒五套全身至半身研究片完成，待整片觀看 — 2026-10-22'
body='''

第五套半身末圖已由使用者明確回「可以，沿用這張半身圖」核准，精確收據`editorial_reset_2026-10-21/F05_half_late_01/user_still_approval.json`。原Grok畫布上傳全身first `f5116434-8cbe-440f-934f-584053a8b243` 與半身guide `c52cfeba-1216-4860-8580-0ab399600c40`；只送一次6秒／720p／9:16、first＋5⅓秒片內keyframe＋M03v3 face/full、last未設的試作。代理UI回報全數接受，內部呼叫未直接觀察。唯一輸出asset `e785251a-279e-4c71-8538-1f45d5ef0c47`，原片SHA `c2d9f0442ea0d9b9c50674fb959b96ae53a8264c3947c509aa91f05e4bec9aa9`，145幀／24fps／720×1280／6.0417秒／6,284,693bytes／AAC；原片與同H264靜音副本均保留。畫布載入與播放紀錄在`F05_half_motion_01/`。

root與獨立抽查：完整頭鞋／裙襬約原片0–3秒可讀，約3.25秒開始裁鞋，比3.75秒草案稍早；後段連續推近，約5.33秒形成頭至大腿構圖，藍包完整、領口與腰線可讀。約1.5–1.75秒右側另露出一組階梯，從邊緣揭露而非抽樣可證的中央增生，但與首圖左階梯的地理關係未成立；不記背景通過。臉、衣服及手包未見抽樣阻擋問題，未量測零滑步。UI原片靜音1x循環播放與截圖不是完整連續目視驗收。

另存完整五套研究預覽 `03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21/F05_half_motion_01/five_look_review_2026-10-22/v1/review.mp4`，SHA `e4ed855809463e9c8421c5c7d4292f62bdf3f12f1c5f30af8f5c0e0a4edd32dc`，18,912,651bytes／511幀／21.2917秒／24fps／720×1280，原速無字無音。385幀前四套＋新F05前144−18幀柔接；新J45為15.2917–16.0417秒，有臉／手臂／腿鞋短暫雙影，尤其裙褲重疊。完整第五套約16.04–18.3秒清楚展示，再靠近至21.25秒半身。root與獨立已看全片25點、密集接點與第五段進程，沒有宣稱完整原速目視或整片已核准。

全511幀解碼與預定合成在編碼容差內：meanMAE1.89639、worst2.54025、minPSNR36.8814dB；前綴／來源SHA前後相同。精確組片、核對、差異、待答問題見`five_look_review_2026-10-22/`。**先請使用者完整看21.29秒版，判斷整體重點／節奏、最後換裝雙影及約17秒新增右側階梯；未自動重生或發布。** 舊片與Drive發布包保留、無外部異動，正式週規則不變。以下待新圖／待生成為歷史，以上結果為準。

'''
p=project/'CURRENT_STATUS.md';t=p.read_text(encoding='utf-8-sig')
if heading not in t:
 pos=t.index('\n## ');t=t[:pos]+'\n'+heading+body+t[pos:]
p.write_text(t,encoding='utf-8')
p=project/'10_automation/CANONICAL_WORKFLOW.md';t=p.read_text(encoding='utf-8-sig')
bullet='- Latest F05 full-to-half completed,2026-10-22: user approved exacthalfstill SHA114300736fbcf321316d20ce992f968bcb39d9dcea0e85542f0491ee97539ab7「可以，沿用這張半身圖」. One originalcanvas6s720p9:16 first f5116434… +5⅓skeyframe c52cfeba… +M03v3face/full,lastunset; acceptance agentUI-reported, internalcallunseen. Uniqueasset e785251a-279e-4c71-8538-1f45d5ef0c47/sourceSHAc2d9f0442ea0d9b9c50674fb959b96ae53a8264c3947c509aa91f05e4bec9aa9,145f24fps720x1280/6.0417s/AAC. Source sampled wholeoutfit0–3s, shoe crop~3.25s earlierthan3.75splan, then continuouspushin/wholebluebag; extra rightstairs reveal~1.5–1.75s, relationtoleftstairsunvalidated, notbackgroundpass. Root/independenteligibleforresearchappend only. Separate511f21.2917s silent/no-text/native five-lookpreview `editorial_reset_2026-10-21/F05_half_motion_01/five_look_review_2026-10-22/v1/review.mp4` SHAe4ed855809463e9c8421c5c7d4292f62bdf3f12f1c5f30af8f5c0e0a4edd32dc.385+144−18,J45at15.2917–16.0417s retainsface/arm/legghosting; additionalstairs~17s. Full511frame technicalfidelity passes, rootdense/full25/progress sampled; UIloop1xsource playback is notcontinuous fullfilmvisualreview. Awaitexactuserfilmfeedback; no regeneration/Drive/GitHub/publish, originalsretained, formalcontractunchanged. Outcome/request/evidence in newmotionfolder. Supersedes pendinghalfstill/generation states below.\n\n'
if '- Latest F05 full-to-half completed,2026-10-22:' not in t:t=t.replace('Active rules:\n\n','Active rules:\n\n'+bullet,1)
p.write_text(t,encoding='utf-8')
print(json.dumps({'film_sha256':sha(out),'frames':511,'seconds':511/24,'status':'awaiting_exact_user_film_visual_feedback','source_calls':1,'root_and_independent_sampled_review_saved':True},ensure_ascii=False))

