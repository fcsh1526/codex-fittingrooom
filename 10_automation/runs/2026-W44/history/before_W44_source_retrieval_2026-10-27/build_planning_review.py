from pathlib import Path
import json, csv, hashlib, math, html, copy
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
OUT=RUN/'planning'; OUT.mkdir(exist_ok=True)
def dump(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(ROOT).as_posix()
index=json.loads((ROOT/'04_prompts/material_pool/material_index.json').read_text(encoding='utf-8-sig'))
materials={e['source_row_id']:e['material_id'] for e in index['entries'] if e['source_week']=='2026-W41'}
sources=[
 {'id':'WX','url':'https://www.cwa.gov.tw/Data/fcst_pdf/W53.pdf','publisher':'中央氣象署','issued_at':'2026-10-27 11:00 +08:00','valid':'2026-10-27 12:00 至 2026-11-03 06:00','finding':'台北10/28白天22–24°C、陰短暫雨，10/29–31白天高溫26–27°C、11/1可達30°C；台中10/27–11/1白天高溫29–31°C，高雄29–31°C。','limit':'逐日縣市預報；不以長期展望的氣候正常值當本週溫度。發布前重查。'},
 {'id':'T1','url':'https://us.princesspolly.com/blogs/princess-polly-blog/fall-style-guide','publisher':'Princess Polly','issued_at':None,'finding':'品牌秋季指南列出層次、深色丹寧、棕／酒紅及短袖長度等方向。','limit':'本次可讀的2026秋季品牌內容；頁面日期未核實，商業選品訊號，不是W44市場排名。'},
 {'id':'T2','url':'https://www.whowhatwear.com/fashion/shopping/new-fall-wardrobe-basics-2026','publisher':'Who What Wear','issued_at':None,'finding':'2026秋季基本款文章列出格紋襯衫、領口變化及合身丹寧外套。','limit':'季節背景，不等於本週新增趨勢；未驗證商品、銷量或平台熱度。'}
]
dump(OUT/'research_receipt.json',{'checked_date':'2026-10-27','timezone':'Asia/Taipei','content_week':'2026-W44','week_dates':['2026-10-26','2026-11-01'],'original_publishing_structure':'missing_on_entry','perplexity':{'url':'https://mika-lin-weekly.pplx.app/data/index.json','web_result':'not accessible','local_http_result':'DNS host not resolved','missing_source_weeks':['2026-W42','2026-W43','2026-W44'],'new_source_csv_imported':False},'pool_refresh':{'as_of':'2026-10-27','window_weeks':3,'current_source_candidates':0,'older_W41_saved_rows':20,'source_claims_independently_verified':False},'sources':sources,'editorial_basis':'W41舊素材重新審視＋本次可查秋季訊號與台灣逐日天氣；不是已完整取得的W44 Perplexity週報。','generation_authorized':False})

series=[
 {'id':'01','model':'M02','title':'室外仍暖，薄外套怎麼搭','question':'早晚或冷氣房要外層，中午又要能敞開；短外套怎麼保留腰線？','answer':'同件奶油白短立領薄外套，分別搭直筒褲與A字裙；看閉合／敞開時的衣長與腰線。','recipe':'continuous_route','layout':'single_sequential','master':'B','region':'台北，陰天有遮簷的辦公街廓；不演雨中機能','source_rows':['W41-P001','W41-P002','W41-P003','W41-P004'],'looks':['奶油白無鋪棉短立領外套（開襟）、白圓領短袖T、可可棕高腰直筒褲、黑低跟樂福鞋、黑小方肩包','同款奶油白短立領外套（鬆扣）、海軍藍短袖圓領上衣、炭灰高腰及小腿A字裙、黑低跟包鞋、黑小方肩包'],'proofs':['開襟處白T與腰胯上方衣長','短外套下襬、裙腰與A字輪廓'],'beats':['全身開襟，沿曲線走近','淺側角度仍見完整頭鞋','相同世界時間換成裙裝','全身收束，讀短衣長／裙線'],'colors':['#e7decb','#4b433b'],'gaps':['連續路線先審共同場地、雙路徑與同步相機視角','兩套各自全身A與proof未生成；不能移轉M03舊片核准']},
 {'id':'02','model':'M01','title':'一件格紋，通勤或週末','question':'同件格紋襯衫，怎麼一眼看出上班與週末的差別？','answer':'同件格紋上衣，左側紮入深色直筒褲、右側敞開罩白T配丹寧；同時看腰線和層次。','recipe':'parallel_comparison','layout':'parallel_comparison','master':'D','region':'台中，有遮蔭的藝文空間','source_rows':['W41-P005','W41-P006','W41-P008'],'looks':['奶油白海軍藍薄格紋長袖襯衫（紮入、袖口預先翻折）、炭灰高腰直筒褲、黑低跟樂福鞋、黑小肩包','同件薄格紋襯衫（敞開）、白圓領短袖T、深藍直筒九分丹寧褲、白低筒鞋、海軍藍小斜背包'],'proofs':['襯衫下襬紮入與腰線','敞開門襟、白T與丹寧層次'],'beats':['左右全身同時出現','左輕轉15°，右自然換重心','持續同尺度讀兩種腰線','正面附近收束，不強制同步'],'colors':['#cbd3d9','#263e59'],'gaps':['手機並排實際人物寬度／格紋清晰度待真圖審查；必要時改為依序','8秒每側需要8秒可用原速來源，不能用6秒片循環補足']},
 {'id':'03','model':'M04','title':'短程出差，一條棕褲兩個場合','question':'少帶一條褲子，移動與見客怎麼分配上衣？','answer':'同件可可棕直筒褲：移動搭白T與短外層，見客換淺藍尖領襯衫；比較領口、衣長及坐姿。','recipe':'everyday_sequence','layout':'single_sequential','master':'B','region':'台中，車站休息區／同棟共享辦公室；獨立片段','source_rows':['W41-P009','W41-P010','W41-P011','W41-P012'],'looks':['米白無鋪棉短外套、白圓領短袖T、可可棕高腰直筒丹寧、黑低跟樂福鞋、深棕拉鍊肩包','淺藍薄棉尖領長袖襯衫（袖口預先翻折、紮入）、同件可可棕直筒丹寧、黑窄皮帶、黑低跟樂福鞋、同款深棕肩包'],'proofs':['坐姿下T恤與短外套層次、褲腰','襯衫尖領與紮入腰線'],'beats':['移動裝全身短步入座旁','已坐妥，讀短外套與褲腰','見客裝已坐妥，相近位置接入','起身後全身，讀襯衫／褲型'],'colors':['#e7decb','#72513d'],'gaps':['新搭配是編輯提案，不聲稱真實打包／材質舒適度測試','坐姿圖須另審；不強迫模型生成坐下到站起的複雜全過程']},
 {'id':'04','model':'M03','title':'下班赴約，正式程度換在哪裡','question':'都保留薄西外，褲裝與裙裝各適合怎樣的晚餐場合？','answer':'米白西外＋T恤直筒褲對照深藍西外＋船領上衣A字裙；看領口與下身輪廓。','recipe':'sequential_lookbook','layout':'single_sequential','master':'C','region':'台北，室內餐館入口的固定取景區','source_rows':['W41-P013','W41-P014','W41-P015','W41-P016'],'looks':['米白輕薄單排扣西外（敞開）、白圓領短袖T、深藍高腰直筒褲、黑低跟便鞋、深棕小肩包','深藍輕薄單排扣西外（敞開）、奶油白船領短袖上衣、炭灰及小腿A字裙、黑低跟包鞋、深棕小肩包'],'proofs':['圓領T與翻領關係','船領、裙腰與西外下襬'],'beats':['第一套領口含臉中景','同套全身，自然淺側轉','第二套相近全身接入','同套含臉腰上中景收束'],'colors':['#e5d9c8','#29374a'],'gaps':['屬已接受依序展示方法的主題變體，不宣稱新影像類型','中景／全身幾何須相容；proof不適合作端點時只作服裝參照']},
 {'id':'05','model':'M05','title':'天氣還暖，秋色放一處','question':'不加厚衣服，如何用一處顏色改變整套感覺？','answer':'第一套用酒紅上衣當大色塊，第二套以鈷藍包當小點綴；看色塊位置與面積。','recipe':'everyday_sequence','layout':'single_sequential','master':'E','region':'高雄，遮蔭書店外／室內書架旁','source_rows':['W41-P017','W41-P018','W41-P019'],'looks':['酒紅不透膚圓領短袖上衣、炭灰高腰直筒褲、黑低跟樂福鞋、黑小肩包、細銀圈耳環','白色尖領短袖襯衫、深藍高腰及小腿A字裙、黑低跟樂福鞋、鈷藍小肩包、同款細銀圈耳環'],'proofs':['酒紅領口與炭灰腰線色塊','完整鈷藍包與白襯衫／深裙上下文'],'beats':['書店外全身，酒紅主色可見','已站在書架旁，含臉讀領口','第二套近景，藍包全貌可見','同套全身，讀小面積點綴色'],'colors':['#752d42','#2455a0'],'gaps':['酒紅是本次外部季節訊號＋編輯新增，不標成W41原始單品','不以藍包移動串鏡當觀看目的；要看整套色塊面積']}
]
for s in series:
 s['source_material_ids']=[materials[x] for x in s['source_rows']]
 s['status']='proposed_awaiting_user_review'
 s['previs_required']=s['recipe']=='continuous_route'
 s['look_ids']=[f"2026-W44-{int(s['id']):03}-L01",f"2026-W44-{int(s['id']):03}-L02"]
dump(OUT/'series_proposals.json',series)

# One scene, one clock, two independently specified quadratic paths.
def bez(points,t): return [(1-t)**2*points[0][i]+2*(1-t)*t*points[1][i]+t*t*points[2][i] for i in range(3)]
PC=[[-.4,0,0],[.65,0,4],[-.1,0,8]]
CC=[[.8,1.1,3.5],[-.9,1.1,7.9],[.6,1.1,11.5]]
geometry=[{'id':'office_wall','vertices':[[-2,0,-1],[-2,3,-1],[-2,3,13],[-2,0,13]]},
 {'id':'window_A','vertices':[[-1.99,.5,2],[-1.99,2.5,2],[-1.99,2.5,4],[-1.99,.5,4]]},
 {'id':'window_B','vertices':[[-1.99,.5,7],[-1.99,2.5,7],[-1.99,2.5,9],[-1.99,.5,9]]},
 {'id':'bench','vertices':[[-1.5,.45,5],[-1.5,.45,6.5],[-.9,.45,6.5],[-.9,.45,5]]}]
for zz in [0,2,4,6,8,10,12]:
 geometry.append({'id':f'paving_{zz}','vertices':[[-2,0,zz],[2.5,0,zz]]})
def at(frame):
 t=frame/318; p=bez(PC,t); c=bez(CC,t); target=[p[0],1.1,p[2]]
 heading=math.degrees(math.atan2(2*((1-t)*(PC[1][0]-PC[0][0])+t*(PC[2][0]-PC[1][0])),8))
 return p,c,target,heading
def project(pt,c,target):
 dx,dz=target[0]-c[0],target[2]-c[2]; norm=math.hypot(dx,dz); fx,fz=dx/norm,dz/norm
 rx,rz=fz,-fx; v=[pt[i]-c[i] for i in range(3)]; dep=v[0]*fx+v[2]*fz
 if dep<=.04: return None
 sy=math.tan(math.radians(40)/2)
 return [.5+(v[0]*rx+v[2]*rz)/(2*dep*sy*9/16),.5-v[1]/(2*dep*sy)]
def clipped(vertices,c,target):
 dx,dz=target[0]-c[0],target[2]-c[2];norm=math.hypot(dx,dz)
 def depth(v):return ((v[0]-c[0])*dx+(v[2]-c[2])*dz)/norm
 result=[]
 for a,b in zip(vertices,vertices[1:]+vertices[:1]):
  da,db=depth(a),depth(b);ina,inb=da>=.06,db>=.06
  if ina:result.append(a)
  if ina!=inb:
   t=(.06-da)/(db-da);result.append([a[i]+t*(b[i]-a[i]) for i in range(3)])
 return result
routes=[]
for sid,bounds in [('S01',[0,168]),('S02',[150,318])]:
 times=[bounds[0],(sum(bounds)//2),bounds[1]]; route={'shot_id':sid,'character_samples':[],'camera_samples':[],'projected_samples':[]}
 for f in times:
  p,c,target,h=at(f); feet=project(p,c,target); head=project([p[0],1.65,p[2]],c,target)
  route['character_samples'].append({'frame':f,'position':p,'heading_degrees':h,'gait_phase':'schematic continuous phase; no physical foot-contact claim'})
  route['camera_samples'].append({'frame':f,'position':c,'target':target,'vertical_fov_degrees':40})
  visible=[g['id'] for g in geometry if any((q:=project(v,c,target)) and 0<=q[0]<=1 and 0<=q[1]<=1 for v in g['vertices'])]
  route['projected_samples'].append({'frame':f,'person_center_uv':[(feet[0]+head[0])/2,(feet[1]+head[1])/2],'person_height_fraction':feet[1]-head[1],'visible_landmark_ids':visible,'visible_clothing':'full outfit, schematic garment only'})
 routes.append(route)
space={'id':'W44_arcade_schematic_v1','units':'schematic','unit_note':'Unmeasured relative scale; stature 1.65 is a schematic unit, not a measured model height. No claim of real site geometry.','axes':'x_right_y_up_z_forward','geometry':geometry,'routes':routes,'curve_controls':{'character':PC,'camera':CC},'clock':{'fps':24,'frame_count':318},'projection':'pinhole vertical FOV 40deg; chest-level horizontal optical axis; 9:16'}
dump(OUT/'shared_space.json',space)

FONT='C:/Windows/Fonts/msjh.ttc'; BOLD='C:/Windows/Fonts/msjhbd.ttc'
def font(n,b=False): return ImageFont.truetype(BOLD if b else FONT,n)
def txt(d,xy,t,n=22,fill='#26313b',b=False): d.text(xy,t,font=font(n,b),fill=fill)
def wrap(t,limit): return [t[i:i+limit] for i in range(0,len(t),limit)]
def person(d,box,color,mode='full',skirt=False,plaid=False,layer=False,inner='#fff',lower='#68717b',bag='#fff'):
 x,y,w,h=box; scale=h/300; cx=x+w/2; top=y+24*scale
 d.ellipse([cx-15*scale,top,cx+15*scale,top+32*scale],outline='#26313b',width=2)
 sy=top+38*scale; waist=sy+75*scale
 d.polygon([(cx-37*scale,sy),(cx+37*scale,sy),(cx+28*scale,waist),(cx-28*scale,waist)],fill=color,outline='#26313b')
 d.line([(cx,sy),(cx,waist)],fill='#59636b',width=2)
 if layer:
  d.polygon([(cx-10*scale,sy),(cx+10*scale,sy),(cx+16*scale,waist),(cx-16*scale,waist)],fill=inner,outline='#59636b')
  d.line([(cx-33*scale,waist-8*scale),(cx+33*scale,waist-8*scale)],fill='#59636b',width=2)
 if plaid:
  for k in range(-2,3): d.line([(cx+k*12*scale,sy),(cx+k*10*scale,waist)],fill='#59636b',width=1)
  for k in range(1,5): d.line([(cx-30*scale,sy+k*14*scale),(cx+30*scale,sy+k*14*scale)],fill='#59636b',width=1)
 d.line([(cx-37*scale,sy),(cx-48*scale,waist+25*scale)],fill='#26313b',width=3)
 d.line([(cx+37*scale,sy),(cx+48*scale,waist+17*scale)],fill='#26313b',width=3)
 if mode=='proof':
  d.rectangle([cx-29*scale,waist,cx+29*scale,waist+50*scale],fill=lower,outline='#26313b')
  d.rectangle([cx+15*scale,waist-5*scale,cx+44*scale,waist+31*scale],fill=bag,outline='#26313b',width=2)
  return
 if mode=='seated':
  d.polygon([(cx-28*scale,waist),(cx+28*scale,waist),(cx+60*scale,waist+45*scale),(cx+45*scale,waist+60*scale),(cx-25*scale,waist+30*scale)],fill=lower,outline='#26313b')
  d.line([(cx+48*scale,waist+50*scale),(cx+47*scale,waist+120*scale)],fill=lower,width=14)
  d.line([(cx+24*scale,waist+47*scale),(cx+18*scale,waist+115*scale)],fill=lower,width=14)
  d.line([(cx-40*scale,waist+35*scale),(cx+20*scale,waist+35*scale)],fill='#59636b',width=4)
  d.line([(cx+37*scale,waist+123*scale),(cx+67*scale,waist+123*scale)],fill='#26313b',width=5)
  d.line([(cx+8*scale,waist+118*scale),(cx+37*scale,waist+118*scale)],fill='#26313b',width=5)
  return
 knee=waist+65*scale; bottom=y+h-20*scale
 if skirt: d.polygon([(cx-27*scale,waist),(cx+27*scale,waist),(cx+46*scale,knee+25*scale),(cx-46*scale,knee+25*scale)],fill=lower,outline='#26313b')
 else:
  d.polygon([(cx-27*scale,waist),(cx+27*scale,waist),(cx+30*scale,bottom-15*scale),(cx+5*scale,bottom-15*scale),(cx,waist+22*scale),(cx-6*scale,bottom-15*scale),(cx-30*scale,bottom-15*scale)],fill=lower,outline='#26313b')
 if skirt:
  d.line([(cx-18*scale,knee+25*scale),(cx-21*scale,bottom-5*scale)],fill='#26313b',width=3);d.line([(cx+18*scale,knee+25*scale),(cx+25*scale,bottom-5*scale)],fill='#26313b',width=3)
 for z in [-21,23]: d.line([(cx+(z-9)*scale,bottom),(cx+(z+10)*scale,bottom)],fill='#26313b',width=5)
 d.rectangle([cx+29*scale,waist-5*scale,cx+55*scale,waist+31*scale],fill=bag,outline='#26313b',width=2)

for s in series:
 im=Image.new('RGB',(1600,980),'#f5f3ed'); d=ImageDraw.Draw(im)
 txt(d,(55,32),f"MIRA / W44  ·  {s['id']}  {s['title']}",34,b=True)
 txt(d,(55,86),s['question'],24); txt(d,(55,127),'線稿提案 v1 · 示意服裝／動作；不代表身份、動態或轉場已通過',19)
 for k in range(4):
  x=55+k*385; d.rounded_rectangle((x,180,x+355,760),radius=12,fill='white',outline='#d3d4ce',width=2)
  if s['recipe']=='parallel_comparison':
   person(d,(x+6,235,168,390),s['colors'][0],plaid=True,bag='#30343a')
   person(d,(x+178,235,168,390),s['colors'][0],plaid=True,layer=True,lower='#263e59',bag='#263e59')
  else:
   look=0 if k<2 else 1; mode='proof' if (s['id']=='04' and k in [0,3]) or (s['id'] in ['03','05'] and k in [1,2]) else 'full'
   if s['id']=='03' and k in [1,2]:mode='seated'
   col='#e7decb' if s['id']=='01' else s['colors'][look]
   if s['id']=='03' and look==1:col='#bbd1e0'
   if s['id']=='05' and look==1:col='#fff'
   low='#72513d' if s['id']=='03' or (s['id']=='01' and look==0) else '#263e59' if s['id']=='05' and look==1 else '#68717b'
   bagcol='#2455a0' if s['id']=='05' and look==1 else '#483b34' if s['id'] in ['03','04'] else '#30343a'
   person(d,(x+35,218,285,405),col,mode,skirt=look==1 and s['id'] in ['01','04','05'],layer=s['id'] in ['01','04'] or (s['id']=='03' and look==0),inner='#fff' if look==0 or s['id']=='04' else '#263e59',lower=low,bag=bagcol)
  d.line([(x+32,635),(x+322,635)],fill='#bec7c9',width=2)
  txt(d,(x+18,650),f"{k+1:02d}  {s['beats'][k]}",18)
  txt(d,(x+18,696),'人物 → 持續前進' if s['previs_required'] else '人物 → 小幅自然動作',17)
  txt(d,(x+18,724),'相機 → 獨立曲線，見同步預演' if s['previs_required'] else '相機：固定／按分鏡取景',16)
 txt(d,(55,790),'L01  '+s['looks'][0],19)
 txt(d,(55,830),'L02  '+s['looks'][1],19)
 txt(d,(55,882),'接點：預設0.75秒柔接；原速、無烙字。讀衣時間、真實動態與舒服度仍待實片驗收。',20)
 txt(d,(55,922),'註：連續路線的真實取景位置以 shared_space.json 同步預演為準；其他線稿為獨立鏡位。',17)
 im.save(OUT/f"series_{s['id']}_storyboard.png")

def camera_svg(frame):
 p,c,target,h=at(frame); parts=['<svg viewBox="0 0 360 640" xmlns="http://www.w3.org/2000/svg"><rect width="360" height="640" fill="#faf9f4"/>']
 for g in geometry:
  qs=[project(v,c,target) for v in clipped(g['vertices'],c,target)]
  if qs and all(q is not None for q in qs):
   pts=' '.join(f'{q[0]*360:.2f},{q[1]*640:.2f}' for q in qs)
   parts.append(f'<polygon points="{pts}" fill="none" stroke="#9caab0" stroke-width="2"/>')
 # schematic articulated body, projected through same camera, not a photoreal person.
 right=[math.cos(math.radians(h)),0,-math.sin(math.radians(h))]
 def wp(x,y,z=0): return [p[0]+right[0]*x,p[1]+y,p[2]+right[2]*x+z]
 def line(a,b,col='#293d4a',width=3):
  q,r=project(wp(*a),c,target),project(wp(*b),c,target)
  if q and r: parts.append(f'<line x1="{q[0]*360:.2f}" y1="{q[1]*640:.2f}" x2="{r[0]*360:.2f}" y2="{r[1]*640:.2f}" stroke="{col}" stroke-width="{width}"/>')
 phase=frame/24*2*math.pi*1.65; swing=.11*math.sin(phase)
 for a,b in [((0,1.47),(0,.88)),((-.22,1.38),(.22,1.38)),((-.22,1.38),(-.29,.92,swing)),((.22,1.38),(.29,.92,-swing)),((0,.88),(-.14,.05,swing)),((0,.88),(.14,.05,-swing))]: line(a,b)
 q=project(wp(0,1.57),c,target); r=project(wp(.09,1.57),c,target)
 parts.append(f'<circle cx="{q[0]*360:.2f}" cy="{q[1]*640:.2f}" r="{abs(r[0]-q[0])*360:.2f}" fill="none" stroke="#293d4a" stroke-width="3"/>')
 parts.append('</svg>'); return ''.join(parts)
def overhead_svg(frame):
 p,c,target,h=at(frame)
 def xy(pt):return (260+pt[0]*75,610-pt[2]*42)
 def path(pts):return ' '.join(f'{xy(v)[0]:.1f},{xy(v)[1]:.1f}' for v in pts)
 P=[bez(PC,i/100) for i in range(101)]; C=[bez(CC,i/100) for i in range(101)]
 a,b=xy(p),xy(c); polys=''
 for g in geometry:
  polys+=f'<polygon points="{path(g["vertices"])}" fill="none" stroke="#c5c9c6" stroke-width="3"/>'
 return f'<svg viewBox="0 0 520 640" xmlns="http://www.w3.org/2000/svg"><rect width="520" height="640" fill="#faf9f4"/>{polys}<polyline points="{path(P)}" fill="none" stroke="#b96843" stroke-width="3"/><polyline points="{path(C)}" fill="none" stroke="#28758a" stroke-width="3"/><line x1="{b[0]}" y1="{b[1]}" x2="{a[0]}" y2="{a[1]}" stroke="#28758a" stroke-dasharray="5 4"/><circle cx="{a[0]}" cy="{a[1]}" r="8" fill="#b96843"/><rect x="{b[0]-7}" y="{b[1]-7}" width="14" height="14" fill="#28758a"/></svg>'
previews=[]
for f in list(range(0,318,3))+[318]:
 previews.append({'frame':f,'seconds':f/24,'overhead':overhead_svg(f),'camera':camera_svg(f)})
dump(OUT/'previs_frames.json',previews)
for f in [0,84,150,159,168,234,318]:
 (OUT/f'route_camera_f{f:03}.svg').write_text(camera_svg(f),encoding='utf-8')
 (OUT/f'route_overhead_f{f:03}.svg').write_text(overhead_svg(f),encoding='utf-8')

# Human-readable paired views from the exact same projection as the HTML.
im=Image.new('RGB',(1600,1000),'#f5f3ed');d=ImageDraw.Draw(im)
txt(d,(45,25),'01 · 人物／相機雙路徑與同步9:16視角',32,b=True)
txt(d,(45,78),'同一場地／座標／時間；示意骨架與服裝，不是已生成影片或實體步態驗證。',21)
def top(pt): return (220+pt[0]*57,820-pt[2]*45)
for g in geometry:
 pts=[top(v) for v in g['vertices']]; d.line(pts+[pts[0]],fill='#a9b4b5',width=2)
for control,color in [(PC,'#b96843'),(CC,'#28758a')]:
 d.line([top(bez(control,i/100)) for i in range(101)],fill=color,width=4)
for k,f in enumerate([0,159,318]):
 p,c,target,h=at(f); a,b=top(p),top(c);d.line([a,b],fill='#8c9697',width=1)
 d.ellipse([a[0]-7,a[1]-7,a[0]+7,a[1]+7],fill='#b96843');d.rectangle([b[0]-6,b[1]-6,b[0]+6,b[1]+6],fill='#28758a')
 txt(d,(b[0]+10,b[1]-13),str(round(f/24,2)),16)
 x=470+k*355;y=160;w=315;hh=560
 d.rectangle([x,y,x+w,y+hh],fill='#fff',outline='#a9b4b5',width=2)
 def pix(v):
  q=project(v,c,target);return (x+q[0]*w,y+q[1]*hh) if q else None
 # Clip each complete projected camera image to its real 9:16 viewport.
 tile=Image.new('RGB',(w,hh),'#fff');td=ImageDraw.Draw(tile)
 def local(v):
  q=project(v,c,target); return (q[0]*w,q[1]*hh) if q else None
 for g in geometry:
  qs=[local(v) for v in clipped(g['vertices'],c,target)]
  if qs and all(q is not None for q in qs):td.line(qs+[qs[0]],fill='#a9b4b5',width=2)
 def wp(xx,yy):return [p[0]+math.cos(math.radians(h))*xx,yy,p[2]-math.sin(math.radians(h))*xx]
 for a1,b1 in [((0,1.47),(0,.88)),((-.22,1.38),(.22,1.38)),((-.22,1.38),(-.29,.92)),((.22,1.38),(.29,.92)),((0,.88),(-.14,.05)),((0,.88),(.14,.05))]:td.line([local(wp(*a1)),local(wp(*b1))],fill='#293d4a',width=3)
 q=local(wp(0,1.57));r=abs(local(wp(.09,1.57))[0]-q[0]);td.ellipse([q[0]-r,q[1]-r,q[0]+r,q[1]+r],outline='#293d4a',width=3)
 im.paste(tile,(x,y));txt(d,(x,y+hh+18),f'{f/24:.3f}秒／f{f}',22,b=True)
 head=project([p[0],1.65,p[2]],c,target);foot=project(p,c,target)
 txt(d,(x,y+hh+57),f'人物高度 {(foot[1]-head[1])*100:.1f}%',20)
txt(d,(45,875),'棕色：人物位置與前進路徑　藍色：相機獨立路徑　灰線：同一時間的觀看方向',22)
txt(d,(45,918),'相機視角的窗牆／長椅由共同幾何投影；衣服重影與引擎遵循程度尚未驗證。',21)
im.save(OUT/'route_previs_contact.png')

refs=list(csv.DictReader((ROOT/'02_brand/mira_reference_images.csv').open(encoding='utf-8-sig')))
identity_check=[]
lookrows=[]
for s in series:
 folder=OUT/f"series_{s['id']}";folder.mkdir(exist_ok=True)
 plan=json.loads((ROOT/'11_skills/mira-reel-director/assets/production_plan.template.json').read_text(encoding='utf-8-sig'))
 plan.update({'plan_id':f"2026-W44-{s['id']}-v1",'path_base':'project','weeks':{'source':['2026-W41'],'content':'2026-W44','delivery':None},'editorial':{'audience':'台灣成年女性日常穿搭','takeaway':s['answer'],'visual_theme':s['title'],'selection_rationale':s['question']},'presentation':{'layout_id':s['layout'],'recipe_id':s['recipe']}})
 row=next(r for r in refs if r['model_profile_id']==s['model']); ids=[]
 for kind in ['face','full']:
  path=ROOT/row[f'reference_{kind}_path']; aid=f"{s['model']}_{kind}";ids.append(aid)
  identity_check.append({'model':s['model'],'role':kind,'path':rel(path),'exists':path.exists(),'reference_status':row['status']})
  plan['assets'].append({'id':aid,'kind':'identity','path':rel(path),'sha256':sha(path) if path.exists() else None})
 plan['models']=[{'id':s['model'],'identity_asset_ids':ids}]
 for k,lid in enumerate(s['look_ids']):
  plan['looks'].append({'id':lid,'model_id':s['model'],'wardrobe_summary':s['looks'][k],'source_asset_ids':['source_W41','research_receipt']})
  lookrows.append({'look_id':lid,'series_id':s['id'],'model_profile_id':s['model'],'wardrobe':s['looks'][k],'proof':s['proofs'][k],'source_material_ids':';'.join(s['source_material_ids']),'editorial_status':'proposed','reel_source':'native 9:16 full person A + vertical proof','carousel':'separate A full + B scene + C accessory','canva_master':s['master']})
 board=OUT/f"series_{s['id']}_storyboard.png";plan['assets'].append({'id':'board','kind':'storyboard','path':rel(board),'sha256':sha(board)})
 for aid,path in [('source_W41',ROOT/'10_automation/runs/2026-W41/source_perplexity.csv'),('research_receipt',OUT/'research_receipt.json')]:
  plan['assets'].append({'id':aid,'kind':'source','path':rel(path),'sha256':sha(path)})
 if s['recipe']=='continuous_route':
  plan['film'].update({'frame_count':318,'duration_seconds':13.25});bounds=[[0,168],[150,318]]; clear=[[[0,150]],[[168,318]]]
  plan['space']=space;plan['shared_space_asset_id']='common_space'
  plan['assets'].append({'id':'common_space','kind':'space_plan','path':rel(OUT/'shared_space.json'),'sha256':sha(OUT/'shared_space.json')})
  # HTML displays the complete synchronized sequence, plus source geometry.
 elif s['recipe']=='parallel_comparison':
  plan['film'].update({'frame_count':192,'duration_seconds':8});bounds=[[0,192]];clear=[[[0,192]]]
 else:
  plan['film'].update({'frame_count':330,'duration_seconds':13.75});bounds=[[0,96],[78,174],[156,252],[234,330]]; clear=[[[0,78]],[[96,156]],[[174,234]],[[252,330]]]
 for k,(b,cl) in enumerate(zip(bounds,clear)):
  lids=s['look_ids'] if s['recipe']=='parallel_comparison' else [s['look_ids'][0 if k<len(bounds)/2 else 1]]
  shot={'id':f'S{k+1:02}','look_ids':lids,'frames':b,'clothing_purpose':s['answer'] if len(bounds)<3 else s['beats'][k],'clear_read_intervals':cl,'storyboard_asset_id':'board','previs_asset_id':'route_previs' if s['previs_required'] else None,'input_asset_ids':[],'scene_reference_asset_ids':[],'space_mode':'shared_world' if s['previs_required'] else 'independent','action_start':s['beats'][min(k*2,3)] if len(bounds)==2 else s['beats'][k],'action_end':'動作自然延續；各套保持身份及衣服','camera':'依同步曲線' if s['previs_required'] else '固定鏡位，或同套一次原生推拉；起始構圖見線稿','missing_input_note':'企劃未核准，尚未生成新圖'}
  if s['previs_required']:shot['overhead_asset_id']='route_overhead'
  if s['recipe']=='parallel_comparison':shot['panels']=[{'id':'left','look_id':lids[0]},{'id':'right','look_id':lids[1]}]
  plan['shots'].append(shot)
  if k:
   plan['transitions'].append({'from_shot':f'S{k:02}','to_shot':f'S{k+1:02}','frames':[b[0],bounds[k-1][1]],'overlap_frames':18,'method':'cross_dissolve'})
 plan['missing_assets']=['本週企劃及精確線稿待使用者確認','新全身圖與proof尚未生成／逐張核准','既有身份核准沿用manifest；尚未把歷史收據轉為本檢查器格式，不重問身份核准']+s['gaps']
 dump(folder/'production_plan.json',plan)
dump(OUT/'identity_reference_check.json',identity_check)
with (OUT/'proposed_look_plan.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=lookrows[0]);w.writeheader();w.writerows(lookrows)

styles='''body{margin:0;background:#f3f0e8;color:#24323b;font:17px "Microsoft JhengHei",sans-serif}main{max-width:1160px;margin:auto;padding:40px 30px}h1{font-size:42px}h2{font-size:28px}p{line-height:1.8}section{background:#fff;padding:26px;margin:24px 0;border-radius:16px}img{width:100%;height:auto}table{width:100%;border-collapse:collapse}td,th{padding:13px;border-bottom:1px solid #ddd;text-align:left}a{color:#176e80}.tag{background:#e9dfca;padding:8px 12px;border-radius:8px}button{padding:10px 22px;font-size:17px}input{width:70%}.views{display:flex;gap:20px;align-items:start}.views div{flex:1}.views svg{height:480px;max-width:100%;border:1px solid #ddd}small{color:#68747a}'''
body='''<h1>MIRA · 本週製作提案</h1><p>2026-W44｜10/26–11/1｜規劃日 10/27（台灣）<br><span class="tag">待確認企劃與分鏡 · 尚未生成起始圖</span></p><section><h2>本週選材依據</h2><p>Perplexity 公開索引目前無法連線；近三週 W42、W43、W44 缺原始 CSV，素材池已重建並如實保留缺口。以下為 W41 舊材料重新編輯，加上這次查到的秋季內容與台灣天氣，不冒稱完整新週報。</p><p>北部先考慮可穿脫薄外層；中南部保留短袖、薄襯衫，以色塊與比例表達秋意。無鋪棉／薄是設計規格，AI 圖不能證明透氣、防水、舒適或防滑。</p>'''
for src in sources:body+=f'<p><a href="{src["url"]}">{src["publisher"]}</a>：{src["finding"]}<br><small>{src["limit"]}</small></p>'
body+='</section><section><h2>五個系列 · 十套</h2><table><tr><th>系列／內部人物</th><th>觀看收穫</th><th>形式／提議片長</th></tr>'
for s in series:
 dur='13.25秒' if s['previs_required'] else '8秒' if s['recipe']=='parallel_comparison' else '13.75秒'
 body+=f'<tr><td><a href="#s{s["id"]}">{s["title"]}</a><br><small>{s["model"]}</small></td><td>{s["answer"]}</td><td>{s["recipe"]}<br>{dur}</td></tr>'
body+='</table><p>保留正式每週五支 Reel、每位兩套；每套另備原生9:16全身＋proof，以及獨立Carousel A全身／B情境／C配件。完整最低清單為20張Reel full/proof＋30張Carousel；proof只有經審查符合直式與清晰度才可共用。這是交付需求，不是此刻自動批量生成數。</p></section>'
body+='''<section><h2>01 連續路線 · 同步空間預演</h2><p>同一辦公街廓：左側窗牆與長椅固定。棕線為人物，藍線為相機；兩者各有曲線控制點，相機水平光軸朝向人物胸高。右側9:16視角由左側同一份座標投影。示意單位未測量，骨架不是M02身份或真實步態。</p><button id="play">播放／暫停</button> <input id="time" type="range" min="0" max="106" value="0"><p id="stamp"></p><div class="views"><div id="over"></div><div id="cam"></div></div><p>6.25–7.00秒：兩套在同一世界時間交疊；這裡只驗空間，不模擬衣服混影。0.75秒柔接舒服度須待實際素材。全身讀衣目標各6.25秒；proof可另外審，不必為用完素材硬剪。相機角度、尺度與地標視差請配合滑桿查看。</p><small>限制：簡化針孔投影、未建遮擋消除／完整衣料／接觸物理；此預演不能證明Grok會照曲線執行。端點318是幾何邊界，實片預計輸出[0,318)幀。</small></section>'''
for s in series:
 body+=f'<section id="s{s["id"]}"><h2>{s["id"]} {s["title"]}</h2><p>{s["answer"]}</p><img src="series_{s["id"]}_storyboard.png" alt="四節點線稿"><p><b>地區／情境：</b>{s["region"]}<br><b>Reel proof：</b>{"；".join(s["proofs"])}<br><b>Carousel：</b>每套A全身；B在該場合另一個角落展示使用；C拍該套包、鞋或腰帶並留衣服上下文。預選模板{s["master"]}，依註冊尺寸另作構圖。</p><p><b>待驗：</b>{"；".join(s["gaps"])}</p><small>來源材料：{", ".join(s["source_rows"])}，完整搭配為本週編輯提案。歷史核准不移轉到本案。</small></section>'
body+='''<section><h2>生成前的確認範圍</h2><p>先確認五個選題／兩套搭配，以及01的雙路徑和相機視角。建議先做01第一套原生9:16全身候選一張，逐張視覺核准後才衍生proof或生成動態；每個look與surface都有自己的服裝鎖。若優先求較低製作風險，可先選02或04。</p><p>W43五套M03片保留原核准版本；快步、雙曲線及閃爍改善仍屬原案待優化，這份新週預演不算原案修復。發布時程尚未定，不倒填已過的週一，也不把五支都擠進週末。無新影像、外部上傳、排程或發文。</p></section>'''
script='''let frames=DATA;let slider=document.querySelector('#time');let playing=false,last=0;function render(){let f=frames[+slider.value];document.querySelector('#over').innerHTML=f.overhead;document.querySelector('#cam').innerHTML=f.camera;document.querySelector('#stamp').textContent=f.seconds.toFixed(3)+' 秒 / 幀 '+f.frame+' · '+(f.frame<150?'L01':f.frame<168?'L01 → L02交疊':'L02');}slider.oninput=()=>{playing=false;render()};document.querySelector('#play').onclick=()=>{playing=!playing;last=performance.now()};function tick(now){if(playing&&now-last>=125){slider.value=(+slider.value+1)%frames.length;render();last=now}requestAnimationFrame(tick)}render();requestAnimationFrame(tick);'''.replace('DATA',json.dumps(previews,ensure_ascii=False))
(OUT/'review.html').write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>Mira W44 待審企劃</title><style>'+styles+'</style><main>'+body+'</main><script>'+script+'</script></html>',encoding='utf-8')
# Bind exact shared source to both view artifacts after the HTML is final.
p=OUT/'series_01/production_plan.json';plan=json.loads(p.read_text(encoding='utf-8'))
for aid,kind in [('route_previs','previs'),('route_overhead','overhead')]:
 plan['assets'].append({'id':aid,'kind':kind,'path':rel(OUT/'review.html'),'sha256':sha(OUT/'review.html'),'derived_from':{'asset_id':'common_space','sha256':sha(OUT/'shared_space.json')}})
dump(p,plan)
summary=['# W44 製作規劃（待使用者確認）','','規劃日：2026-10-27（台灣）；內容週：2026-W44，10/26–11/1。','', '原先缺少本週publishing_structure，本次依使用者「開始新一週」指示建立待審規劃，未啟動新圖。','', '## 研究狀態','','Perplexity索引Web不可讀、本機DNS無法解析；W42–W44原始CSV缺少，近三週候選0。W41保存20筆作較早重審材料，不冒充本週趨勢。補充查得秋季品牌／媒體訊號，完整來源與限制見 planning/research_receipt.json。','', '氣象署10/27 11:00縣市預報有效至11/3：台北10/28有雨22–24°C；10/29–31回暖，11/1可達30°C。台中／高雄白天高溫多29–31°C。選薄外層、短袖與秋色色塊；不因秋季名稱加厚裝。發布前重查。','', '## 本週系列','','|系列|人物|形式|狀態|','|---|---|---|---|']
for s in series: summary.append(f"|{s['id']} {s['title']}|{s['model']}|{s['recipe']}|提案待審|")
summary+=['','五主題、五位各一次、兩套各位、十套、五支Reel；每套native9:16 full/proof＋獨立Carousel A/B/C。全套服裝與material_id見planning/proposed_look_plan.csv，人物雙參照路徑已查存在。','','## 分鏡與預演','','[打開可播放的企劃與同步預演](planning/review.html)。01使用同一shared_space.json產生俯視與相機視角，路線／時間／投影一致；簡化骨架與未測量示意場地，不能當生成動態驗收。其他系列沒有連續共用世界需求，以四節點線稿審構圖；獨立場景不冒稱連續推軌。','','01兩鏡：[0,168)、[150,318)，24fps／13.25秒，18f重疊，每套6.25秒清楚全身。02同時左右兩側：[0,192)，8秒，兩側需各8秒來源，不能6秒拉長。03–05四鏡：[0,96)、[78,174)、[156,252)、[234,330)，13.75秒；各0.75秒柔接。清楚讀衣區間合計11.5秒，每套5.75秒（含full/proof）。所有時間為設計預算，來源不足就明示缺口。','','## 生成閘門','','狀態 proposed_awaiting_user_review；尚無新圖核准。先確認選題／兩套／線稿及01同步預演，再開始首張Reel全身候選。後續照片逐張核准才入動態；舊身份核准沿用，不重問。所有計畫ready_for_generation應為false。','','未指定發布日期／網址／成效皆留空；不倒填週一、不啟動發文／排程。W43既有影片與M03五套例外保留，這份新週計畫不代表舊案快步／閃爍已修復。']
(RUN/'publishing_structure.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
dump(OUT/'planning_receipt.json',{'date':'2026-10-27','status':'proposed_awaiting_user_review','series':5,'models':sorted(s['model'] for s in series),'looks':len(lookrows),'identity_pairs_exist':all(x['exists'] for x in identity_check),'ai_stills_generated':0,'motion_generated':0,'approval_receipts_created':0,'shared_scene_sha256':sha(OUT/'shared_space.json'),'review_html_sha256':sha(OUT/'review.html'),'limitation':'線稿／同步示意投影僅供設計審查；未通過使用者視覺或實際引擎驗收。'})
print(json.dumps({'series':len(series),'looks':len(lookrows),'references_exist':all(x['exists'] for x in identity_check),'review':str(OUT/'review.html')},ensure_ascii=True))
