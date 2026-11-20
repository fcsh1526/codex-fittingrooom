"""Shared-world static key views for the motivated-performance test.

Coordinates are schematic, not a surveyed street or a gait simulation.
"""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT = 'C:/Windows/Fonts/msjh.ttc'
small = ImageFont.truetype(FONT, 18)
medium = ImageFont.truetype(FONT, 22)
large = ImageFont.truetype(FONT, 28)
CAM = {'position':[0, 1.35, 0], 'target':[0, 1.35, 6],
       'focal_length_look_mm':50, 'portrait_sensor':[20.25,36],
       'note':'Illustrative normal-lens projection, not calibrated photography.'}
states = [
 {'t':0.0, 'p':[-.5,.1,5.6], 'gaze':'forward', 'label':'出現｜完整造型', 'note':'站在遠側人行道，尚未察看'},
 {'t':2.2, 'p':[-.42,.1,4.88], 'gaze':'right', 'label':'察看｜再跨出路緣', 'note':'視線朝畫面右側車流來向'},
 {'t':5.5, 'p':[-.18,0,2.8], 'gaze':'forward', 'label':'過街｜接近鏡頭', 'note':'看回行進方向，笑容逐漸展開'},
 {'t':10.0, 'p':[0,.1,1.3], 'gaze':'camera', 'label':'會合｜眼神與微笑', 'note':'上半身近景，保持正常頭身比例'}]
scene = {'version':1, 'units':'schematic', 'unit_note':'Not measured metres; no exact model-control claim.',
 'camera':CAM, 'body_height':1.65, 'far_curb_z':4.8, 'near_curb_z':1.8,
 'far_pavement_y':.1, 'road_y':0, 'traffic_origin':'positive x / screen right',
 'camera_route':[{'t':s['t'],'position':CAM['position'],'target':CAM['target']} for s in states],
 'character_route':states, 'review_status':'draft static key-view design; dynamic gait not simulated'}

def project(p,w=360,h=640):
    x,y,z=p
    return ((.5+x*50/20.25/z)*w, (.5-(y-1.35)*50/36/z)*h)

def view(s):
    im=Image.new('RGB',(360,640),'#e9e6df'); d=ImageDraw.Draw(im)
    def polygon(vertices,fill,outline=None):
        d.polygon([project(p) for p in vertices],fill=fill,outline=outline)
    def line(a,b,fill,width=2):
        d.line([project(a),project(b)],fill=fill,width=width)
    polygon([(-5,0,7.3),(5,0,7.3),(5,4.5,7.3),(-5,4.5,7.3)],'#e8e3d8')
    for x0,x1 in [(-1.5,-.5),(.5,1.8)]:
        polygon([(x0,.1,7.25),(x1,.1,7.25),(x1,2.4,7.25),(x0,2.4,7.25)],'#8d9490','#787d78')
    polygon([(-5,.1,4.8),(5,.1,4.8),(5,.1,7.3),(-5,.1,7.3)],'#d7d4cc')
    polygon([(-5,0,1.8),(5,0,1.8),(5,0,4.8),(-5,0,4.8)],'#a6a7a4')
    polygon([(-5,.1,4.8),(5,.1,4.8),(5,0,4.8),(-5,0,4.8)],'#c2c0b8','#81827d')
    for z in [5.2,5.7,6.4]: line((-5,.1,z),(5,.1,z),'#bdbbb4')
    for x in [-2,-1,0,1,2]:line((x,.1,4.8),(x,.1,7.3),'#bdbbb4')
    x,y,z=s['p']
    def p(a,b,c=0):return project((x+a,y+b,z+c))
    sx,sy=p(0,0)
    d.ellipse([sx-20*5.6/z,sy-3*5.6/z,sx+23*5.6/z,sy+3*5.6/z],fill='#797c79')
    # Simplified clothed mannequin, with fixed human proportions.
    d.line([p(-.11,.77),p(-.12,.39),p(-.13,.03)],fill='#555960',width=max(3,int(17*5.6/z)))
    d.line([p(.11,.77),p(.12,.39),p(.15,.03)],fill='#555960',width=max(3,int(17*5.6/z)))
    d.line([p(-.13,.02),p(-.05,.02)],fill='#f3f2ed',width=max(3,int(7*5.6/z)))
    d.line([p(.12,.02),p(.23,.02)],fill='#f3f2ed',width=max(3,int(7*5.6/z)))
    d.polygon([p(-.23,1.37),p(.23,1.37),p(.19,.78),p(-.19,.78)],fill='#75608f')
    d.polygon([p(-.13,1.35),p(.13,1.35),p(.12,.85),p(-.12,.85)],fill='#f6f4ee')
    for sign in [-1,1]:
        d.line([p(sign*.23,1.32),p(sign*.29,1.04),p(sign*.27,.81)],fill='#75608f',width=max(3,int(8*5.6/z)))
    d.line([p(.2,1.35),p(.29,.8)],fill='#32383c',width=max(2,int(3*5.6/z)))
    d.polygon([p(.23,.85),p(.37,.85),p(.37,.63),p(.23,.63)],fill='#343b3e')
    a,b=p(-.105,1.65),p(.105,1.4)
    d.ellipse([a,b],fill='#dec6ae',outline='#726655',width=2)
    if s['gaze']=='right':
        a=p(0,1.53);b=(a[0]+38,a[1]);d.line([a,b],fill='#cf773e',width=3)
        d.polygon([b,(b[0]-8,b[1]-5),(b[0]-8,b[1]+5)],fill='#cf773e')
    top=project((x,y+1.65,z))[1]/640; foot=project((x,y,z))[1]/640
    return im,{'t':s['t'],'person_height_fraction':round(foot-top,3),
               'head_top_v':round(top,3),'shoe_v':round(foot,3),
               'person_center_u':round(project((x,y+.825,z))[0]/360,3),
               'camera_position':CAM['position'],'person_position':s['p']}

sheet=Image.new('RGB',(1504,810),'#faf8f3');d=ImageDraw.Draw(sheet)
d.text((20,10),'共用分鏡｜同一人物、路口、鏡頭與動作；B 只多原因句',font=large,fill='#333e40')
projected=[]
for i,s in enumerate(states):
    im,m=view(s);projected.append(m);x=20+i*372
    d.text((x,62),f"{s['t']:g} 秒 · {s['label']}",font=medium,fill='#333e40')
    sheet.paste(im,(x,100))
    d.text((x,747),s['note'],font=small,fill='#444e50')
    if i==0: im.save(HERE/'start_composition_guide.png')
d.text((20,780),'示意預演：人物尺度與地標由同一場景投影；不代表 Grok 已執行、步態已驗證或照片已核准。',font=small,fill='#636b6c')
sheet.save(HERE/'shared_storyboard.png')

im=Image.new('RGB',(900,820),'#faf8f3');d=ImageDraw.Draw(im)
def overhead(x,z):return (450+x*100,745-z*80)
d.text((25,15),'共同空間與視線方向（示意）',font=large,fill='#333e40')
d.rectangle([overhead(-3.8,7.8),overhead(3.8,4.8)],fill='#dfddd5')
d.rectangle([overhead(-3.8,4.8),overhead(3.8,1.8)],fill='#afb3b2')
d.rectangle([overhead(-3.8,1.8),overhead(3.8,.25)],fill='#dfddd5')
for z in [1.8,4.8]:d.line([overhead(-3.8,z),overhead(3.8,z)],fill='#777f7d',width=4)
d.line([overhead(*[s['p'][k] for k in [0,2]]) for s in states],fill='#7b598e',width=5)
for s in states:
    x,y=overhead(s['p'][0],s['p'][2]);d.ellipse([x-10,y-10,x+10,y+10],fill='#7b598e')
    d.text((x+17,y-13),f"{s['t']:g}s",font=medium,fill='#45344d')
a=overhead(3.3,3.45);b=overhead(1.6,3.45)
d.line([a,b],fill='#b46d3b',width=5);d.polygon([b,(b[0]+12,b[1]-7),(b[0]+12,b[1]+7)],fill='#b46d3b')
d.text((580,420),'車流從畫面右側來',font=small,fill='#664b36')
a=overhead(-.42,4.88);b=overhead(1.25,4.88)
d.line([a,b],fill='#d58a4a',width=4);d.text((535,305),'先察看',font=small,fill='#664b36')
x,y=overhead(0,0);d.rectangle([x-20,y-12,x+20,y+12],fill='#36494e')
d.line([overhead(0,0),overhead(-1.52,7.5)],fill='#889b9d',width=2)
d.line([overhead(0,0),overhead(1.52,7.5)],fill='#889b9d',width=2)
d.text((x+30,y-15),'相機固定｜在近側人行道',font=small,fill='#36494e')
d.text((25,780),'沒有實測公尺、腳步物理或精準生成控制；原片末段重構圖在本次對照中先固定。',font=small,fill='#636b6c')
im.save(HERE/'overhead_route.png')
scene['projected_samples']=projected
(HERE/'shared_scene.json').write_text(json.dumps(scene,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'projected_samples':projected,'artifacts':['shared_storyboard.png','overhead_route.png','start_composition_guide.png']},ensure_ascii=False))
