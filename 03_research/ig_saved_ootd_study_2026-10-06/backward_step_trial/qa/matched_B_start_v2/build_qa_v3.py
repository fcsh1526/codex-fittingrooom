from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import hashlib, json
root = Path(r'C:/Users/Brandon_ChangChien/Documents/Codex/人物試衣間')
out = root/'03_research/ig_saved_ootd_study_2026-10-06/backward_step_trial/qa/matched_B_start_v2'
look = root/'10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel'
p2=look/'body_distance_matched_start_v2/2026-W37-001-L02_M02_body_distance_matched_start_candidate_v2.png'
p3=look/'body_distance_matched_start_v2/2026-W37-001-L02_M02_body_distance_matched_start_candidate_v3.png'
po=look/'paired_scene_v1/2026-W37-001-L02_M02_reel_full_master_candidate_v1.png'
ims=[Image.open(p).convert('RGB') for p in [p2,p3,po]]
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21)
board=Image.new('RGB',(1440,1320),'white'); d=ImageDraw.Draw(board)
for i in range(2):
    im=ImageOps.contain(ims[i],(720,1280),Image.Resampling.LANCZOS)
    board.paste(im,(i*720,40))
    d.text((i*720+8,8),['V2 rejected strap - QA only','V3 strap corrected - QA only'][i],font=font,fill='black')
    for y in [185,473,1020]:
        d.line((i*720,40+y,(i+1)*720-1,40+y),fill=(0,160,180),width=1)
        d.text((i*720+5,45+y),str(y),font=font,fill=(0,110,130))
board.save(out/'v2_v3_same_canvas_720_QA.jpg',quality=95)
detail=Image.new('RGB',(1500,740),'white'); dd=ImageDraw.Draw(detail)
for i,(im,box,label) in enumerate(zip(ims,[(510,400,700,810),(510,400,700,810),(535,330,735,850)],['V2 dark narrow strap','V3 grey strap','Approved B grey strap'])):
    cr=ImageOps.contain(im.crop(box),(480,690),Image.Resampling.LANCZOS)
    detail.paste(cr,(500*i+10,40))
    dd.text((500*i+8,8),label+' - QA crop',font=font,fill='black')
detail.save(out/'v2_v3_approved_B_strap_QA.jpg',quality=96)
meta={'candidate_v3_path':str(p3),'candidate_v3_size':ims[1].size,'candidate_v3_sha256':hashlib.sha256(p3.read_bytes()).hexdigest(),'QA_only':True,'delivery_asset_modified':False}
(out/'qa_v3_input.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in meta.items() if k!='candidate_v3_path'}))
