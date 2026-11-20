"""Planning-only shared-space projection. No AI image/video generation."""
from pathlib import Path
import json,math,hashlib,copy
from PIL import Image,ImageDraw,ImageFont,ImageColor
import numpy as np
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent
OUT=RUN/'editorial_reset_v3_2026-10-28';OUT.mkdir(exist_ok=True)
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(R).as_posix()
def mix(a,b,t):return [x*(1-t)+y*t for x,y in zip(a,b)]
def bez(pts,t):return [sum(p[j]*w for p,w in zip(pts,[(1-t)**3,3*(1-t)**2*t,3*(1-t)*t*t,t**3])) for j in range(3)]
def tangent(pts,t):return [3*((1-t)**2*(pts[1][j]-pts[0][j])+2*(1-t)*t*(pts[2][j]-pts[1][j])+t*t*(pts[3][j]-pts[2][j])) for j in range(3)]
def norm(v):m=math.sqrt(sum(x*x for x in v));return [x/m for x in v]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
PC=[[0,0,0],[0,0,5],[.5,0,10],[5,0,12]]
CC=[[2.1,1.1,3.0],[5.4,1.1,4.0],[3.8,1.1,12.5],[6,1.1,14.2]]
# Reparameterize the person by arc length. Camera retains its independent time curve.
arc=[0.0];dense=[bez(PC,k/2000) for k in range(2001)]
for a,b in zip(dense,dense[1:]):arc.append(arc[-1]+math.dist(a,b))
def u_for(t):
 import bisect
 s=t*arc[-1];i=min(2000,max(1,bisect.bisect_left(arc,s)));return (i-1+(s-arc[i-1])/(arc[i]-arc[i-1]))/2000
def at(frame):
 t=frame/384;u=u_for(t);p=bez(PC,u);camera_u=t+.35*math.sin(math.pi*t)/math.pi;c=bez(CC,camera_u)
 # The final approach is a planned continuous knee/upper-thigh shot, not a post crop.
 close=max(0,min(1,(t-.84)/.16));vfov=40;cytarget=1.1+.1*close
 base=norm([p[0]-c[0],0,p[2]-c[2]]);right=[-base[2],0,base[0]]
 desired=.46+.085*math.sin(2*math.pi*t-.3)
 delta=math.atan((.5-desired)*2*math.tan(math.radians(vfov)/2)*9/16)
 f=[base[0]*math.cos(delta)+right[0]*math.sin(delta),0,base[2]*math.cos(delta)+right[2]*math.sin(delta)]
 distance=math.dist(p,[c[0],0,c[2]])
 target=[c[0]+f[0]*distance,cytarget,c[2]+f[2]*distance]
 forward=norm([target[i]-c[i] for i in range(3)]);rv=norm(cross(forward,[0,1,0]));up=cross(rv,forward)
 tan=math.tan(math.radians(vfov)/2);heading=math.degrees(math.atan2(*[tangent(PC,u)[j] for j in [0,2]]))
 return {'frame':frame,'p':p,'c':c,'target':target,'heading':heading,'forward':forward,'right':rv,'up':up,'tan':tan,'vfov':vfov,'u':u}
def project(v,a):
 d=[v[i]-a['c'][i] for i in range(3)];z=dot(d,a['forward'])
 if z<.06:return None
 return [.5+dot(d,a['right'])/(2*z*a['tan']*9/16),.5-dot(d,a['up'])/(2*z*a['tan'])]
def clip(poly,a):
 result=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  z1=dot([p[i]-a['c'][i] for i in range(3)],a['forward']);z2=dot([q[i]-a['c'][i] for i in range(3)],a['forward']);i1=z1>=.061;i2=z2>=.061
  if i1:result.append(p)
  if i1!=i2:result.append(mix(p,q,(.061-z1)/(z2-z1)))
 return result
geometry=[]
def face(id,vs,color,edge='#9da4a2'):geometry.append({'id':id,'vertices':vs,'fill':color,'edge':edge})
def box(id,x,y,z,w,h,d,col):
 v=[[x+sx*w/2,y+sy*h,z+sz*d/2] for sy in [0,1] for sx,sz in [(-1,-1),(1,-1),(1,1),(-1,1)]]
 for k,inds in enumerate([[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7],[4,5,6,7]]):face(id+f'_{k}',[v[i] for i in inds],col)
face('wall',[[-2,0,-3],[-2,3,-3],[-2,3,7.2],[-2,0,7.2]],'#e4e0d7')
for z in [-1.5,1.2,4.4]:face('window_'+str(z),[[-1.98,.5,z],[-1.98,2.5,z],[-1.98,2.5,z+1.7],[-1.98,.5,z+1.7]],'#c9d9dc')
face('canopy',[[-2,2.85,-3],[3.8,2.85,-3],[3.8,2.85,8.9],[-2,2.85,8.9]],'#e9e5db')
anchor=at(189);col=mix(anchor['p'],anchor['c'],.52);pillar=[col[0],0,col[2]]
box('reveal_column',pillar[0],0,pillar[2],.23,2.85,.23,'#ddd7c9')
box('bench',-1.0,.42,9.6,.65,.12,2.0,'#c8aa82')
box('planter',-1.5,0,12.1,1,.6,1.1,'#b6c8a4')
face('plaza_edge',[[-2,0,8.9],[7,0,8.9],[7,.1,9],[-2,.1,9]],'#c8c7bd')
def avatar(a,look):
 p=a['p'];h=math.radians(a['heading']);right=[math.cos(h),0,-math.sin(h)];front=[math.sin(h),0,math.cos(h)]
 phase=a['frame']/24*2*math.pi*1.6;bounce=.008*math.cos(2*phase)
 def world(x,y,z=0):return [p[0]+right[0]*x+front[0]*z,y+bounce,p[2]+right[2]*x+front[2]*z]
 shapes=[]
 def f(name,pts,col):shapes.append({'id':name,'vertices':[world(*q) for q in pts],'fill':col,'edge':'#35404a'})
 def cuboid(name,x,y,z,w,h,d,col):
  v=[(x+sx*w/2,y+sy*h,z+sz*d/2) for sy in [0,1] for sx,sz in [(-1,-1),(1,-1),(1,1),(-1,1)]]
  for k,ii in enumerate([[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7],[4,5,6,7]]):f(name+str(k),[v[i] for i in ii],col)
 def limb(name,x,y0,y1,z0,z1,w,color):
  f(name,[(x-w/2,y0,z0),(x+w/2,y0,z0),(x+w/2,y1,z1),(x-w/2,y1,z1)],color)
 cuboid('torso',0,.91,0,.43,.48,.21,'#7d55aa' if look==1 else '#faf8ee')
 if look==1:
  f('white_tee',[(-.11,.94,.111),(.11,.94,.111),(.09,1.37,.111),(-.09,1.37,.111)],'#fbfaf3')
  cuboid('leg_left',-.105,.08,-.10*math.sin(phase),.16,.83,.17,'#59616c');cuboid('leg_right',.105,.08,.10*math.sin(phase),.16,.83,.17,'#59616c')
 else:
  # Whole navy dress is a new silhouette; the white sleeves remain above its straps.
  cuboid('dress',0,.46,0,.46,.76,.25,'#253d59')
  f('dress_front',[(-.2,1.22,.14),(0,1.15,.14),(.2,1.22,.14),(.23,.46,.14),(-.23,.46,.14)],'#253d59')
  for xx in [-.15,.15]:f('strap',[(xx-.016,1.21,.14),(xx+.016,1.21,.14),(xx+.016,1.38,.12),(xx-.016,1.38,.12)],'#253d59')
  limb('calf_left',-.105,.46,.07,0,-.10*math.sin(phase),.1,'#dac0a6');limb('calf_right',.105,.46,.07,0,.10*math.sin(phase),.1,'#dac0a6')
 for xx,zz in [(-.105,-.10*math.sin(phase)),(.105,.10*math.sin(phase))]:cuboid('shoe',xx,.025,zz+.03,.16,.07,.3,'#eeefeb')
 for xx,zz in [(-.27,.06*math.sin(phase)),(.27,-.06*math.sin(phase))]:limb('arm',xx,1.36,.84,0,zz,.085,'#7d55aa' if look==1 else '#f7f6ee')
 cuboid('bag',.32,.75,0,.2,.23,.12,'#35383b' if look==1 else '#756047')
 # Head as an eight-sided schematic form, with a face marker in the real heading direction.
 cuboid('head',0,1.43,0,.20,.22,.19,'#ead2b8')
 f('face_marker',[(-.018,1.50,.106),(.018,1.50,.106),(.018,1.58,.106),(-.018,1.58,.106)],'#67584b')
 return shapes
def camera(frame,look,width=270):
 a=at(frame);height=round(width*16/9)
 pixels=np.full((height,width,3),ImageColor.getrgb('#f7f5ee'),dtype=np.uint8);depth=np.full((height,width),np.inf)
 shapes=geometry+avatar(a,look)
 for z in range(-2,20,2):shapes.append({'id':'ground','vertices':[[-3,0,z],[8,0,z],[8,0,z+.025],[-3,0,z+.025]],'fill':'#c8cbc5','edge':None})
 for s in shapes:
  verts=clip(s['vertices'],a)
  if len(verts)<3:continue
  ps=[project(v,a) for v in verts]
  if any(q is None for q in ps):continue
  pts=[(q[0]*width,q[1]*height) for q in ps]
  zs=[dot([v[i]-a['c'][i] for i in range(3)],a['forward']) for v in verts]
  # Per-pixel perspective-correct depth: a long wall cannot hide a nearer person
  # merely because the polygon's average depth is small.
  for i in range(1,len(pts)-1):
   ii=[0,i,i+1];tri=[pts[k] for k in ii];zz=[zs[k] for k in ii]
   x0=max(0,int(math.floor(min(v[0] for v in tri))));x1=min(width-1,int(math.ceil(max(v[0] for v in tri))))
   y0=max(0,int(math.floor(min(v[1] for v in tri))));y1=min(height-1,int(math.ceil(max(v[1] for v in tri))))
   if x0>x1 or y0>y1:continue
   (ax,ay),(bx,by),(cx,cy)=tri;den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
   if abs(den)<1e-9:continue
   Y,X=np.mgrid[y0:y1+1,x0:x1+1];X=X+.5;Y=Y+.5
   w0=((by-cy)*(X-cx)+(cx-bx)*(Y-cy))/den;w1=((cy-ay)*(X-cx)+(ax-cx)*(Y-cy))/den;w2=1-w0-w1
   inside=(w0>=-1e-8)&(w1>=-1e-8)&(w2>=-1e-8)
   inv=w0/zz[0]+w1/zz[1]+w2/zz[2]
   z=np.divide(1,inv,out=np.full_like(inv,np.inf),where=inv>0)
   region=depth[y0:y1+1,x0:x1+1];mask=inside&(z<region);region[mask]=z[mask]
   rgb=pixels[y0:y1+1,x0:x1+1];rgb[mask]=ImageColor.getrgb(s['fill'])
  if s['edge']:
   for i in range(len(pts)):
    j=(i+1)%len(pts);aa,bb=pts[i],pts[j];n=min(2500,max(2,int(math.dist(aa,bb))+1));u=np.linspace(0,1,n)
    xx=np.rint(aa[0]+u*(bb[0]-aa[0])).astype(int);yy=np.rint(aa[1]+u*(bb[1]-aa[1])).astype(int)
    good=(xx>=0)&(xx<width)&(yy>=0)&(yy<height);xx=xx[good];yy=yy[good];uu=u[good]
    dz=1/((1-uu)/zs[i]+uu/zs[j]);good=dz<=depth[yy,xx]+.025;pixels[yy[good],xx[good]]=ImageColor.getrgb(s['edge'])
 return Image.fromarray(pixels)
def view(frame,width=270):
 if frame<180:return camera(frame,1,width)
 if frame>=198:return camera(frame,2,width)
 return Image.blend(camera(frame,1,width),camera(frame,2,width),(frame-180)/18)
def overhead(frame,size=(350,480)):
 a=at(frame);im=Image.new('RGB',size,'#f7f5ee');d=ImageDraw.Draw(im)
 def xy(p):return (size[0]*(p[0]+3)/11,size[1]*(18-p[2])/22)
 # Ground footprints use the same fixed source geometry.
 for s in geometry:
  if 'column' in s['id'] or s['id'] in ['wall','bench_4','planter_4']:
   ps=[xy(v) for v in s['vertices']];d.line(ps+[ps[0]],fill='#a4aaa3',width=1)
 d.line([xy(at(k)['p']) for k in range(385)],fill='#b76f46',width=3)
 d.line([xy(at(k)['c']) for k in range(385)],fill='#2c7e92',width=3)
 pp,cc=xy(a['p']),xy(a['c']);d.line([pp,cc],fill='#9da5a6',width=1)
 d.ellipse([pp[0]-5,pp[1]-5,pp[0]+5,pp[1]+5],fill='#b76f46');d.rectangle([cc[0]-5,cc[1]-5,cc[0]+5,cc[1]+5],fill='#2c7e92')
 return im
F='C:/Windows/Fonts/msjh.ttc'
def txt(d,xy,s,n=17):d.text(xy,s,font=ImageFont.truetype(F,n),fill='#293944')
samples=[]
for f in range(385):
 a=at(f);p=a['p'];head=project([p[0],1.65,p[2]],a);foot=project(p,a);waist=project([p[0],.95,p[2]],a)
 angle=math.degrees(math.atan2(a['c'][0]-p[0],a['c'][2]-p[2]))-a['heading'];angle=(angle+180)%360-180
 samples.append({'frame':f,'character_position':p,'heading_degrees':a['heading'],'camera_position':a['c'],'target':a['target'],'vertical_fov_degrees':a['vfov'],'person_center_uv':[(head[0]+foot[0])/2,(head[1]+foot[1])/2],'person_height_fraction':foot[1]-head[1],'head_uv':head,'feet_uv':foot,'waist_uv':waist,'relative_camera_angle_degrees':angle})
space={'id':'W44_editorial_reset_v3_shared_world','units':'schematic','unit_note':'Unmeasured fictional schematic units; no calibrated photoreal scene or real camera control claimed.','axes':'x_right_y_up_z_forward','geometry':geometry,'curve_controls':{'character':PC,'camera':CC},'timing':'person arc-length progression; camera independent cubic time curve; no per-look ease/reset','routes':[],'clock':{'fps':24,'frame_count':384}}
for sid,bounds in [('S01',[0,198]),('S02',[180,384])]:
 ts=[bounds[0],sum(bounds)//2,bounds[1]];r={'shot_id':sid,'character_samples':[],'camera_samples':[],'projected_samples':[]}
 for f in ts:
  a=samples[f];r['character_samples'].append({'frame':f,'position':a['character_position'],'heading_degrees':a['heading_degrees'],'gait_phase':'diagram sine phase only; physical gait unvalidated'})
  r['camera_samples'].append({'frame':f,'position':a['camera_position'],'target':a['target'],'vertical_fov_degrees':a['vertical_fov_degrees']})
  r['projected_samples'].append({'frame':f,'person_center_uv':a['person_center_uv'],'person_height_fraction':a['person_height_fraction'],'visible_landmark_ids':[],'visible_clothing':'planned full outfit then intentional closer closing view; actual bounds in projection_samples.json'})
 space['routes'].append(r)
dump(OUT/'shared_space.json',space);dump(OUT/'projection_samples.json',samples)
space['motion_parameters']={'character_parameter':'normalized arc length of cubic curve, lookup2000 samples over16s','camera_curve_parameter':'t + 0.35*sin(pi*t)/pi, t=global_frame/384','aim_horizontal_target':'0.46 + 0.085*sin(2*pi*t-0.3)','camera_target_height':'1.1 + 0.1*clamp((t-0.84)/0.16,0,1)','vertical_fov_degrees':40,'schematic_person_height':1.65,'projected_samples_file':'projection_samples.json','projected_samples_sha256':sha(OUT/'projection_samples.json')}
dump(OUT/'shared_space.json',space)
timed=[]
for f in range(0,384,3):
 im=Image.new('RGB',(660,560),'#eee9df');im.paste(overhead(f),(10,42));im.paste(view(f),(380,42));d=ImageDraw.Draw(im)
 txt(d,(12,8),f"MIRA v3 · {f/24:05.2f}s · "+('紫外搭褲裝' if f<180 else '0.75秒換裝窗口' if f<198 else '白T內搭深藍洋裝'))
 txt(d,(12,530),'共同場地／時鐘／投影；示意動作，非生成影片或物理驗證',15);timed.append(im)
timed[0].save(OUT/'shared_route_previs_16s.gif',save_all=True,append_images=timed[1:],duration=[120,130]*64,loop=0)
keys=[(0,'斜前方完整褲裝'),(72,'逐漸側向，讀褲線'),(144,'近柱，開闊處出現'),(180,'換裝窗口開始'),(198,'換裝窗口結束'),(240,'展開洋裝輪廓'),(312,'仍有完整裙長'),(384,'靠近讀白T與肩帶')]
board=Image.new('RGB',(1600,1160),'#f3efe6');d=ImageDraw.Draw(board);txt(d,(35,20),'MIRA W44 · 整片改案 v3（待審）',30)
for k,(f,label) in enumerate(keys):
 x=35+(k%4)*393;y=80+(k//4)*530
 img=view(f,255);board.paste(img,(x+48,y))
 d=ImageDraw.Draw(board);txt(d,(x,y+462),f'{f/24:.2f}s · {label}',17)
board.save(OUT/'connected_storyboard_v3.png')
for f in [0,144,180,189,198,240,312,384]:view(f,540).save(OUT/f'camera_f{f:03}.png')
stats={'horizontal_center_range':[min(s['person_center_uv'][0] for s in samples),max(s['person_center_uv'][0] for s in samples)],'height_fraction_range':[min(s['person_height_fraction'] for s in samples),max(s['person_height_fraction'] for s in samples)],'relative_camera_angle_range':[min(s['relative_camera_angle_degrees'] for s in samples),max(s['relative_camera_angle_degrees'] for s in samples)],'head_in_frame_all':all(0<=s['head_uv'][0]<=1 and 0<=s['head_uv'][1]<=1 for s in samples),'feet_in_frame_until_13s':all(0<=s['feet_uv'][1]<=1 for s in samples[:313]),'shared_clock_frames':384,'preview_frames':128,'preview_fps':8,'duration_seconds':16,'limits':'Projection checks only. No physical gait, exact AI adherence, comfortable dissolve or full continuous human playback certification.'}
dump(OUT/'projection_checks.json',stats)
print(json.dumps(stats))
