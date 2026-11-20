"""Build the W45 editorial proposal and schematic boards. No media generation or approval."""
import copy
import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[4]
RUN = ROOT / '10_automation/runs/2026-W45'
HERE = RUN / 'planning'
DATE = '2026-11-03'
WEEK = '2026-W45'
FONT = 'C:/Windows/Fonts/msjh.ttc'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def dump(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def writecsv(p, rows, fields):
    with p.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def material_id(week, row):
    s = json.dumps([week, row], ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return 'mi_' + hashlib.sha256(s.encode()).hexdigest()[:20]

def look(mid, order, name, clothing, silhouette, sources, colors, scene, decision, proof, action):
    return dict(model=mid, order=order, name=name, clothing=clothing,
                silhouette=silhouette, sources=sources, colors=colors, scene=scene,
                decision=decision, proof=proof, action=action)

CONFIG=json.loads((HERE/'w45_editorial_config.json').read_text(encoding='utf-8'))
LOOKS=CONFIG['looks']
FILMS=CONFIG['films']

def font(size):
    return ImageFont.truetype(FONT, size)

def wrap(draw, text, size, width):
    rows=[]; line=''
    for ch in text:
        if ch=='\n': rows.append(line); line=''; continue
        if draw.textlength(line+ch, font=font(size)) > width and line:
            rows.append(line); line=ch
        else: line+=ch
    if line: rows.append(line)
    return rows

def textblock(d, xy, text, size, width, fill='#26323b', gap=7):
    x,y=xy
    for line in wrap(d,text,size,width):
        d.text((x,y),line,font=font(size),fill=fill); y+=size+gap
    return y

def person(d, box, look, hfrac=.74, cx=.5, top=.14, pose=0, detail=False):
    x,y,w,h=box
    H=h*hfrac; center=x+w*cx; headtop=y+h*top
    unit=H/7.5; shoulder=headtop+unit*1.65; waist=headtop+unit*3.3
    hips=headtop+unit*3.9; bottom=headtop+H
    ink='#2f3941'; sw=max(2,int(w/160)); torso=unit*.82
    d.ellipse((center-unit*.42,headtop,center+unit*.42,headtop+unit),outline=ink,width=sw,fill='#f4e7da')
    d.line([(center-unit*.16,headtop+unit),(center-unit*.16,shoulder),(center+unit*.16,shoulder),(center+unit*.16,headtop+unit)],fill=ink,width=sw)
    d.polygon([(center-unit*.8,shoulder),(center+unit*.8,shoulder),(center+torso,hips),(center-torso,hips)],fill=look['colors'][0],outline=ink,width=sw)
    if '格紋' in look['clothing']:
        for off in [-.6,-.3,0,.3,.6]: d.line([(center+unit*off,shoulder),(center+unit*off,hips)],fill='#77736c',width=sw)
        for j in range(5): d.line([(center-torso,shoulder+j*(hips-shoulder)/5),(center+torso,shoulder+j*(hips-shoulder)/5)],fill='#77736c',width=sw)
    if '敞開' in look['clothing'] or '西外' in look['clothing']:
        inner='#694936' if '深棕不透光背心' in look['clothing'] else '#f6f3eb'
        d.polygon([(center-unit*.22,shoulder),(center+unit*.22,shoulder),(center+unit*.36,hips),(center-unit*.36,hips)],fill=inner,outline=ink,width=sw)
    if '工裝' in look['clothing']:
        for sign in [-1,1]:
            px=center+sign*unit*.57
            d.rectangle((px-unit*.17,waist-unit*.1,px+unit*.17,waist+unit*.35),outline=ink,width=sw)
    if '花卉' in look['clothing'] and look['silhouette']=='trousers':
        for j in range(3):
            for sign in [-1,1]:
                fx=center+sign*unit*.39;fy=shoulder+unit*(.4+j*.62);rad=unit*.13
                for ax,ay in [(0,-1),(1,0),(0,1),(-1,0)]:
                    d.ellipse((fx+ax*rad*.6-rad*.65,fy+ay*rad*.6-rad*.65,fx+ax*rad*.6+rad*.65,fy+ay*rad*.6+rad*.65),fill='#ae6372',outline='#e4d9c9')
    if look['silhouette']=='trousers':
        for sign in [-1,1]:
            d.polygon([(center+sign*unit*.08,hips),(center+sign*unit*.82,hips),(center+sign*unit*.72,bottom-unit*.25),(center+sign*unit*.16,bottom-unit*.25)],fill=look['colors'][1],outline=ink,width=sw)
    else:
        wid=1.35 if look['silhouette']=='skirt' else .9
        d.polygon([(center-torso,waist),(center+torso,waist),(center+unit*wid,bottom-unit*1.15),(center-unit*wid,bottom-unit*1.15)],fill=look['colors'][1],outline=ink,width=sw)
        if '細肩帶' in look['clothing']:
            d.polygon([(center-unit*.63,shoulder+unit*.52),(center+unit*.63,shoulder+unit*.52),(center+torso,waist),(center-torso,waist)],fill=look['colors'][1],outline=ink,width=sw)
            for sign in [-1,1]: d.line([(center+sign*unit*.56,shoulder),(center+sign*unit*.56,shoulder+unit*.55)],fill=ink,width=sw)
        for sign in [-1,1]: d.line([(center+sign*unit*.38,bottom-unit*1.15),(center+sign*unit*.38,bottom-unit*.2)],fill=ink,width=sw)
    for sign in [-1,1]:
        sx=center+sign*unit*.76
        if pose==1:
            elbow=(sx+sign*unit*.7,shoulder-unit*.15); wrist=(sx+sign*unit*1.12,shoulder-unit*.65)
        elif pose==2 and sign==-1:
            elbow=(sx+sign*unit*.55,shoulder+unit*.2); wrist=(sx+sign*unit*.92,shoulder-unit*.1)
        else:
            elbow=(sx+sign*unit*.12,waist+unit*.1); wrist=(sx+sign*unit*.06,hips+unit*.42)
        d.line([(sx,shoulder),elbow,wrist],fill=ink,width=sw)
        d.ellipse((wrist[0]-unit*.1,wrist[1]-unit*.13,wrist[0]+unit*.1,wrist[1]+unit*.13),outline=ink,width=sw,fill='#f4e7da')
        d.rounded_rectangle((center+sign*unit*.39-unit*.24,bottom-unit*.22,center+sign*unit*.39+unit*.3,bottom),radius=3,fill='#e4e6e3',outline=ink,width=sw)
    bagfill=('#ad302c' if '正紅' in look['clothing'] else '#763d42' if '暗紅' in look['clothing'] else '#8b8375' if '灰褐' in look['clothing'] else '#33383c' if '黑小肩包' in look['clothing'] else '#785e4a')
    bx=center+unit*.88; by=waist+unit*.1
    d.line([(center+unit*.66,shoulder),(bx,by)],fill=ink,width=sw)
    d.rounded_rectangle((bx-unit*.32,by,bx+unit*.34,by+unit*.52),radius=5,fill=bagfill,outline=ink,width=sw)
    if '提花' in look['clothing']:
        for j in range(3): d.line([(bx-unit*.28,by+unit*(j*.13+.09)),(bx+unit*.3,by+unit*(j*.13+.09))],fill='#e7d6bc',width=sw)
    d.arc((center-unit*.2,headtop+unit*.42,center+unit*.2,headtop+unit*.77),0,180,fill=ink,width=sw)

def stage(d, box, look, pose=0, hfrac=.74, cx=.5, top=.14, parallel_look=None, wall_floor_v=None):
    x,y,w,h=box
    d.rectangle((x,y,x+w,y+h),fill='#eeece6',outline='#98a2aa',width=2)
    floor=.89 if wall_floor_v is None else wall_floor_v
    d.line([(x,y+h*floor),(x+w,y+h*floor)],fill='#b9b5ad',width=2)
    if wall_floor_v is None:
        d.line([(x+w*.08,y),(x+w*.08,y+h*floor)],fill='#d1cbc2',width=2)
    if parallel_look:
        d.line([(x+w*.5,y),(x+w*.5,y+h)],fill='#fff',width=5)
        person(d,(x,y,w*.5,h),look,hfrac,.5,top,0)
        person(d,(x+w*.5,y,w*.5,h),parallel_look,hfrac,.5,top,0)
    else: person(d,box,look,hfrac,cx,top,pose)

def render_board(film):
    mid=film['model']; ls=[l for l in LOOKS if l['model']==mid]
    p=HERE/mid; p.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGB',(1660,1280),'#fbfaf6'); d=ImageDraw.Draw(im)
    d.text((36,25),f"W45 · {mid} · {film['title']}",font=font(36),fill='#233b41')
    textblock(d,(36,85),film['purpose'],23,1580)
    specs={
      'M01':[(ls[0],0,0,'0秒｜深褲，已看見朋友'),(ls[0],1,3,'3秒｜展臂回應招呼'),(ls[1],0,5.5,'5.5秒｜淺色裙形揭露'),(ls[1],1,9,'9秒｜笑著回正')],
      'M02':[(ls[0],0,0,'0秒｜認出朋友，全身68%'),(ls[0],2,2,'2秒｜笑並打開一手'),(ls[0],0,5,'5秒｜靠近停穩，全身79%'),(ls[0],0,8,'8秒｜保持距離，笑著回應')],
      'M03':[(ls[0],0,0,'0秒｜海軍藍西外與炭灰褲'),(ls[1],0,4,'4秒｜同件西外配淺色裙'),(ls[1],2,6,'6秒｜看見朋友後轉肩'),(ls[1],0,9,'9秒｜同套中景笑談')],
      'M04':[(ls[0],0,0,'0秒｜上衣花卉，下身素色'),(ls[0],0,4,'4秒｜花卉與衣料中近景'),(ls[0],2,7.25,'7.25秒｜回到全身'),(ls[0],0,9.5,'9.5秒｜回應同伴微笑')],
      'M05':[(ls[0],0,0,'0秒｜左短袖，右薄外層'),(ls[0],0,2,'2秒｜保留清楚閱讀'),(ls[0],0,5,'5秒｜各自回笑、小角度轉肩'),(ls[0],0,8,'8秒｜回正，層次維持清楚')],
    }[mid]
    for i,(l,pose,t,caption) in enumerate(specs):
        x=36+i*407; box=(x,190,360,640)
        if mid=='M02':
            v=project(character(t)); stage(d,box,l,pose,v['person_height_fraction'],v['person_center_uv'][0],v['top'],wall_floor_v=PRINCIPAL_V+1.15*FOCAL/4.4)
        elif mid=='M03' and i==3:
            medium=Image.new('RGB',(360,640),'#eeece6')
            stage(ImageDraw.Draw(medium),(0,0,360,640),l,pose,1.75,.5,.08)
            im.paste(medium,(x,190))
        elif mid=='M04' and i==1:
            d.rectangle((x,190,x+360,830),fill='#eeece6',outline='#98a2aa',width=2)
            d.rectangle((x+20,270,x+335,710),fill=l['colors'][0],outline='#2f3941',width=3)
            d.line([(x+115,270),(x+180,350),(x+245,270)],fill='#e4d9c9',width=4)
            for j in range(3):
                for fx in [x+100,x+260]:
                    fy=390+j*105;rad=19
                    for ax,ay in [(0,-1),(1,0),(0,1),(-1,0)]:
                        d.ellipse((fx+ax*rad*.6-rad*.65,fy+ay*rad*.6-rad*.65,fx+ax*rad*.6+rad*.65,fy+ay*rad*.6+rad*.65),fill='#ae6372',outline='#e4d9c9',width=2)
        else: stage(d,box,l,pose,parallel_look=ls[1] if mid=='M05' else None)
        if mid=='M05' and i==2:
            d.text((x+113,395),'↶',font=font(32),fill='#a75c35')
            d.text((x+292,395),'↷',font=font(32),fill='#a75c35')
        textblock(d,(x,850),caption,22,360)
        label=l['name'] if mid!='M05' else '左：短袖／右：加薄外層\n兩側全身74%，同高同落點'
        textblock(d,(x,915),label,21,360)
    yy=textblock(d,(36,1000),' → '.join(film['motives']),22,1580)
    yy=textblock(d,(36,yy+12),'時間：'+'；'.join(film['timing']),21,1580)
    textblock(d,(36,yy+12),'待驗證：'+film['risk']+' 線稿僅為構圖／表演提案；非AI照片、非生成結果或動態QA。',20,1580,fill='#90502e')
    im.save(p/'storyboard.png')
    return p/'storyboard.png'

# One common schematic route, clock and projection for both views; no gait simulation.
HUMAN=1.68; FOCAL=.68*3.5/HUMAN; PRINCIPAL_V=.338
def character(t):
    u=max(0,min(1,(t-2)/3))
    return [.30*(1-u)+.07*math.sin(math.pi*u),0,3.5-.5*u]

def project(pos):
    x,_,z=pos; hh=HUMAN*FOCAL/z
    cy=PRINCIPAL_V+(1.15-HUMAN/2)*FOCAL/z
    return dict(person_center_uv=[.5+x*FOCAL/z/(9/16),cy],person_height_fraction=hh,top=cy-hh/2)

def space_data():
    frames=[0,48,84,120,192]
    return dict(id='W45_M02_short_meeting_v2',units='schematic',
      unit_note='Relative schematic units; physical scale is unmeasured. Framing uses an explicit off-centre principal point, not a calibrated lens or a promised engine trajectory.',
      axes='x_right_y_up_z_forward',geometry=[
        dict(id='wall',vertices=[[-2,0,4.4],[2,0,4.4],[2,2.6,4.4],[-2,2.6,4.4]]),
        dict(id='pavement',vertices=[[-2,0,2.5],[2,0,2.5],[2,0,4.4],[-2,0,4.4]])],
      render_model=dict(person_height=HUMAN,normalized_focal_length=FOCAL,principal_point_uv=[.5,PRINCIPAL_V],
        note='Simplified perspective/framing illustration only; level camera, fixed independent camera path. Not anatomy, gait or physical camera calibration.'),
      routes=[dict(shot_id='S01',
        character_samples=[dict(frame=f,position=character(f/24),heading_degrees=180,gait_phase='standing; contact must be checked in generated footage' if f<=48 or f>=120 else 'short approach; gait phase not simulated') for f in frames],
        camera_samples=[dict(frame=f,position=[0,1.15,0],target=[0,1.15,4],vertical_fov_degrees=math.degrees(2*math.atan(.5/FOCAL))) for f in frames],
        projected_samples=[dict(frame=f,**{k:v for k,v in project(character(f/24)).items() if k!='top'},visible_landmark_ids=['wall','pavement'],visible_clothing='full outfit; moss-green upper and cocoa-brown trousers remain separate') for f in frames])])

def render_previs(space):
    p=HERE/'M02'; p.mkdir(parents=True,exist_ok=True)
    # Render positions from the exported source, with the same analytic route recorded below.
    def at(t):
        # Analytic expression is part of the exported common source, rather than a separate path.
        u=max(0,min(1,(t-space['route_function']['start_seconds'])/space['route_function']['move_seconds']))
        a=space['route_function']
        return [a['x_start']*(1-u)+a['x_bulge']*math.sin(math.pi*u),0,a['z_start']-a['z_travel']*u]
    def uv(pos):
        rm=space['render_model']; cam=space['routes'][0]['camera_samples'][0]['position']
        z=pos[2]-cam[2]; ff=rm['normalized_focal_length']; height=rm['person_height']*ff/z
        v=rm['principal_point_uv'][1]+(cam[1]-rm['person_height']/2)*ff/z
        return [.5+(pos[0]-cam[0])*ff/z/(9/16),v,height]
    frames=[]
    for n in range(96):
        t=n/12; pos=at(t); u,v,h=uv(pos)
        im=Image.new('RGB',(1100,790),'#fbfaf6'); d=ImageDraw.Draw(im)
        d.text((28,18),'W45 M02｜同一時間的俯視與相機構圖',font=font(30),fill='#233b41')
        d.text((28,67),f'{t:04.1f}s / 8.0s    相機固定 · 人物短程接近',font=font(23),fill='#3b5459')
        # Overhead coordinates use the exact same scene positions and camera location.
        def overhead(q): return (270+q[0]*170,660-q[2]*120)
        wall=space['geometry'][0]['vertices']
        d.line([overhead(q) for q in [wall[0],wall[1]]],fill='#6f7c80',width=8)
        path=[overhead(at(i/12)) for i in range(25,61)]
        d.line(path,fill='#b8c5bc',width=5)
        cam=overhead(space['routes'][0]['camera_samples'][0]['position'])
        end=overhead([0,0,4.4]); d.line([cam,end],fill='#adb5b9',width=2)
        d.rectangle((cam[0]-13,cam[1]-8,cam[0]+13,cam[1]+8),fill='#334e5a')
        now=overhead(pos); d.ellipse((now[0]-12,now[1]-12,now[0]+12,now[1]+12),fill='#b13a36')
        d.text((30,160),'俯視：紅點是人物，藍色是相機',font=font(20),fill='#26323b')
        d.text((30,700),'2–5秒移動，其餘停穩回應朋友',font=font(21),fill='#26323b')
        wall_z=space['geometry'][0]['vertices'][0][2]
        cam_y=space['routes'][0]['camera_samples'][0]['position'][1]
        wall_v=space['render_model']['principal_point_uv'][1]+cam_y*space['render_model']['normalized_focal_length']/wall_z
        stage(d,(635,120,315,560),LOOKS[2],2 if 1.3<t<2.6 else 0,h,u,v-h/2,wall_floor_v=wall_v)
        textblock(d,(600,700),'人物68% → 約79%；保持完整頭身與鞋。線稿未模擬步態，不能認定腳掌接地通過。',20,465)
        frames.append(im)
    frames[0].save(p/'previs.gif',save_all=True,append_images=frames[1:],duration=[80,80,90]*32,loop=0,optimize=False)
    frames[0].save(p/'overhead_and_view.png')
    # Static contact sheet to inspect start / movement / stop without claiming native-video QA.
    contact=Image.new('RGB',(2200,1580),'white')
    for i,n in enumerate([0,24,60,95]): contact.paste(frames[n],((i%2)*1100,(i//2)*790))
    contact.save(p/'previs_contact_sheet.png')

def main():
    HERE.mkdir(parents=True,exist_ok=True)
    for i,f in enumerate(FILMS,1):
        f['carousel_id']=f'{WEEK}-{i:03d}'
        for l in [x for x in LOOKS if x['model']==f['model']]:
            l['carousel_id']=f['carousel_id']; l['look_id']=f"{f['carousel_id']}-L{l['order']:02d}"
            l['source_material_ids']=[material_id('2026-'+s.split('-')[0],s) for s in l['sources']]
    space=space_data()
    space['route_function']=dict(start_seconds=2,move_seconds=3,x_start=.30,x_bulge=.07,z_start=3.5,z_travel=.5)
    dump(HERE/'M02/space.json',space)
    render_previs(space)
    refs=list(csv.DictReader((ROOT/'02_brand/mira_reference_images.csv').open(encoding='utf-8-sig')))
    results={}
    spec=importlib.util.spec_from_file_location('mira_plan_check',ROOT/'11_skills/mira-reel-director/scripts/plan.py')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    for f in FILMS:
        mid=f['model']; p=HERE/mid; board=render_board(f)
        ls=[x for x in LOOKS if x['model']==mid]
        used=[x for x in ls if x['order'] in f['reel_orders']]
        ref=next(x for x in refs if x['model_profile_id']==mid)
        plan=json.loads((ROOT/'11_skills/mira-reel-director/assets/production_plan.template.json').read_text(encoding='utf-8-sig'))
        plan.update(plan_id=f'W45_{mid}_v2',status='in_review',path_base='project')
        plan['weeks']=dict(source=sorted({'2026-'+s.split('-')[0] for l in used for s in l['sources']}),content=WEEK,delivery=None)
        plan['editorial']=dict(audience='台灣日常穿搭讀者',takeaway=f['purpose'],visual_theme='薄層次、生活中的表情與清楚服裝輪廓',selection_rationale=f['hook']+'；已核對W45原報與20筆CSV，來源單品與本專案完整搭配分開。')
        plan['presentation']=dict(layout_id=f['layout'],recipe_id=f['recipe'])
        if f['recipe']=='custom_experiment':
            plan['presentation'].update(recipe_name='固定鏡頭的認出與短程會合',viewer_mechanism='先看認出朋友的反應，再看穿搭在短程走近時的樣子',evidence_status='proposed_transfer_of_prior_motivated_performance')
        plan['film'].update(frame_count=f['frames'],duration_seconds=f['duration'])
        assets=[]
        def asset(aid,kind,path,**extra):
            rec=dict(id=aid,kind=kind,path=path.relative_to(ROOT).as_posix(),sha256=sha(path),**extra)
            assets.append(rec); return aid
        face=ROOT/ref['reference_face_path']; full=ROOT/ref['reference_full_path']
        assert face.is_file() and full.is_file() and ref['status']=='approved'
        asset(mid+'_face','identity',face); asset(mid+'_full','identity',full)
        plan['models']=[dict(id=mid,identity_asset_ids=[mid+'_face',mid+'_full'])]
        plan['looks']=[dict(id=l['look_id'],model_id=mid,wardrobe_summary=l['clothing'],source_asset_ids=[]) for l in used]
        asset('board','storyboard',board)
        plan['shots']=[]
        for i,((interval,orders),read) in enumerate(zip(f['shots'],f['reads']),1):
            shot=dict(id=f'S{i:02d}',look_ids=[l['look_id'] for l in ls if l['order'] in orders],frames=interval,
              clothing_purpose=f['purpose'] if not(mid=='M04' and i==2) else '只讀花卉與衣料；此段不計完整全身讀衣',
              clear_read_intervals=read,storyboard_asset_id='board',previs_asset_id=None,input_asset_ids=[],
              scene_reference_asset_ids=[],space_mode='independent',performance=f['motives'][min(i-1,len(f['motives'])-1)],
              execution_mode='generate',camera='fixed',source_duration_note='Output timing is editorial. Available Grok lengths, real usable intervals and source shortage must be recorded at execution; no retiming/freezes.')
            if mid=='M03' and i==3: shot['framing']='same-look medium shot; new approved source or exact approved-footage lineage required'
            if mid=='M04' and i==2: shot['framing']='floral blouse with neck and sleeve context; no full-outfit claim'
            if mid=='M05':
                shot['panels']=[dict(id='left',look_id=ls[0]['look_id'],height_fraction=.74,head_v=.14,shoe_v=.88),dict(id='right',look_id=ls[1]['look_id'],height_fraction=.74,head_v=.14,shoe_v=.88)]
            plan['shots'].append(shot)
        plan['transitions']=[dict(from_shot=f'S{i:02d}',to_shot=f'S{i+1:02d}',frames=[f['shots'][i][0][0],f['shots'][i-1][0][1]],overlap_frames=18,method='cross_dissolve') for i in range(1,len(f['shots']))]
        if mid=='M02':
            plan['space']=space; plan['shared_space_asset_id']='common_space'
            asset('common_space','space_plan',p/'space.json')
            source=dict(asset_id='common_space',sha256=sha(p/'space.json'))
            asset('previs','previs',p/'previs.gif',derived_from=source)
            asset('overhead','overhead',p/'overhead_and_view.png',derived_from=source)
            plan['shots'][0].update(space_mode='shared_world',previs_asset_id='previs',overhead_asset_id='overhead')
        plan['assets']=assets
        plan['missing_assets']=['使用者對W45具體企劃與線稿的確認；不從「繼續W45」推定新圖核准',
          '各鏡全新、逐張核准的原生9:16起始圖；現有身份參照不等於新造型圖',
          '正式生成當下的Grok額度、可用片長與設定尚待核對；未送工作']
        if mid in ['M03','M04']: plan['missing_assets'].append('額外同套中景／細節構圖來源，或有精確來源與適用核准範圍的影片影格')
        dump(p/'production_plan.json',plan)
        result=module.Check(plan,p/'production_plan.json',ROOT).run()
        dump(p/'planning_validation.json',result)
        results[mid]=dict(status=result['status'],ready_for_generation=result['ready_for_generation'],errors=result['errors'],timeline=result['timeline'])
        card=[f"# W45 {mid}｜{f['title']}",'','狀態：完整提案，待使用者確認；未生成起始圖或影片。','',
              '觀眾看點：'+f['purpose'],'','入片：'+str(len(used))+'套；週庫存：2套。',
              '來源單品：'+'、'.join(sorted({s for l in ls for s in l['sources']}))+'；完整搭配與情境為本專案編輯提案。','',
              '![連接分鏡](storyboard.png)','','## 拍攝卡','']
        for i,s in enumerate(plan['shots']):
            card += [f"- {s['id']}：{s['frames'][0]/24:g}–{s['frames'][1]/24:g}秒；"+s['performance']+'。',
                     f"  服裝閱讀區間：{[[a/24,b/24] for a,b in s['clear_read_intervals']]}秒；相鄰鏡沿用0.75秒疊化比較基準。"]
        card += ['','風險及重試界線：'+f['risk'],'',
          '生成策略：簡短情境／動機＋必要可見反應，保留合理自然變體；不每秒堆手勢。每個相同機制至多兩次失敗，之後改設計或轉研究。',
          '審查：先實際起始圖服裝、身份與構圖；再逐鏡原速看手／腳／頭身、連續性；有接點先看完整重疊段，最後整片。解碼與抽格不等於原速QA。',
          '來源設定：片長為剪輯目標，不是聲稱Grok可精確輸出；依實際可用原速素材選段，素材不足即縮短／補拍，不用變速或停格補足。',
          '身份參照：'+ref['reference_face_path']+'；'+ref['reference_full_path']+'。',
          '照片鏡頭沿用全片幅無反、50mm、接近胸高、水平光軸；實際構圖要再比對，預演不是引擎或物理標定。']
        if mid=='M02': card += ['','![共同空間預演](previs.gif)','', '空間／相機構圖同用 space.json。人物全身目標68%→79%，相機不移動。相對示意單位，步態未模擬。']
        elif mid=='M05': card += ['','必要預演：線稿已按實際9:16並排版面畫兩側等高人物；動畫與AI原片尚未產出。先做短段的同時尺度／節奏對照。']
        else: card += ['','空間雙路徑預演：不適用。固定站位或獨立鏡頭；連接線稿已列起訖、景別和重疊區間。']
        (p/'SHOT_CARDS.md').write_text('\n'.join(card)+'\n',encoding='utf-8')
    dump(HERE/'planning_validation_summary.json',results)
    assert all(not r['errors'] for r in results.values()), results
    dump(HERE/'editorial_plan.json',dict(schema_version=1,content_week=WEEK,planning_date=DATE,status='proposed_pending_user_plan_review',
         source_gap=None, source_receipt='../source_receipt.json', revision=2,
         weekly_inventory_looks=10,weekly_reels=5,reel_look_count=8,companion_only_looks=2,films=FILMS,looks=LOOKS,
         production_order=['M02','M01','M03','M04','M05'],generated_stills=0,generated_videos=0,cloud_paid_requests=0))
    oldlook=list(csv.DictReader((ROOT/'10_automation/runs/2026-W44/weekly_look_plan.csv').open(encoding='utf-8-sig')))
    fields=list(oldlook[0]); rows=[]
    for l in LOOKS:
        f=next(x for x in FILMS if x['model']==l['model'])
        row={k:'' for k in fields}; row.update(week_id=WEEK,carousel_id=l['carousel_id'],model_profile_id=l['model'],look_id=l['look_id'],look_order=l['order'],theme_name=f['title'],opening_hook=f['hook'],look_name=l['name'],dressing_decision=l['decision'],occasion='日常外出／赴約',clothing_item=l['clothing'],color_palette=l['palette_text'],fabric='薄棉／薄針織等編輯材質；不是來源商品規格',fit=l['proof'],styling_rules='全套依本列鎖定；來源單品不等於整套來源',visual_proof=l['proof'],practical_rule=l['decision'],scene=l['scene'],visible_action=l['action'],frame_plan='Reel: native 9:16 full A + reviewed styling-proof; Carousel: A full / B scene / C detail',required_frames='Reel A+proof; Carousel A+B+C',status='editorial_proposed_pending_plan_review',next_action='W45方案確認後，先製作M02 L01起始圖候選；各張核准後才進動態')
        rows.append(row)
    writecsv(RUN/'weekly_look_plan.csv',rows,fields)
    packetfields=list(next(csv.DictReader((ROOT/'10_automation/runs/2026-W44/weekly_content_packet.csv').open(encoding='utf-8-sig'))))
    packet=[]
    for f in FILMS:
        l=next(x for x in LOOKS if x['model']==f['model'] and x['order']==1)
        r={k:'' for k in packetfields};r.update(week_id=WEEK,carousel_id=f['carousel_id'],market='TW',model_profile_id=f['model'],trend_name=f['title'],content_bucket='utility_with_immersion',audience='台灣日常穿搭讀者',occasion='日常外出／赴約',content_engine=f['recipe'],dressing_decision=l['decision'],visible_action=l['action'],audience_problem=f['hook'],editorial_answer=f['purpose'],opening_hook=f['hook'],visual_proof=l['proof'],practical_rule=l['decision'],clothing_item=l['clothing'],color_palette=l['palette_text'],scene=l['scene'],status='editorial_proposed_pending_plan_review',next_action='先確認企劃／分鏡，再生成首張候選圖')
        packet.append(r)
    writecsv(RUN/'weekly_content_packet.csv',packet,packetfields)
    needs=[]
    for l in LOOKS:
        f=next(x for x in FILMS if x['model']==l['model'])
        for surface,role in [('reel','A_full_9x16'),('reel','styling_proof'),('carousel','A_full'),('carousel','B_scene'),('carousel','C_accessory')]:
            needs.append(dict(look_id=l['look_id'],model=l['model'],surface=surface,role=role,reel_used=l['order'] in f['reel_orders'],status='missing_not_generated',reuse_candidate='proof may reuse an exact-outfit approved view only after vertical/clarity review' if role=='styling_proof' else '',plan='No W44 outfit is asserted to match this new complete outfit; identity refs reuse only.'))
    needs += [dict(look_id='2026-W45-003-L02',model='M03',surface='reel',role='medium_S03',reel_used=True,status='missing_or_exact_frame_lineage_needed',reuse_candidate='Review same-outfit footage after generation',plan='May be fulfilled by reviewed same-outfit proof if composition supports it.'),dict(look_id='2026-W45-004-L01',model='M04',surface='reel',role='floral_detail_S02',reel_used=True,status='missing_or_reviewed_proof_needed',reuse_candidate='Review same-outfit proof',plan='May be fulfilled by clear vertical styling-proof; no automatic crop approval.')]
    writecsv(RUN/'asset_requirements.csv',needs,list(needs[0]))
    dump(RUN/'reuse_assessment.json',dict(date=DATE,scope='wardrobe metadata and exact identity-file presence/hash; not visual acceptance of legacy stills',
        existing_look_plan='10_automation/runs/2026-W44/weekly_look_plan.csv',existing_film_receipts='10_automation/runs/2026-W44/publishing_structure.md',
        finding='W44 films remain delivered as W44. Proposed W45 complete outfits differ; no exact still/clip reuse is certified. Approved identity anchors reused. Styling proofs may reuse a new approved exact-outfit view only after composition/clarity review.',
        role_count=52,baseline_roles=50,additional_view_roles=2,unique_new_image_range='40–52 planning range, conditional on 10 proof reuses and 2 medium/detail roles being satisfied by those views. No promised reuse before visual review.',
        new_generation_jobs_submitted=0,paid_cloud_requests=0))
    overview=Image.new('RGB',(1660,1710),'#fbfaf6'); d=ImageDraw.Draw(overview)
    d.text((35,24),'W45｜五個看點，五位模特兒',font=font(40),fill='#233b41')
    d.text((35,82),'10套週庫存 · 5支Reel提案 · 未生成照片或影片',font=font(26),fill='#56676d')
    for i,f in enumerate(FILMS):
        y=140+i*306
        board=Image.open(HERE/f['model']/'storyboard.png')
        # Four actual portrait panels in a compact strip, plus editorial purpose beside them.
        strip=board.crop((36,190,1617,830)); strip.thumbnail((750,290))
        overview.paste(strip,(35,y))
        d.text((805,y),f"{f['model']}  {f['title']}",font=font(27),fill='#233b41')
        yy=textblock(d,(805,y+52),f['purpose'],22,800)
        textblock(d,(805,yy+12),f"入片{len(f['reel_orders'])}套｜{f['duration']:g}秒｜"+('固定鏡頭短程走近' if f['model']=='M02' else f['recipe']),21,800,fill='#8e4c32')
    overview.save(HERE/'W45_overview.png')
    print(json.dumps(dict(week=WEEK,themes=5,inventory_looks=10,reel_looks=8,boards=5,common_space_previs=1,validation=results),ensure_ascii=False))

if __name__=='__main__': main()
