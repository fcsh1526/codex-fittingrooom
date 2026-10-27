"""Draw production-planning diagrams; never read or alter approved photo/video files.

The hand-drawn motion only describes framing, direction and editorial time.
It is not a simulation of Grok, photographic realism or verified human gait.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / '10_automation').is_dir())
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
import imageio_ffmpeg

PLAN = json.loads((HERE / 'storyboard_plan.json').read_text(encoding='utf-8'))
PAPER = '#fbfaf6'
INK = '#333736'
SOFT = '#bec2bc'
LIGHT = '#e6e7e0'
ACCENT = '#a24c31'
FONT = Path('C:/Windows/Fonts/msjh.ttc')
BOLD = Path('C:/Windows/Fonts/msjhbd.ttc')
COLORS = {'long_blazer':('#eee8d8','#354353','#66503f'),
          'short_jacket':('#ede7d9','#62656a','#383b3c'),
          'plaid_shirt':('#eee9db','#62656a','#383b3c'),
          'a_skirt':('#f7f6ef','#3e4141','#45648f'),
          'brown_denim':('#f7f6ef','#8c6e54','#383b3c')}


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def mix(a, b, t):
    return a + (b-a)*t


def arrow(draw, a, b, color=ACCENT, width=3, dashed=False):
    if dashed:
        length = math.dist(a,b)
        n = max(1, int(length/12))
        for k in range(0,n,2):
            draw.line((mix(a[0],b[0],k/n),mix(a[1],b[1],k/n),
                       mix(a[0],b[0],min(1,(k+1)/n)),mix(a[1],b[1],min(1,(k+1)/n))), fill=color,width=width)
    else:
        draw.line((*a,*b),fill=color,width=width)
    ang = math.atan2(b[1]-a[1],b[0]-a[0])
    head = 11
    draw.line((b[0]-head*math.cos(ang-.45),b[1]-head*math.sin(ang-.45),*b),fill=color,width=width)
    draw.line((b[0]-head*math.cos(ang+.45),b[1]-head*math.sin(ang+.45),*b),fill=color,width=width)


def profile_person(draw, cx, foot, h, phase, kind, background=False):
    top,bottom,bag=COLORS[kind]
    ink=SOFT if background else INK
    if background:top,bottom,bag=LIGHT,'#d6d8d1','#c4c8c2'
    cy=foot-h-abs(math.sin(phase))*h*.004
    stride=.115*math.sin(phase)
    def p(x,y):return(cx+x*h,cy+y*h)
    def poly(points,fill):
        pts=[p(x,y) for x,y in points]
        draw.polygon(pts,fill=fill);draw.line(pts+[pts[0]],fill=ink,width=max(1,round(h*.003)),joint='curve')
    def line(points,color=ink,width=.003):draw.line([p(x,y) for x,y in points],fill=color,width=max(1,round(h*width)),joint='curve')
    draw.ellipse((cx-h*.20,foot-h*.007,cx+h*.20,foot+h*.006),fill=LIGHT)
    ankles=[(-.025-stride,.957),(.025+stride,.963)]
    for sign,(xx,yy) in zip([-1,1],ankles):
        knee=-.02+sign*stride*.62
        if kind=='a_skirt':
            poly([(-.035+sign*.012,.68),(.012+sign*.012,.68),(xx+.014,yy),(xx-.014,yy)],'#ded6c9')
        else:
            poly([(-.065,.35),(.06,.35),(knee+.038,.66),(xx+.038,.95),(xx-.039,.95),(knee-.041,.66)],bottom)
            line([(-.005,.43),(knee,.66),(xx,.94)],'#8c9088',.0015)
        poly([(xx-.035,yy-.005),(xx+.022,yy-.005),(xx+.074,yy+.012),(xx+.074,yy+.025),(xx-.035,yy+.025)],'#414544')
    if kind=='a_skirt':
        sway=.018*math.sin(phase)
        poly([(-.063,.345),(.067,.345),(.13+sway,.73),(-.125+sway,.73)],bottom)
        line([(-.01,.42),(.01+sway,.70)],'#858982',.0015)
    # Genuine side outline: back at left, chest/placket at right.
    poly([(-.038,.145),(.035,.15),(.068,.20),(.085,.245),(.068,.35),(-.073,.35),(-.075,.205)],top)
    if kind=='plaid_shirt':
        for x in [-.05,-.018,.015,.045,.071]:line([(x,.19),(x,.34)],'#7c8790',.0025)
        for y in [.21,.245,.28,.315]:line([(-.07,y),(.073,y)],'#7c8790',.0025)
    if kind in ['a_skirt','brown_denim','plaid_shirt']:
        poly([(.026,.145),(.059,.168),(.04,.198),(.01,.167)],top)
        line([(.065,.21),(.064,.345)],width=.0015)
    if kind in ['long_blazer','short_jacket']:
        hem=.49 if kind=='long_blazer' else .34
        poly([(-.045,.144),(.042,.158),(.074,.22),(.07,hem),(-.085,hem),(-.081,.21)],top)
        line([(.035,.165),(.02,.22),(.06,.245),(.063,.36)],width=.002)
    if kind=='brown_denim':poly([(-.069,.345),(.068,.345),(.068,.361),(-.069,.361)],'#414544')
    # One near arm shows side-facing walking; the far arm stays behind torso.
    elbow=.025+stride*.65
    hand=.025+stride*.95
    line([(-.015,.18),(elbow,.34),(hand,.49)],width=.028)
    line([(-.015,.18),(elbow,.34),(hand,.49)],top if kind in ['long_blazer','short_jacket'] else '#ded6c9',.022)
    if kind not in ['long_blazer','short_jacket']:
        line([(-.015,.18),(.002+stride*.3,.26)],width=.032)
        line([(-.015,.18),(.002+stride*.3,.26)],top,.026)
    line([(.015,.175),(.082,.36)],bag,.007)
    poly([(.04,.35),(.13,.35),(.13,.434),(.04,.434)],bag)
    line([(.046,.37),(.125,.37)],'#a0a69e',.0015)
    poly([(-.02,.10),(.025,.10),(.028,.153),(-.028,.153)],'#e5ddd0')
    poly([(-.044,.018),(-.01,.0),(.028,.012),(.041,.039),(.066,.061),(.041,.071),(.038,.106),(.014,.123),(-.032,.108),(-.052,.059)],'#e5ddd0')
    line([(-.043,.085),(-.051,.042),(-.036,.012),(-.008,0),(.024,.012),(.034,.031)],width=.012)
    line([(-.045,.043),(-.055,.113),(-.031,.133)],width=.012)
    ex,ey=p(.025,.046);draw.ellipse((ex-1,ey-1,ex+1,ey+1),fill=ink)


def person(draw, cx, foot, h, angle, phase, kind, background=False):
    """Schematic ordinary-proportion woman with garment-specific silhouettes."""
    if angle>=.75:
        profile_person(draw,cx,foot,h,phase,kind,background)
        return
    top, bottom, bag = COLORS[kind]
    ink = SOFT if background else INK
    if background:
        top, bottom, bag = LIGHT, '#d6d8d1', '#c4c8c2'
    width = 0.84-0.28*angle
    swing = math.sin(phase)
    bob = -abs(math.sin(phase))*h*.004
    cy = foot-h+bob
    def p(x,y): return (cx+x*h*width,cy+y*h)
    def poly(points, fill, line=True):
        points = [p(x,y) for x,y in points]
        draw.polygon(points,fill=fill)
        if line: draw.line(points+[points[0]],fill=ink,width=max(1,round(h*.0033)),joint='curve')
    def line(points, color=ink, w=.003):
        draw.line([p(x,y) for x,y in points],fill=color,width=max(1,round(h*w)),joint='curve')
    lw=max(1,round(h*.0035))
    # Ground contact ellipse and rear arm.
    draw.ellipse((cx-h*.16,foot-h*.007,cx+h*.16,foot+h*.006),fill=LIGHT)
    a = swing*.055
    line([(.10,.19),(.16-a,.37),(.14-a*.6,.48)],w=.025)
    line([(.10,.19),(.16-a,.37),(.14-a*.6,.48)],color=top,w=.020)
    # Two trouser legs or skirt and bare shins. Knees and feet alternate.
    stride = (.018+.042*angle)*swing
    left_ankle=(-.063-stride,.955)
    right_ankle=(.063+stride,.963)
    if kind=='a_skirt':
        for hip,ankle in [(-.06,left_ankle),(.06,right_ankle)]:
            poly([(hip-.025,.69),(hip+.025,.69),(ankle[0]+.018,.96),(ankle[0]-.018,.96)],'#ded6c9')
        hem = .73
        poly([(-.105,.35),(.105,.35),(.18+stride*.3,hem),(.035,hem+.008),(-.18+stride*.3,hem)],bottom)
        line([(-.015,.39),(-.05,.69)],color='#797c79',w=.0016)
    else:
        for sign,ankle in [(-1,left_ankle),(1,right_ankle)]:
            hip=sign*.058
            knee=hip-sign*stride*.5
            poly([(hip-.057,.35),(hip+.057,.35),(knee+.045,.66),(ankle[0]+.045,.95),
                  (ankle[0]-.047,.95),(knee-.05,.67)],bottom)
            line([(hip,.41),(knee,.66),(ankle[0],.93)],color='#9b9d97' if background else '#888b85',w=.0013)
    for ankle in [left_ankle,right_ankle]:
        x,y=ankle
        poly([(x-.039,y-.005),(x+.031,y-.005),(x+.083,y+.012),(x+.083,y+.026),(x-.039,y+.026)],'#414544' if not background else '#bec2bc')
    # Shirt or tee shape and neck opening.
    poly([(-.075,.145),(-.14,.19),(-.118,.25),(-.095,.24),(-.097,.36),(.10,.36),(.10,.24),(.126,.25),(.145,.195),(.071,.145)],top if kind in ['plaid_shirt','a_skirt','brown_denim'] else '#f7f6ef')
    if kind in ['a_skirt','brown_denim','plaid_shirt']:
        poly([(-.05,.15),(-.012,.18),(-.047,.205),(-.078,.162)],top)
        poly([(.05,.15),(-.012,.18),(.029,.205),(.078,.162)],top)
        line([(-.012,.18),(-.012,.35)],w=.0015)
        for y in [.22,.27,.32]:
            q=p(-.006,y); rr=max(1,h*.0017);draw.ellipse((q[0]-rr,q[1]-rr,q[0]+rr,q[1]+rr),fill=ink)
        if kind=='plaid_shirt':
            for x in [-.08,-.035,.015,.06,.1]: line([(x,.20),(x,.345)],color='#7c8790',w=.003)
            for y in [.215,.25,.285,.32]:line([(-.10,y),(.105,y)],color='#7c8790',w=.003)
    else:
        line([(-.045,.153),(-.035,.172),(0,.18),(.035,.172),(.045,.153)],w=.0023)
    if kind in ['long_blazer','short_jacket']:
        hem=.49 if kind=='long_blazer' else .34
        poly([(-.065,.145),(-.145,.18),(-.13,.28),(-.12,hem),(-.016,hem),(-.025,.26),(-.034,.17)],top)
        poly([(.065,.145),(.145,.18),(.13,.28),(.12,hem),(.02,hem),(.025,.26),(.034,.17)],top)
        if kind=='long_blazer':
            line([(-.035,.16),(-.077,.22),(-.035,.24),(-.022,.31)],w=.002)
            line([(.035,.16),(.077,.22),(.035,.24),(.022,.31)],w=.002)
            line([(-.105,.37),(-.05,.37)],w=.002)
            line([(.05,.37),(.105,.37)],w=.002)
        else:
            poly([(-.073,.15),(-.042,.13),(-.027,.16),(-.03,.18)],top)
            poly([(.073,.15),(.042,.13),(.027,.16),(.03,.18)],top)
            line([(-.115,.32),(-.025,.32)],w=.002)
    if kind=='brown_denim':
        poly([(-.10,.345),(.103,.345),(.103,.362),(-.10,.362)],'#404240')
        line([(-.012,.345),(-.012,.365),(.014,.365),(.014,.345)],color='#b9b7ac',w=.002)
    # Front arm and relaxed hand, without fine clothing contact.
    sleeve_end=.31 if kind in ['long_blazer','short_jacket'] else .225
    line([(-.11,.18),(-.16+a,.35)],w=.038)
    line([(-.11,.18),(-.16+a,.35)],color=top,w=.031)
    if sleeve_end<.3:
        line([(-.13,.23),(-.16+a,.35),(-.15+a*.7,.49)],w=.021)
        line([(-.13,.23),(-.16+a,.35),(-.15+a*.7,.49)],color='#ded6c9',w=.016)
    else:
        line([(-.16+a,.35),(-.15+a*.7,.49)],w=.02)
        line([(-.16+a,.35),(-.15+a*.7,.49)],color='#ded6c9',w=.014)
    # Small shoulder bag stays by the hip, keeping main garment visible.
    line([(.106,.175),(.16,.36)],color=bag,w=.008)
    poly([(.10,.35),(.205,.35),(.20,.435),(.10,.435)],bag)
    line([(.11,.37),(.19,.37)],color='#a5aaa2',w=.0015)
    # Neck, face outline, hair and readable viewing direction.
    poly([(-.025,.10),(.026,.10),(.032,.151),(-.031,.151)],'#e5ddd0')
    hx,hy=p(0,.065)
    rx,ry=h*.052*width,h*.065
    draw.ellipse((hx-rx,hy-ry,hx+rx,hy+ry),fill='#e5ddd0',outline=ink,width=lw)
    draw.arc((hx-rx*1.13,hy-ry*1.10,hx+rx*1.03,hy+ry*.5),175,350,fill=ink,width=max(2,round(h*.014)))
    line([(-.055,.055),(-.052,.12),(-.033,.135)],w=.012)
    nose=p(.027+angle*.024,.065)
    line([(.018+angle*.014,.046),(.038+angle*.02,.065),(.024+angle*.018,.073)],w=.0017)
    eye=p(.016+angle*.01,.045)
    draw.ellipse((eye[0]-1,eye[1]-1,eye[0]+1,eye[1]+1),fill=ink)


def background(draw, size, shot, progress):
    w,h=size
    shift=(-progress*42 if shot['movement']=='track' else 0)*w/540
    def line(coords,fill=SOFT,width=1):
        draw.line([(x*w+shift,y*h) for x,y in coords],fill=fill,width=width)
    scene=shot['scene']
    horizon=.47
    line([(0,horizon),(1,horizon)],fill='#d7dad4')
    if scene=='office_corner':
        for coords in [[(0,.08),(.37,.15),(.37,.67),(0,.72)],[(.38,.15),(.96,.05),(.96,.70),(.38,.67)]]:
            line(coords+[coords[0]])
        for x in [.08,.18,.29,.48,.63,.79,.93]:line([(x,.16),(x,.67)])
        for y in [.24,.34,.44,.55]:line([(0,y),(.37,y+.03),(.98,y)])
        line([(0,.95),(.42,.63),(1,.86)])
    elif scene=='colonnade':
        for x,width in [(-.12,.1),(.2,.1),(.55,.085),(.86,.1),(1.18,.1)]:
            line([(x,.06),(x,.78),(x+width,.78),(x+width,.06)])
            line([(x-.025,.09),(x+width+.025,.09)])
        line([(0,.77),(1,.77)]);line([(0,.91),(1,.83)])
        for y in [.84,.95]:line([(0,y),(1,y-.07)])
    elif scene=='plaza':
        for x,y,ww in [(-.05,.10,.22),(.22,.19,.24),(.75,.08,.3)]:
            line([(x,.66),(x,y),(x+ww,y),(x+ww,.66)])
            for yy in [y+.09,y+.2,y+.32]:line([(x,yy),(x+ww,yy)])
        line([(0,.75),(1,.75)])
        for x in [-.5,0,.5,1,1.5]:line([(.5,.66),(x,1)])
        for y in [.80,.92]:line([(0,y),(1,y)])
        # street tree, not an empty studio.
        line([(.77,.46),(.77,.69)],width=2)
        draw.ellipse((w*.68+shift,h*.35,w*.87+shift,h*.49),outline=SOFT,width=1)
    elif scene=='crossing':
        line([(0,.10),(.31,.13),(.31,.66),(0,.66)])
        line([(.74,.05),(.97,.05),(.97,.65),(.74,.65),(.74,.05)])
        for y in [.20,.32,.44]:line([(0,y),(.31,y+.02)])
        line([(0,.70),(1,.70)]);line([(0,.74),(1,.74)])
        for x in [-.35,-.10,.15,.40,.65,.90,1.15]:
            points=[((x+shift/w)*w,.79*h),((x+.12+shift/w)*w,.79*h),((x+.22+shift/w)*w,.96*h),((x+.06+shift/w)*w,.96*h)]
            draw.polygon(points,fill='#ecece5',outline='#d2d5cd')
        line([(.86,.40),(.86,.68)],width=2)
        draw.rectangle((w*.83+shift,h*.35,w*.9+shift,h*.42),outline=SOFT,width=1)
    else:
        for x in [-.05,.24,.57,.91]:
            line([(x,.02),(x,.77),(x+.065,.77),(x+.065,.02)])
        line([(0,.10),(1,.10)]);line([(0,.16),(1,.16)])
        line([(.20,.31),(.44,.31),(.44,.70),(.20,.70),(.20,.31)])
        line([(.66,.31),(.86,.31),(.86,.70),(.66,.70),(.66,.31)])
        line([(0,.81),(1,.81)]);line([(0,.97),(1,.88)])
    # Distant commuters are secondary, never cover the main clothing.
    for k,(x,hh) in enumerate([(.16,.19),(.83,.22),(.92,.15)]):
        bx=(x+math.sin(progress*2+k)*.035)*w+shift*.3
        person(draw,bx,h*(.66+k*.015),h*hh,.65,progress*9+k,'brown_denim',background=True)


def frame(shot, p, arrows=False):
    w,h=540,960
    img=Image.new('RGB',(w,h),PAPER);d=ImageDraw.Draw(img)
    background(d,(w,h),shot,p)
    x=mix(*shot['x'],p)*w
    height=mix(*shot['height'],p)*h
    foot=mix(*shot['foot_y'],p)*h
    angle=mix(*shot['orientation'],p)
    person(d,x,foot,height,angle,2*math.pi*(p*4.5*1.1+.10),shot['wardrobe'])
    if arrows:
        # Arrows belong only on planning boards, never the sketch film.
        if shot['movement']=='approach':arrow(d,(w*.29,h*.81),(w*.38,h*.91),width=4)
        else:arrow(d,(w*.19,h*.84),(w*.40,h*.84),width=4)
        if shot['movement']=='track':arrow(d,(w*.70,h*.18),(w*.89,h*.18),width=3,dashed=True)
    return img


def wrap(draw, text, ft, width):
    lines=[];current=''
    for c in text:
        if c=='\n':lines.append(current);current='';continue
        if draw.textlength(current+c,font=ft)>width and current:
            lines.append(current);current=c
        else:current+=c
    if current:lines.append(current)
    return lines


def textblock(draw,xy,text,size,width,fill=INK,bold=False,gap=1.45):
    ft=font(size,bold);x,y=xy
    for line in wrap(draw,text,ft,width):
        draw.text((x,y),line,font=ft,fill=fill);y+=round(size*gap)
    return y


def stamp_panel(canvas,xy,shot,p,size,arrows=True):
    im=frame(shot,p,arrows).resize(size,Image.Resampling.LANCZOS)
    canvas.paste(im,xy)
    d=ImageDraw.Draw(canvas);x,y=xy;w,h=size
    d.rectangle((x,y,x+w,y+h),outline=SOFT,width=1)


def boards():
    im=Image.new('RGB',(1560,930),PAPER);d=ImageDraw.Draw(im)
    d.text((46,28),'一週通勤穿搭靈感｜線條分鏡 v1',font=font(39,True),fill=INK)
    d.text((48,91),'先看整支：西外 → 短外套 → 格紋 → 裙裝 → 棕丹寧',font=font(25),fill=INK)
    d.text((48,133),'19.5 秒草稿  ·  同一人物五套  ·  每次接續 0.75 秒疊化',font=font(22),fill=ACCENT)
    for i,s in enumerate(PLAN['shots']):
        x=48+i*301
        d.text((x,190),f"0{i+1}  {s['title']}",font=font(24,True),fill=INK)
        stamp_panel(im,(x,237),s,.48,(260,462))
        start,end=s['timeline_interval'];clear=s['clear_interval']
        textblock(d,(x,720),f'{start:g}–{end:g} 秒',23,270,ACCENT,True)
        textblock(d,(x,760),s['viewing_point'],22,268)
    d.text((48,874),'實線箭頭：人物走向　虛線箭頭：攝影機跟拍　｜　線稿只預覽構圖與時間，衣服與動作仍須實片驗收。',font=font(20),fill=INK)
    im.save(HERE/'overview.png')
    for page,(offset,shots) in enumerate([(0,PLAN['shots'][:3]),(3,PLAN['shots'][3:])],1):
        row_h=555;im=Image.new('RGB',(1470,190+row_h*len(shots)),PAPER);d=ImageDraw.Draw(im)
        d.text((42,27),f'起點 → 終點｜分鏡詳圖 {page}/2',font=font(36,True),fill=INK)
        d.text((44,87),'先看人物尺度、動作與相鄰接點；圖外文字與箭頭僅為製作註記。',font=font(23),fill=INK)
        for i,s in enumerate(shots):
            y=156+i*row_h
            d.text((42,y),f"{offset+i+1:02d}  {s['title']}",font=font(27,True),fill=INK)
            stamp_panel(im,(44,y+55),s,0,(216,384))
            stamp_panel(im,(298,y+55),s,1,(216,384))
            arrow(d,(272,y+238),(286,y+238),width=3)
            d.text((44,y+448),'起點',font=font(22),fill=INK);d.text((298,y+448),'終點',font=font(22),fill=INK)
            x,yy=564,y+53
            start,end=s['timeline_interval'];a,b=s['clear_interval']
            yy=textblock(d,(x,yy),f'時間 {start:g}–{end:g} 秒；清楚讀衣 {b-a:g} 秒',25,850,ACCENT,True)+8
            yy=textblock(d,(x,yy),'看點｜'+s['viewing_point'],25,850,bold=True)+12
            yy=textblock(d,(x,yy),'動作｜'+s['action'],23,850)+10
            yy=textblock(d,(x,yy),'鏡頭｜'+s['camera'],23,850)+10
            yy=textblock(d,(x,yy),'接續｜'+s['join_after'],23,850)+10
            yy=textblock(d,(x,yy),'服裝｜'+s['outfit'],22,850)
            if yy>y+row_h-25:raise RuntimeError('Board text exceeds row')
            d.line((44,y+row_h-26,1424,y+row_h-26),fill=LIGHT,width=2)
        im.save(HERE/f'detailed_board_{page:02d}.png')


def video():
    fps=PLAN['fps'];n=round(PLAN['total_seconds']*fps)
    out=HERE/'sketch_animatic.mp4'
    exe=imageio_ffmpeg.get_ffmpeg_exe()
    args=[exe,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo',
          '-s','540x960','-pix_fmt','rgb24','-r',str(fps),'-i','-',
          '-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    proc=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for f in range(n):
            t=f/fps
            active=[s for s in PLAN['shots'] if s['timeline_interval'][0]<=t<s['timeline_interval'][1]]
            if len(active) not in [1,2]:raise ValueError(f'Timeline gap/overlap at{t}')
            im=frame(active[0],(t-active[0]['timeline_interval'][0])/PLAN['shot_seconds'])
            if len(active)==2:
                nxt=active[1];alpha=(t-nxt['timeline_interval'][0])/PLAN['overlap_seconds']
                im=Image.blend(im,frame(nxt,(t-nxt['timeline_interval'][0])/PLAN['shot_seconds']),alpha)
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        stderr=proc.stderr.read().decode('utf-8','replace')
        if proc.wait()!=0:raise RuntimeError(stderr)
    except Exception:
        proc.kill();raise
    # Verify actual encoded geometry, frame count and absence of audio once.
    scan=subprocess.run([exe,'-hide_banner','-i',str(out),'-map','0:v:0','-f','null','-'],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if scan.returncode:raise RuntimeError(scan.stderr)
    if 'Audio:' in scan.stderr:raise RuntimeError('Unexpected audio')
    import re
    counts=re.findall(r'frame=\s*(\d+)',scan.stderr)
    actual=int(counts[-1])
    if actual!=n:raise RuntimeError(f'Wrong frames {actual}!={n}')
    record={'stage':'line_storyboard_not_generated_footage','seconds':n/fps,'frames':actual,'fps':fps,'pixels':[540,960],
            'audio':False,'baked_text':False,'arrows_in_video':False,'timing_match':True,
            'joins':[s['interval'] for s in PLAN['joins']],
            'photoreal_assets_generated':0,'grok_calls':0,'existing_media_modified':False,
            'full_film_user_approval':None,'actual_gait_or_dynamic_quality_verified':False,
            'files':{}}
    for name in ['overview.png','detailed_board_01.png','detailed_board_02.png','sketch_animatic.mp4','storyboard_plan.json']:
        p=HERE/name;record['files'][name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    (HERE/'render_receipt.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'frames':actual,'seconds':n/fps,'directory':str(HERE)},ensure_ascii=False))


if __name__=='__main__':
    assert len(PLAN['shots'])==5
    assert PLAN['total_seconds']==len(PLAN['shots'])*PLAN['shot_seconds']-(len(PLAN['shots'])-1)*PLAN['overlap_seconds']
    boards();video()
