from pathlib import Path
import json, hashlib, shutil, sys
project=Path.cwd()
sys.path.insert(0,str(project/'10_automation/.video_dependencies'))
from PIL import Image,ImageOps,ImageDraw
base=project/'03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21'
d=base/'F05_half_late_01'
src=Path('C:/Users/Brandon_ChangChien/.codex/generated_images/01a0a39c-4727-7593-ac24-1a8727f9ff61/exec-140ac2c2-c67f-471b-a1e9-1ece94079b94.png')
dst=d/'F05_M03_L04_half_late_candidate_A.png'
if dst.exists(): raise FileExistsError(dst)
shutil.copy2(src,dst)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
first=base/'F05_full_start_01/F05_M03_L04_full_start_candidate_A.png'
r={'date':'2026-10-22','mode':'built-in image_gen','intent':'Approved F05 full-to-half single-shot plan, new head-to-mid-thigh late control candidate','storyboard_approval_receipt':'../half_integration_2026-10-22/user_storyboard_approval.json','first_still_approval_receipt':'../F05_full_start_01/user_still_approval.json','input_roles':[
{'path':str(first),'sha256':sha(first),'role':'Exact approved first: wardrobe, direction, camera flank, lighting and visible site'},
{'path':'02_brand/reference_models/M03_start_v3_face.png','sha256':sha(project/'02_brand/reference_models/M03_start_v3_face.png'),'role':'Approved M03 v3 face identity only'},
{'path':'02_brand/reference_models/M03_start_v3_full.png','sha256':sha(project/'02_brand/reference_models/M03_start_v3_full.png'),'role':'Approved ordinary body proportion only; do not borrow studio wardrobe'}
],'generation_calls':1,'targeted_edits':0,'tool_wait_seconds':48.322,'active_minutes':None,'prompt':'prompt.txt','prompt_sha256':sha(d/'prompt.txt'),'generated_source':str(src),'workspace_copy':dst.name,'sha256':sha(dst),'bytes':dst.stat().st_size,'dimensions':list(Image.open(dst).size),'status':'candidate_pending_exact_user_still_visual_approval','Grok_uploaded':False,'F05_motion_generated':False,'root_review':{'viewed':['built-in returned native image'],'findings':['Whole head, pointed white collar, turned short cuff, black high waist, complete cobalt bag and both hands visible','Direction remains rightward, forward closed-mouth gaze, near arm bent and far arm swinging','No new door/crosswalk/people visible'],'differences_to_disclose':['Far hand now visible and forward in a different walking phase','Some tree/planter/glass details regenerated in tighter perspective; exact parallax not established','Fine skirt fabric pattern retained from approved source'],'motion_pass':False},'independent_still_review':None,'next':'Compare with approved first, exact user visual approval, then one bounded six-second single-shot trial with about3s pure full-outfit reading before continuous push-in; verify controls and achieved timing, no assumed literal pin.'}
(d/'generation_receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
q='請確認第五套半身收束圖：臉、白襯衫領口／黑裙腰線、完整鈷藍包與手部是否可以沿用？遠側手與背景樹、花台的角度有變化，連續推近仍待影片驗證。依你的新圖核准流程，確認後才送Grok做第五鏡。'
(d/'user_review_request.json').write_text(json.dumps({'date':'2026-10-22','asset':dst.name,'sha256':sha(dst),'question':q,'options':['可以，沿用這張半身圖','臉或服裝需要修正','構圖或背景需要調整'],'answer':None,'status':'awaiting_exact_user_still_visual_approval','F05_motion_approval':False,'complete_film_approval':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
w,h=360,640
board=Image.new('RGB',(720,682),'white'); draw=ImageDraw.Draw(board)
for i,(p,label) in enumerate([(first,'APPROVED FULL FIRST'),(dst,'CANDIDATE HALF LATE')]):
 im=ImageOps.contain(Image.open(p).convert('RGB'),(w,h))
 board.paste(im,(i*w+(w-im.width)//2,42+(h-im.height)//2));draw.text((i*w+8,15),label,fill='black')
board.save(d/'first_half_comparison.jpg',quality=94)
print(json.dumps({'sha256':r['sha256'],'bytes':r['bytes'],'dimensions':r['dimensions'],'wait_seconds':r['tool_wait_seconds']},ensure_ascii=False))

