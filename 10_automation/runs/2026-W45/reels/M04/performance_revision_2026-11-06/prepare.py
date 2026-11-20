from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path.cwd(); P=Path(__file__).resolve().parent
def dump(name,obj): (P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
first=ROOT/'10_automation/runs/2026-W45/generated_images/2026-W45-004/looks/2026-W45-004-L01/reel/2026-W45-004-L01_M04_reel_candidate_A_face_v2.png'
assert hashlib.sha256(first.read_bytes()).hexdigest()=='5e6c7a2a00997c2774d0f7a6a1dfa27075cb1304afeb9a81c66cf3133e01957c'
prompt='''Continue naturally from the supplied first frame. She is showing her new floral blouse to the friend filming her outside the bookstore before they leave together. With easy confidence she makes one clear three-quarter body turn to show the side of the outfit, letting her free arm move with the turn while the bag stays on her shoulder. She turns her face back to her friend and briefly waits for their reaction. Amused by the friend's response, her smile opens into a short warm laugh, with a relaxed shoulder release. She then turns toward the open arcade and starts walking away with one or two easy diagonal steps, glancing back at her friend as if inviting them along. Let the gaze, expression, shoulders, arms and weight respond together in one fluid everyday interaction. Give the reaction room to develop; no repetitive swaying or dance routine.

One continuous six-second real-time shot, level chest-height camera with the same natural 50mm look. Begin with the approved full-person composition; keep her face legible and her movement within the frame without zooming toward her face. Preserve the exact woman, normal head/body proportions, tied-back black hair and natural skin texture. Keep the same dark berry-red and cream floral blouse, plain black straight trousers, brown loafers and shoulder bag, silver earrings and fine necklace, with coherent print, daylight and bookstore geometry. No cuts, slow motion, outfit change or text.'''
(P/'S01_prompt.txt').write_text(prompt+'\n',encoding='utf-8')
request='''W45 M04 表演修訂。一支6秒原片，沿用本次附上的三張已核對素材：檔名含reel_candidate_A_face_v2為唯一first，M04_start_v3_face及M04_start_v3_full只作身份參照。先查看三張並回報實際UUID。以本次新英文指令取代上次同距離小側步指令。
只送一次6秒、720p、9:16，不設last/keyframes、不生成照片、不自動重試／剪輯／延伸、不加購升級換服務；若額度／素材不符或需額外付費則停止回報。音訊有實際控制就關，沒有則如實記錄。
以下英文逐字作生成prompt，標記不送入：
PROMPT_BEGIN
'''+prompt+'''
PROMPT_END
完成後回報first／identity UUID、實際設定與影片UUID。控制回報不等於影片品質通過。'''
(P/'S01_request.txt').write_text(request,encoding='utf-8')
dump('source_plan.json',{'date':'2026-11-06','status':'prepared_not_submitted','purpose':'單套花卉上衣搭素色下身；讓觀眾感受自在向朋友展示穿搭的互動','film_method':'sequential_lookbook','stage':'performance source before editorial selection','user_reply':'ok','reply_scope':'Proceed with described performance-direction approach; no new still or finished-film acceptance inferred','source_seconds_requested':6,'source_jobs_limit':1,'first_path':first.relative_to(ROOT).as_posix(),'first_sha256':hashlib.sha256(first.read_bytes()).hexdigest(),'new_stills':0,'beats':['正面銜接明顯三分之二側轉，呈現上衣與褲型','臉回望拍攝者，短暫等待反應','受到回應後笑容展開、肩膀放鬆','轉向騎樓斜向走一兩步並回望同伴'],'timing':'Beats are ordering guidance, not mandatory exact-second keyframes','camera':'stationary level chest height; brief diagonal exit, no shared curved tracking system','detail_edit':'Decide only after source performance review; preserve face during response, do not impose previous crop intervals','previs':'Connected line board sufficient for a stationary shot with short step; no precision route reproduction claimed','prior_rejection_retained':True,'remaining_quota':'unknown'})
font=lambda s:ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',s)
im=Image.new('RGB',(1400,900),'#f4f1eb');d=ImageDraw.Draw(im)
d.text((35,20),'M04｜表演修訂：自在展示 → 等待回應 → 笑開 → 一起離開',font=font(30),fill='#233537')
d.text((35,65),'6秒來源的動作順序示意；時間依實際表演選段。不是生成結果。',font=font(21),fill='#566767')
titles=['1 側轉展示','2 回望同伴','3 笑容展開','4 斜向離開']
notes=[['一次明顯側轉','手臂隨身體帶動','讀花襯衫＋素黑褲'],['臉回向拍攝者','短暫等候反應','保留側身輪廓'],['笑容自然展開','肩膀放鬆回應','此處保留臉與身體'],['一兩步走向騎樓','回望同行者','動作有目的與收尾']]
for i in range(4):
 x=35+i*342; y=145; w=300; h=533
 d.text((x,110),titles[i],font=font(24),fill='#233537')
 d.rectangle((x,y,x+w,y+h),fill='#fffdf8',outline='#b3bbb7',width=2)
 d.line((x+40,y,x+40,y+400,x+w,y+460),fill='#d8d5cd',width=3)
 d.line((x,y+480,x+w,y+480),fill='#d8d5cd',width=3)
 cx=x+150+(15 if i==3 else 0); hy=y+67+(22 if i==3 else 0); s=.92 if i==3 else 1
 # Schematic figure; diagram only, not an edit of approved photography.
 d.ellipse((cx-25,hy-32,cx+25,hy+32),outline='#334849',width=4)
 eye=cx+(8 if i==0 else -3)
 d.ellipse((eye-3,hy-7,eye+3,hy-1),fill='#334849')
 d.arc((cx-12,hy+1,cx+14,hy+19),0,165,fill='#334849',width=3)
 sw=29 if i in (0,1) else 43
 shoulder=hy+46; waist=hy+180*s
 d.polygon([(cx-sw,shoulder),(cx+sw,shoulder),(cx+35,waist),(cx-35,waist)],fill='#6b4850',outline='#334849')
 for fx,fy in [(cx,shoulder+24),(cx-12,shoulder+70),(cx+15,shoulder+100)]:d.ellipse((fx-6,fy-6,fx+6,fy+6),fill='#c29b8f')
 d.line((cx-sw,shoulder,cx-sw-27,shoulder+75,cx-sw-25,waist+45),fill='#334849',width=8)
 d.line((cx+sw,shoulder,cx+sw+20,shoulder+80,cx+sw+10,waist+35),fill='#334849',width=8)
 feet=hy+395*s
 d.line((cx-18,waist,cx-23-(18 if i==3 else 0),feet),fill='#283839',width=24)
 d.line((cx+18,waist,cx+25+(23 if i==3 else 0),feet-15*(i==3)),fill='#283839',width=24)
 if i<2:d.arc((cx-85,hy+120,cx+85,hy+220),200,335,fill='#b77841',width=4)
 if i==3:
  d.line((x+210,y+460,x+260,y+400),fill='#b77841',width=4)
  d.polygon([(x+260,y+400),(x+244,y+406),(x+254,y+418)],fill='#b77841')
 for j,t in enumerate(notes[i]):d.text((x,y+h+18+j*32),t,font=font(21),fill='#334849')
d.text((35,835),'鏡頭：胸高、水平、固定。先看完整表演，再安排穿搭細節；不在主要反應時切掉臉。',font=font(22),fill='#233537')
im.save(P/'storyboard.png')
print(str(P/'storyboard.png'))
