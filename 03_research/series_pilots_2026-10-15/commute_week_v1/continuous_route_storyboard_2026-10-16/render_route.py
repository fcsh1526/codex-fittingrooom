"""One shared fictional scene and continuous world/camera paths for a sketch film."""
from __future__ import annotations
import importlib.util
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
PLAN=json.loads((HERE/'route_plan.json').read_text(encoding='utf-8'))
old=HERE.parent/'line_storyboard_2026-10-16/render_storyboard.py'
spec=importlib.util.spec_from_file_location('line_drawing_primitives',old)
art=importlib.util.module_from_spec(spec);spec.loader.exec_module(art)
SIZE=(540,960)
K=PLAN['path_keyframes']
TIMES=np.array([k['t'] for k in K])
POS=np.array([[k['x'],k['z']] for k in K],float)
VEL=np.array([(POS[min(i+1,len(K)-1)]-POS[max(i-1,0)])/(TIMES[min(i+1,len(K)-1)]-TIMES[max(i-1,0)]) for i in range(len(K))])


def position(t):
    j=min(len(K)-2,max(0,int(np.searchsorted(TIMES,t,side='right')-1)))
    dt=TIMES[j+1]-TIMES[j];u=float(np.clip((t-TIMES[j])/dt,0,1))
    return (2*u**3-3*u**2+1)*POS[j]+(u**3-2*u**2+u)*dt*VEL[j]+(-2*u**3+3*u**2)*POS[j+1]+(u**3-u**2)*dt*VEL[j+1]


def camera(t):
    p=position(t)
    v=position(min(19.5,t+.03))-position(max(0,t-.03));v/=np.linalg.norm(v)
    left=np.array([v[1],-v[0]])
    # One continuous camera arc, independent of garment-change boundaries.
    a=math.radians(32+(145-32)*(t/19.5))
    c=p+3.65*(v*math.cos(a)+left*math.sin(a))
    forward=(p-c)/3.65
    right=np.array([-forward[1],forward[0]])
    return p,c,forward,right,a


class World:
    def __init__(self,t,size=SIZE):
        self.t=t;self.w,self.h=size
        self.p,self.c,self.fwd,self.right,self.a=camera(t)
        self.im=Image.new('RGB',size,art.PAPER);self.d=ImageDraw.Draw(self.im)
        self.focal=self.h*1.65
        self.faces=[];self.lines=[]

    def project(self,p):
        x,y,z=p
        vec=np.array([x,z])-self.c
        dep=float(np.dot(vec,self.fwd))
        if dep<=.15:return None
        return (self.w*.5+float(np.dot(vec,self.right))*self.focal/dep,
                self.h*.40-(y-1.05)*self.focal/dep,dep)

    def polygon(self,pts,fill,outline=art.SOFT):
        self.faces.append((pts,fill,outline))

    def line(self,pts,color=art.SOFT,width=1):
        self.lines.append((pts,color,width))

    def quad(self,x0,x1,z,y0,y1,fill):
        self.polygon([(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)],fill)

    def box(self,x0,x1,z0,z1,height,fill):
        self.quad(x0,x1,z0,0,height,fill)
        self.quad(x0,x1,z1,0,height,fill)
        self.polygon([(x0,0,z0),(x0,0,z1),(x0,height,z1),(x0,height,z0)],fill)
        self.polygon([(x1,0,z0),(x1,0,z1),(x1,height,z1),(x1,height,z0)],fill)
        self.polygon([(x0,height,z0),(x1,height,z0),(x1,height,z1),(x0,height,z1)],fill)

    def ground_rect(self,x0,x1,z0,z1,fill):
        self.polygon([(x0,0,z0),(x1,0,z0),(x1,0,z1),(x0,0,z1)],fill)

    def geometry(self):
        self.ground_rect(-28,38,2.5,5.4,'#dfe1db')
        for z in [2.5,5.4]:self.line([(-28,0,z),(38,0,z)],'#b9beb6',2)
        for z in np.arange(2.65,5.3,.46):self.ground_rect(11.35,13.7,float(z),float(z+.23),'#faf9f3')
        for x in np.arange(-8,23,1.5):
            self.line([(float(x),0,-2),(float(x),0,2.5)],'#e0e2da')
            self.line([(float(x),0,5.4),(float(x),0,8.8)],'#e0e2da')
        for z in [-1,0,.95,1.9,6.3,7.3,8.3]:self.line([(-9,0,z),(23,0,z)],'#e0e2da')
        # Fixed company facade, opening, canopy and lobby.
        self.quad(-6,11.7,8.8,0,6.5,'#e0e6e4')
        self.quad(13.3,20,8.8,0,6.5,'#e0e6e4')
        self.quad(11.7,13.3,8.8,2.8,6.5,'#e0e6e4')
        self.quad(10.7,14.3,11.5,0,3.3,'#d5ddda')
        self.ground_rect(10.7,14.3,8.8,11.5,'#e9ece5')
        for x in [-6,-4,-2,0,2,4,6,8,10,11.7,13.3,15.5,17.5,20]:self.line([(x,0,8.8),(x,6.5,8.8)],'#929f98')
        for y in [2.8,4.5,6.5]:self.line([(-6,y,8.8),(20,y,8.8)],'#a5afa7')
        self.polygon([(10.9,2.9,7.4),(14.1,2.9,7.4),(14.1,2.9,9),(10.9,2.9,9)],'#c9d2cd')
        for x in [11.7,13.3]:self.line([(x,0,8.8),(x,2.8,8.8)],'#6e8077',3)
        # Fixed opposite corner and colonnade, adjacent plaza.
        self.box(-4.1,4.0,-5.5,-4.5,4.7,'#e7e3d8')
        self.polygon([(-4.2,3.0,-4.5),(4.1,3.0,-4.5),(4.1,3.0,1.55),(-4.2,3.0,1.55)],'#dedbd0')
        for x in [-3.5,-1.3,1.0,3.7]:self.box(x-.08,x+.08,1.3,1.46,3.0,'#dcdcd2')
        self.line([(-4.1,1.9,-4.45),(4,1.9,-4.45)],'#c5c7bc')
        # Same planter/tree bases are visible as the camera travels.
        for x,z in [(7.0,-.5),(10.0,-.65)]:
            self.box(x-.45,x+.45,z-.4,z+.4,.42,'#d8dbce')
            self.line([(x,.4,z),(x,2.4,z)],'#a2b09d',3)
            for dx,dz in [(-.55,0),(0,.2),(.5,-.1)]:self.line([(x,1.7,z),(x+dx,2.5,z+dz)],'#b3bfa7',2)

    @staticmethod
    def clip_near(pts,c,fwd):
        out=[]
        for i,b in enumerate(pts):
            a=pts[i-1]
            da=float(np.dot(np.array([a[0],a[2]])-c,fwd))-.16
            db=float(np.dot(np.array([b[0],b[2]])-c,fwd))-.16
            if (da>=0)!=(db>=0):
                q=da/(da-db);out.append(tuple(a[k]+q*(b[k]-a[k]) for k in range(3)))
            if db>=0:out.append(b)
        return out

    def draw_geometry(self):
        self.geometry()
        ordered=sorted(self.faces,key=lambda f:np.mean([np.dot(np.array([p[0],p[2]])-self.c,self.fwd) for p in f[0]]),reverse=True)
        for pts,fill,outline in ordered:
            clipped=self.clip_near(pts,self.c,self.fwd)
            proj=[self.project(p) for p in clipped]
            if len(proj)>2:
                xy=[(max(-4000,min(4000,p[0])),max(-4000,min(4000,p[1]))) for p in proj]
                self.d.polygon(xy,fill=fill)
                self.d.line(xy+[xy[0]],fill=outline,width=1)
        for pts,color,width in self.lines:
            for a,b in zip(pts,pts[1:]):
                da=float(np.dot(np.array([a[0],a[2]])-self.c,self.fwd))-.16
                db=float(np.dot(np.array([b[0],b[2]])-self.c,self.fwd))-.16
                if da<0 and db<0:continue
                if (da>=0)!=(db>=0):
                    q=da/(da-db);v=tuple(a[k]+q*(b[k]-a[k]) for k in range(3))
                    if da<0:a=v
                    else:b=v
                pa,pb=self.project(a),self.project(b)
                if pa and pb:self.d.line((pa[0],pa[1],pb[0],pb[1]),fill=color,width=width)
        # Continuous secondary walkers in the same world coordinates.
        for i,(x,z) in enumerate([(-.6,1.0),(5.2,1.7),(9.0,6.7),(16.8,6.6),(18.0,6.7)]):
            x+=math.sin(self.t*.17+i)*.3
            p=self.project((x,0,z));top=self.project((x,1.55,z))
            if p and top and p[2]>4.1:
                hh=p[1]-top[1]
                if hh>10:art.person(self.d,p[0],p[1],hh,.85,self.t*5+i,'brown_denim',True)

    def draw_model(self,wardrobe):
        p=self.project((self.p[0],0,self.p[1]));top=self.project((self.p[0],1.68,self.p[1]))
        hh=p[1]-top[1]
        degrees=math.degrees(self.a)
        angle=.4 if degrees<70 or degrees>130 else .85
        art.person(self.d,p[0],p[1],hh,angle,self.t*2*math.pi*1.1,wardrobe)
        if degrees>130:
            # Rear marker: simplified hair/back collar. Not identity reference.
            cx=p[0];yy=p[1]-hh
            self.d.ellipse((cx-hh*.043,yy+hh*.002,cx+hh*.043,yy+hh*.116),fill='#555951',outline=art.INK,width=2)
        return self.im


def frame(t):
    active=[s for s in PLAN['segments'] if s['window'][0]<=t<s['window'][1] or (t==19.5 and s['id']=='C05')]
    if not active:raise ValueError(t)
    world=World(t);world.draw_geometry();base=world.im.copy()
    first=world.draw_model(active[0]['wardrobe'])
    if len(active)==1:return first
    world.im=base;world.d=ImageDraw.Draw(world.im)
    second=world.draw_model(active[1]['wardrobe'])
    alpha=(t-active[1]['window'][0])/.75
    return Image.blend(first,second,max(0,min(1,alpha)))


def route_map():
    im=Image.new('RGB',(1420,1160),art.PAPER);d=ImageDraw.Draw(im)
    d.text((44,25),'同一條上班路，五天的穿搭｜連貫空間圖',font=art.font(36,True),fill=art.INK)
    d.text((46,83),'全部發生在公司門前附近；換衣服時，人、鏡頭、背景都接續。',font=art.font(25),fill=art.INK)
    # Top down schematic; north at top, relative units only.
    def q(x,z):return(80+(x+6)*44,830-(z+3)*49)
    def rect(x0,z0,x1,z1,fill):
        a,b=q(x0,z0),q(x1,z1)
        d.rectangle((min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1])),fill=fill,outline=art.SOFT,width=2)
    rect(-6,8.8,20,10.8,'#dce5e0')
    d.text(q(7.6,10.45),'同一棟公司',font=art.font(30,True),fill=art.INK)
    rect(11.65,8.4,13.35,9.0,'#a5b6aa')
    d.text(q(14.2,9.25),'公司入口',font=art.font(23),fill=art.INK)
    rect(-6,2.5,22,5.4,'#e0e2da')
    for z in np.arange(2.7,5.25,.46):rect(11.35,float(z),13.7,float(z+.23),'#faf9f3')
    d.text(q(-4.5,4.6),'公司門前路口',font=art.font(25),fill=art.INK)
    rect(-4.1,-5.5,4,-4.5,'#e7e3d8')
    rect(-4.1,-4.5,4,1.4,'#eeeadd')
    for x in [-3.5,-1.3,1,3.7]:
        xx,yy=q(x,1.3);d.ellipse((xx-6,yy-6,xx+6,yy+6),fill='#b9bdaf')
    rect(4.1,-.8,11,2.4,'#eceee4')
    d.text(q(-3.5,-1.6),'騎樓',font=art.font(25),fill=art.INK)
    d.text(q(5.1,.25),'退縮小廣場',font=art.font(23),fill=art.INK)
    pts=[q(*position(float(t))) for t in np.linspace(0,19.5,180)]
    d.line(pts,fill=art.ACCENT,width=6,joint='curve')
    for t in [1.5,5.4,9.3,13.3,17.3]:
        art.arrow(d,q(*position(t-.22)),q(*position(t+.22)),width=5)
    # Camera path is a separate continuous arc, all in the same coordinate frame.
    cpts=[]
    for t in np.linspace(0,19.5,150):
        _,c,*_=camera(float(t));cpts.append(q(*c))
    for i in range(0,len(cpts)-1,3):d.line(cpts[i:min(i+2,len(cpts))],fill='#778d88',width=3)
    for i,t in enumerate([1.5,5.6,9.4,13.2,17.7]):
        pp,cc,*_=camera(t);p=q(*pp);c=q(*cc)
        d.line((c,p),fill='#bac5bc',width=1)
        d.ellipse((p[0]-17,p[1]-17,p[0]+17,p[1]+17),fill=art.PAPER,outline=art.ACCENT,width=3)
        d.text((p[0]-7,p[1]-13),str(i+1),font=art.font(22,True),fill=art.ACCENT)
        d.rectangle((c[0]-9,c[1]-6,c[0]+9,c[1]+6),fill='#778d88')
    d.text((44,1023),'紅線／編號：人物路徑與五套服裝　　灰綠虛線：攝影機連續跟拍與繞行',font=art.font(24),fill=art.INK)
    d.text((44,1070),'概念場地示意，非真實地址或測量比例。鏡頭繞行幅度與時間仍可在草稿階段調整。',font=art.font(23),fill=art.INK)
    im.save(HERE/'route_map.png')


def storyboard():
    im=Image.new('RGB',(1560,1050),art.PAPER);d=ImageDraw.Draw(im)
    d.text((44,24),'連續跟拍分鏡｜空間不停，衣服改變',font=art.font(38,True),fill=art.INK)
    d.text((46,88),'前斜方跟拍 → 側向跟行 → 斜後方跟進公司；角度在途中逐漸改變。',font=art.font(24),fill=art.INK)
    for i,(s,t) in enumerate(zip(PLAN['segments'],[1.7,5.7,9.5,13.3,18.2])):
        x=46+i*303
        d.text((x,154),f"0{i+1}  {s['label']}",font=art.font(24,True),fill=art.INK)
        pic=frame(t).resize((260,462),Image.Resampling.LANCZOS);im.paste(pic,(x,203))
        d.rectangle((x,203,x+260,665),outline=art.SOFT,width=1)
        st,en=s['window']
        yy=art.textblock(d,(x,689),f'{st:g}–{en:g} 秒',24,270,art.ACCENT,True)+8
        yy=art.textblock(d,(x,yy),s['location'],22,268)+12
        art.textblock(d,(x,yy),s['purpose'],22,268)
    d.text((46,970),'換裝交疊仍約0.75秒；整個場地、鏡頭位置與步伐不因換衣服而重設。',font=art.font(23),fill=art.INK)
    im.save(HERE/'continuous_storyboard.png')


def video():
    fps=PLAN['fps'];n=round(19.5*fps);exe=art.imageio_ffmpeg.get_ffmpeg_exe();out=HERE/'continuous_route_animatic.mp4'
    proc=subprocess.Popen([exe,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-s','540x960','-pix_fmt','rgb24','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    for f in range(n):proc.stdin.write(frame(f/fps).tobytes())
    proc.stdin.close();err=proc.stderr.read().decode('utf-8','replace')
    if proc.wait():raise RuntimeError(err)
    scan=subprocess.run([exe,'-hide_banner','-i',str(out),'-map','0:v:0','-f','null','-'],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if scan.returncode:raise RuntimeError(scan.stderr)
    count=int(re.findall(r'frame=\s*(\d+)',scan.stderr)[-1])
    assert count==n and 'Audio:' not in scan.stderr
    # Numerical continuity at wardrobe boundaries: same single path, no resets.
    continuity=[]
    for j in PLAN['joins']:
        t=j['interval'][0]
        pa,ca,*_=camera(t-.00001);pb,cb,*_=camera(t+.00001)
        continuity.append({'t':t,'person_delta':float(np.linalg.norm(pb-pa)),'camera_delta':float(np.linalg.norm(cb-ca))})
    record={'stage':'continuous_shared_world_sketch','frames':count,'seconds':count/fps,'pixels':[540,960],'fps':fps,'audio':False,'text':False,
            'world_count':1,'continuous_world_and_camera':True,'boundary_numeric_checks':continuity,
            'photoreal_stills_generated':0,'grok_calls':0,'existing_media_modified':False,'user_exact_draft_acceptance':None,
            'limits':'Simplified billboard characters and schematic geometry. Limb/projection/occlusion errors do not validate generated shot quality. No verified five-day interpretation or attraction.',
            'files':{}}
    for name in ['route_map.png','continuous_storyboard.png','continuous_route_animatic.mp4','route_plan.json']:
        p=HERE/name;record['files'][name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    (HERE/'render_receipt.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'frames':count,'seconds':count/fps,'one_world':True,'numeric_continuity':continuity}))


if __name__=='__main__':
    route_map();storyboard();video()
