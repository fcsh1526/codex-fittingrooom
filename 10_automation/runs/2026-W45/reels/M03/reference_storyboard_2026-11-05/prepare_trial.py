from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent; ROOT=P.parents[5]; W=ROOT/'10_automation/runs/2026-W45'; T=P/'L01_trial_01'
T.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
assert not (T/'submission.json').exists(), 'Do not overwrite a submitted job'
verification=read(P/'verification.json')
for name,scope,digest in [('storyboard.png','storyboard',verification['storyboard_sha256']),('timing_animatic.gif','previs',verification['animatic_sha256'])]:
    assert sha(P/name)==digest
    put(P/f'user_{scope}_approval_2026-11-05.json',{'actor':'user','decision':'approved','scope':scope,'target_sha256':digest,'quote':'ok','recorded_at':'2026-11-05',
      'context':'Direct reply to displayed six-view9s connected storyboard and linked9s timing animatic; final reply explicitly described one-side trial next and slight upward re-aim during approach.',
      'limits':'Plan/framing approval and authorization for the single-side test, not acceptance of ungenerated footage, new stills, final film, publication or extra purchases.'})
prompt='''She is showing this outfit directly to the person filming, with lively, confident ease. Continue from the supplied smiling first image. First she brings one hand to her waist and lets her shoulders and chin join the change of stance. She releases that hand as she takes one clear short diagonal step and turns into a three-quarter view, briefly showing the blazer side line and the straight trousers. Her head, arms, weight and clothes respond together; her attention remains naturally with the camera. She turns back toward the viewer without a long pose-hold, then takes two ordinary forward steps to bring the blazer lapels, white neckline and her expression closer. Her smile develops and softens naturally rather than staying exaggerated. This is an outfit presentation, not dancing or repeated left-right rocking.

One continuous ten-second real-time shot. Keep the full outfit and both shoes readable through roughly the first half, then approach smoothly to head-through-knees framing. Keep the camera position and50mm lens fixed; allow a gentle upward tilt only during the approach to retain all her hair. End before she crowds the lens. Preserve normal head-to-body proportions, M03 identity, long wavy brown hair, open deep-navy blazer, white crewneck tee, charcoal straight trousers, black loafers, small black bag on her left shoulder and silver necklace. Keep the same shaded office windows, bench, paving and coherent daylight. No running, repeated swaying, zoom, slow motion, cut, text or outfit change.'''
(T/'video_prompt.txt').write_text(prompt+'\n',encoding='utf-8')
request=f'''W45 M03參考轉分鏡：使用者已對剛展示的9秒連接線稿回覆ok，現在只生成L01褲裝一支新10秒試片。重點為「主動展示→短步／側向讀輪廓→兩步靠近看西外與表情」，不是先前95b2f7fe的單轉身站定，也不是414c5d81的搖擺／高V。原媒體全部保留，不刪改、不重試、不做裙裝、不補圖、不升級／加購／換服務。

已核准First frame: 2e8df556-7034-4788-92d8-3a769fcdfed3（M03 L01 framing_v2：海軍藍西外、白T、炭灰直褲、黑樂福、小黑左肩包，原辦公遮簷場景）。身份asset_ids: ["26e03f42-2907-488c-b75c-239a2a19b9c8","15c720b2-46b6-45e0-a150-60290e3290e6"]，只鎖M03 v3身份與普通比例，不複製棚拍服裝。
先查看三個UUID，核對實際可用控制。duration:"10", resolution_name:"720p", aspect_ratio:"9:16"，不設last或keyframes，不傳影片參照。若原圖／身份不符、不可用、額度不足或需要額外付款，停止回報，不代換。音訊有實際開關才關，沒有如實記錄，不因音訊重做。
以下英文原文作prompt；標記不傳入：
PROMPT_BEGIN
{prompt}
PROMPT_END
只執行上述一支。完成回報實際first／identity IDs、設定接受情況、新UUID與實際時長／像素／音軌。參數回報、畫面觀察與動態品質通過分開；不要自動補圖、續片或合片。
'''
(T/'grok_request.txt').write_text(request,encoding='utf-8')
still=read(W/'approvals/M03_L01_still_approval_2026-11-04.json');assert sha(ROOT/still['asset_path'])==still['target_sha256']
put(T/'shot_plan.json',{'date':'2026-11-05','status':'prepared_not_submitted','look':'L01','source_still':still['asset_path'],'source_still_sha256':still['target_sha256'],
 'first_frame_asset_id':'2e8df556-7034-4788-92d8-3a769fcdfed3','identity_asset_ids':['26e03f42-2907-488c-b75c-239a2a19b9c8','15c720b2-46b6-45e0-a150-60290e3290e6'],
 'duration_requested':10,'editorial_target_seconds':9,'resolution_requested':'720p','aspect_requested':'9:16','last_frame_asset_id':None,'keyframes':None,
 'prompt_sha256':sha(T/'video_prompt.txt'),'max_new_jobs':1,'new_jobs_submitted':0,'new_still_calls':0,'remaining_quota':'unknown','seed':'unknown','model_version':'unknown',
 'storyboard_approval':rel(P/'user_storyboard_approval_2026-11-05.json'),'previs_approval':rel(P/'user_previs_approval_2026-11-05.json'),
 'review_requirements':['reference-derived development','native performance and proportions','gait/foot contact','hands and bag','full-frame before panel crop','actual 400px panel envelope','approach scale and top of head'],
 'following_action':'No automatic second look or retry; review this exact new source first.'})
plan=read(P/'production_plan.json')
for aid,scope,filename in [('board','storyboard','storyboard.png'),('animatic','previs','timing_animatic.gif')]:
    plan['approvals'].append({'asset_id':aid,'scope':scope,'decision':'approved','target_sha256':sha(P/filename),'receipt_path':rel(P/f'user_{scope}_approval_2026-11-05.json')})
plan['missing_assets']=['生成當下可用控制／額度待核對；單側實片品質仍須驗證。']
plan['generation_scope']['status']='single_L01_test_authorized_prepared'
put(P/'production_plan.json',plan)
print(json.dumps({'prepared':rel(T),'max_new_jobs':1,'new_stills':0}))
