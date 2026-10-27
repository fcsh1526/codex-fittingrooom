"""One clean, shared-site layout reference for the environment master candidate."""
from pathlib import Path
import importlib.util
import hashlib
import json
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
src=BASE/'static_key_views_2026-10-16/build_key_views.py'
spec=importlib.util.spec_from_file_location('site_keys_for_environment',src)
keys=importlib.util.module_from_spec(spec);spec.loader.exec_module(keys)
root=next(p for p in HERE.parents if (p/'10_automation').is_dir())
for name in ['M03_start_v3_face.png','M03_start_v3_full.png']:
    assert (root/'02_brand/reference_models'/name).is_file(),name
film=BASE/'accepted_keys_previs_2026-10-16/accepted_keys_five_outfits_animatic.mp4'
assert hashlib.sha256(film.read_bytes()).hexdigest()=='b10d8df45560165aec160a45588677a45dd24ac198aeb9f0f64212c8ebcb07a0'

w=keys.KeyWorld(keys.VIEWS[0])
w.w,w.h=1536,864
w.im=keys.Image.new('RGB',(w.w,w.h),keys.art.PAPER);w.d=keys.ImageDraw.Draw(w.im)
w.c=np.array([-24.0,-26.0]);w.aim=np.array([6.0,3.0])
w.fwd=w.aim-w.c;w.fwd/=np.linalg.norm(w.fwd)
w.right=np.array([w.fwd[1],-w.fwd[0]])
w.focal=1536*50/36
w.eye_height=15.0;w.horizon=.50
camera3=np.array([w.c[0],w.eye_height,w.c[1]])
target3=np.array([6.0,.5,3.0])
forward3=target3-camera3;forward3/=np.linalg.norm(forward3)
right3=np.cross(np.array([0.,1.,0.]),forward3);right3/=np.linalg.norm(right3)
up3=np.cross(forward3,right3)
def elevated_project(point):
    vec=np.array(point)-camera3;depth=float(np.dot(vec,forward3))
    if depth<=.15:return None
    return(w.w*.5+float(np.dot(vec,right3))*w.focal/depth,
           w.h*.5-float(np.dot(vec,up3))*w.focal/depth,depth)
w.project=elevated_project
w.geometry()
# Geometry only: prevent schematic passers from becoming new scene contents.
w.draw_geometry=lambda:None
ordered=sorted(w.faces,key=lambda f:np.mean([np.dot(np.array([p[0],p[2]])-w.c,w.fwd) for p in f[0]]),reverse=True)
for pts,fill,outline in ordered:
    clipped=w.clip_near(pts,w.c,w.fwd)
    pp=[w.project(p) for p in clipped]
    if len(pp)>2:
        xy=[(max(-5000,min(5000,p[0])),max(-5000,min(5000,p[1]))) for p in pp]
        w.d.polygon(xy,fill=fill);w.d.line(xy+[xy[0]],fill=outline,width=1)
for pts,color,width in w.lines:
    for a,b in zip(pts,pts[1:]):
        pa,pb=w.project(a),w.project(b)
        if pa and pb:w.d.line((pa[0],pa[1],pb[0],pb[1]),fill=color,width=width)
# Coplanar road markings need explicit final ground-layer order.
for z in np.arange(2.65,5.3,.46):
    points=[(11.35,.012,float(z)),(13.7,.012,float(z)),(13.7,.012,float(z+.23)),(11.35,.012,float(z+.23))]
    pp=[w.project(p) for p in points]
    w.d.polygon([p[:2] for p in pp],fill='#faf9f3')
folder=HERE/'environment';folder.mkdir(parents=True,exist_ok=True)
path=folder/'E00_layout_reference.png';w.im.save(path)
record={'date':'2026-10-19','role':'shared_site_geometry_reference_only','file':str(path),'pixels':[w.w,w.h],
        'camera_position':camera3.tolist(),'camera_target':target3.tolist(),'eye_height':w.eye_height,
        'elevated_view_for_auxiliary_site_design_only':True,
        'not_a_reel_start_image':True,'not_a_new_model_identity':True,
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'planned_generated_asset':'one no-person photoreal environment master candidate, subject to visual review'}
(folder/'layout_reference_receipt.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
