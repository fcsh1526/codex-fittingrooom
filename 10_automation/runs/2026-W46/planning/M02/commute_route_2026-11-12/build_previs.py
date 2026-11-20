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

SCENE={'id':'M02_office_greenway_v1','units':'schematic','unit_note':'Fictional blockout, not a measured location; adult height1.68 schematic units.','axes':'x right, y up, z toward office','duration_seconds':12,'fps':24,'person_control_points':[[-.8,0],[-.7,2.8],[.1,5.8],[1.5,8.8],[2.1,11.7]],'camera_control_points':[[-2.7,3.0],[-3.6,4.7],[-3.3,6.8],[-2.4,9.6],[-.4,14.0]],'camera_height':1.35,'vertical_fov_degrees':34,'target_height':.90,'office_footprint':[1.4,6,12.4,16],'planters':[[4,2],[4.5,6],[-5,3],[-5,8]],'person_time':'arc-length uniform until10s, then decelerate to rest at12s','camera_time':'independent curve with uniform arc-length progression','wardrobe':'white pointed-collar shirt, dark-indigo ankle straight jeans, black penny loafers, burgundy shoulder bag','approval':'proposed, not a generated shot or approved scene'}
SCENE['camera_control_points']=[[-2.7,3.0],[-3.0,4.7],[-2.5,7.3],[-1.7,10.2],[.2,14.8]]
P,PS=dense_curve(SCENE['person_control_points']);C,CS=dense_curve(SCENE['camera_control_points'])
def sample(a,ss,q):
    s=np.clip(q,0,1)*ss[-1];j=min(len(ss)-2,max(0,int(np.searchsorted(ss,s)-1)));u=(s-ss[j])/max(1e-8,ss[j+1]-ss[j]);return a[j]*(1-u)+a[j+1]*u
def state(t):
    # 11 units of weighted travel: ten uniform seconds + two seconds linear deceleration.
    q=t/11 if t<=10 else (10+(t-10)-.25*(t-10)**2)/11
    p=sample(P,PS,q);c=sample(C,CS,t/12)
    back=sample(P,PS,max(0,q-.002));ahead=sample(P,PS,min(1,q+.002));heading=ahead-back;heading/=np.linalg.norm(heading)
    cam=np.array([c[0],SCENE['camera_height'],c[1]])
    target=np.array([p[0],SCENE['target_height'],p[1]])
    f=target-cam;f/=np.linalg.norm(f);right=np.cross(f,[0,1,0]);right/=np.linalg.norm(right);up=np.cross(right,f)
    return p,c,heading,cam,f,right,up

def camera_view(t,size=(360,640)):
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
    for z in np.arange(-1,17,.9):line([(-6,0,z),(6,0,z)],'#deded4')
    for x in np.arange(-6,7,1):line([(x,0,-1),(x,0,17)],'#e4e2d8')
    # Fixed office elevation and tree/planter landmarks in the same world as the map.
    for x in [1.4,2.2,3.4,4.6,6]:line([(x,0,12.4),(x,4.2,12.4)],'#839a9b',2)
    for y in [0,2.6,4.2]:line([(1.4,y,12.4),(6,y,12.4)],'#839a9b',2)
    line([(1.4,2.8,11.8),(6,2.8,11.8),(6,2.8,12.4)],'#839a9b',2)
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
    phase=2*math.pi*(t if t<=10 else 10+(t-10)-.25*(t-10)**2)*1.05
    stride=.17*math.sin(phase)*(1 if t<=10 else max(0,(12-t)/2))
    # Give the body depth, so the same geometry remains readable in a side view.
    for dep in [-.09,.09]:
        poly([v(-.2,1.41,dep),v(.2,1.41,dep),v(.18,.89,dep),v(-.18,.89,dep)],'#fffdf8')
    for side in [-1,1]:
        poly([v(side*.2,1.41,-.09),v(side*.2,1.41,.09),v(side*.18,.89,.09),v(side*.18,.89,-.09)],'#e8e6df')
    for side,step in [(-.105,stride),(.105,-stride)]:
        for dep in [-.065,.065]:poly([v(side-.08,.9,dep),v(side+.08,.9,dep),v(side+.065,.08,step+dep),v(side-.065,.08,step+dep)],'#293b54')
        poly([v(side+.08,.9,-.065),v(side+.08,.9,.065),v(side+.065,.08,step+.065),v(side+.065,.08,step-.065)],'#344962')
        line([v(side-.075,.04,step-.05),v(side+.075,.04,step+.12)],INK,5)
    for side in [-1,1]:line([v(side*.2,1.35),v(side*.27,1.08,side*stride*.3),v(side*.28,.86,-side*stride*.3)],INK,3)
    poly([v(-.27,1.0),v(-.47,1.0),v(-.47,.72),v(-.27,.72)],'#8f4f53')
    line([v(-.2,1.4),v(-.38,.96)],'#8f4f53',3)
    top=proj(v(0,1.68));bottom=proj(v(0,0));head=proj(v(0,1.53));r=foc*.10/float(np.dot(np.array(v(0,1.53))-cam,f))
    d.ellipse((head[0]-r,head[1]-r*1.25,head[0]+r,head[1]+r*1.25),fill='#e7d6bf',outline=INK,width=2)
    # Nose points along the actual body heading; marker is a sketch, not identity QA.
    nose=proj(v(0,1.53,.12));d.line([head,nose],fill=INK,width=2)
    d.rectangle((1,1,w-2,h-2),outline='#7a8988',width=2)
    return im,{'time':t,'person_xz':p.tolist(),'camera_xz':c.tolist(),'heading_xz':heading.tolist(),'distance':float(np.linalg.norm(p-c)),'height_fraction':(bottom[1]-top[1])/h,'top_uv':[top[0]/w,top[1]/h],'bottom_uv':[bottom[0]/w,bottom[1]/h],'front_angle_degrees':math.degrees(math.acos(float(np.clip(np.dot(heading,(c-p)/np.linalg.norm(c-p)),-1,1))))}

def overhead(t=None,size=(800,800)):
    im=Image.new('RGB',size,PAPER);d=ImageDraw.Draw(im)
    def uv(q):return (80+(q[0]+6)*48,720-(q[1]+1)*37)
    text(d,(25,15),'M02 走路上班｜共用場地俯瞰線稿',26)
    text(d,(25,55),'藍：人物　紅：相機　灰色箭頭：拍攝方向',18)
    a=uv((-4.5,-1));b=uv((3.2,12.4));d.rectangle((a[0],b[1],b[0],a[1]),fill='#ebe9dd')
    x0,x1,z0,z1=SCENE['office_footprint'];a=uv((x0,z0));b=uv((x1,z1));d.rectangle((a[0],b[1],b[0],a[1]),fill='#dbe5e5',outline=INK,width=2);text(d,(a[0]+8,b[1]+15),'辦公大樓',18);text(d,(a[0]+8,a[1]+7),'入口前停步',16)
    for x,z in SCENE['planters']:
        a=uv((x,z));d.ellipse((a[0]-16,a[1]-16,a[0]+16,a[1]+16),fill='#c8d6af',outline='#81956a')
    d.line([uv(p) for p in P],fill=BLUE,width=5);d.line([uv(c) for c in C],fill=RED,width=4)
    for tt in [0,3,6,9,12]:
        p,c,*_=state(tt);pp,cc=uv(p),uv(c)
        d.line([cc,pp],fill='#afb7b2',width=1)
        vv=np.array(pp)-np.array(cc);vv/=np.linalg.norm(vv);tip=np.array(cc)*.25+np.array(pp)*.75;normal=np.array([-vv[1],vv[0]])
        d.polygon([tuple(tip),tuple(tip-vv*10+normal*4),tuple(tip-vv*10-normal*4)],fill='#afb7b2')
        for xy,col in [(pp,BLUE),(cc,RED)]:d.ellipse((xy[0]-5,xy[1]-5,xy[0]+5,xy[1]+5),fill=col)
        text(d,(pp[0]+9,pp[1]-6),f'P {tt}s',16,BLUE);text(d,(cc[0]-67,cc[1]-22),f'C {tt}s',16,RED)
    if t is not None:
        p,c,*_=state(t);pp,cc=uv(p),uv(c);d.line([cc,pp],fill=INK,width=3)
        d.ellipse((pp[0]-10,pp[1]-10,pp[0]+10,pp[1]+10),fill=BLUE)
        d.rectangle((cc[0]-9,cc[1]-7,cc[0]+9,cc[1]+7),fill=RED)
        text(d,(25,745),f'共同時間 {t:05.2f} 秒',22)
    else:text(d,(25,745),'12秒單套通勤路段提案｜示意單位，非實測場地',18)
    return im

def main():
    (HERE/'shared_scene.json').write_text(json.dumps(SCENE,ensure_ascii=False,indent=2),encoding='utf-8')
    overhead().save(HERE/'overhead_routes.png')
    keys=[0,2.4,4.8,7.2,9.6,12];board=Image.new('RGB',(1440,990),PAPER);d=ImageDraw.Draw(board);text(d,(30,15),'同一場地、同一時鐘投影｜相機畫框線稿（人物非身份參考）',27)
    notes=['前側接近：白領與褲鞋同讀','轉到側向：包、手與步伐','側向讀褲線：不換裝','開始繞回：留意入口同事','接近入口：放慢、微笑','入口前停步：全身收尾']
    for i,tt in enumerate(keys):
        im,m=camera_view(tt,(220,392));x=20+(i%6)*237;board.paste(im,(x,70));text(d,(x,475),f'{tt:g}s / {m["front_angle_degrees"]:.0f}°',18);text(d,(x,507),notes[i][:8],17);text(d,(x,532),notes[i][8:],17);text(d,(x,563),f'畫高 {m["height_fraction"]:.0%}',17)
    text(d,(30,640),'人物 P(t) 沿林蔭步道走向大樓；攝影機 C(t) 走另一條曲線，先到側面讀褲線，再回前側看反應。',22)
    text(d,(30,685),'0–10秒依弧長前進，10–12秒自然減速停步；不在每個時間點重新起步。',22)
    text(d,(30,730),'此版先規劃通勤單套路段；週末第二套仍保留於W46素材計畫，未在此段中途換裝。',22)
    text(d,(30,790),'線稿用於檢查方位、尺度、地標與路線，不代表生成引擎已能精確執行或步態已通過。',20)
    board.save(HERE/'camera_storyboard.png')
    metrics=[];ff=ROOT/'openmontage/.local/bin/ffmpeg.exe'
    args=[str(ff),'-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x800','-r','24','-i','-','-an','-c:v','libx264','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(HERE/'synchronized_previs.mp4')]
    proc=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    for n in range(288):
        tt=n/24;im,m=camera_view(tt,(360,640));metrics.append(m);canvas=Image.new('RGB',(1280,800),PAPER);canvas.paste(overhead(tt),(0,0));canvas.paste(im,(860,70));dd=ImageDraw.Draw(canvas);text(dd,(850,15),'同時間相機畫框 9:16',24);text(dd,(850,730),f'{tt:.2f}s　方位 {m["front_angle_degrees"]:.0f}°',21);proc.stdin.write(canvas.tobytes())
    proc.stdin.close();assert proc.wait()==0
    metrics.append(camera_view(12)[1]);(HERE/'projected_samples.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
    collision=[]
    for m in metrics:
        for who in ['person_xz','camera_xz']:
            x,z=m[who];x0,x1,z0,z1=SCENE['office_footprint']
            if x0<=x<=x1 and z0<=z<=z1:collision.append([m['time'],who,'office'])
            for px,pz in SCENE['planters']:
                if abs(px-x)<.55 and abs(pz-z)<.55:collision.append([m['time'],who,'planter'])
    summary={'scene_sha256':hashlib.sha256((HERE/'shared_scene.json').read_bytes()).hexdigest(),'same_scene_and_clock':True,'camera_is_independent_curve':True,'render_frames':288,'fps':24,'seconds':12,'height_fraction_range':[min(m['height_fraction'] for m in metrics),max(m['height_fraction'] for m in metrics)],'front_angle_range':[min(m['front_angle_degrees'] for m in metrics),max(m['front_angle_degrees'] for m in metrics)],'top_min':min(m['top_uv'][1] for m in metrics),'bottom_max':max(m['bottom_uv'][1] for m in metrics),'collisions_blockout':collision,'limits':'Schematic geometry, approximate human; not real gait, identity or video-engine trajectory verification. Visual review pending.'}
    (HERE/'geometry_check.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
