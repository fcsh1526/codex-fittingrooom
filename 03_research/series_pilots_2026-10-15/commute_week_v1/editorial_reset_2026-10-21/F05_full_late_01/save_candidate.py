from pathlib import Path
import json, hashlib, shutil, sys
sys.path.insert(0, str(Path.cwd() / '10_automation' / '.video_dependencies'))
from PIL import Image, ImageOps, ImageDraw
base = Path.cwd() / '03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21'
d = base / 'F05_full_late_01'
src = Path('C:/Users/Brandon_ChangChien/.codex/generated_images/01a0a39c-4727-7593-ac24-1a8727f9ff61/exec-e9688d43-2fd9-4cf0-afae-cdbe5817e763.png')
dst = d / 'F05_M03_L04_full_late_candidate_A.png'
if dst.exists():
    raise FileExistsError(dst)
shutil.copy2(src, dst)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
first = base / 'F05_full_start_01/F05_M03_L04_full_start_candidate_A.png'
question = '請確認第五套收束圖：臉、白短袖襯衫／黑A字裙、鈷藍包、黑鞋與跨步是否可以沿用？同一外立面前的樹、花台及玻璃角度有變化，場景連貫仍待影片驗證；這版不進門。依你的新圖核准規則，確認後才生成第五段影片。'
receipt = {
    'date':'2026-10-21','mode':'built-in image_gen','intent':'Compatible full-person late walking guide after exact F05 first-still approval',
    'generation_calls':1,'targeted_edits':0,'tool_wait_seconds':27.896,'active_minutes':None,
    'input_roles':[
        {'path':str(first),'sha256':sha(first),'role':'User-approved exact F05 first: same wardrobe, direction, visible site and light; not old doorway'},
        {'path':'02_brand/reference_models/M03_start_v3_face.png','sha256':sha(Path.cwd()/'02_brand/reference_models/M03_start_v3_face.png'),'role':'Approved identity only'},
        {'path':'02_brand/reference_models/M03_start_v3_full.png','sha256':sha(Path.cwd()/'02_brand/reference_models/M03_start_v3_full.png'),'role':'Approved identity/body proportion only'}
    ],
    'prompt':'prompt.txt','prompt_sha256':sha(d/'prompt.txt'),
    'generated_source':str(src),'workspace_copy':dst.name,'sha256':sha(dst),'bytes':dst.stat().st_size,'dimensions':list(Image.open(dst).size),
    'planned_role':'Late full-person control around 4.0s, f96 within selected [0,102) at 24fps; not 6s last frame or demonstrated literal pin',
    'first_still_approval_receipt':'../F05_full_start_01/user_still_approval.json',
    'status':'candidate_pending_exact_user_still_visual_approval',
    'Grok_uploaded':False,'F05_motion_generated':False,'complete_film_approval':False,
    'independent_image_review':None,
    'root_review':{'viewed':['built-in returned native image'],'findings':['Full white shirt / calf-length A-line skirt / cobalt bag / both plain black heels remain immediately readable','Same rightward front-side gait family and sunlight; no invented entry, crosswalk or people visible','Planter and trees now reprojected left and glass grid changed; physical geometry not established'],'differences_to_disclose':['Late image retains similar rather than decisively more frontal angle','Head slightly higher and shoes lower: person a little taller in frame than first','Far hand now swings forward; hem and shoe placement changed','Tree/planter/glass arrangement reprojected; no claim of exact spatial continuity','Fine skirt texture remains'],'motion_pass':False},
    'next':'Inspect candidate and first/late pair; obtain exact new-still user visual approval before one bounded Grok motion trial.'
}
(d/'generation_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
(d/'user_review_request.json').write_text(json.dumps({'date':'2026-10-21','asset':dst.name,'sha256':sha(dst),'question':question,'options':['可以，沿用這張收束圖','臉或服裝需要修正','構圖或背景需要調整'],'answer':None,'status':'awaiting_exact_user_still_visual_approval','F05_motion_approval':False,'complete_film_approval':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
w,h=360,640
board=Image.new('RGB',(w*2,h+42),'white')
draw=ImageDraw.Draw(board)
for i,(p,label) in enumerate([(first,'APPROVED FIRST'),(dst,'CANDIDATE LATE ~4s')]):
    im=Image.open(p).convert('RGB')
    im=ImageOps.contain(im,(w,h))
    board.paste(im,(i*w+(w-im.width)//2,42+(h-im.height)//2))
    draw.text((i*w+8,14),label,fill='black')
board.save(d/'first_late_comparison.jpg',quality=94)
print(json.dumps({'sha256':sha(dst),'bytes':dst.stat().st_size,'dimensions':receipt['dimensions'],'wait_seconds':receipt['tool_wait_seconds']},ensure_ascii=False))

