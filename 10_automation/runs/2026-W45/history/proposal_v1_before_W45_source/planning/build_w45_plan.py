"""Build the W45 editorial proposal and schematic boards. No media generation or approval."""
import copy
import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[4]
RUN = ROOT / '10_automation/runs/2026-W45'
HERE = RUN / 'planning'
DATE = '2026-11-03'
WEEK = '2026-W45'
FONT = 'C:/Windows/Fonts/msjh.ttc'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def dump(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def writecsv(p, rows, fields):
    with p.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def material_id(week, row):
    s = json.dumps([week, row], ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return 'mi_' + hashlib.sha256(s.encode()).hexdigest()[:20]

def look(mid, order, name, clothing, silhouette, sources, colors, scene, decision, proof, action):
    return dict(model=mid, order=order, name=name, clothing=clothing,
                silhouette=silhouette, sources=sources, colors=colors, scene=scene,
                decision=decision, proof=proof, action=action)

LOOKS = [
    look('M01',1,'小格紋＋深棕直筒褲','米灰小格紋薄棉襯衫敞開、白棉短袖T、巧克力棕高腰直筒牛仔褲、米白低筒鞋、深棕小斜背包','trousers', ['W43-P005','W43-P001'], ['#d5c7b1','#694936'], '台中有遮簷的咖啡店側牆', '格紋只放上半身，褲裝維持俐落直線', '敞開襯衫、白T、棕褲三段分開可見；褲腳不拖地', '聽見朋友從左前方招呼，回看、展開空著的雙手、笑出來'),
    look('M01',2,'咖啡白格紋＋奶油A字裙','咖啡白格紋薄棉短襯衫敞開、深棕不透光背心、奶油白膝下A字棉裙、米白低筒鞋、深棕小斜背包','skirt', ['W43-P007'], ['#947557','#e8dfcc'], '同一咖啡店側牆，不假稱同一連續時間', '保留格紋主題，改用明亮、有展幅的裙形', '深褲直線與淺裙展幅明顯；裙擺和鞋完整入畫', '朋友拿起相機，她扶穩站姿、肩膀轉向朋友後開心張臂'),
    look('M02',1,'深藍＋奶油裙，一只正紅小包','深藍薄棉短袖針織上衣、奶油白小腿中段A字裙、正紅小型肩背包、深藍米白平底包鞋、細銀耳環','skirt', ['W44-P013'], ['#293c53','#e7dfcd'], '台北乾燥、有遮簷的街角咖啡店外', '讓正紅小包成為深藍與奶油白之間唯一高彩度', '一秒能找到紅包；包與上衣、裙子不混色', '認出鏡頭旁等候的朋友，先笑並伸開空著的一手，再自然走近兩三小步'),
    look('M02',2,'淺灰襯衫＋深藍寬褲，紅包延用','淺灰薄棉短袖襯衫半紮、深藍高腰寬褲、同款正紅小型肩背包、奶油白平底包鞋、細銀耳環','trousers', ['W44-P013'], ['#c7c9ca','#293c53'], '台北有遮簷街角；伴隨Carousel，不強塞入本片', '紅包搭褲裝亦保持單一亮點', '紅包輪廓完整、腰線與褲寬清楚', '停在店外等朋友，重心安定、愉快看向店內'),
    look('M03',1,'上班：灰外層與深褲的直線','淺灰無內裡薄西外、白棉圓領T、炭灰高腰直筒九分褲、酒紅窄版皮帶、黑低跟包鞋、黑小肩包','trousers', ['W44-P014'], ['#a7a9ab','#45464a'], '台北辦公樓外有遮簷的休息凳旁', '工作造型用薄外層與直線輪廓', '西外、腰帶、褲線完整可讀；不靠配件色差假裝變裝', '下班後在休息凳旁等朋友，聽到招呼後轉肩、鬆一口氣地笑'),
    look('M03',2,'赴約：梅紫短袖與奶油百褶裙','梅紫細針織圓領短袖上衣、奶油白小腿中段百褶裙、暗紅小肩包、黑低跟包鞋、細銀耳環','skirt', ['W44-P002','W44-P016'], ['#764657','#e9dfca'], '附近有遮簷餐館的外側休息凳；用剪輯表達另一次穿搭', '赴約改柔軟裙形與一個飽和上身色塊', '灰色褲裝與梅紫淺裙在明度、輪廓、材質均有差異', '朋友到來，她站穩後轉肩迎向朋友，笑意從嘴角發展到開懷'),
    look('M04',1,'森林綠素面＋可可提花包','森林綠薄棉圓領短袖上衣、米白高腰直筒長褲、可可棕提花小肩包、深棕樂福鞋、簡單金色耳針','trousers', ['W43-P015'], ['#43564a','#e8e1d4'], '台中書店有遮簷的外牆與櫥窗旁', '衣服保持素面，把紋理留給一只包', '先看整套比例，再看提花織紋與上衣接觸的關係', '看完櫥窗的書，肩膀輕鬆展開，回頭回應同伴；包一直安定掛在肩上'),
    look('M04',2,'奶油素面＋深藍白提花包','奶油白薄棉短袖上衣、深藍直身小腿裙、深藍奶油白提花小肩包、深棕樂福鞋、簡單金色耳針','straight_dress', ['W43-P013'], ['#e8e1d4','#293c53'], '同一書店街區；伴隨Carousel', '用深底提花包配淺上衣，避免圖案在衣服上重複', '提花包不被手臂擋住、深裙與淺上衣分界清楚', '站在櫥窗外側輕鬆回望同伴，雙手自然分離'),
    look('M05',1,'同雙拼色鞋：白T＋深藍寬褲','白棉圓領短袖T、深藍高腰九分寬褲、深藍白拼色低筒球鞋、灰褐柔軟弧形小肩包、細銀耳環','trousers', ['W44-P012','W43-P019'], ['#ece9e2','#263a51'], '高雄戶外展覽入口陰影牆前，固定鏡頭', '先看寬褲如何留出完整低筒鞋面', '腰線、褲腳空隙、拼色鞋面同時可見', '朋友問準備好了嗎，她先歪肩回笑，再將身體轉約二十度展示褲線'),
    look('M05',2,'同雙拼色鞋：白T＋炭灰直身洋裝','同款白棉短袖T、炭灰不貼身細肩帶小腿中段直身洋裝、同款深藍白拼色低筒球鞋、同款灰褐弧形小肩包、細銀耳環','straight_dress', ['W44-P008','W44-P012','W43-P019'], ['#ece9e2','#4c4d51'], '同一展覽入口陰影牆，獨立片段並排而非同時兩人', '同雙鞋配裙時，把腳踝與鞋面留清楚', '裙裝與褲裝輪廓同時可比，兩側頭高、腳底落點一致', '她愉快轉肩看鏡頭再回正，手留在輪廓內，裙擺可自然擺動'),
]

FILMS = [
    dict(model='M01', title='格紋出門，褲裝與裙裝各有精神', hook='同樣是格紋，一眼分出俐落褲線與輕鬆裙形', purpose='看格紋外層配深色直褲或淺色A字裙的輪廓差；人物對朋友的開心反應把穿搭帶進生活。', recipe='sequential_lookbook', layout='single_sequential', reel_orders=[1,2], duration=10.25, frames=246, shots=[([0,132],[1]),([114,246],[2])], reads=[[[0,114]],[[132,246]]], motives=['聽見朋友招呼 → 看向左前方 → 笑並展臂 → 放鬆收回','朋友要拍照 → 站穩轉肩 → 開心展臂 → 回正笑'], timing=['0–2秒已讀得到深棕褲與格紋；2–4秒展臂，不交叉手腕','4.75–5.5秒疊化；5.5–10.25秒淺色裙形完整可讀'], risk='M01先前轉身手漂移：只做小角度轉肩，手離開軀幹、不甩到背後；不是用剪掉壞幀來宣稱修復。'),
    dict(model='M02', title='看到你，就笑著走近', hook='先認出朋友，再有一個開心的靠近', purpose='單套生活代入：看認出朋友時的表情、迎接動作與有限走近；正紅小包一直是服裝焦點。', recipe='custom_experiment', layout='single_sequential', reel_orders=[1], duration=8, frames=192, shots=[([0,192],[1])], reads=[[[0,192]]], motives=['認出鏡頭旁的朋友 → 眼神先定住並笑 → 空著的一手自然打開 → 兩三小步走近 → 停穩笑談'], timing=['0–2秒從全身約68%開始，笑容先有原因','2–5秒沿短而輕微彎曲的路線接近；5–8秒停在約79%全身，不到大頭近景'], risk='步數、實際路線及表演留合理變體；不跑、不要求逐秒仿拍。不以放大畫面遮蓋頭身變形。'),
    dict(model='M03', title='下班赴約，把直線換成柔軟', hook='灰色褲裝，換成梅紫與淺色裙擺', purpose='以明確的褲／裙、深／淺及直線／柔軟材質差異，呈現兩種下班赴約提案。', recipe='everyday_sequence', layout='single_sequential', reel_orders=[1,2], duration=10.5, frames=252, shots=[([0,96],[1]),([78,186],[2]),([168,252],[2])], reads=[[[0,78]],[[96,168]],[[186,252]]], motives=['等待同伴，聽見招呼後從工作狀態放鬆','換一套赴約提案；看見朋友，肩膀轉向對方、笑容展開','中景收回笑意再笑出來，視線仍有對象，雙手不突然入畫'], timing=['0–3.25秒讀工作褲裝；3.25–4秒疊化','4–7秒讀完整赴約裙裝；7–7.75秒疊化；7.75–10.5秒中景回應'], risk='第三鏡需同套L02中景來源或精確可用影格；不可臨時裁掉前鏡腳部當作步態通過。'),
    dict(model='M04', title='素色穿搭，把紋理留給包', hook='先看整套，再走進織紋', purpose='讓觀眾看懂提花小包在素色穿搭中的大小與位置，再用中近景讀出織紋。', recipe='sequential_lookbook', layout='single_sequential', reel_orders=[1], duration=10, frames=240, shots=[([0,96],[1]),([78,174],[1]),([156,240],[1])], reads=[[[0,78]],[[96,156]],[[174,240]]], motives=['看書店櫥窗後回應同伴，肩膀放鬆打開','包掛在同一肩，中近景看織紋與衣料；不伸手抓帶或開拉鍊','回到全身，她向同伴微笑收尾，保持包的位置'], timing=['0–3.25秒全身；3.25–4秒疊化；4–6.5秒包與衣料','6.5–7.25秒疊化；7.25–10秒全身；細節鏡不冒充完整讀衣'], risk='不以AI示意圖宣稱容量、機能或觸感。近景需要可辨織紋的同套來源，不能AI補畫圖案再當同一包。'),
    dict(model='M05', title='同雙低筒鞋，裙褲都留出鞋面', hook='同一位模特兒、同一雙鞋，兩邊輪廓直接比', purpose='同時比較深藍九分寬褲與炭灰直身裙的下擺、腳踝及同雙拼色鞋；不用觀眾憑記憶比。', recipe='parallel_comparison', layout='parallel_comparison', reel_orders=[1,2], duration=8, frames=192, shots=[([0,192],[1,2])], reads=[[[0,192]]], motives=['兩個獨立片段並排；各自回應鏡頭旁朋友，可不同步笑或轉肩，但不走出窄面板'], timing=['0–2秒先讀裙褲差與鞋；2–6秒各自轉肩回笑；6–8秒回正','兩側目標全身74%、頭頂14%、鞋底88%；實圖及成片再量，不以線稿代替驗收'], risk='左右尺度、相同鞋型、包與手的邊界須先比。先做兩側短片的同時對照，兩次不成立就改全幅依序。'),
]

def font(size):
    return ImageFont.truetype(FONT, size)

def wrap(draw, text, size, width):
    rows=[]; line=''
    for ch in text:
        if ch=='\n': rows.append(line); line=''; continue
        if draw.textlength(line+ch, font=font(size)) > width and line:
            rows.append(line); line=ch
        else: line+=ch
    if line: rows.append(line)
    return rows

def textblock(d, xy, text, size, width, fill='#26323b', gap=7):
    x,y=xy
    for line in wrap(d,text,size,width):
        d.text((x,y),line,font=font(size),fill=fill); y+=size+gap
    return y

def person(d, box, look, hfrac=.74, cx=.5, top=.14, pose=0, detail=False):
    x,y,w,h=box
    H=h*hfrac; center=x+w*cx; headtop=y+h*top
    unit=H/7.5; shoulder=headtop+unit*1.65; waist=headtop+unit*3.3
    hips=headtop+unit*3.9; bottom=headtop+H
    ink='#2f3941'; sw=max(2,int(w/160)); torso=unit*.82
    d.ellipse((center-unit*.42,headtop,center+unit*.42,headtop+unit),outline=ink,width=sw,fill='#f4e7da')
    d.line([(center-unit*.16,headtop+unit),(center-unit*.16,shoulder),(center+unit*.16,shoulder),(center+unit*.16,headtop+unit)],fill=ink,width=sw)
    d.polygon([(center-unit*.8,shoulder),(center+unit*.8,shoulder),(center+torso,hips),(center-torso,hips)],fill=look['colors'][0],outline=ink,width=sw)
    if '格紋' in look['clothing']:
        for off in [-.6,-.3,0,.3,.6]: d.line([(center+unit*off,shoulder),(center+unit*off,hips)],fill='#77736c',width=sw)
        for j in range(5): d.line([(center-torso,shoulder+j*(hips-shoulder)/5),(center+torso,shoulder+j*(hips-shoulder)/5)],fill='#77736c',width=sw)
    if '敞開' in look['clothing'] or '西外' in look['clothing']:
        inner='#694936' if '深棕不透光背心' in look['clothing'] else '#f6f3eb'
        d.polygon([(center-unit*.22,shoulder),(center+unit*.22,shoulder),(center+unit*.36,hips),(center-unit*.36,hips)],fill=inner,outline=ink,width=sw)
    if look['silhouette']=='trousers':
        for sign in [-1,1]:
            d.polygon([(center+sign*unit*.08,hips),(center+sign*unit*.82,hips),(center+sign*unit*.72,bottom-unit*.25),(center+sign*unit*.16,bottom-unit*.25)],fill=look['colors'][1],outline=ink,width=sw)
    else:
        wid=1.35 if look['silhouette']=='skirt' else .9
        d.polygon([(center-torso,waist),(center+torso,waist),(center+unit*wid,bottom-unit*1.15),(center-unit*wid,bottom-unit*1.15)],fill=look['colors'][1],outline=ink,width=sw)
        if '細肩帶' in look['clothing']:
            d.polygon([(center-unit*.63,shoulder+unit*.52),(center+unit*.63,shoulder+unit*.52),(center+torso,waist),(center-torso,waist)],fill=look['colors'][1],outline=ink,width=sw)
            for sign in [-1,1]: d.line([(center+sign*unit*.56,shoulder),(center+sign*unit*.56,shoulder+unit*.55)],fill=ink,width=sw)
        for sign in [-1,1]: d.line([(center+sign*unit*.38,bottom-unit*1.15),(center+sign*unit*.38,bottom-unit*.2)],fill=ink,width=sw)
    for sign in [-1,1]:
        sx=center+sign*unit*.76
        if pose==1:
            elbow=(sx+sign*unit*.7,shoulder-unit*.15); wrist=(sx+sign*unit*1.12,shoulder-unit*.65)
        elif pose==2 and sign==-1:
            elbow=(sx+sign*unit*.55,shoulder+unit*.2); wrist=(sx+sign*unit*.92,shoulder-unit*.1)
        else:
            elbow=(sx+sign*unit*.12,waist+unit*.1); wrist=(sx+sign*unit*.06,hips+unit*.42)
        d.line([(sx,shoulder),elbow,wrist],fill=ink,width=sw)
        d.ellipse((wrist[0]-unit*.1,wrist[1]-unit*.13,wrist[0]+unit*.1,wrist[1]+unit*.13),outline=ink,width=sw,fill='#f4e7da')
        d.rounded_rectangle((center+sign*unit*.39-unit*.24,bottom-unit*.22,center+sign*unit*.39+unit*.3,bottom),radius=3,fill='#e4e6e3',outline=ink,width=sw)
    bagfill=('#ad302c' if '正紅' in look['clothing'] else '#763d42' if '暗紅' in look['clothing'] else '#8b8375' if '灰褐' in look['clothing'] else '#33383c' if '黑小肩包' in look['clothing'] else '#785e4a')
    bx=center+unit*.88; by=waist+unit*.1
    d.line([(center+unit*.66,shoulder),(bx,by)],fill=ink,width=sw)
    d.rounded_rectangle((bx-unit*.32,by,bx+unit*.34,by+unit*.52),radius=5,fill=bagfill,outline=ink,width=sw)
    if '提花' in look['clothing']:
        for j in range(3): d.line([(bx-unit*.28,by+unit*(j*.13+.09)),(bx+unit*.3,by+unit*(j*.13+.09))],fill='#e7d6bc',width=sw)
    d.arc((center-unit*.2,headtop+unit*.42,center+unit*.2,headtop+unit*.77),0,180,fill=ink,width=sw)

def stage(d, box, look, pose=0, hfrac=.74, cx=.5, top=.14, parallel_look=None, wall_floor_v=None):
    x,y,w,h=box
    d.rectangle((x,y,x+w,y+h),fill='#eeece6',outline='#98a2aa',width=2)
    floor=.89 if wall_floor_v is None else wall_floor_v
    d.line([(x,y+h*floor),(x+w,y+h*floor)],fill='#b9b5ad',width=2)
    if wall_floor_v is None:
        d.line([(x+w*.08,y),(x+w*.08,y+h*floor)],fill='#d1cbc2',width=2)
    if parallel_look:
        d.line([(x+w*.5,y),(x+w*.5,y+h)],fill='#fff',width=5)
        person(d,(x,y,w*.5,h),look,hfrac,.5,top,0)
        person(d,(x+w*.5,y,w*.5,h),parallel_look,hfrac,.5,top,0)
    else: person(d,box,look,hfrac,cx,top,pose)

def render_board(film):
    mid=film['model']; ls=[l for l in LOOKS if l['model']==mid]
    p=HERE/mid; p.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGB',(1660,1280),'#fbfaf6'); d=ImageDraw.Draw(im)
    d.text((36,25),f"W45 · {mid} · {film['title']}",font=font(36),fill='#233b41')
    textblock(d,(36,85),film['purpose'],23,1580)
    specs={
      'M01':[(ls[0],0,0,'0秒｜深褲，已看見朋友'),(ls[0],1,3,'3秒｜展臂回應招呼'),(ls[1],0,5.5,'5.5秒｜淺色裙形揭露'),(ls[1],1,9,'9秒｜笑著回正')],
      'M02':[(ls[0],0,0,'0秒｜認出朋友，全身68%'),(ls[0],2,2,'2秒｜笑並打開一手'),(ls[0],0,5,'5秒｜靠近停穩，全身79%'),(ls[0],0,8,'8秒｜保持距離，笑著回應')],
      'M03':[(ls[0],0,0,'0秒｜灰色褲裝等候'),(ls[1],0,4,'4秒｜淺裙與梅紫完整讀衣'),(ls[1],2,6,'6秒｜看見朋友後轉肩'),(ls[1],0,9,'9秒｜同套中景笑談')],
      'M04':[(ls[0],0,0,'0秒｜素面全身與包的位置'),(ls[0],0,4,'4秒｜包與衣料中近景'),(ls[0],2,7.25,'7.25秒｜回到全身'),(ls[0],0,9.5,'9.5秒｜回應同伴微笑')],
      'M05':[(ls[0],0,0,'0秒｜同雙鞋，裙褲一起看'),(ls[0],0,2,'2秒｜保留清楚閱讀'),(ls[0],0,5,'5秒｜各自回笑、小角度轉肩'),(ls[0],0,8,'8秒｜回正，鞋面持續可見')],
    }[mid]
    for i,(l,pose,t,caption) in enumerate(specs):
        x=36+i*407; box=(x,190,360,640)
        if mid=='M02':
            v=project(character(t)); stage(d,box,l,pose,v['person_height_fraction'],v['person_center_uv'][0],v['top'],wall_floor_v=PRINCIPAL_V+1.15*FOCAL/4.4)
        elif mid=='M03' and i==3:
            medium=Image.new('RGB',(360,640),'#eeece6')
            stage(ImageDraw.Draw(medium),(0,0,360,640),l,pose,1.75,.5,.08)
            im.paste(medium,(x,190))
        elif mid=='M04' and i==1:
            d.rectangle((x,190,x+360,830),fill='#eeece6',outline='#98a2aa',width=2)
            d.rectangle((x+20,270,x+335,710),fill=l['colors'][0],outline='#2f3941',width=3)
            d.line([(x+195,230),(x+200,420)],fill='#5b4e42',width=7)
            d.rounded_rectangle((x+110,420,x+295,605),radius=18,fill='#785e4a',outline='#2f3941',width=4)
            for j in range(6): d.line([(x+120,435+j*26),(x+285,435+j*26)],fill='#e7d6bc',width=3)
        else: stage(d,box,l,pose,parallel_look=ls[1] if mid=='M05' else None)
        if mid=='M05' and i==2:
            d.text((x+113,395),'↶',font=font(32),fill='#a75c35')
            d.text((x+292,395),'↷',font=font(32),fill='#a75c35')
        textblock(d,(x,850),caption,22,360)
        label=l['name'] if mid!='M05' else '左：九分寬褲／右：直身裙\n兩側全身74%，同高同落點'
        textblock(d,(x,915),label,21,360)
    yy=textblock(d,(36,1000),' → '.join(film['motives']),22,1580)
    yy=textblock(d,(36,yy+12),'時間：'+'；'.join(film['timing']),21,1580)
    textblock(d,(36,yy+12),'待驗證：'+film['risk']+' 線稿僅為構圖／表演提案；非AI照片、非生成結果或動態QA。',20,1580,fill='#90502e')
    im.save(p/'storyboard.png')
    return p/'storyboard.png'

# One common schematic route, clock and projection for both views; no gait simulation.
HUMAN=1.68; FOCAL=.68*3.5/HUMAN; PRINCIPAL_V=.338
def character(t):
    u=max(0,min(1,(t-2)/3))
    return [.30*(1-u)+.07*math.sin(math.pi*u),0,3.5-.5*u]

def project(pos):
    x,_,z=pos; hh=HUMAN*FOCAL/z
    cy=PRINCIPAL_V+(1.15-HUMAN/2)*FOCAL/z
    return dict(person_center_uv=[.5+x*FOCAL/z/(9/16),cy],person_height_fraction=hh,top=cy-hh/2)

def space_data():
    frames=[0,48,84,120,192]
    return dict(id='W45_M02_short_meeting_v1',units='schematic',
      unit_note='Relative schematic units; physical scale is unmeasured. Framing uses an explicit off-centre principal point, not a calibrated lens or a promised engine trajectory.',
      axes='x_right_y_up_z_forward',geometry=[
        dict(id='wall',vertices=[[-2,0,4.4],[2,0,4.4],[2,2.6,4.4],[-2,2.6,4.4]]),
        dict(id='pavement',vertices=[[-2,0,2.5],[2,0,2.5],[2,0,4.4],[-2,0,4.4]])],
      render_model=dict(person_height=HUMAN,normalized_focal_length=FOCAL,principal_point_uv=[.5,PRINCIPAL_V],
        note='Simplified perspective/framing illustration only; level camera, fixed independent camera path. Not anatomy, gait or physical camera calibration.'),
      routes=[dict(shot_id='S01',
        character_samples=[dict(frame=f,position=character(f/24),heading_degrees=180,gait_phase='standing; contact must be checked in generated footage' if f<=48 or f>=120 else 'short approach; gait phase not simulated') for f in frames],
        camera_samples=[dict(frame=f,position=[0,1.15,0],target=[0,1.15,4],vertical_fov_degrees=math.degrees(2*math.atan(.5/FOCAL))) for f in frames],
        projected_samples=[dict(frame=f,**{k:v for k,v in project(character(f/24)).items() if k!='top'},visible_landmark_ids=['wall','pavement'],visible_clothing='full outfit; red bag stays on shoulder') for f in frames])])

def render_previs(space):
    p=HERE/'M02'; p.mkdir(parents=True,exist_ok=True)
    # Render positions from the exported source, with the same analytic route recorded below.
    def at(t):
        # Analytic expression is part of the exported common source, rather than a separate path.
        u=max(0,min(1,(t-space['route_function']['start_seconds'])/space['route_function']['move_seconds']))
        a=space['route_function']
        return [a['x_start']*(1-u)+a['x_bulge']*math.sin(math.pi*u),0,a['z_start']-a['z_travel']*u]
    def uv(pos):
        rm=space['render_model']; cam=space['routes'][0]['camera_samples'][0]['position']
        z=pos[2]-cam[2]; ff=rm['normalized_focal_length']; height=rm['person_height']*ff/z
        v=rm['principal_point_uv'][1]+(cam[1]-rm['person_height']/2)*ff/z
        return [.5+(pos[0]-cam[0])*ff/z/(9/16),v,height]
    frames=[]
    for n in range(96):
        t=n/12; pos=at(t); u,v,h=uv(pos)
        im=Image.new('RGB',(1100,790),'#fbfaf6'); d=ImageDraw.Draw(im)
        d.text((28,18),'W45 M02｜同一時間的俯視與相機構圖',font=font(30),fill='#233b41')
        d.text((28,67),f'{t:04.1f}s / 8.0s    相機固定 · 人物短程接近',font=font(23),fill='#3b5459')
        # Overhead coordinates use the exact same scene positions and camera location.
        def overhead(q): return (270+q[0]*170,660-q[2]*120)
        wall=space['geometry'][0]['vertices']
        d.line([overhead(q) for q in [wall[0],wall[1]]],fill='#6f7c80',width=8)
        path=[overhead(at(i/12)) for i in range(25,61)]
        d.line(path,fill='#b8c5bc',width=5)
        cam=overhead(space['routes'][0]['camera_samples'][0]['position'])
        end=overhead([0,0,4.4]); d.line([cam,end],fill='#adb5b9',width=2)
        d.rectangle((cam[0]-13,cam[1]-8,cam[0]+13,cam[1]+8),fill='#334e5a')
        now=overhead(pos); d.ellipse((now[0]-12,now[1]-12,now[0]+12,now[1]+12),fill='#b13a36')
        d.text((30,160),'俯視：紅點是人物，藍色是相機',font=font(20),fill='#26323b')
        d.text((30,700),'2–5秒移動，其餘停穩回應朋友',font=font(21),fill='#26323b')
        wall_z=space['geometry'][0]['vertices'][0][2]
        cam_y=space['routes'][0]['camera_samples'][0]['position'][1]
        wall_v=space['render_model']['principal_point_uv'][1]+cam_y*space['render_model']['normalized_focal_length']/wall_z
        stage(d,(635,120,315,560),LOOKS[2],2 if 1.3<t<2.6 else 0,h,u,v-h/2,wall_floor_v=wall_v)
        textblock(d,(600,700),'人物68% → 約79%；保持完整頭身與鞋。線稿未模擬步態，不能認定腳掌接地通過。',20,465)
        frames.append(im)
    frames[0].save(p/'previs.gif',save_all=True,append_images=frames[1:],duration=[80,80,90]*32,loop=0,optimize=False)
    frames[0].save(p/'overhead_and_view.png')
    # Static contact sheet to inspect start / movement / stop without claiming native-video QA.
    contact=Image.new('RGB',(2200,1580),'white')
    for i,n in enumerate([0,24,60,95]): contact.paste(frames[n],((i%2)*1100,(i//2)*790))
    contact.save(p/'previs_contact_sheet.png')

def main():
    HERE.mkdir(parents=True,exist_ok=True)
    for i,f in enumerate(FILMS,1):
        f['carousel_id']=f'{WEEK}-{i:03d}'
        for l in [x for x in LOOKS if x['model']==f['model']]:
            l['carousel_id']=f['carousel_id']; l['look_id']=f"{f['carousel_id']}-L{l['order']:02d}"
            l['source_material_ids']=[material_id('2026-'+s.split('-')[0],s) for s in l['sources']]
    space=space_data()
    space['route_function']=dict(start_seconds=2,move_seconds=3,x_start=.30,x_bulge=.07,z_start=3.5,z_travel=.5)
    dump(HERE/'M02/space.json',space)
    render_previs(space)
    refs=list(csv.DictReader((ROOT/'02_brand/mira_reference_images.csv').open(encoding='utf-8-sig')))
    results={}
    spec=importlib.util.spec_from_file_location('mira_plan_check',ROOT/'11_skills/mira-reel-director/scripts/plan.py')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    for f in FILMS:
        mid=f['model']; p=HERE/mid; board=render_board(f)
        ls=[x for x in LOOKS if x['model']==mid]
        used=[x for x in ls if x['order'] in f['reel_orders']]
        ref=next(x for x in refs if x['model_profile_id']==mid)
        plan=json.loads((ROOT/'11_skills/mira-reel-director/assets/production_plan.template.json').read_text(encoding='utf-8-sig'))
        plan.update(plan_id=f'W45_{mid}_v1',status='in_review',path_base='project')
        plan['weeks']=dict(source=['2026-W43','2026-W44'],content=WEEK,delivery=None)
        plan['editorial']=dict(audience='台灣日常穿搭讀者',takeaway=f['purpose'],visual_theme='薄層次、生活中的表情與清楚服裝輪廓',selection_rationale=f['hook']+'；W45上游週報缺，近週來源與11/3補充查核分開記錄。')
        plan['presentation']=dict(layout_id=f['layout'],recipe_id=f['recipe'])
        if f['recipe']=='custom_experiment':
            plan['presentation'].update(recipe_name='固定鏡頭的認出與短程會合',viewer_mechanism='先看認出朋友的反應，再看穿搭在短程走近時的樣子',evidence_status='proposed_transfer_of_prior_motivated_performance')
        plan['film'].update(frame_count=f['frames'],duration_seconds=f['duration'])
        assets=[]
        def asset(aid,kind,path,**extra):
            rec=dict(id=aid,kind=kind,path=path.relative_to(ROOT).as_posix(),sha256=sha(path),**extra)
            assets.append(rec); return aid
        face=ROOT/ref['reference_face_path']; full=ROOT/ref['reference_full_path']
        assert face.is_file() and full.is_file() and ref['status']=='approved'
        asset(mid+'_face','identity',face); asset(mid+'_full','identity',full)
        plan['models']=[dict(id=mid,identity_asset_ids=[mid+'_face',mid+'_full'])]
        plan['looks']=[dict(id=l['look_id'],model_id=mid,wardrobe_summary=l['clothing'],source_asset_ids=[]) for l in used]
        asset('board','storyboard',board)
        plan['shots']=[]
        for i,((interval,orders),read) in enumerate(zip(f['shots'],f['reads']),1):
            shot=dict(id=f'S{i:02d}',look_ids=[l['look_id'] for l in ls if l['order'] in orders],frames=interval,
              clothing_purpose=f['purpose'] if not(mid=='M04' and i==2) else '只讀包與衣料的織紋；此段不計完整全身讀衣',
              clear_read_intervals=read,storyboard_asset_id='board',previs_asset_id=None,input_asset_ids=[],
              scene_reference_asset_ids=[],space_mode='independent',performance=f['motives'][min(i-1,len(f['motives'])-1)],
              execution_mode='generate',camera='fixed',source_duration_note='Output timing is editorial. Available Grok lengths, real usable intervals and source shortage must be recorded at execution; no retiming/freezes.')
            if mid=='M03' and i==3: shot['framing']='same-look medium shot; new approved source or exact approved-footage lineage required'
            if mid=='M04' and i==2: shot['framing']='bag plus upper-body garment context; no full-outfit claim'
            if mid=='M05':
                shot['panels']=[dict(id='left',look_id=ls[0]['look_id'],height_fraction=.74,head_v=.14,shoe_v=.88),dict(id='right',look_id=ls[1]['look_id'],height_fraction=.74,head_v=.14,shoe_v=.88)]
            plan['shots'].append(shot)
        plan['transitions']=[dict(from_shot=f'S{i:02d}',to_shot=f'S{i+1:02d}',frames=[f['shots'][i][0][0],f['shots'][i-1][0][1]],overlap_frames=18,method='cross_dissolve') for i in range(1,len(f['shots']))]
        if mid=='M02':
            plan['space']=space; plan['shared_space_asset_id']='common_space'
            asset('common_space','space_plan',p/'space.json')
            source=dict(asset_id='common_space',sha256=sha(p/'space.json'))
            asset('previs','previs',p/'previs.gif',derived_from=source)
            asset('overhead','overhead',p/'overhead_and_view.png',derived_from=source)
            plan['shots'][0].update(space_mode='shared_world',previs_asset_id='previs',overhead_asset_id='overhead')
        plan['assets']=assets
        plan['missing_assets']=['使用者對W45具體企劃與線稿的確認；不從「繼續W45」推定新圖核准',
          '各鏡全新、逐張核准的原生9:16起始圖；現有身份參照不等於新造型圖',
          'W45上游週報／原始CSV尚未取得；可評估本提案但必須保留此來源缺口',
          '正式生成當下的Grok額度、可用片長與設定尚待核對；未送工作']
        if mid in ['M03','M04']: plan['missing_assets'].append('額外同套中景／細節構圖來源，或有精確來源與適用核准範圍的影片影格')
        dump(p/'production_plan.json',plan)
        result=module.Check(plan,p/'production_plan.json',ROOT).run()
        dump(p/'planning_validation.json',result)
        results[mid]=dict(status=result['status'],ready_for_generation=result['ready_for_generation'],errors=result['errors'],timeline=result['timeline'])
        card=[f"# W45 {mid}｜{f['title']}",'','狀態：完整提案，待使用者確認；未生成起始圖或影片。','',
              '觀眾看點：'+f['purpose'],'','入片：'+str(len(used))+'套；週庫存：2套。',
              '來源單品：'+'、'.join(sorted({s for l in ls for s in l['sources']}))+'；完整搭配與情境為本專案編輯提案。','',
              '![連接分鏡](storyboard.png)','','## 拍攝卡','']
        for i,s in enumerate(plan['shots']):
            card += [f"- {s['id']}：{s['frames'][0]/24:g}–{s['frames'][1]/24:g}秒；"+s['performance']+'。',
                     f"  服裝閱讀區間：{[[a/24,b/24] for a,b in s['clear_read_intervals']]}秒；相鄰鏡沿用0.75秒疊化比較基準。"]
        card += ['','風險及重試界線：'+f['risk'],'',
          '生成策略：簡短情境／動機＋必要可見反應，保留合理自然變體；不每秒堆手勢。每個相同機制至多兩次失敗，之後改設計或轉研究。',
          '審查：先實際起始圖服裝、身份與構圖；再逐鏡原速看手／腳／頭身、連續性；有接點先看完整重疊段，最後整片。解碼與抽格不等於原速QA。',
          '來源設定：片長為剪輯目標，不是聲稱Grok可精確輸出；依實際可用原速素材選段，素材不足即縮短／補拍，不用變速或停格補足。',
          '身份參照：'+ref['reference_face_path']+'；'+ref['reference_full_path']+'。',
          '照片鏡頭沿用全片幅無反、50mm、接近胸高、水平光軸；實際構圖要再比對，預演不是引擎或物理標定。']
        if mid=='M02': card += ['','![共同空間預演](previs.gif)','', '空間／相機構圖同用 space.json。人物全身目標68%→79%，相機不移動。相對示意單位，步態未模擬。']
        elif mid=='M05': card += ['','必要預演：線稿已按實際9:16並排版面畫兩側等高人物；動畫與AI原片尚未產出。先做短段的同時尺度／節奏對照。']
        else: card += ['','空間雙路徑預演：不適用。固定站位或獨立鏡頭；連接線稿已列起訖、景別和重疊區間。']
        (p/'SHOT_CARDS.md').write_text('\n'.join(card)+'\n',encoding='utf-8')
    dump(HERE/'planning_validation_summary.json',results)
    assert all(not r['errors'] for r in results.values()), results
    dump(HERE/'editorial_plan.json',dict(schema_version=1,content_week=WEEK,planning_date=DATE,status='proposed_pending_user_plan_review',
         source_gap='Perplexity public index latest W44; W45 report absent as checked 2026-11-03; no substituted source CSV.',
         weekly_inventory_looks=10,weekly_reels=5,reel_look_count=8,companion_only_looks=2,films=FILMS,looks=LOOKS,
         production_order=['M02','M01','M03','M04','M05'],generated_stills=0,generated_videos=0,cloud_paid_requests=0))
    oldlook=list(csv.DictReader((ROOT/'10_automation/runs/2026-W44/weekly_look_plan.csv').open(encoding='utf-8-sig')))
    fields=list(oldlook[0]); rows=[]
    for l in LOOKS:
        f=next(x for x in FILMS if x['model']==l['model'])
        row={k:'' for k in fields}; row.update(week_id=WEEK,carousel_id=l['carousel_id'],model_profile_id=l['model'],look_id=l['look_id'],look_order=l['order'],theme_name=f['title'],opening_hook=f['hook'],look_name=l['name'],dressing_decision=l['decision'],occasion='日常外出／赴約',clothing_item=l['clothing'],color_palette='；'.join(l['colors']),fabric='薄棉／薄針織等編輯材質；不是來源商品規格',fit=l['proof'],styling_rules='全套依本列鎖定；來源單品不等於整套來源',visual_proof=l['proof'],practical_rule=l['decision'],scene=l['scene'],visible_action=l['action'],frame_plan='Reel: native 9:16 full A + reviewed styling-proof; Carousel: A full / B scene / C detail',required_frames='Reel A+proof; Carousel A+B+C',status='editorial_proposed_pending_plan_review',next_action='W45方案確認後，先製作M02 L01起始圖候選；各張核准後才進動態')
        rows.append(row)
    writecsv(RUN/'weekly_look_plan.csv',rows,fields)
    packetfields=list(next(csv.DictReader((ROOT/'10_automation/runs/2026-W44/weekly_content_packet.csv').open(encoding='utf-8-sig'))))
    packet=[]
    for f in FILMS:
        l=next(x for x in LOOKS if x['model']==f['model'] and x['order']==1)
        r={k:'' for k in packetfields};r.update(week_id=WEEK,carousel_id=f['carousel_id'],market='TW',model_profile_id=f['model'],trend_name=f['title'],content_bucket='utility_with_immersion',audience='台灣日常穿搭讀者',occasion='日常外出／赴約',content_engine=f['recipe'],dressing_decision=l['decision'],visible_action=l['action'],audience_problem=f['hook'],editorial_answer=f['purpose'],opening_hook=f['hook'],visual_proof=l['proof'],practical_rule=l['decision'],clothing_item=l['clothing'],color_palette='；'.join(l['colors']),scene=l['scene'],status='editorial_proposed_pending_plan_review',next_action='先確認企劃／分鏡，再生成首張候選圖')
        packet.append(r)
    writecsv(RUN/'weekly_content_packet.csv',packet,packetfields)
    needs=[]
    for l in LOOKS:
        f=next(x for x in FILMS if x['model']==l['model'])
        for surface,role in [('reel','A_full_9x16'),('reel','styling_proof'),('carousel','A_full'),('carousel','B_scene'),('carousel','C_accessory')]:
            needs.append(dict(look_id=l['look_id'],model=l['model'],surface=surface,role=role,reel_used=l['order'] in f['reel_orders'],status='missing_not_generated',reuse_candidate='proof may reuse an exact-outfit approved view only after vertical/clarity review' if role=='styling_proof' else '',plan='No W44 outfit is asserted to match this new complete outfit; identity refs reuse only.'))
    needs += [dict(look_id='2026-W45-003-L02',model='M03',surface='reel',role='medium_S03',reel_used=True,status='missing_or_exact_frame_lineage_needed',reuse_candidate='Review same-outfit footage after generation',plan='May be fulfilled by reviewed same-outfit proof if composition supports it.'),dict(look_id='2026-W45-004-L01',model='M04',surface='reel',role='bag_detail_S02',reel_used=True,status='missing_or_reviewed_proof_needed',reuse_candidate='Review same-outfit proof',plan='May be fulfilled by clear vertical styling-proof; no automatic crop approval.')]
    writecsv(RUN/'asset_requirements.csv',needs,list(needs[0]))
    dump(RUN/'reuse_assessment.json',dict(date=DATE,scope='wardrobe metadata and exact identity-file presence/hash; not visual acceptance of legacy stills',
        existing_look_plan='10_automation/runs/2026-W44/weekly_look_plan.csv',existing_film_receipts='10_automation/runs/2026-W44/publishing_structure.md',
        finding='W44 films remain delivered as W44. Proposed W45 complete outfits differ; no exact still/clip reuse is certified. Approved identity anchors reused. Styling proofs may reuse a new approved exact-outfit view only after composition/clarity review.',
        role_count=52,baseline_roles=50,additional_view_roles=2,unique_new_image_range='40–52 planning range, conditional on 10 proof reuses and 2 medium/detail roles being satisfied by those views. No promised reuse before visual review.',
        new_generation_jobs_submitted=0,paid_cloud_requests=0))
    overview=Image.new('RGB',(1660,1710),'#fbfaf6'); d=ImageDraw.Draw(overview)
    d.text((35,24),'W45｜五個看點，五位模特兒',font=font(40),fill='#233b41')
    d.text((35,82),'10套週庫存 · 5支Reel提案 · 未生成照片或影片',font=font(26),fill='#56676d')
    for i,f in enumerate(FILMS):
        y=140+i*306
        board=Image.open(HERE/f['model']/'storyboard.png')
        # Four actual portrait panels in a compact strip, plus editorial purpose beside them.
        strip=board.crop((36,190,1617,830)); strip.thumbnail((750,290))
        overview.paste(strip,(35,y))
        d.text((805,y),f"{f['model']}  {f['title']}",font=font(27),fill='#233b41')
        yy=textblock(d,(805,y+52),f['purpose'],22,800)
        textblock(d,(805,yy+12),f"入片{len(f['reel_orders'])}套｜{f['duration']:g}秒｜"+('固定鏡頭短程走近' if f['model']=='M02' else f['recipe']),21,800,fill='#8e4c32')
    overview.save(HERE/'W45_overview.png')
    print(json.dumps(dict(week=WEEK,themes=5,inventory_looks=10,reel_looks=8,boards=5,common_space_previs=1,validation=results),ensure_ascii=False))

if __name__=='__main__': main()
