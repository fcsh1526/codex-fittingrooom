from pathlib import Path
import json, math, hashlib, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
FONT='C:/Windows/Fonts/msjh.ttc'
def font(s): return ImageFont.truetype(FONT,s)
PAPER='#f7f4ed'; INK='#38434a'; BLUE='#216f9b'; RED='#b85542'
def text(d,xy,s,size=20,fill=INK): d.text(xy,s,font=font(size),fill=fill)

def dense_curve(points):
    a=np.array(points,float); out=[]
    for i in range(len(a)-1):
        p0=a[max(i-1,0)];p1=a[i];p2=a[i+1];p3=a[min(i+2,len(a)-1)]
        for u in np.linspace(0,1,250,endpoint=False):
            out.append(.5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u*u+(-p0+3*p1-3*p2+p3)*u*u*u))
    out.append(a[-1]); out=np.array(out)
    lengths=np.r_[0,np.cumsum(np.linalg.norm(np.diff(out,axis=0),axis=1))]
    return out,lengths

SCENE={'id':'M02_office_greenway_v1','units':'schematic','unit_note':'Fictional blockout, not a measured location; adult height1.68 schematic units.','axes':'x right, y up, z toward office','duration_seconds':12,'fps':24,'person_control_points':[[-.8,0],[-.7,2.8],[.1,5.8],[1.5,8.8],[2.1,11.7]],'camera_control_points':[[-2.7,3.0],[-3.6,4.7],[-3.3,6.8],[-2.4,9.6],[-.4,14.0]],'camera_height':1.35,'vertical_fov_degrees':34,'target_height':.90,'office_footprint':[1.4,6,21.8,16],'planters':[[4,2],[4.5,6],[-5,3],[-5,8]],'person_time':'arc-length uniform until10s, then decelerate to rest at12s','camera_time':'independent curve with uniform arc-length progression','wardrobe':'white pointed-collar shirt, dark-indigo ankle straight jeans, black penny loafers, burgundy shoulder bag','approval':'proposed, not a generated shot or approved scene'}
SCENE.update(id='M02_five_look_wide_start_v2',duration_seconds=20,person_control_points=[[-.8,0],[-.7,5],[.1,10.5],[1.5,15.8],[2.1,21]],camera_control_points=[[-3.46,4.2],[-3,7.5],[-2.5,12],[-1.7,17],[.2,24.1]],office_footprint=[1.4,6,21.8,26],planters=[[4,4],[4.5,11],[-5,6],[-5,14]],person_time='arc-length uniform0-18s, decelerate18-20s',camera_time='independent arc-length curve with smooth phase offset qC=qP-.025sin(pi*qP); common20s clock, no restart at clothing changes',wardrobe='five proposed workday combinations, same dark-indigo jeans',approval='user chose five-look format; wardrobe, route, duration and new images remain proposed')
LOOKS=[{'id':'F01','name':'週一 白襯衫','top':'#fffdf8','bag':'#8f4f53','shoe':'#303237','weekly_look':'2026-W46-002-L01'}, {'id':'F02','name':'週二 藍條紋襯衫','top':'#c2d4e0','bag':'#a69a83','shoe':'#735744','weekly_look':None}, {'id':'F03','name':'週三 燕麥薄針織','top':'#d6c8ae','bag':'#a69a83','shoe':'#303237','weekly_look':None}, {'id':'F04','name':'週四 淺灰薄西外','top':'#b9bfc4','bag':'#7d8487','shoe':'#303237','weekly_look':None}, {'id':'F05','name':'週五 白T帆布鞋','top':'#fffdf8','bag':'#7797aa','shoe':'#d7dbd8','weekly_look':'2026-W46-002-L02'}]
P,PS=dense_curve(SCENE['person_control_points']);C,CS=dense_curve(SCENE['camera_control_points'])
def sample(a,ss,q):
    s=np.clip(q,0,1)*ss[-1];j=min(len(ss)-2,max(0,int(np.searchsorted(ss,s)-1)));u=(s-ss[j])/max(1e-8,ss[j+1]-ss[j]);return a[j]*(1-u)+a[j+1]*u
def state(t):
    # 11 units of weighted travel: ten uniform seconds + two seconds linear deceleration.
    q=t/19 if t<=18 else (18+(t-18)-.25*(t-18)**2)/19
    p=sample(P,PS,q);c=sample(C,CS,q-.025*math.sin(math.pi*q))
    back=sample(P,PS,max(0,q-.002));ahead=sample(P,PS,min(1,q+.002));heading=ahead-back;heading/=np.linalg.norm(heading)
    cam=np.array([c[0],SCENE['camera_height'],c[1]])
    target=np.array([p[0],SCENE['target_height'],p[1]])
    f=target-cam;f/=np.linalg.norm(f);right=np.cross(f,[0,1,0]);right/=np.linalg.norm(right);up=np.cross(right,f)
    return p,c,heading,cam,f,right,up

def camera_view(t,size=(360,640),look_override=None):
    ix=min(4,int(t//4)) if look_override is None else look_override
    TOP=LOOKS[ix]["top"]; BAG=LOOKS[ix]["bag"]; SHOE=LOOKS[ix]["shoe"]
    w,h=size;p,c,heading,cam,f,right,up=state(t)
    im=Image.new('RGB',size,PAPER);d=ImageDraw.Draw(im);foc=h/(2*math.tan(math.radians(SCENE['vertical_fov_degrees']/2)))
    def proj(v):
        q=np.array(v)-cam;dep=np.dot(q,f)
        if dep<.25:return None
        return (w/2+np.dot(q,right)*foc/dep,h/2-np.dot(q,up)*foc/dep)
    def line(pts,color='#b8bdb5',width=1):
        for a,b in zip(pts,pts[1:]):
            aa,bb=proj(a),proj(b)
            if aa and bb:d.line([tuple(np.clip(aa,-3000,3000)),tuple(np.clip(bb,-3000,3000))],fill=color,width=width)
    for z in np.arange(-1,27,.9):line([(-6,0,z),(6,0,z)],'#deded4')
    for x in np.arange(-6,7,1):line([(x,0,-1),(x,0,27)],'#e4e2d8')
    # Fixed office elevation and tree/planter landmarks in the same world as the map.
    for x in [1.4,2.2,3.4,4.6,6]:line([(x,0,21.8),(x,4.2,21.8)],'#839a9b',2)
    for y in [0,2.6,4.2]:line([(1.4,y,21.8),(6,y,21.8)],'#839a9b',2)
    line([(1.4,2.8,21.2),(6,2.8,21.2),(6,2.8,21.8)],'#839a9b',2)
    for x,z in SCENE['planters']:
        for dx in [-.4,.4]:line([(x+dx,0,z-.4),(x+dx,.45,z-.4),(x+dx,.45,z+.4),(x+dx,0,z+.4)],'#9ba887',2)
        line([(x,.45,z),(x,2.6,z)],'#9ba887',3)
        for dx in [-.7,0,.7]:line([(x,1.9,z),(x+dx,2.9,z+.25)],'#9ba887',3)
    lat=np.array([heading[1],-heading[0]])
    def v(side,y,forward=0):
        a=p+lat*side+heading*forward;return (a[0],y,a[1])
    def poly(pts,fill):
        a=[proj(q) for q in pts]
        if all(q is not None for q in a):d.polygon(a,fill=fill,outline=INK)
    phase=2*math.pi*(t if t<=18 else 18+(t-18)-.25*(t-18)**2)*1.05
    stride=.17*math.sin(phase)*(1 if t<=18 else max(0,(20-t)/2))
    # Give the body depth, so the same geometry remains readable in a side view.
    for dep in [-.09,.09]:
        poly([v(-.2,1.41,dep),v(.2,1.41,dep),v(.18,.89,dep),v(-.18,.89,dep)],TOP)
    for side in [-1,1]:
        poly([v(side*.2,1.41,-.09),v(side*.2,1.41,.09),v(side*.18,.89,.09),v(side*.18,.89,-.09)],TOP)
    if ix in [0,1]:
        poly([v(-.12,1.41,.1),v(0,1.28,.11),v(.12,1.41,.1)],'#f8faf9')
        line([v(0,1.29,.11),v(0,.91,.11)],'#aab0ad',1)
    elif ix==3:
        poly([v(-.1,1.41,.1),v(0,1.12,.12),v(.1,1.41,.1)],'#fffdf8')
        line([v(-.11,1.40,.12),v(-.18,1.22,.12),v(0,1.03,.12)],INK,1)
        line([v(.11,1.40,.12),v(.18,1.22,.12),v(0,1.03,.12)],INK,1)
    elif ix==2:
        line([v(0,1.4,.12),v(0,.90,.12)],'#b6a689',2)
    if ix==1:
        for side in [-.14,-.07,0,.07,.14]:line([v(side,1.36,.12),v(side,.92,.12)],'#6b91af',1)
    for side,step in [(-.105,stride),(.105,-stride)]:
        for dep in [-.065,.065]:poly([v(side-.08,.9,dep),v(side+.08,.9,dep),v(side+.065,.08,step+dep),v(side-.065,.08,step+dep)],'#293b54')
        poly([v(side+.08,.9,-.065),v(side+.08,.9,.065),v(side+.065,.08,step+.065),v(side+.065,.08,step-.065)],'#344962')
        line([v(side-.075,.04,step-.05),v(side+.075,.04,step+.12)],SHOE,5)
    for side in [-1,1]:line([v(side*.2,1.35),v(side*.27,1.08,side*stride*.3),v(side*.28,.86,-side*stride*.3)],INK,3)
    poly([v(-.27,1.0),v(-.47,1.0),v(-.47,.72),v(-.27,.72)],BAG)
    line([v(-.2,1.4),v(-.38,.96)],BAG,3)
    top=proj(v(0,1.68));bottom=proj(v(0,0));head=proj(v(0,1.53));r=foc*.10/float(np.dot(np.array(v(0,1.53))-cam,f))
    d.ellipse((head[0]-r,head[1]-r*1.25,head[0]+r,head[1]+r*1.25),fill='#e7d6bf',outline=INK,width=2)
    # Nose points along the actual body heading; marker is a sketch, not identity QA.
    nose=proj(v(0,1.53,.12));d.line([head,nose],fill=INK,width=2)
    d.rectangle((1,1,w-2,h-2),outline='#7a8988',width=2)
    return im,{'time':t,'person_xz':p.tolist(),'camera_xz':c.tolist(),'heading_xz':heading.tolist(),'distance':float(np.linalg.norm(p-c)),'height_fraction':(bottom[1]-top[1])/h,'top_uv':[top[0]/w,top[1]/h],'bottom_uv':[bottom[0]/w,bottom[1]/h],'front_angle_degrees':math.degrees(math.acos(float(np.clip(np.dot(heading,(c-p)/np.linalg.norm(c-p)),-1,1))))}

def overhead(t=None,size=(800,800)):
    im=Image.new('RGB',size,PAPER);d=ImageDraw.Draw(im)
    def uv(q):return (80+(q[0]+6)*48,720-(q[1]+1)*22)
    text(d,(25,15),'M02 五套沿路換裝｜共用場地俯瞰線稿',26)
    text(d,(25,55),'藍：人物　紅：相機　灰色箭頭：拍攝方向',18)
    a=uv((-4.5,-1));b=uv((3.2,21.8));d.rectangle((a[0],b[1],b[0],a[1]),fill='#ebe9dd')
    x0,x1,z0,z1=SCENE['office_footprint'];a=uv((x0,z0));b=uv((x1,z1));d.rectangle((a[0],b[1],b[0],a[1]),fill='#dbe5e5',outline=INK,width=2);text(d,(a[0]+8,b[1]+15),'辦公大樓',18);text(d,(a[0]+8,a[1]+7),'入口前停步',16)
    for x,z in SCENE['planters']:
        a=uv((x,z));d.ellipse((a[0]-16,a[1]-16,a[0]+16,a[1]+16),fill='#c8d6af',outline='#81956a')
    d.line([uv(p) for p in P],fill=BLUE,width=5);d.line([uv(c) for c in C],fill=RED,width=4)
    for tt in [0,5,10,15,20]:
        p,c,*_=state(tt);pp,cc=uv(p),uv(c)
        d.line([cc,pp],fill='#afb7b2',width=1)
        vv=np.array(pp)-np.array(cc);vv/=np.linalg.norm(vv);tip=np.array(cc)*.25+np.array(pp)*.75;normal=np.array([-vv[1],vv[0]])
        d.polygon([tuple(tip),tuple(tip-vv*10+normal*4),tuple(tip-vv*10-normal*4)],fill='#afb7b2')
        for xy,col in [(pp,BLUE),(cc,RED)]:d.ellipse((xy[0]-5,xy[1]-5,xy[0]+5,xy[1]+5),fill=col)
        text(d,(pp[0]+9,pp[1]-6),f'P {tt}s',16,BLUE);text(d,(cc[0]-67,cc[1]-22),f'C {tt}s',16,RED)
    for n,tt in enumerate([4,8,12,16],1):
        pp=uv(state(tt)[0]);d.ellipse((pp[0]-12,pp[1]-12,pp[0]+12,pp[1]+12),outline='#bd913e',width=4);text(d,(pp[0]+18,pp[1]-15),f'換裝{n} / {tt}s',16,'#96702e')
    if t is not None:
        p,c,*_=state(t);pp,cc=uv(p),uv(c);d.line([cc,pp],fill=INK,width=3)
        d.ellipse((pp[0]-10,pp[1]-10,pp[0]+10,pp[1]+10),fill=BLUE)
        d.rectangle((cc[0]-9,cc[1]-7,cc[0]+9,cc[1]+7),fill=RED)
        text(d,(25,745),f'共同時間 {t:05.2f} 秒',22)
    else:text(d,(25,745),'20秒五套提案｜金圈為換裝點｜示意場地非實測',18)
    return im

def film_frame(t,size=(360,640)):
    for n,b in enumerate([4,8,12,16]):
        if b-.375<=t<b+.375:
            a,m=camera_view(t,size,n);bb,_=camera_view(t,size,n+1);return Image.blend(a,bb,(t-b+.375)/.75),m
    return camera_view(t,size)

def main():
    SCENE['looks']=LOOKS;SCENE['change_centers_seconds']=[4,8,12,16];SCENE['overlap_seconds']=.75
    (HERE/'shared_scene.json').write_text(json.dumps(SCENE,ensure_ascii=False,indent=2),encoding='utf-8')
    overhead().save(HERE/'overhead_routes.png')
    keys=[2,6,10,14,18];board=Image.new('RGB',(1390,850),PAPER);d=ImageDraw.Draw(board);text(d,(25,15),'同一路線五套通勤｜每格由同一場地與時鐘投影',28)
    for i,tt in enumerate(keys):
        im,m=camera_view(tt,(250,444));x=20+i*274;board.paste(im,(x,75));text(d,(x,535),LOOKS[i]['name'],21);text(d,(x,572),f'{tt}s / 視角{m["front_angle_degrees"]:.0f}°',18);text(d,(x,605),f'人物畫高{m["height_fraction"]:.0%}',18)
    text(d,(25,670),'換裝中心：4 / 8 / 12 / 16秒。人物、步相、攝影機和場景時間都不重設。',23)
    text(d,(25,715),'全部保留同一深靛直褲，以領口、外層、鞋與包呈現五天正式度；服裝搭配仍為提案。',22)
    text(d,(25,760),'示意配色與簡化人體只用來檢查路線、接點和讀衣時間，不是寫實圖或實際動態品質證明。',20)
    board.save(HERE/'five_look_storyboard.png')
    metrics=[];ff=ROOT/'openmontage/.local/bin/ffmpeg.exe';proc=subprocess.Popen([str(ff),'-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x800','-r','24','-i','-','-an','-c:v','libx264','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(HERE/'five_look_synchronized_previs.mp4')],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    for n in range(480):
        tt=n/24;im,m=film_frame(tt);metrics.append(m);canvas=Image.new('RGB',(1280,800),PAPER);canvas.paste(overhead(tt),(0,0));canvas.paste(im,(860,70));dd=ImageDraw.Draw(canvas);text(dd,(850,15),'同時間換裝相機畫框',24);text(dd,(845,730),f'{tt:.2f}s / '+LOOKS[min(4,int(tt//4))]['name'],18);proc.stdin.write(canvas.tobytes())
    proc.stdin.close();assert proc.wait()==0
    metrics.append(camera_view(20)[1]);(HERE/'projected_samples.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
    collisions=[]
    for m in metrics:
        for who in ['person_xz','camera_xz']:
            x,z=m[who];x0,x1,z0,z1=SCENE['office_footprint']
            if x0<=x<=x1 and z0<=z<=z1:collisions.append([m['time'],who,'office'])
            for px,pz in SCENE['planters']:
                if abs(px-x)<.55 and abs(pz-z)<.55:collisions.append([m['time'],who,'planter'])
    summary={'scene_sha256':hashlib.sha256((HERE/'shared_scene.json').read_bytes()).hexdigest(),'same_scene_and_clock':True,'camera_is_independent_curve':True,'render_frames':480,'fps':24,'seconds':20,'look_count':5,'transition_count':4,'transition_centers':[4,8,12,16],'transition_overlap_seconds':.75,'height_fraction_range':[min(m['height_fraction'] for m in metrics),max(m['height_fraction'] for m in metrics)],'front_angle_range':[min(m['front_angle_degrees'] for m in metrics),max(m['front_angle_degrees'] for m in metrics)],'top_min':min(m['top_uv'][1] for m in metrics),'bottom_max':max(m['bottom_uv'][1] for m in metrics),'collisions_blockout':collisions,'limits':'Five-look format accepted; proposed wardrobe/routes/timing not yet visually approved. Mathematical pose equality in overlaps is not real video ghosting/gait verification.'}
    (HERE/'geometry_check.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
