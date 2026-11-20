"""Continue the accepted single-source performance into the other approved look."""
import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
BR=Path(__file__).resolve().parent;ROOT=BR.parents[5];LEFT=BR/'trial_02';P=BR/'L02_trial_01'
P.mkdir(exist_ok=True)
if (P/'submission.json').exists():raise SystemExit('Skirt submission already exists.')
def rel(p):return p.relative_to(ROOT).as_posix()
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=read(LEFT/'submission.json')
receipt={'actor':'user','decision':'approved','quote':'ok','recorded_at':'2026-11-05','timezone':'Asia/Taipei','scope':'exact trial02 full-frame10.041667s source performance and naturalness, as presented; continue in existing M03 production context','target_sha256':s['silent_sha256'],'source_sha256':s['source_sha256'],'target_asset_id':s['video_asset_id'],'target_path':rel(LEFT/'M03_W45_expressive_trial02_silent_review.mp4'),'context':'Direct reply to the displayed revised performance test with waist/hip poses, high V, side turn, bent knee and presentation finish.','limits':'Not finished parallel-film acceptance, publication/delivery approval, zero-defect technical certification or permission for unseen new stills.'}
put(LEFT/'user_performance_acceptance_2026-11-05.json',receipt)
s.update(status='user_accepted_exact_source_performance',user_acceptance=True,user_acceptance_receipt=rel(LEFT/'user_performance_acceptance_2026-11-05.json'));put(LEFT/'submission.json',s)
v=read(LEFT/'visual_review.json');v.update(status='user_accepted_exact_source_performance',user_acceptance=True,user_acceptance_receipt=rel(LEFT/'user_performance_acceptance_2026-11-05.json'));put(LEFT/'visual_review.json',v)
approval=read(ROOT/'10_automation/runs/2026-W45/approvals/M03_L02_still_approval_2026-11-04.json')
source=ROOT/approval['asset_path'];assert h(source)==approval['target_sha256']
prompt=(LEFT/'video_prompt.txt').read_text(encoding='utf-8').strip().replace('white crewneck tee, charcoal straight trousers, black loafers','cream-white short-sleeve fine-knit top, cream-white calf-length A-line skirt, white-grey low-top sneakers')
prompt=prompt.replace('The bag and clothes respond naturally to her body.','The bag and clothes respond naturally to her body; the A-line skirt sways and opens naturally as her hips and feet change direction, preserving its calf length.')
(P/'video_prompt.txt').write_text(prompt+'\n',encoding='utf-8')
request='''M03 W45 裙裝側延伸，使用者已對精確褲裝414c5d81的多姿態表演回覆ok。現在只生成另一套一支獨立10秒720p9:16來源，延續對鏡頭、活潑大幅多姿態；不要求兩側逐格同步。這不是重生褲裝、不是重用11/4退件裙裝片，不是新照片或整片，不重試、不加購／換服務、不改刪舊媒體。
精確First frame: 1499ae56-08c0-4503-b88f-898a373738e0，使用者已核准M03 L02：同件海軍藍西外、奶油白短袖針織、奶油白及小腿A字裙、白灰球鞋、小黑左肩包、細銀項鍊；長棕捲髮，原辦公遮簷玻璃／長凳／地磚，完整頭鞋。
asset_ids: ["26e03f42-2907-488c-b75c-239a2a19b9c8","15c720b2-46b6-45e0-a150-60290e3290e6"]，只鎖M03 v3身份與普通比例，不複製棚拍服裝。
先實際查看三個UUID與可用設定；不符／不可用／額度不足就停止回報，不代換。duration:"10", resolution_name:"720p", aspect_ratio:"9:16"，不設last/keyframes。以下英文原文作prompt，標記不傳入：
PROMPT_BEGIN
'''+prompt+'''
PROMPT_END
鏡頭是注意對象，不眼睛追手或看虛構物件；自然活潑的完整穿搭換姿，不靠嘴角獨演。音訊有實際開關才關，沒有如實回報。完成列真正First/identity IDs、新影片UUID、設定與實際時長／像素／音軌。參數接受、畫面觀察與物理／真人感通過分開；只此一次，不做新圖或第二支。
'''
(P/'grok_request.txt').write_text(request,encoding='utf-8')
put(P/'shot_plan.json',{'date':'2026-11-05','status':'prepared_not_submitted','source_still':approval['asset_path'],'source_still_sha256':h(source),'still_approval':'10_automation/runs/2026-W45/approvals/M03_L02_still_approval_2026-11-04.json','first_frame_asset_id':'1499ae56-08c0-4503-b88f-898a373738e0','identity_asset_ids':s['identity_asset_ids'],'duration_requested':10,'resolution_requested':'720p','aspect_requested':'9:16','prompt_sha256':h(P/'video_prompt.txt'),'source_performance_acceptance':rel(LEFT/'user_performance_acceptance_2026-11-05.json'),'authorization_note':'Continue M03 after scoped source-performance ok, within existing approved two-look production. No unseen still/final-film/publication approval inferred.','max_new_jobs':1,'new_still_calls':0,'new_jobs_submitted':0,'last_frame_asset_id':None,'keyframes':None,'seed':'unknown','model_version':'unknown','remaining_quota':'unknown'})
print(json.dumps({'accepted_scope':'trial02 source performance only','skirt_prepared':True,'new_stills':0}))
