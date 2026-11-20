"""Prepare a user-requested broader pose sequence, preserving trial01."""
import hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;ROOT=P.parents[6];PREV=P.parent/'trial_01'
if (P/'submission.json').exists():raise SystemExit('Submission exists; do not reset this trial.')
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
quote='側步抬臂眼睛也跟著看手臂，其實整體有點莫名，動作再大一點，再多一點'
feedback={'date':'2026-11-05','actor':'user','quote':quote,'target_asset_id':'a9d31a19-5434-4f47-8682-f8963b6f1d86','target_sha256':sha(PREV/'source.mp4'),'scope':'Trial01 performance not accepted: arm-following gaze feels purposeless; requests larger/more varied action. Not a new physical-quality diagnosis.','decision':'not_accepted_revision_requested','next_authorization':'One revised broader pose test in existing service, retaining approved still; not a finished-film or new-still approval.'}
put(PREV/'user_performance_feedback_2026-11-05.json',feedback)
old=json.loads((PREV/'submission.json').read_text(encoding='utf-8-sig'));old.update(status='user_not_accepted_purposeless_arm_gaze_more_action_requested',user_video_acceptance=False,latest_user_feedback=rel(PREV/'user_performance_feedback_2026-11-05.json'));put(PREV/'submission.json',old)
source=ROOT/old['source_still'];assert sha(source)==old['source_still_sha256']
prompt="""A playful, confident fashion model is showing off her outfit directly to the camera, enjoying a lively sequence of clearly different full-body poses. Her attention stays with the person filming, with warm eye contact and a spontaneous changing smile. Her eyes do not follow her hands or look up at an imaginary object.

Flow through four generous posing phrases at ordinary lively human speed: put both hands on her waist and make a pronounced left-right hip shift with alternating shoulder angles; lift both bent arms forward and then open them into an exuberant high V while smiling toward the lens; lower her arms and make a clear side-facing turn with a real foot pivot, then return toward the camera; finish by opening her bent arms in a playful presenting gesture and settling into a different hand-on-hip pose. The head, torso, hips, knees, feet, arms and clothes participate together. Give each different pose a brief readable beat, with flowing natural transitions and no long idle hold. This should feel like someone happily trying poses for an outfit video, not an isolated arm raise.

One continuous ten-second real-time full-person shot, original locked level chest-height 50mm camera and original subject distance. Use the full portrait width for the performance; keep complete hair, hands and both shoes within the image. Preserve exact M03 identity, ordinary body proportions, long wavy brown hair, open deep-navy blazer, white crewneck tee, charcoal straight trousers, black loafers, small black bag on her left shoulder and silver necklace. The bag and clothes respond naturally to her body. Preserve the shaded office wall, windows, bench, paving and coherent daylight. No camera move, slow motion, outfit change, cut or text."""
(P/'video_prompt.txt').write_text(prompt+'\n',encoding='utf-8')
request='''本次只執行一次新trial02，不是重放a9d31a19。使用者明確回饋上一版「側步抬臂眼睛也跟著看手臂，其實整體有點莫名，動作再大一點，再多一點」。改為面向拍攝者的活潑、多姿態穿搭展示；先用完整9:16幅面測表演，不加入左右窄欄限制，不把動作縮成輕晃。只生成一支10秒720p9:16新影片，不補圖、不做第二套、不重試、不合片、不加購額度／換服務，不改刪舊媒體。
精確First: 2e8df556-7034-4788-92d8-3a769fcdfed3，仍是已核准M03 framing_v2：長棕捲髮、深藍西外白T炭灰直褲、黑樂福、小黑包在她左肩，辦公遮簷長凳，完整頭鞋。face/full asset_ids: ["26e03f42-2907-488c-b75c-239a2a19b9c8","15c720b2-46b6-45e0-a150-60290e3290e6"]，只鎖M03身份／普通比例。不用其他M03舊服裝、選取殘留或上一支影片作first。
先實際查看三個UUID與可用設定。duration:"10", resolution_name:"720p", aspect_ratio:"9:16"，不設last/keyframes。若來源不符／不可用、10秒不支援或額度不足，停下回報，不代換、不生成額外照片。
以下英文逐字傳入prompt，標記不傳入：
PROMPT_BEGIN
'''+prompt+'''
PROMPT_END
重點是四組可辨大幅換姿及面向鏡頭的展示態度；不要眼睛追手或假裝看東西。音軌有真實開關才關，沒有如實回報，不為音訊重生。完成列實際First/identity IDs、設定是否接受、新影片UUID、實際時長／像素／音軌；參數回報、畫面觀察與物理／真人感驗收分開，不自行宣稱通過。
'''
(P/'grok_request.txt').write_text(request,encoding='utf-8')
plan={'date':'2026-11-05','status':'prepared_not_submitted','user_authorization_quote':quote,'context':'Direct request for larger/more varied poses after trial01; ten seconds gives more distinct poses time to read. Not a single-variable A/B experiment.','first_frame_asset_id':old['first_frame_asset_id'],'identity_asset_ids':old['identity_asset_ids'],'source_still':old['source_still'],'source_still_sha256':sha(source),'still_approval':old['still_approval'],'duration_requested':10,'resolution_requested':'720p','aspect_requested':'9:16','max_new_jobs':1,'new_jobs_submitted':0,'new_still_calls':0,'native_speed_required':True,'full_film_generation_authorized':False,'prompt_sha256':sha(P/'video_prompt.txt'),'performance_phrases':['hands on waist, large left-right hip/shoulder poses','both arms forward and high V, attention to lens','side turn and foot pivot, return frontal','bent-arm presentation and new hip pose'],'layout_scope':'Full-frame performance test; no guarantee of narrow-panel fit. Existing parallel film design requires reassessment.','seed':'unknown','model_version':'unknown','remaining_quota':'unknown','last_frame_asset_id':None,'keyframes':None}
put(P/'shot_plan.json',plan)
# A diagram of action peaks, not new photographs or human-motion simulation.
im=Image.new('RGB',(1280,850),'#f5f3ec');d=ImageDraw.Draw(im);f=lambda n:ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',n)
d.text((28,20),'M03 trial02｜面向鏡頭，連續大幅換姿',font=f(30),fill='#213b49')
d.text((28,66),'10秒表演預算｜完整畫幅先測｜原核准首圖不變｜不以本圖認定動態成功',font=f(19),fill='#536365')
names=['叉腰擺臀／轉肩','雙臂高舉／看鏡頭','明顯轉側／回正','攤手展示／收姿']
for i,name in enumerate(names):
 x=22+i*316;y=120;w=290;h=630;cx=x+w/2
 d.rectangle((x,y,x+w,y+h),outline='#b2c1bd',width=2)
 d.text((x+8,y+8),f'{i+1}｜{name}',font=f(18),fill='#213b49')
 head=(cx,y+118);d.ellipse((cx-22,head[1]-33,cx+22,head[1]+33),fill='#d9b29a',outline='#31434b',width=2)
 d.line([(cx,head[1]+32),(cx,y+181)],fill='#31434b',width=4)
 sx=cx-(12 if i==2 else 0);d.polygon([(sx-47,y+184),(sx+47,y+184),(cx+35,y+350),(cx-35,y+350)],fill='#213b54')
 for foot in [cx-29,cx+38]:d.line([(cx+(-17 if foot<cx else 17),y+348),(foot,y+551)],fill='#555c61',width=26);d.line([(foot-13,y+557),(foot+17,y+557)],fill='#26333a',width=7)
 if i==0:arms=[[(sx-47,y+189),(sx-75,y+263),(cx-28,y+327)],[(sx+47,y+189),(sx+77,y+263),(cx+29,y+327)]]
 elif i==1:arms=[[(sx-47,y+189),(sx-72,y+113),(cx-64,y+57)],[(sx+47,y+189),(sx+72,y+113),(cx+64,y+57)]]
 elif i==2:arms=[[(sx-35,y+189),(sx-49,y+277),(sx-42,y+343)],[(sx+35,y+189),(sx+50,y+277),(sx+42,y+343)]]
 else:arms=[[(sx-47,y+189),(sx-66,y+267),(cx-102,y+222)],[(sx+47,y+189),(sx+66,y+267),(cx+102,y+222)]]
 for pts in arms:d.line(pts,fill='#213b54',width=17);hx,hy=pts[-1];d.ellipse((hx-6,hy-7,hx+6,hy+7),fill='#d9b29a')
 d.text((x+10,y+h-40),'示意姿態，非生成影格',font=f(16),fill='#536365')
 d.line([(cx-5,head[1]),(cx+5,head[1])],fill='#31434b',width=2)
d.text((28,790),'視線：與拍攝者交流；不追手。動作需有起落、腳掌實際轉移、手包／衣料合理連動。',font=f(19),fill='#536365')
im.save(P/'action_board.png')
put(P/'preflight.json',{'approved_source_sha256_matches':True,'identity_files_exist':all((ROOT/x).is_file() for x in ['02_brand/reference_models/M03_start_v3_face.png','02_brand/reference_models/M03_start_v3_full.png']),'new_stills_needed_for_first_test':False,'same_service':True,'prior_failed_trials_in_this_expressive_branch':1,'this_request_max_jobs':1,'pause_after_second_failure_unless_user_further_directs':True})
print(json.dumps({'trial02_prepared':True,'duration_requested':10,'new_stills':0,'prior_feedback_saved':True}))
