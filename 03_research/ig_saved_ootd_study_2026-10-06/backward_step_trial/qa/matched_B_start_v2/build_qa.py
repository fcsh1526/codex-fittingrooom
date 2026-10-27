from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import hashlib, json

root = Path(r'C:/Users/Brandon_ChangChien/Documents/Codex/人物試衣間')
out = root / '03_research/ig_saved_ootd_study_2026-10-06/backward_step_trial/qa/matched_B_start_v2'
out.mkdir(parents=True, exist_ok=True)
paths = {
    'A native f96': root / '03_research/ig_saved_ootd_study_2026-10-06/backward_step_trial/qa/near_A1/full/frame_000096.png',
    'New B candidate v2': root / '10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/body_distance_matched_start_v2/2026-W37-001-L02_M02_body_distance_matched_start_candidate_v2.png',
    'Approved B wardrobe master': root / '10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/paired_scene_v1/2026-W37-001-L02_M02_reel_full_master_candidate_v1.png',
}
try:
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 21)
except OSError:
    font = ImageFont.load_default()
panels = []
metadata = []
for name, path in paths.items():
    im = Image.open(path).convert('RGB')
    contained = ImageOps.contain(im, (720,1280), Image.Resampling.LANCZOS)
    panel = Image.new('RGB', (720,1280), (225,225,225))
    panel.paste(contained, ((720-contained.width)//2,(1280-contained.height)//2))
    panel.save(out / (name.replace(' ', '_') + '_720_QA.png'))
    panels.append(panel)
    metadata.append({'label':name, 'path':str(path), 'native_size':im.size, 'qa_contained_size':contained.size, 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
board = Image.new('RGB', (2160,1320), 'white')
d = ImageDraw.Draw(board)
for i, (name, panel) in enumerate(zip(paths,panels)):
    board.paste(panel,(i*720,40))
    d.text((i*720+12,8),name+' - QA only',font=font,fill='black')
board.save(out/'full_same_canvas_720_QA.jpg',quality=94)
# Labels and guides exist only on this QA derivative.
guided = Image.new('RGB',(1440,1320),'white')
gd = ImageDraw.Draw(guided)
for i in range(2):
    guided.paste(panels[i],(i*720,40))
    gd.text((i*720+12,8),list(paths)[i]+' - QA only',font=font,fill='black')
    for y in range(100,1280,100):
        gd.line((i*720,y+40,(i+1)*720-1,y+40),fill=(0,160,180),width=1)
        gd.text((i*720+5,y+43),str(y),font=font,fill=(0,110,130))
    gd.line((i*720+360,40,i*720+360,1319),fill=(0,160,180),width=1)
guided.save(out/'A_f96_vs_new_B_grid_720_QA.jpg',quality=94)
# Proportional crops for static face/neckline/shoe inspection. No output assets are edited.
crops=[('A face',panels[0],(280,170,445,330)),('New B face',panels[1],(285,180,420,330)),('Old B face',panels[2],(260,95,445,285)),
       ('New B neckline',panels[1],(260,310,455,495)),('New B shoes',panels[1],(305,905,415,1040)),('Old B neckline',panels[2],(260,265,465,505))]
cb=Image.new('RGB',(1800,680),'white'); cd=ImageDraw.Draw(cb)
for i,(name,im,box) in enumerate(crops):
    x=(i%3)*600; y=(i//3)*340
    crop=ImageOps.contain(im.crop(box),(580,300),Image.Resampling.LANCZOS)
    cb.paste(crop,(x+(600-crop.width)//2,y+40))
    cd.text((x+12,y+7),name+' - QA crop',font=font,fill='black')
cb.save(out/'identity_outfit_details_QA.jpg',quality=95)
(out/'qa_inputs.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(metadata,ensure_ascii=False))
