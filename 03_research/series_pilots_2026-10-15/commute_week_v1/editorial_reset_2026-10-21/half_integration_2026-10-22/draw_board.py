from pathlib import Path
import sys

PROJECT = next(p for p in Path(__file__).resolve().parents if (p/'CURRENT_STATUS.md').exists())
sys.path.insert(0, str(PROJECT/'10_automation/.video_dependencies'))
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
im=Image.new('RGB',(1600,1240),'#f6f4ed')
d=ImageDraw.Draw(im)
INK='#263b44'
def f(n): return ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',n)
def text(x,y,t,n=25,color=INK): d.text((x,y),t,font=f(n),fill=color)
def line(pts,color=INK,w=3): d.line(pts,fill=color,width=w)
def arrow(x,y,xx,yy):
    line([(x,y),(xx,yy)],'#557e72',5)
    line([(xx-13,yy-8),(xx,yy),(xx-13,yy+8)],'#557e72',5)

text(50,28,'五套通勤｜半身放在最後一套的同一鏡內',41)
text(50,91,'分鏡提案；尚未生成這個新鏡頭。先看整套，再靠近看白襯衫與藍包。',25)

text(50,146,'前四套：保留已接受的16.04秒版本',28)
labels=['長西外／深藍褲','白襯衫／棕丹寧','短外套／灰褲','格紋襯衫／灰褲']
colors=['#d8cdbb','#b99779','#c3c8b8','#b6c5ce']
for i,(lab,col) in enumerate(zip(labels,colors)):
    x=50+i*379
    d.rounded_rectangle((x,194,x+357,263),radius=9,fill=col)
    text(x+15,213,str(i+1)+'  '+lab,25)
text(50,285,'第四套→第五套：原人物尺度對齊，約0.75秒柔接；接點仍需看片驗收。',24)

def figure_panel(x,y,w,h,scale,phase):
    p=Image.new('RGB',(w,h),'#edf0eb'); q=ImageDraw.Draw(p)
    for gx in range(-10,w+40,69): q.line([(gx,0),(gx,210)],fill='#c2ceca',width=2)
    q.line([(0,94),(w,94)],fill='#c2ceca',width=2)
    q.rectangle((0,207,w,292),fill='#dfd8ca')
    q.line([(0,292),(w,292)],fill='#c1b8a4',width=3)
    for gy in (344,399,464,530): q.line([(0,gy),(w,gy)],fill='#cdd0c8',width=2)
    # Schematic figure is drawn separately; no photographic identity or gait claim.
    human=Image.new('RGBA',(260,530),(0,0,0,0)); a=ImageDraw.Draw(human)
    a.ellipse((103,14,153,68),fill='#e8ccb8',outline=INK,width=3)
    a.arc((84,6,157,91),170,342,fill='#685247',width=15)
    a.polygon([(101,70),(151,70),(166,222),(91,222)],fill='#fffef7',outline=INK)
    a.polygon([(102,75),(126,97),(126,132),(117,100)],fill='#ebece6',outline=INK)
    a.polygon([(147,75),(127,97),(127,132),(137,98)],fill='#ebece6',outline=INK)
    a.line([(128,132),(128,220)],fill='#bac2be',width=2)
    for by in (151,172,193): a.ellipse((125,by,129,by+4),fill=INK)
    a.polygon([(92,221),(166,221),(207,410),(64,410)],fill='#30373b',outline=INK)
    a.line([(109,411),(84,467),(72,486)],fill='#e3c3ad',width=16)
    a.line([(163,411),(196,475),(218,486)],fill='#e3c3ad',width=16)
    a.line([(65,487),(97,490)],fill='#273038',width=13)
    a.line([(207,488),(239,490)],fill='#273038',width=13)
    a.line([(99,81),(75,166),(115,215)],fill='#e3c3ad',width=15)
    a.line([(151,84),(174,166),(194,211)],fill='#e3c3ad',width=14)
    a.line([(104,87),(69,239)],fill='#355b9a',width=8)
    a.rounded_rectangle((35,211,94,284),radius=10,fill='#31599e',outline=INK,width=3)
    a.line([(49,232),(81,232)],fill='#9bafd2',width=2)
    nw,nh=round(260*scale),round(530*scale)
    human=human.resize((nw,nh),Image.Resampling.LANCZOS)
    px=round(w*.47-nw*.5); py=round(43-14*scale)
    p.paste(human,(px,py),human)
    im.paste(p,(x,y)); d.rectangle((x,y,x+w,y+h),outline='#aab8af',width=2)

panels=[(50,.94,'第五套前段：全身','先讀完整裙裝比例','純展示約3秒'),(568,1.28,'同鏡連續推近','裙裝 → 白襯衫與藍包','靠近約1.5秒'),(1086,1.75,'第五套末段：半身','領口、腰線、藍包更清楚','短收束約0.75秒')]
for x,scale,title,purpose,t in panels:
    text(x,342,title,28)
    figure_panel(x,390,464,525,scale,0)
    text(x+6,932,purpose,25)
    text(x+6,974,t,23,'#4f7568')
arrow(519,653,554,653); arrow(1037,653,1072,653)

text(50,1030,'同一鏡內靠近：不新增剪接、不改人物速度，保持同側、同方向與同一外立面。',26)
text(50,1075,'整片預算約21.29秒；比原全身草案多1.75秒。來源是否能完成此節奏仍待測試。',24)
text(50,1118,'舊半身影片保留；它的背景與新版不同，不能直接塞回。原第五套全身末圖仍未核准。',23)
text(50,1161,'線稿僅說明景別與觀看順序；不是實拍素材，不代表步態、臉孔或空間已通過。',23,'#786957')
im.save(OUT/'half_shot_board.png')
print('half_shot_board.png rendered 1600x1240')
