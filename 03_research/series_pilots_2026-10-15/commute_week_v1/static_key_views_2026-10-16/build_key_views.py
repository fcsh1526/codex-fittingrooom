"""Four static spatial key views from a shared site, with matching camera maps.

Planning diagram only; no animations, source-image edits or generation calls.
"""
from __future__ import annotations
import importlib.util
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
src=HERE.parent/'continuous_route_storyboard_2026-10-16/render_route.py'
spec=importlib.util.spec_from_file_location('shared_site',src)
site=importlib.util.module_from_spec(spec);spec.loader.exec_module(site)
art=site.art
VIEWS=[
    {'id':'K1','title':'街角走出，往騎樓前進','short_title':'街角走出','t':3.2,'angle_deg':40,'aim_to_door':0,
     'camera_note':'鏡頭在人物前側方，朝她拍攝；沿騎樓方向開始跟行。',
     'person_note':'身體朝行走方向；從對面街角走出，接向右邊的騎樓。',
     'landmarks':'畫內保留A柱列；B公司與D入口位於畫外右前方。',
     'continuity':'下一格延續同一排柱列；人物沒有跳到另一條街。'},
    {'id':'K2','title':'走過騎樓，接到旁邊小廣場','short_title':'騎樓接小廣場','t':8.6,'angle_deg':80,'aim_to_door':0,
     'camera_note':'鏡頭漸移到側面，與人物平行前行；視角轉變由前段接來。',
     'person_note':'繼續沿同一側人行空間走；尚未轉向公司過街。',
     'landmarks':'A柱列已退到畫外左後方；畫內保留B公司外牆。',
     'continuity':'下一格才向公司轉彎；C斑馬線保持在同一路口。'},
    {'id':'K3','title':'到同一路口，轉向公司過街','short_title':'同一路口過街','t':13.4,'angle_deg':145,'aim_to_door':.16,'focal_ratio':.85,
     'camera_note':'鏡頭在斜後方；過街這格放寬環境構圖，同時看人物與公司入口。',
     'person_note':'沿C斑馬線走向公司，不在路口突然換一條行進方向。',
     'landmarks':'畫內C斑馬線通向D公司入口；B玻璃外牆仍相同。',
     'continuity':'下一格延續同一斑馬線到入口；不更換公司門面。'},
    {'id':'K4','title':'過街後，跟到同一公司入口','short_title':'同一公司入口','t':18.4,'angle_deg':155,'aim_to_door':.15,
     'camera_note':'鏡頭在斜後方跟到門口；可用背影收束，不突然轉回正面。',
     'person_note':'穿過公司側人行道，沿D入口進門；這格先停在門檻前。',
     'landmarks':'D雙門框接續上一格同一入口；雨棚近緣已在畫外上方。',
     'continuity':'精確進門動作與尾幀，待這四格空間讀得懂後再設計。'}
]


class KeyWorld(site.World):
    def __init__(self,v):
        super().__init__(v['t'])
        self.v=v
        self.p=site.position(v['t'])
        forward=site.position(v['t']+.03)-site.position(v['t']-.03);forward/=np.linalg.norm(forward)
        side=np.array([forward[1],-forward[0]])
        a=math.radians(v['angle_deg'])
        self.c=self.p+4.25*(forward*math.cos(a)+side*math.sin(a))
        self.aim=self.p+(np.array([12.5,8.8])-self.p)*v['aim_to_door']
        self.fwd=(self.aim-self.c);self.fwd/=np.linalg.norm(self.fwd)
        # Screen right follows the camera's real view direction in the plan.
        self.right=np.array([self.fwd[1],-self.fwd[0]])
        self.focal=self.h*v.get('focal_ratio',1.20)
        self.eye_height=1.30
        self.horizon=.42

    def project(self,p):
        x,y,z=p;vec=np.array([x,z])-self.c
        dep=float(np.dot(vec,self.fwd))
        if dep<=.15:return None
        return(self.w*.5+float(np.dot(vec,self.right))*self.focal/dep,
               self.h*self.horizon-(y-self.eye_height)*self.focal/dep,dep)

    def marker(self,label,point,dx=0,dy=0):
        p=self.project(point)
        if p is None:return
        x,y,_=p
        if not(12<x<self.w-12 and 14<y<self.h-14):return
        tx=max(20,min(self.w-25,x+dx));ty=max(24,min(self.h-26,y+dy))
        self.d.line((x,y,tx,ty),fill=art.ACCENT,width=2)
        self.d.ellipse((tx-15,ty-15,tx+15,ty+15),fill=art.PAPER,outline=art.ACCENT,width=2)
        self.d.text((tx-8,ty-13),label,font=art.font(20,True),fill=art.ACCENT)

    def draw_directional_person(self):
        # A small 3D garment/body marker. All points use the route's actual heading.
        t=self.v['t'];p=self.p
        forward=site.position(t+.03)-site.position(t-.03);forward/=np.linalg.norm(forward)
        side=np.array([forward[1],-forward[0]])
        origin=np.array([p[0],0,p[1]])
        def W(lateral,y,along=0):
            xz=p+side*lateral+forward*along
            return(float(xz[0]),y,float(xz[1]))
        def poly(points,fill,outline=art.INK):
            coords=[self.project(q) for q in points]
            if any(q is None for q in coords):return
            xy=[q[:2] for q in coords]
            self.d.polygon(xy,fill=fill);self.d.line(xy+[xy[0]],fill=outline,width=2,joint='curve')
        def line(points,color=art.INK,width=2):
            pp=[self.project(q) for q in points]
            if all(q is not None for q in pp):self.d.line([q[:2] for q in pp],fill=color,width=width,joint='curve')
        def prism(cx,cz,y0,y1,rx,rz,fill):
            rings=[]
            for y in [y0,y1]:rings.append([W(cx-rx,y,cz-rz),W(cx+rx,y,cz-rz),W(cx+rx,y,cz+rz),W(cx-rx,y,cz+rz)])
            faces=[rings[0],rings[1]]+[[rings[0][i],rings[0][(i+1)%4],rings[1][(i+1)%4],rings[1][i]] for i in range(4)]
            faces.sort(key=lambda f:np.mean([self.project(q)[2] for q in f]),reverse=True)
            for face in faces:poly(face,fill)
        # Navy trousers with a modest step, same pose definition in world coordinates.
        for side_sign,along in [(-1,-.105),(1,.105)]:
            lateral=side_sign*.095
            prism(lateral,along,.08,.83,.07,.065,'#3e4b58')
            prism(lateral,along+.045,.02,.085,.075,.115,'#3e4240')
        # Ivory blazer has a front, back and side, rather than a front-facing billboard.
        # Torso is 0.36m shoulder width, tapering normally; ordinary schematic proportions.
        left_back=[W(-.18,1.39,-.075),W(-.145,.82,-.08)]
        right_back=[W(.18,1.39,-.075),W(.145,.82,-.08)]
        torso=[left_back[0],right_back[0],right_back[1],left_back[1]]
        front=[W(-.18,1.39,.075),W(.18,1.39,.075),W(.145,.82,.08),W(-.145,.82,.08)]
        faces=[torso,front,[torso[0],front[0],front[3],torso[3]],[torso[1],front[1],front[2],torso[2]]]
        faces.sort(key=lambda f:np.mean([self.project(q)[2] for q in f]),reverse=True)
        for face in faces:poly(face,'#e9e3d4')
        view_vec=(self.c-self.p);view_vec/=np.linalg.norm(view_vec)
        if np.dot(forward,view_vec)>.10:
            poly([W(-.055,1.39,.082),W(.055,1.39,.082),W(.045,.92,.088),W(-.045,.92,.088)],'#f8f6ee')
            line([W(-.08,1.38,.09),W(-.10,1.27,.09),W(-.055,1.23,.09),W(-.04,1.1,.09)])
            line([W(.08,1.38,.09),W(.10,1.27,.09),W(.055,1.23,.09),W(.04,1.1,.09)])
        # Arms stay at sides; no elaborate simulated hand movement is needed.
        for ss,along in [(-1,.025),(1,-.025)]:
            prism(ss*.205,along,.91,1.34,.04,.045,'#e9e3d4')
            line([W(ss*.205,.91,along),W(ss*.20,.84,along)],'#a99d8c',7)
        prism(.25,-.015,.78,.97,.055,.095,'#6f5744')
        line([W(.20,1.37,0),W(.25,.97,0)],'#6f5744',3)
        prism(0,0,1.37,1.48,.034,.033,'#ddd3c4')
        # Project head and forward-facing nose as separate world points.
        hp=self.project(W(0,1.55,0));top=self.project(W(0,1.68,0));low=self.project(W(0,1.45,0))
        hh=low[1]-top[1];rx=hh*.35;cx,cy=hp[:2]
        self.d.ellipse((cx-rx,top[1],cx+rx,low[1]),fill='#ddd3c4',outline=art.INK,width=2)
        facing=float(np.dot(forward,view_vec))
        if facing<-.25:
            self.d.ellipse((cx-rx,top[1],cx+rx,low[1]-.02*hh),fill='#555950',outline=art.INK,width=2)
        else:
            self.d.arc((cx-rx*1.04,top[1]-1,cx+rx*1.04,low[1]-.4*hh),180,360,fill=art.INK,width=5)
            nose=self.project(W(0,1.54,.16));line([W(0,1.57,.10),W(0,1.54,.16),W(0,1.52,.10)],width=2)
        # Path arrow sits on the ground, using exactly the same projection.
        start=self.project(W(-.34,.012,-.20));end=self.project(W(-.34,.012,.50))
        if start and end:art.arrow(self.d,start[:2],end[:2],width=3)


def make_view(v):
    w=KeyWorld(v);w.draw_geometry();w.draw_directional_person()
    # Fixed-landmark labels are planning annotations, never future film text.
    anchor_groups=[('A',[(-3.5,1.6,1.4),(1.0,1.6,1.4),(3.7,1.6,1.4)]),
                   ('B',[(-5.5,3.4,8.8),(-4,3.4,8.8),(0,3.4,8.8),(6,3.4,8.8),(9.5,3.4,8.8),(15.5,3.4,8.8)]),
                   ('C',[(12.5,.03,3.8)]),('D',[(12.5,2.3,8.8)])]
    for label,points in anchor_groups:
        for point in points:
            p=w.project(point)
            if p and 18<p[0]<w.w-18 and 20<p[1]<w.h-20:
                w.marker(label,point,-22,-25);break
    w.im.save(HERE/(v['id']+'_view.png'))
    return w.im


def mini_map(v,size=(680,470)):
    w,h=size;im=Image.new('RGB',size,art.PAPER);d=ImageDraw.Draw(im)
    def q(x,z):return(35+(x+7)*22,385-(z+4)*24)
    def rect(x0,z0,x1,z1,fill):
        a,b=q(x0,z0),q(x1,z1)
        d.rectangle((min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1])),fill=fill,outline=art.SOFT,width=1)
    rect(-6,8.8,20,10.5,'#dce5e0');rect(11.7,8.5,13.3,9.1,'#8b9e91')
    rect(-6,2.5,20,5.4,'#dfe2da')
    for z in np.arange(2.7,5.25,.46):rect(11.35,float(z),13.7,float(z+.23),art.PAPER)
    rect(-4.1,-4.5,4,1.4,'#ece8dc');rect(4.1,-.8,11,2.4,'#eceee4')
    for x in [-3.5,-1.3,1,3.7]:
        xx,yy=q(x,1.3);d.ellipse((xx-3,yy-3,xx+3,yy+3),fill=art.SOFT)
    path=[q(*site.position(float(t))) for t in np.linspace(0,19.5,100)]
    d.line(path,fill='#c3c8bb',width=3)
    kw=KeyWorld(v);p=kw.p;c=kw.c
    # The view cone comes from the same focal length/projection as its 9:16 frame.
    fov=math.atan((kw.w/2)/kw.focal)
    viewdir=kw.fwd
    rays=[]
    for a in [-fov,fov]:
        R=np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
        rays.append(q(*(c+R@viewdir*16)))
    overlay=Image.new('RGBA',im.size,(0,0,0,0));od=ImageDraw.Draw(overlay)
    od.polygon([q(*c),*rays],fill=(132,167,139,30))
    im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB');d=ImageDraw.Draw(im)
    for r in rays:d.line([q(*c),r],fill='#9aac9e',width=1)
    cx,cy=q(*c);px,py=q(*p)
    d.line(((cx,cy),q(*(c+viewdir*5))),fill='#718a7e',width=2)
    d.rectangle((cx-8,cy-5,cx+8,cy+5),fill='#718a7e')
    d.ellipse((px-7,py-7,px+7,py+7),fill=art.ACCENT)
    tangent=site.position(v['t']+.03)-site.position(v['t']-.03);tangent/=np.linalg.norm(tangent)
    art.arrow(d,(px,py),q(*(p+tangent*1.5)),width=3)
    for label,(x,z) in {'A':(3.7,1.3),'B':(4.8,9.3),'C':(12.5,4),'D':(12.5,9.2)}.items():
        xx,yy=q(x,z);d.text((xx+7,yy-15),label,font=art.font(18,True),fill=art.INK)
    d.text((28,421),'紅點／箭頭：人物與走向　綠方塊／扇形：鏡頭與拍攝範圍',font=art.font(20),fill=art.INK)
    return im


def pages():
    rendered=[]
    for v in VIEWS:rendered.append(make_view(v))
    for k in range(2):
        im=Image.new('RGB',(1450,1590),art.PAPER);d=ImageDraw.Draw(im)
        d.text((40,24),f'連貫上班路｜關鍵視角 {k+1}/2',font=art.font(38,True),fill=art.INK)
        d.text((42,84),'四格先固定同一套示意服裝，核對人物朝向、鏡頭與地標；五套換裝安排保留。',font=art.font(23),fill=art.INK)
        for row,i in enumerate(range(k*2,k*2+2)):
            v=VIEWS[i];y=146+row*700
            d.text((42,y),f"{v['id']}　{v['title']}",font=art.font(30,True),fill=art.INK)
            im.paste(rendered[i].resize((300,533),Image.Resampling.LANCZOS),(44,y+61))
            d.rectangle((44,y+61,344,y+594),outline=art.SOFT,width=1)
            im.paste(mini_map(v),(385,y+47))
            yy=y+515
            yy=art.textblock(d,(385,yy),v['camera_note'],23,1005)+6
            yy=art.textblock(d,(385,yy),'人物｜'+v['person_note'],22,1005)+6
            yy=art.textblock(d,(385,yy),'地標｜'+v['landmarks'],22,1005)+6
            art.textblock(d,(385,yy),'接續｜'+v['continuity'],22,1005)
            d.line((42,y+681,1404,y+681),fill=art.LIGHT,width=2)
        d.text((44,1550),'A 同一柱列　B 公司玻璃外牆　C 同一斑馬線　D 公司入口雨棚／門框',font=art.font(22),fill=art.INK)
        im.save(HERE/f'key_views_{k+1:02d}.png')
    overview=Image.new('RGB',(1510,1010),art.PAPER);d=ImageDraw.Draw(overview)
    d.text((40,25),'同一上班路｜四個關鍵視角',font=art.font(38,True),fill=art.INK)
    d.text((42,87),'街角走出 → 騎樓／小廣場 → 同一路口過街 → 同一公司入口',font=art.font(25),fill=art.INK)
    for i,(v,pic) in enumerate(zip(VIEWS,rendered)):
        x=42+i*367
        d.text((x,153),f"{v['id']}　{v['short_title']}",font=art.font(24,True),fill=art.INK)
        overview.paste(pic.resize((324,576),Image.Resampling.LANCZOS),(x,200))
        d.rectangle((x,200,x+324,776),outline=art.SOFT,width=1)
        art.textblock(d,(x,799),v['landmarks'],23,325)
    d.text((42,952),'同一套服裝僅供空間檢查；圖上字母與箭頭都是分鏡註記，不會放進成片。',font=art.font(23),fill=art.INK)
    overview.save(HERE/'four_key_views_overview.png')
    records=[]
    for v in VIEWS:
        world=KeyWorld(v)
        # Exact camera point and heading used by both the perspective view and plan.
        pp=world.project((world.p[0],0,world.p[1]));top=world.project((world.p[0],1.68,world.p[1]))
        assert 90<pp[0]<world.w-90 and 0<top[1]<pp[1]<world.h
        records.append({**v,'person_position':world.p.tolist(),'camera_position':world.c.tolist(),'camera_look_target':world.aim.tolist(),
                        'camera_forward':world.fwd.tolist(),'screen_right':world.right.tolist(),'focal_ratio':world.focal/world.h,
                        'person_feet_pixel':list(pp[:2]),'person_top_pixel':list(top[:2]),
                        'view_and_map_share_camera':True})
    receipt={'date':'2026-10-16','stage':'static_spatial_key_views_pending_review','view_count':4,'views':records,
             'animation_generated':False,'photoreal_stills_generated':0,'grok_calls':0,'existing_files_replaced':False,
             'fixes':['Camera screen-right orientation derived from the plan view instead of mirrored projection.',
                      'Human marker points use actual world walking direction instead of independently switching front/side sprite.',
                      'Each view shares its exact camera point, field of view and route position with an accompanying plan.'],
             'limits':['Static key frames cannot validate the intervening camera motion or continuous transitions.',
                       'Simplified human/garment geometry is a position marker, not a new M03 identity or wardrobe approval.',
                       'The exact four views and production feasibility remain pending user review.'],
             'files':{}}
    for name in ['four_key_views_overview.png','key_views_01.png','key_views_02.png']:
        p=HERE/name;receipt['files'][name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    (HERE/'key_views_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'views':4,'pages':2,'new_animation':False,'new_generated_stills':0}))


if __name__=='__main__':pages()
