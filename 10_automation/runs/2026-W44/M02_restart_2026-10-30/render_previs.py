import math,json
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).parent
def norm(v):
 s=sum(x*x for x in v)**.5;return [x/s for x in v]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
raw=[(.46*math.sin(2*math.pi*i/1000),3*i/1000) for i in range(1001)]
length=[0]
for a,b in zip(raw,raw[1:]):length.append(length[-1]+math.dist(a,b))
def pos(s):
 goal=s*length[-1];i=next((i for i,x in enumerate(length) if x>=goal),1000);return raw[i]
def state(t):
 s=max(0,min(1,(t-1.5)/8.5));x,z=pos(s)
 c=[1.2+.3*math.sin(math.pi*s),1.1,2.8+2.7*s]
 return [x,0,z],c,[x,.88,z],s
def project(p,c,target):
 f=norm(sub(target,c));right=norm(cross(f,[0,1,0]));up=cross(right,f);v=sub(p,c);depth=dot(v,f)
 if depth<=.05:return None
 fy=470/(2*math.tan(math.radians(40)/2));return (455+dot(v,right)*fy/depth,290-dot(v,up)*fy/depth)
def overhead(p):return (100+p[0]*55,430-p[2]*65)
def render(t):
 im=Image.new('RGB',(660,560),'#f4f1ea');d=ImageDraw.Draw(im);p,c,target,s=state(t)
 d.text((18,15),f'M02 NEW PLAN | {t:04.1f}s | schematic, not generated footage',fill='black')
 d.text((18,45),'TOP: separate character / camera routes',fill='black')
 for route,col in [( [([x,0,z]) for x,z in raw[::10]],'#be496a'),([state(1.5+8.5*i/100)[1] for i in range(101)],'#287d94')]:
  pts=[overhead(v) for v in route];d.line(pts,fill=col,width=3)
 pp=overhead(p);cc=overhead(c);d.line([pp,cc],fill='#999999',width=1)
 for q,col in [(pp,'#be496a'),(cc,'#287d94')]:d.ellipse((q[0]-5,q[1]-5,q[0]+5,q[1]+5),fill=col)
 d.text((18,495),'pink: model / blue: camera',fill='black')
 base=im.copy()
 d.rectangle((320,55,590,535),fill='#e7e8df',outline='black',width=2)
 for z in [-1,0,1,2,3,4,5]:
  pts=[project([x,0,z],c,target) for x in [-3,3]]
  if all(pts):d.line(pts,fill='#bdbdb4',width=1)
 for x in [-2,-1,0,1,2]:
  pts=[project([x,0,z],c,target) for z in [-1,5]]
  if all(pts):d.line(pts,fill='#bdbdb4',width=1)
 phase=2*math.pi*1.65*max(0,t-1.5);swing=.16*math.sin(phase) if 1.5<t<10 else 0
 pts={k:project([p[0]+x,y,p[2]+z],c,target) for k,(x,y,z) in {'head':(0,1.6,0),'neck':(0,1.42,0),'hip':(0,.85,0),'ls':(-.2,1.35,0),'rs':(.2,1.35,0),'lh':(-.34,1.05,swing),'rh':(.34,1.05,-swing),'lf':(-.1,0,swing),'rf':(.1,0,-swing)}.items()}
 colour='#753997' if t<6 else '#21334d'
 d.polygon([pts['ls'],pts['rs'],(pts['hip'][0]+16,pts['hip'][1]),(pts['hip'][0]-16,pts['hip'][1])],fill=colour)
 for a,b in [('neck','hip'),('ls','lh'),('rs','rh'),('hip','lf'),('hip','rf')]:d.line([pts[a],pts[b]],fill=colour,width=7)
 q=pts['head'];d.ellipse((q[0]-12,q[1]-17,q[0]+12,q[1]+17),fill='#c58d70')
 top=project([p[0],1.72,p[2]],c,target);bottom=project([p[0],0,p[2]],c,target)
 ratio=(bottom[1]-top[1])/480
 d.text((330,65),f'CAMERA: body height {ratio:.0%}',fill='black')
 action='recognise friend / smile' if t<1.5 else ('curved approach / eye contact' if t<10 else 'settle / turn shoulder')
 d.text((330,515),action,fill='black')
 base.paste(im.crop((320,55,591,536)),(320,55))
 return base,{'t':t,'person':p,'camera':c,'target':target,'height_fraction':ratio,'travel_s':s}
frames=[];samples=[]
for i in range(97):
 im,s=render(i/8);frames.append(im);samples.append(s)
frames[0].save(R/'shared_route_previs.gif',save_all=True,append_images=frames[1:],duration=125,loop=0)
sheet=Image.new('RGB',(1320,1120),'white')
for j,i in enumerate([0,24,48,80]):sheet.paste(frames[i],((j%2)*660,(j//2)*560))
sheet.save(R/'storyboard_and_routes.png')
(R/'shared_space_samples.json').write_text(json.dumps({'units':'schematic_unmeasured','projection':'40 degree vertical pinhole, common scene and clock','note':'limbs simplified; not a gait or engine-control validation','samples':samples},indent=2),encoding='utf-8')
print('Rendered common-data overhead/camera previs, 12 seconds.')
