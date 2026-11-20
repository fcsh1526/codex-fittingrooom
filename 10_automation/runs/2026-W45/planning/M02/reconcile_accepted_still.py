"""Schematic framing check for the accepted closer image, not motion certification."""
import hashlib
import json
import math
import runpy
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[5]
RUN=ROOT/'10_automation/runs/2026-W45'
OUT=RUN/'reels/M02/trial_01'
OUT.mkdir(parents=True,exist_ok=True)
base=runpy.run_path(str(RUN/'planning/build_w45_plan.py'))
font=base['font'];stage=base['stage'];look=base['LOOKS'][2]
source=RUN/'generated_images/2026-W45-002/looks/2026-W45-002-L01/reel/2026-W45-002-L01_M02_reel_candidate_A.png'
height=1.68;focal=1.416666666666667
h0=(1566-205)/1672;cy0=(1566+205)/2/1672;cx0=.642
z0=height*focal/h0;pv=.338;camera_y=height/2+(cy0-pv)*z0/focal
x0=(cx0-.5)*z0*(9/16)/focal

def position(t):
    u=max(0,min(1,(t-1.5)/1.0))
    return [x0+(.09-x0)*u,0,z0-.07*u]

def projection(p):
    x,_,z=p;h=height*focal/z;v=pv+(camera_y-height/2)*focal/z
    return dict(center_uv=[.5+x*focal/z/(9/16),v],height_fraction=h,top=v-h/2,bottom=v+h/2)

times=[0,1.5,2.5,6]
space=dict(id='W45_M02_accepted_closer_v3',units='schematic',unit_note='Unmeasured relative units; manually calibrated frame bounds only, not physical lens/anatomy/gait calibration.',axes='x_right_y_up_z_forward',source_still_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),source_manual_bounds=dict(top_px=205,bottom_px=1566,image_height=1672,center_x_fraction=cx0),camera=dict(position=[0,camera_y,0],target=[0,camera_y,4],normalized_focal=focal,principal_uv=[.5,pv],fixed=True),geometry=dict(wall_z=4.4,pavement_extent=[-2,2,2.5,4.4]),route_function=dict(start_seconds=1.5,move_seconds=1,x_start=x0,x_end=.09,z_start=z0,z_travel=.07),key_views=[dict(seconds=t,position=position(t),projection=projection(position(t))) for t in times],performance='Recognizes waiting friend, opens free right arm in welcome, one small relaxed step toward friend, settles and laughs warmly; no continuous walk.',limits='Approval covers exact still and disclosed reduced-approach intent. This schematic is an operator reconciliation, not a separate user-watched previs or proof Grok follows coordinates.')
(OUT/'adapted_space.json').write_text(json.dumps(space,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
im=Image.new('RGB',(1920,1440),'#fbfaf6');d=ImageDraw.Draw(im)
for i,t in enumerate(times):
    ox=(i%2)*960;oy=(i//2)*720
    d.text((ox+24,oy+18),f'M02｜{t:g}s｜固定鏡頭，小步會合',font=font(28),fill='#233b41')
    p=position(t);v=projection(p)
    def top(q):return (ox+220+q[0]*190,oy+590-q[2]*135)
    wall=[top([-1.2,0,4.4]),top([1.2,0,4.4])];d.line(wall,fill='#7d898a',width=5)
    d.line([top(position(1.5)),top(position(2.5))],fill='#b7c3b6',width=7)
    cam=top([0,0,0]);now=top(p)
    d.line([cam,top([0,0,4.4])],fill='#b2babc',width=2)
    d.rectangle((cam[0]-12,cam[1]-8,cam[0]+12,cam[1]+8),fill='#334e5a')
    d.ellipse((now[0]-10,now[1]-10,now[0]+10,now[1]+10),fill='#b13a36')
    wall_v=pv+camera_y*focal/4.4
    stage(d,(ox+535,oy+85,315,560),look,2 if 0<t<=1.5 else 0,v['height_fraction'],v['center_uv'][0],v['top'],wall_floor_v=wall_v)
    d.text((ox+24,oy+630),'俯視與相機構圖共用同一資料；未模擬步態',font=font(19),fill='#405255')
    d.text((ox+510,oy+665),f"人物 {v['height_fraction']:.1%}；鞋底 {v['bottom']:.1%}",font=font(21),fill='#8e4c32')
im.save(OUT/'adapted_previs_contact.png')
assert all(0<v['projection']['top'] and v['projection']['bottom']<.97 for v in space['key_views'])
print(json.dumps(dict(source_height_fraction=h0,end_height_fraction=projection(position(6))['height_fraction'],end_bottom=projection(position(6))['bottom'],fixed_camera=True,shot_seconds=6,scope='schematic bounds only')))
