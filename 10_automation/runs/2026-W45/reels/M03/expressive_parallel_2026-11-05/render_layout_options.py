"""Review mockups only: exact source frames, no production-source edits."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json
BR=Path(__file__).resolve().parent;ROOT=BR.parents[5];P=BR/'paired_review_v1';P.mkdir(exist_ok=True)
left=Image.open(BR/'trial_02/qa/frame_013.jpg').convert('RGB')
right=ImageOps.fit(Image.open(ROOT/'10_automation/runs/2026-W45/generated_images/2026-W45-003/looks/2026-W45-003-L02/reel/2026-W45-003-L02_M03_reel_candidate_A.png').convert('RGB'),(720,1280))
paired=Image.new('RGB',(720,1280),'#f1eee6')
for i,im in enumerate([left,right]):
 im=im.crop((135,0,585,1280));im.thumbnail((356,1280));paired.paste(im,(364*i,(1280-im.height)//2))
paired.save(P/'layout_selected_poses.png')
canvas=Image.new('RGB',(1000,1000),'#f5f3ec');d=ImageDraw.Draw(canvas);f=lambda n:ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',n)
d.text((26,18),'M03｜實際版面取捨',font=f(30),fill='#243c49')
d.text((26,64),'左：並排選段，保留兩套同時比較。右：依序全畫面，人物與完整動作較大。',font=f(18),fill='#536365')
for i,(im,title,note) in enumerate([(paired,'A｜左右並排選段','高V／寬幅攤手另保留在完整表演片'),(left,'B｜兩套依序全畫面','完整表演保留；先看完一套再看另一套')]):
 x=38+i*490;im=im.resize((432,768));canvas.paste(im,(x,145));d.text((x,108),title,font=f(23),fill='#243c49');d.text((x,930),note,font=f(17),fill='#536365')
d.text((26,972),'構圖示意：A右側暫用已核准裙裝首圖；不是新成片／新照片。',font=f(16),fill='#536365')
canvas.save(P/'layout_options.png')
(P/'layout_plan.json').write_text(json.dumps({'status':'editorial_layout_options_not_approved_film','aspect_ratio':'9:16','A':{'method':'parallel selected poses','fixed_source_crop':[135,0,585,1280],'panel_width':356,'gutter':8,'scale':356/450,'preserves_native_speed':True,'excluded_for_layout':['two-arm high V','wide-palms presentation'],'note':'Keep full-frame accepted source separate; omit broad gestures for layout, never claim this fixes motion physics.'},'B':{'method':'single sequential','scale':1,'both_sources_full_width':True,'transition_seconds':.75},'right_mockup_is_still':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Layout alternatives rendered for review.')
