"""Interpolate approved spatial keys; render new-only schematic wardrobe preview."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
KEY_DIR=HERE.parent/'static_key_views_2026-10-16'
spec=importlib.util.spec_from_file_location('accepted_spatial_keys',KEY_DIR/'build_key_views.py')
keys=importlib.util.module_from_spec(spec);spec.loader.exec_module(keys)
site,art=keys.site,keys.art
PLAN=json.loads((HERE/'previs_plan.json').read_text(encoding='utf-8'))
APPROVAL=json.loads((KEY_DIR/'user_key_view_approval_2026-10-16.json').read_text(encoding='utf-8'))
for f in APPROVAL['approved_files']:
    assert hashlib.sha256((KEY_DIR/f['path']).read_bytes()).hexdigest()==f['sha256'],f['path']

NODES=[dict(keys.VIEWS[0],t=0.0,angle_deg=30,aim_to_door=0),*keys.VIEWS,
       dict(keys.VIEWS[-1],t=19.5,angle_deg=158,aim_to_door=.15)]
TIMES=np.array([n['t'] for n in NODES])
CAMERAS=np.array([keys.KeyWorld(n).c for n in NODES])
VEL=np.array([(CAMERAS[min(i+1,len(NODES)-1)]-CAMERAS[max(i-1,0)])/(TIMES[min(i+1,len(NODES)-1)]-TIMES[max(i-1,0)]) for i in range(len(NODES))])


def interval(t):
    j=min(len(NODES)-2,max(0,int(np.searchsorted(TIMES,t,side='right')-1)))
    dt=TIMES[j+1]-TIMES[j]
    return j,dt,float(np.clip((t-TIMES[j])/dt,0,1))


def camera_values(t):
    j,dt,u=interval(t)
    c=(2*u**3-3*u**2+1)*CAMERAS[j]+(u**3-2*u**2+u)*dt*VEL[j]+(-2*u**3+3*u**2)*CAMERAS[j+1]+(u**3-u**2)*dt*VEL[j+1]
    smooth=u*u*(3-2*u)
    aim_ratio=art.mix(NODES[j]['aim_to_door'],NODES[j+1]['aim_to_door'],smooth)
    focal_ratio=art.mix(NODES[j].get('focal_ratio',1.2),NODES[j+1].get('focal_ratio',1.2),smooth)
    p=site.position(t)
    aim=p+(np.array([12.5,8.8])-p)*aim_ratio
    return p,c,aim,focal_ratio


class MovingWorld(keys.KeyWorld):
    def __init__(self,t):
        super().__init__(dict(keys.VIEWS[0],t=t))
        self.p,self.c,self.aim,f=camera_values(t)
        self.v={'t':t}
        self.fwd=self.aim-self.c;self.fwd/=np.linalg.norm(self.fwd)
        self.right=np.array([self.fwd[1],-self.fwd[0]])
        self.focal=self.h*f

    def model(self,kind):
        t=self.v['t'];p=self.p
        forward=site.position(t+.03)-site.position(t-.03);forward/=np.linalg.norm(forward)
        side=np.array([forward[1],-forward[0]])
        top_color,bottom_color,bag_color=art.COLORS[kind]
        shirt=kind in ['brown_denim','plaid_shirt','a_skirt']
        def W(lateral,y,along=0):
            xz=p+side*lateral+forward*along
            return(float(xz[0]),y,float(xz[1]))
        def poly(points,fill,outline=art.INK):
            pp=[self.project(q) for q in points]
            if any(q is None for q in pp):return
            xy=[q[:2] for q in pp]
            self.d.polygon(xy,fill=fill);self.d.line(xy+[xy[0]],fill=outline,width=2,joint='curve')
        def line(points,color=art.INK,width=2):
            pp=[self.project(q) for q in points]
            if all(q is not None for q in pp):self.d.line([q[:2] for q in pp],fill=color,width=width,joint='curve')
        def prism(cx,cz,y0,y1,rx,rz,fill):
            rings=[[W(cx-rx,y,cz-rz),W(cx+rx,y,cz-rz),W(cx+rx,y,cz+rz),W(cx-rx,y,cz+rz)] for y in [y0,y1]]
            faces=[rings[0],rings[1]]+[[rings[0][i],rings[0][(i+1)%4],rings[1][(i+1)%4],rings[1][i]] for i in range(4)]
            faces.sort(key=lambda f:np.mean([self.project(q)[2] for q in f]),reverse=True)
            for f in faces:poly(f,fill)
        def garment(y0,y1,fill,lower=.145):
            bottom=[W(-lower,y0,-.08),W(lower,y0,-.08),W(lower,y0,.08),W(-lower,y0,.08)]
            upper=[W(-.18,y1,-.075),W(.18,y1,-.075),W(.18,y1,.075),W(-.18,y1,.075)]
            faces=[[bottom[i],bottom[(i+1)%4],upper[(i+1)%4],upper[i]] for i in range(4)]
            faces.sort(key=lambda f:np.mean([self.project(q)[2] for q in f]),reverse=True)
            for f in faces:poly(f,fill)
        phase=t*2*math.pi*1.05
        for ss in [-1,1]:
            along=ss*.105*math.sin(phase)
            lift=max(0,ss*math.sin(phase))*.027
            if kind=='a_skirt':prism(ss*.095,along,.08+lift,.39,.042,.04,'#d7cdbb')
            else:prism(ss*.095,along,.08+lift,.84,.07,.065,bottom_color)
            prism(ss*.095,along+.045,.02+lift,.085+lift,.075,.115,'#3e4240')
        if kind=='a_skirt':
            garment(.33,.86,bottom_color,lower=.23)
        if kind=='short_jacket':
            garment(.83,1.39,'#f7f5ed')
            garment(1.01,1.39,top_color)
        else:garment(.82 if kind=='long_blazer' else .86,1.39,top_color)
        toward_camera=self.c-self.p;toward_camera/=np.linalg.norm(toward_camera)
        facing=float(np.dot(forward,toward_camera))
        if kind=='long_blazer' and facing>.04:
            poly([W(-.055,1.39,.082),W(.055,1.39,.082),W(.045,.92,.088),W(-.045,.92,.088)],'#f8f6ee')
            for ss in [-1,1]:line([W(ss*.08,1.38,.09),W(ss*.10,1.27,.09),W(ss*.055,1.23,.09),W(ss*.04,1.1,.09)])
        if kind=='short_jacket' and facing>.04:
            poly([W(-.055,1.38,.082),W(.055,1.38,.082),W(.045,1.0,.09),W(-.045,1.0,.09)],'#f8f6ee')
            line([W(-.14,1.02,.085),W(.14,1.02,.085)],width=2)
        if kind=='plaid_shirt':
            for depth in [-.081,.081]:
                for xx in [-.12,-.06,0,.06,.12]:line([W(xx,.87,depth),W(xx,1.37,depth)],'#6c7d8d',2)
                for y in [.92,1.02,1.12,1.22,1.32]:line([W(-.15,y,depth),W(.15,y,depth)],'#6c7d8d',2)
        if shirt and facing>.04:
            for ss in [-1,1]:
                poly([W(ss*.02,1.38,.085),W(ss*.085,1.36,.085),W(ss*.055,1.27,.09)],top_color)
            line([W(0,1.28,.09),W(0,.88,.09)],width=1)
        if kind=='brown_denim':prism(0,0,.85,.88,.15,.085,'#353936')
        for ss in [-1,1]:
            along=ss*.025*math.sin(phase)
            if shirt:
                prism(ss*.205,along,1.15,1.34,.04,.045,top_color)
                prism(ss*.205,along,.90,1.15,.028,.03,'#d7cdbb')
            else:prism(ss*.205,along,.91,1.34,.04,.045,top_color)
            line([W(ss*.205,.91,along),W(ss*.20,.84,along)],'#a99d8c',6)
        prism(.25,-.015,.78,.97,.055,.095,bag_color)
        line([W(.20,1.37,0),W(.25,.97,0)],bag_color,3)
        prism(0,0,1.37,1.48,.034,.033,'#ddd3c4')
        hp=self.project(W(0,1.55,0));top=self.project(W(0,1.68,0));low=self.project(W(0,1.45,0))
        hh=low[1]-top[1];rx=hh*.35;cx,cy=hp[:2]
        skin=np.array([221,211,196]);hair=np.array([85,89,80])
        back=float(np.clip(-facing,0,1));fill=tuple(np.round(skin*(1-back)+hair*back).astype(int))
        self.d.ellipse((cx-rx,top[1],cx+rx,low[1]),fill=fill,outline=art.INK,width=2)
        self.d.arc((cx-rx*1.04,top[1]-1,cx+rx*1.04,low[1]-.4*hh),180,360,fill=art.INK,width=4)
        if facing>-.2:line([W(0,1.57,.10),W(0,1.54,.16),W(0,1.52,.10)],width=2)
        return self.im


def active_looks(t):
    return [v for v in PLAN['looks'] if v['interval'][0]<=t<v['interval'][1] or t==19.5 and v['id']=='L04']


def frame(t):
    world=MovingWorld(t);world.draw_geometry();base=world.im.copy()
    active=active_looks(t);assert len(active) in [1,2]
    first=world.model(active[0]['wardrobe'])
    if len(active)==1:return first
    world.im=base;world.d=ImageDraw.Draw(world.im)
    second=world.model(active[1]['wardrobe'])
    return Image.blend(first,second,float(np.clip((t-active[1]['interval'][0])/.75,0,1)))


def board():
    samples=[(1.5,'起步，沿街角走出'),(3.2,'K1：已接受的街角位置'),(5.8,'襯衫丹寧放在前側方'),(8.6,'K2：騎樓接小廣場'),
             (10.5,'轉向前，鏡頭繞到側後'),(13.4,'K3：同一路口過街'),(16.5,'裙裝延續，靠近入口'),(18.4,'K4：同一公司門框前')]
    im=Image.new('RGB',(1420,1670),art.PAPER);d=ImageDraw.Draw(im)
    d.text((40,24),'連續上班路｜轉彎、繞行與換裝草稿',font=art.font(36,True),fill=art.INK)
    d.text((42,84),'四個已接受位置保留；中間補連續鏡頭。衣服改變時，人物與背景不重設。',font=art.font(23),fill=art.INK)
    for i,(t,label) in enumerate(samples):
        x=42+(i%4)*348;y=147+(i//4)*665
        d.text((x,y),f'{t:g} 秒',font=art.font(24,True),fill=art.ACCENT)
        pic=frame(t).resize((298,530),Image.Resampling.LANCZOS);im.paste(pic,(x,y+44))
        d.rectangle((x,y+44,x+298,y+574),outline=art.SOFT,width=1)
        yy=art.textblock(d,(x,y+590),label,22,302)+3
        art.textblock(d,(x,yy),active_looks(t)[-1]['label'],21,302)
    d.text((42,1501),'換裝順序：長西外 → 白襯衫棕丹寧 → 短外套灰褲 → 格紋灰褲 → 白襯衫黑裙藍包',font=art.font(23),fill=art.INK)
    d.text((42,1548),'四次0.75秒柔接；首尾清楚讀衣各3.75秒，中間各3秒。後兩套以側後方輪廓為主。',font=art.font(23),fill=art.INK)
    d.text((42,1595),'人形僅示意方向、位置與服裝差異；無新寫實圖或Grok影片，不代表實際生成已可連貫。',font=art.font(22),fill=art.INK)
    im.save(HERE/'eight_frame_board.png')


def checks():
    matched=[]
    for v in keys.VIEWS:
        old=keys.KeyWorld(v);new=MovingWorld(v['t'])
        err=max(float(np.linalg.norm(old.p-new.p)),float(np.linalg.norm(old.c-new.c)),float(np.linalg.norm(old.fwd-new.fwd)),abs(old.focal-new.focal))
        assert err<1e-8,(v['id'],err)
        matched.append({'id':v['id'],'max_camera_projection_error':err})
    centres=[];collision=[];yaws=[];deltas=[]
    for t in np.linspace(0,19.5,469):
        w=MovingWorld(float(t));x,z=w.c
        if -4.1<x<4 and -5.5<z<-4.5:collision.append({'t':float(t),'object':'opposite building'})
        if -6<x<20 and z>8.8 and not (11.7<x<13.3):collision.append({'t':float(t),'object':'company wall'})
        for px in [-3.5,-1.3,1,3.7]:
            if abs(x-px)<.18 and abs(z-1.38)<.18:collision.append({'t':float(t),'object':'column'})
        feet=w.project((w.p[0],0,w.p[1]));top=w.project((w.p[0],1.68,w.p[1]))
        assert feet and top and 70<feet[0]<470 and 0<top[1]<feet[1]<960,(t,feet,top)
        centres.append([feet[0],top[1],feet[1]])
        yaws.append(math.atan2(w.fwd[0],w.fwd[1]))
    assert not collision,collision[:5]
    yaw_step=np.diff(np.unwrap(yaws))*180/math.pi
    return {'approved_key_matches':matched,'sample_count':469,'camera_inside_checked_buildings_or_columns':False,
            'body_centre_top_and_feet_fit_all_samples':True,'max_adjacent_yaw_change_deg_at24fps':float(np.max(abs(yaw_step))),
            'limits':'Centre/top/feet checks do not prove every sleeve/bag contour or foreground occlusion. Camera curve continuity is a schematic property, not actual generated motion.'}


def movie():
    verification=checks();board()
    out=HERE/'accepted_keys_five_outfits_animatic.mp4';fps=24;n=468
    exe=art.imageio_ffmpeg.get_ffmpeg_exe()
    proc=subprocess.Popen([exe,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-s','540x960','-pix_fmt','rgb24','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    for i in range(n):proc.stdin.write(frame(i/fps).tobytes())
    proc.stdin.close();err=proc.stderr.read().decode('utf-8','replace')
    if proc.wait():raise RuntimeError(err)
    scan=subprocess.run([exe,'-hide_banner','-i',str(out),'-map','0:v:0','-f','null','-'],capture_output=True,text=True,encoding='utf-8',errors='replace')
    assert scan.returncode==0,scan.stderr
    assert int(re.findall(r'frame=\s*(\d+)',scan.stderr)[-1])==n and 'Audio:' not in scan.stderr
    receipt={'date':'2026-10-16','stage':'new_timed_sketch_pending_user_review','frames':n,'seconds':19.5,'fps':24,'pixels':[540,960],
             'audio':False,'text':False,'arrows_in_video':False,'approved_static_keys_retained':True,
             'new_camera_path_and_outfit_schedule_accepted':None,'photoreal_stills_generated':0,'grok_calls':0,
             'existing_approved_files_modified':False,'geometry_checks':verification,'files':{}}
    for name in ['eight_frame_board.png','accepted_keys_five_outfits_animatic.mp4','previs_plan.json']:
        p=HERE/name;receipt['files'][name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    (HERE/'previs_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'frames':n,'seconds':19.5,'geometry_checks':verification}))


if __name__=='__main__':movie()
