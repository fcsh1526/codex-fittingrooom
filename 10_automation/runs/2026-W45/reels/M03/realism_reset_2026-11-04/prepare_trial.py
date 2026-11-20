"""Freeze one redesigned six-second source test; no external submission here."""
import hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'10_automation/CANONICAL_WORKFLOW.md').is_file());W=ROOT/'10_automation/runs/2026-W45'
T=HERE/'trial_01';T.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
approval=json.loads((W/'approvals/M03_L01_still_approval_2026-11-04.json').read_text(encoding='utf-8'))
assert sha(ROOT/approval['asset_path'])==approval['target_sha256']
assert sha(ROOT/'02_brand/reference_models/M03_start_v3_face.png')=='ca479fe686d72abb6ba75ff95fee621542860a4f22d9d852e6560119ab481c6d'
assert sha(ROOT/'02_brand/reference_models/M03_start_v3_full.png')=='e6707116027bea5d36ca1215159652e8a728a972f33f79f5f37fd221e727e890'
prompt='''A friend is filming her outfit outside the office. Begin from the exact approved image, already relaxed. She casually shifts her weight and turns her hips and shoulders a little toward frame-left to show the blazer's side line. As her body settles, she briefly looks back to the friend at the lens with an easy smile, then lets her attention follow the direction of her body. Her head, eyes, expression, arms, balance and fabric respond together with ordinary pauses, like a candid moment during a quick outfit video.

One continuous six-second real-time full-person shot with the original locked, level chest-height 50mm camera. Allow comfortable natural foot repositioning for the small turn; retain complete hair and both shoes in frame. Keep the open blazer, white neckline, waist and charcoal-trouser silhouette readable. Keep the same M03 face, long wavy brown hair, deep-navy soft-shouldered blazer, white crewneck cotton tee, charcoal straight trousers, black loafers, small black bag on her left shoulder and fine silver necklace. Preserve the shaded office wall, windows, bench and paving. No sustained posed grin, theatrical laugh, speech, full spin, walk toward camera, camera movement, slow motion, cut or text.
'''
(T/'video_prompt.txt').write_text(prompt,encoding='utf-8')
request='''本次只生成一支W45 M03 L01真人感重設trial01，6秒720p原生9:16。使用者已同意先測單鏡身體／視線／表情連動。不是舊L01 trial01/trial02，不是M03兩套重剪，也不是L02；新機制只這一次，不重試、不合片、不補新圖、不修改刪除既有媒體、不加購額度或換服務。

精確輸入：
first_frame_asset_id: "2e8df556-7034-4788-92d8-3a769fcdfed3"
asset_ids: ["26e03f42-2907-488c-b75c-239a2a19b9c8","15c720b2-46b6-45e0-a150-60290e3290e6"]
duration: "6"
resolution_name: "720p"
aspect_ratio: "9:16"
不設last_frame_asset_id或keyframes。

先實際看三張圖：first必須是核准framing_v2（長棕捲髮M03，深藍西外／白T／炭灰直褲／黑樂福／黑左肩包，辦公樓遮簷長凳，人物約74%畫高）。face/full只鎖M03 v3身份與自然比例，不複製棚拍白襯衫造型。三個UUID此前實際下載SHA已核對；找不到、內容不符、額度不足或6秒設定不支援就停下，不代換。不能沿用a5cdb89d或2919da8e舊片冒充新輸出。

本鏡目的：完整讀褲裝與西外側線，做連動的自然小轉身；不把雙腳全程鎖死、雙手固定、持續直視或大笑當作附加要求。不要加額外笑容演出或招手。
以下英文逐字傳入prompt，標記不傳入：
PROMPT_BEGIN
'''+prompt.rstrip()+'''
PROMPT_END
音訊僅有實際開關才關；沒有便如實保留AAC，不能為音訊重生。完成列實際輸入UUID、可用設定、英文原文是否傳入、新影片UUID、實際時長／像素／音軌。seed、明確模型版本與剩餘額度無欄位就unknown。代理回報、可見畫面、實際檔案與原速審查分開，不宣告真人感、身份或物理通過。'''
(T/'grok_request.txt').write_text(request,encoding='utf-8')
submission={'date':'2026-11-04','status':'prepared_not_submitted','model':'M03','look':'2026-W45-003-L01','branch':'realism_reset_trial01','user_authorization_quote':'好','authorization_context':'Direct assent to single-source integrated body/gaze/expression test after exact v2 realism rejection. Not acceptance of unseen result.','first_frame_asset_id':'2e8df556-7034-4788-92d8-3a769fcdfed3','asset_ids':['26e03f42-2907-488c-b75c-239a2a19b9c8','15c720b2-46b6-45e0-a150-60290e3290e6'],'source_still_path':approval['asset_path'],'source_still_sha256':approval['target_sha256'],'source_still_approval':'10_automation/runs/2026-W45/approvals/M03_L01_still_approval_2026-11-04.json','duration_requested':6,'resolution_requested':'720p','aspect_requested':'9:16','max_new_jobs':1,'prompt_sha256':sha(T/'video_prompt.txt'),'last_frame_asset_id':None,'keyframes':None,'seed':'unknown','model_version':'unknown','remaining_quota':'unknown','user_video_acceptance':None,'publication_approval':None,'changes':'Performance redesign: free coordinated weight/hip/shoulder turn with brief social gaze, instead of planted body plus sustained face performance. No new source still/outfit/camera.'}
(T/'submission.json').write_text(json.dumps(submission,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
plan={'date':'2026-11-04','viewer_purpose':'Read the same approved work outfit and blazer side line while testing integrated believable performance.','execution_mode':'generate_one_source','duration_request_seconds':6,'camera':'locked full person, original framing','action_sequence':['Already relaxed at approved starting view','Weight, hips and shoulders turn slightly toward frame-left to expose side line','Brief lens-directed friendly response during the turn settling','Attention follows the body direction, ordinary pause'], 'timing_note':'Order only, not second-by-second choreography or guaranteed engine timing.','source_still':approval['asset_path'],'additional_new_stills':0,'whole_film_integration':'Not yet. Review raw full source before two-look joins.','success_criteria':['Whole-person reaction feels plausible at native speed; cannot be certified by sampled smile frames.','Body/head/gaze/expression develop together with natural pauses; no imposed fixed stare or theatrical surprise.','Original outfit/identity/proportions remain stable, hands/foot repositioning/bag/scene inspected.','Full outfit remains readable; no full spin, approaching camera or new cut.'],'failure_handling':'Record observed defect; no automatic retry or second look extension. Same-source recutting is not a realism repair.','new_generation_budget_jobs':1,'reference_comparison_limits':'This redesigned performance changes several linked constraints; not a single-variable causal experiment.'}
(T/'shot_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
inspector=(W/'reels/M03/L01_trial_02/inspect_clip.py').read_text(encoding='utf-8').replace('ROOT=HERE.parents[5]',"ROOT=next(p for p in HERE.parents if (p/'10_automation/CANONICAL_WORKFLOW.md').is_file())").replace('M03_W45_L01_trial02_silent_review.mp4','M03_W45_realism_trial01_silent_review.mp4')
(T/'inspect_clip.py').write_text(inspector,encoding='utf-8')
print(T)
