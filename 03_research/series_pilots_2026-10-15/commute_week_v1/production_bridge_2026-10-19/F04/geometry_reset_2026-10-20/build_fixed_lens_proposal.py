"""Converged fixed-projection camera proposal; direct deterministic Pillow board.

Preserve existing4/4 camera endpoints and approved site/path. No lens/FOV change,
no renderer install, no browser and no image/video generation service.
"""
import importlib.util
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('fixed_lens_audit',HERE/'build_geometry_proposal.py')
helpers=importlib.util.module_from_spec(spec);spec.loader.exec_module(helpers)
fixed=helpers.fixed
from PIL import Image,ImageDraw


def main():
    protected=[HERE/'geometry-proposal-plan.json',HERE/'geometry-proposal.html',HERE/'geometry-proposal-receipt.json',HERE/'geometry_plan.json']
    protection={str(p):fixed.digest(p) for p in protected}
    data=json.loads(protected[0].read_text(encoding='utf-8'))
    original=json.loads((HERE/'geometry_plan.json').read_text(encoding='utf-8'))
    focal=original['frames'][0]['focal'];checks=[]
    for i,f in enumerate(data['frames']):
        f['focal']=focal
        top=fixed.project([f['person'][0],1.7,f['person'][1]],f)
        feet=fixed.project([f['person'][0],0,f['person'][1]],f)
        visible=[]
        for stripe in data['stripes']:
            pp=[fixed.project(v,f) for v in stripe['points']]
            if all(v is not None for v in pp) and len(helpers.clip_screen(pp))>=3:visible.append(stripe['id'])
        assert top and feet and 0<top[0]<360 and 0<feet[0]<360 and 0<top[1]<feet[1]<640
        assert visible
        checks.append({'percentage':i,'head_top':top,'feet':feet,'body_height_fraction':(feet[1]-top[1])/640,'visible_stripes':visible})
    data['stage']='fixed_projection_camera_proposal_pending_user_approval'
    fixed.write_new(HERE/'geometry-fixed-lens-plan.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    template=(HERE/'f04-fixed-crosswalk.template.html').read_text(encoding='utf-8')
    template=template.replace('mira-f04-fixed-crosswalk-20261020','mira-f04-fixed-lens-20261020').replace('mira-f04-progress','mira-f04-fixed-lens-progress')
    template=template.replace('第四段：同一組白線，鏡頭持續移動','第四段提案：固定視角，側面過街')
    template=template.replace('由同一地面六條固定白線與原分鏡相機計算的透視圖','同一組六條白線與固定投影比例相機的過街提案')
    template=template.replace('>首幀<','>起點<').replace('>中景<','>途中<').replace('>末幀<','>終點<')
    template=template.replace('原分鏡中景：白條接近橫向；與核准中景的朝遠處方向不同。','固定投影比例；途中白條朝景深延伸。新鏡位待確認。')
    template=template.replace('固定6條白線；只有人物與相機沿原路徑移動。','固定6條白線與人物路線；人物途中、終點較小。')
    fixed.write_new(HERE/'geometry-fixed-lens.html',template.replace('__MODEL_DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':'))))
    art=fixed.previs.art
    board=Image.new('RGB',(1240,850),art.PAPER);draw=ImageDraw.Draw(board)
    draw.text((28,20),'第四段鏡位提案｜固定視角，同一組白線',font=art.font(30,True),fill=art.INK)
    draw.text((30,64),'起點接原鏡位 → 相機移到人物側面 → 稍落後，跟到公司側',font=art.font(21),fill=art.INK)
    for k,i in enumerate([0,50,100]):
        f=data['frames'][i];pic=Image.new('RGB',(360,640),art.PAPER);d=ImageDraw.Draw(pic)
        def poly(points,fill,stroke=art.SOFT):
            points=fixed.previs.site.World.clip_near(points,fixed.previs.np.array(f['camera']),fixed.previs.np.array(f['forward']))
            pp=[fixed.project(v,f) for v in points]
            if len(pp)>2 and all(v is not None for v in pp):
                pp=[(max(-3000,min(3000,p[0])),max(-3000,min(3000,p[1]))) for p in pp]
                d.polygon(pp,fill=fill);d.line(pp+[pp[0]],fill=stroke,width=1)
        def line(points,color=art.SOFT,width=1):
            pp=[fixed.project(v,f) for v in points]
            if all(v is not None for v in pp):d.line([tuple(p) for p in pp],fill=color,width=width)
        poly([(-6,0,8.8),(20,0,8.8),(20,6.5,8.8),(-6,6.5,8.8)],'#e0e6e4')
        for x in range(6,21,2):line([(x,0,8.8),(x,6.5,8.8)],'#929f98')
        for y in [2.8,4.5,6.5]:line([(-6,y,8.8),(20,y,8.8)],'#a5afa7')
        poly([(-6,0,2.5),(20,0,2.5),(20,0,5.4),(-6,0,5.4)],'#c7ccc7')
        for stripe in data['stripes']:poly(stripe['points'],'#faf9f3','#92998f')
        for z in data['road_z']:line([(8,0,z),(18,0,z)],'#7e8b82',2)
        p=f['person'];h=f['heading'];side=[h[1],-h[0]]
        def W(l,y,a=0):return[p[0]+side[0]*l+h[0]*a,y,p[1]+side[1]*l+h[1]*a]
        for points in [[W(0,1.48),W(0,.86),W(-.11,.06,-.1)],[W(0,.86),W(.11,.06,.1)],
                       [W(-.24,1.0),W(-.18,1.36),W(.18,1.36),W(.24,1.0)]]:line(points,art.ACCENT,4)
        hp=fixed.project(W(0,1.58),f);tp=fixed.project(W(0,1.70),f);lp=fixed.project(W(0,1.48),f)
        rx=abs(lp[1]-tp[1])*.33;ry=abs(lp[1]-tp[1])*.5
        d.ellipse((hp[0]-rx,hp[1]-ry,hp[0]+rx,hp[1]+ry),fill=art.ACCENT)
        x=30+k*405;board.paste(pic,(x,143));draw.rectangle((x,143,x+360,783),outline=art.SOFT,width=1)
        draw.text((x,108),['起點','途中','終點'][k],font=art.font(24,True),fill=art.INK)
    draw.text((30,804),'六條白線位置不變；人物僅示意。新鏡位尚待確認，沒有匹配舊照片或生成影片。',font=art.font(20),fill=art.INK)
    png=HERE/'geometry-fixed-lens-three-views.png'
    with png.open('xb') as stream:board.save(stream,format='PNG')
    for path,sha in protection.items():assert fixed.digest(Path(path))==sha
    receipt={'stage':'fixed_projection_camera_proposal_pending_user_review','fixed_focal_ratio':focal,
             'focal_ratio_varies':False,'physical_50mm_calibration_proven':False,
             'camera_offset_knots':data['frames'][0]['camera_offset_from_person'] if 'camera_offset_from_person' in data['frames'][0] else None,
             'camera_motion_reused_from_proposal':True,'same_six_world_stripes':data['stripes']==original['stripes'],
             'same101_person_positions':all(f['person']==o['person'] for f,o in zip(data['frames'],original['frames'])),
             'all101_head_and_feet_fit':True,'all101_at_least_one_paint_polygon_visible':True,
             'start_mid_end_checks':[checks[i] for i in [0,50,100]],'checks':checks,'protected_files_unchanged':protection,
             'AI_calls':0,'Grok_calls':0,'browser_visual_QA':False,'user_approval':None,
             'limitations':['No zoom/FOV change; original abstract projection retained, not physical lens certification.',
                            'Person occupies about55%/42%/40% of frame height at start/mid/end; garment details are smaller.',
                            'Only final stripe remains visible at endpoint; not all6 stay on screen.',
                            'Marker head/feet checks do not validate all body/bag contours, real reconstruction or walking.',
                            'This is a new camera proposal; does not match approved photos or replace accepted sources.'],
             'files':{p.name:{'sha256':fixed.digest(p),'bytes':p.stat().st_size} for p in [png,HERE/'geometry-fixed-lens.html',HERE/'geometry-fixed-lens-plan.json']}}
    fixed.write_new(HERE/'geometry-fixed-lens-receipt.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'png':str(png),'all101_head_feet_fit':True,'fixed_focal_ratio':focal,'start_mid_end_body_height':[checks[i]['body_height_fraction'] for i in [0,50,100]]},ensure_ascii=False))


if __name__=='__main__':main()
