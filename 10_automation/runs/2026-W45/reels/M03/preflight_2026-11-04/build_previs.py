"""One clock/space for stationary subject and a straight camera approach; schematic only."""
from pathlib import Path
import json,math,runpy,sys
from PIL import Image,ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5]
base=runpy.run_path(str(ROOT/'10_automation/runs/2026-W45/planning/build_w45_plan.py'))
font=base['font'];stage=base['stage'];look=[x for x in base['LOOKS'] if x['model']=='M03'][1]
H=1.68;focal=1.53125;z=3.5;pv=.338;h0=(1467-238)/1672;top0=238/1672;cx=.528
# Reconcile focal to the accepted source bounds at the arbitrary initial distance.
focal=h0*z/H;cy0=H/2+(top0+h0/2-pv)*z/focal
h1=1.42;top1=.08;dist1=H*focal/h1;cy1=H/2+(top1+h1/2-pv)*dist1/focal
person_x=(cx-.5)*z*(9/16)/focal;cam_x1=person_x-(cx-.5)*dist1*(9/16)/focal
def sample(t):
    u=max(0,min(1,(t-3.25)/2));u=u*u*(3-2*u)
    cam=[cam_x1*u,cy0+(cy1-cy0)*u,(z-dist1)*u]
    d=z-cam[2];hh=H*focal/d;vv=pv+(cam[1]-H/2)*focal/d
    return {'seconds':t,'camera_position':cam,'character_position':[person_x,0,z],'projection':{'height_fraction':hh,'top':vv-hh/2,'bottom':vv+hh/2,'center_uv':[.5+(person_x-cam[0])*focal/d/(9/16),vv]}}
times=[0,3.25,4.25,5.25,7.25]
space={'date':'2026-11-04','units':'unmeasured_relative_units','unit_note':'A simple projection illustration calibrated to source image bounds, not surveyed office geometry or exact Grok controls.','subject_height_assumption':H,'camera_focal_normalized':focal,'principal_uv':[.5,pv],'character_route':'stationary; no walk','camera_route':'one straight forward/slightly upward approach, eased over source3.25-5.25s; level optical axis, no orbit or zoom','fixed_scene':{'right_wall_x':1.0,'bench_x':.7,'bench_z_range':[2.5,5.0],'rear_wall_z':5.5},'key_views':[sample(t) for t in times],'limits':'No gait, expression or generated-identity simulation. Target final medium deliberately omits lower legs; not foot-contact certification.'}
(HERE/'shared_space.json').write_text(json.dumps(space,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def render(t):
    s=sample(t);v=s['projection'];cam=s['camera_position'];im=Image.new('RGB',(380,930),'#f8f7f2');d=ImageDraw.Draw(im)
    d.text((12,12),f"L02 {t:g}s｜全片 {t+3.25:g}s",font=font(21),fill='#263d49')
    frame=Image.new('RGB',(315,560),'#e9e8e1');floor=pv+cam[1]*focal/(5.5-cam[2]);stage(ImageDraw.Draw(frame),(0,0,314,559),look,0,v['height_fraction'],v['center_uv'][0],v['top'],wall_floor_v=floor);im.paste(frame,(30,65))
    d.text((12,642),f"人物 {v['height_fraction']:.1%}；頭頂 {v['top']:.1%}",font=font(19),fill='#7c583e')
    d.text((12,675),'同一人物不走動；相機視角↑',font=font(19),fill='#3e5963')
    def overhead(x,zz):return (155+x*100,895-zz*29)
    d.line([overhead(1,0),overhead(1,6)],fill='#8d989c',width=3)
    d.line([overhead(.7,2.5),overhead(.7,5)],fill='#8a6850',width=7)
    d.line([overhead(0,0),overhead(cam_x1,z-dist1)],fill='#8fa7b2',width=5)
    pc=overhead(person_x,z);cc=overhead(cam[0],cam[2]);d.ellipse((pc[0]-6,pc[1]-6,pc[0]+6,pc[1]+6),fill='#ae5b46');d.rectangle((cc[0]-9,cc[1]-5,cc[0]+9,cc[1]+5),fill='#31566b');d.line((cc,pc),fill='#a5b7bf',width=2)
    d.text((12,905),'俯視／畫框共用同一時鐘與座標',font=font(17),fill='#49616a');return im
contact=Image.new('RGB',(380*5,930),'#f8f7f2')
for i,t in enumerate(times):contact.paste(render(t),(i*380,0))
contact.save(HERE/'push_in_previs_contact.png')
frames=[render(i/8) for i in range(59)];frames[0].save(HERE/'push_in_previs.gif',save_all=True,append_images=frames[1:],duration=125,loop=0)
assert abs(sample(0)['projection']['height_fraction']-h0)<1e-9
assert all(sample(t)['projection']['top']>=.0799 for t in [i/20 for i in range(146)])
print(json.dumps({'start_height':h0,'end_height':h1,'camera_start':sample(0)['camera_position'],'camera_end':sample(7.25)['camera_position'],'head_safe_schematic':True,'exact_engine_control':False}))
