"""Render three direct9:16 camera guides from the accepted fixed-projection plan.

Deterministic position/ground markers only: no photo edits, raster cropping,
AI calls, video generation or embedded lettering. Existing files are protected.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
SIZE=(720,1280)
PAPER='#faf9f5';INK='#a44d30';SOFT='#b5bdb4'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def project(point,frame):
    x,y,z=point;dx=x-frame['camera'][0];dz=z-frame['camera'][1]
    fx,fz=frame['forward'];depth=dx*fx+dz*fz
    if depth<=.15:return None
    return (SIZE[0]*.5+(dx*fz-dz*fx)*SIZE[1]*frame['focal']/depth,
            SIZE[1]*.42-(y-1.30)*SIZE[1]*frame['focal']/depth)


def clip(points,frame):
    out=[]
    def depth(p):return(p[0]-frame['camera'][0])*frame['forward'][0]+(p[2]-frame['camera'][1])*frame['forward'][1]-.16
    for i,b in enumerate(points):
        a=points[i-1];da,db=depth(a),depth(b)
        if(da>=0)!=(db>=0):
            t=da/(da-db);out.append(tuple(a[k]+t*(b[k]-a[k]) for k in range(3)))
        if db>=0:out.append(b)
    return out


def render(frame,data):
    image=Image.new('RGB',SIZE,PAPER);draw=ImageDraw.Draw(image)
    def polygon(points,fill,stroke=SOFT):
        points=clip(points,frame);projected=[project(p,frame) for p in points]
        if len(projected)>2 and all(p is not None for p in projected):
            pp=[(max(-6000,min(6000,p[0])),max(-6000,min(6000,p[1]))) for p in projected]
            draw.polygon(pp,fill=fill);draw.line(pp+[pp[0]],fill=stroke,width=2)
    def line(points,color=SOFT,width=2):
        pp=[project(p,frame) for p in points]
        if all(p is not None for p in pp):draw.line(pp,fill=color,width=width)
    # Same minimal facade, plane and paint as the approved three-view drawing.
    polygon([(-6,0,8.8),(20,0,8.8),(20,6.5,8.8),(-6,6.5,8.8)],'#e0e6e4')
    for x in range(6,21,2):line([(x,0,8.8),(x,6.5,8.8)],'#929f98')
    for y in[2.8,4.5,6.5]:line([(-6,y,8.8),(20,y,8.8)],'#a5afa7')
    polygon([(-6,0,2.5),(20,0,2.5),(20,0,5.4),(-6,0,5.4)],'#c7ccc7')
    for stripe in data['stripes']:polygon(stripe['points'],'#faf9f3','#92998f')
    for z in data['road_z']:line([(8,0,z),(18,0,z)],'#7e8b82',4)
    p=frame['person'];heading=frame['heading'];side=[heading[1],-heading[0]]
    def world(l,y,a=0):return[p[0]+side[0]*l+heading[0]*a,y,p[1]+side[1]*l+heading[1]*a]
    for points in[[world(0,1.48),world(0,.86),world(-.11,.06,-.1)],
                  [world(0,.86),world(.11,.06,.1)],
                  [world(-.24,1.0),world(-.18,1.36),world(.18,1.36),world(.24,1.0)]]:
        line(points,INK,8)
    head=project(world(0,1.58),frame);top=project(world(0,1.70),frame);low=project(world(0,1.48),frame)
    rx=abs(low[1]-top[1])*.33;ry=abs(low[1]-top[1])*.5
    draw.ellipse((head[0]-rx,head[1]-ry,head[0]+rx,head[1]+ry),fill=INK)
    return image


def main():
    plan=BASE/'geometry-fixed-lens-plan.json';receipt=BASE/'geometry-fixed-lens-receipt.json';board=BASE/'geometry-fixed-lens-three-views.png'
    proof=json.loads(receipt.read_text(encoding='utf-8'))
    assert sha(plan)==proof['files'][plan.name]['sha256']
    assert sha(board)==proof['files'][board.name]['sha256']
    protected={str(p):sha(p) for p in[plan,receipt,board]}
    data=json.loads(plan.read_text(encoding='utf-8'))
    assert len(data['stripes'])==6 and len({f['focal'] for f in data['frames']})==1
    outputs=[]
    for name,index in[('start',0),('mid',50),('end',100)]:
        frame=data['frames'][index];path=HERE/f'F04_camera_{name}_guide.png'
        image=render(frame,data)
        with path.open('xb') as stream:image.save(stream,format='PNG')
        with Image.open(path) as check:assert check.size==SIZE
        outputs.append({'role':name,'path':str(path),'sha256':sha(path),'pixels':list(SIZE),
                        'route_percentage':index,'source_schematic_t':frame['source_t'],
                        'camera':frame['camera'],'forward':frame['forward'],'person':frame['person'],
                        'focal_ratio':frame['focal'],'text':'none','photo_crop_or_edit':False,
                        'world_paint_vertices_sha256':hashlib.sha256(json.dumps(data['stripes'],sort_keys=True).encode()).hexdigest()})
    for path,digest in protected.items():assert sha(Path(path))==digest
    record={'created_at_taipei':datetime.now(timezone(timedelta(hours=8))).isoformat(),
            'stage':'deterministic_guides_derived_from_user_accepted_camera_plan',
            'user_acceptance_supplied_by_root':'可以，沿這個分鏡繼續',
            'acceptance_scope':'camera storyboard only; not new photoreal still or video approval',
            'protected_inputs_unchanged':protected,'outputs':outputs,
            'same_world_and_stripes_for_all_guides':True,'AI_calls':0,'Grok_calls':0,
            'normal_speed_video_QA':None,'publishable':False,
            'limits':['Direct schematic projections, not photographic calibration or50mm lens certification.',
                      'Person is only a world-position/heading marker, not body, identity, pose or wardrobe reference.',
                      'Planters/trees/material texture/background people are omitted, not determined by these guides.',
                      'Static projected edges do not guarantee motion interpolation or prevent generator paint morph.',
                      'Endpoint intentionally retains only part of final stripe; no need to invent a second crossing.']}
    with(HERE/'camera_guide_manifest.json').open('x',encoding='utf-8') as stream:json.dump(record,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print(json.dumps({'guides':[r['path'] for r in outputs],'pixels':list(SIZE),'text':'none','protected_inputs_unchanged':True},ensure_ascii=False))


if __name__=='__main__':main()
