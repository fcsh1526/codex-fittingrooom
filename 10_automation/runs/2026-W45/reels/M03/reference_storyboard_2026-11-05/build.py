"""Create directing diagrams, not generated fashion stills or a finished Reel."""
from pathlib import Path
import json, math, hashlib, copy
from PIL import Image, ImageDraw, ImageFont

P = Path(__file__).resolve().parent
ROOT = P.parents[5]
W = ROOT / '10_automation/runs/2026-W45'
INK, NAVY, PAPER, MUTED, ACCENT = '#253846', '#283747', '#f5f1e9', '#687477', '#a45a39'
FONT = 'C:/Windows/Fonts/msjh.ttc'
def font(size): return ImageFont.truetype(FONT, size)
def rel(path): return path.relative_to(ROOT).as_posix()
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def put(path, data): path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

# Screen-space directing targets. No physical camera calibration or gait is claimed.
keys = [
 {'t':0.0, 'title':'01  開場就看見兩種輪廓', 'detail':['同件西外；直褲／淺裙同時可讀。','從已核准首圖起勢，不先演等待。'], 'l':[0,0,0,0], 'r':[0,0,0,0], 'size':1.0},
 {'t':1.5, 'title':'02  主動展示，視線留給鏡頭', 'detail':['左側一手到腰，肩與下巴一起轉向。','右側一腳斜開，裙身自然展開。'], 'l':[-5,0.25,1,0], 'r':[0,-0.2,0,1], 'size':1.0},
 {'t':3.2, 'title':'03  短步與側角，各自給新資訊', 'detail':['左：斜向落步，讀直褲與西外側線。','右：一次轉成斜側面，讀裙幅。'], 'l':[-3,0.95,0,1], 'r':[3,-0.95,0,1], 'size':1.0},
 {'t':5.0, 'title':'04  帶著動勢回到正面', 'detail':['手臂隨身體回落，沒有重複搖擺。','完整鞋型最後讀清，再開始走近。'], 'l':[-2,0.1,0,0], 'r':[2,-0.12,1,0], 'size':1.0},
 {'t':6.8, 'title':'05  兩步靠近，畫面開始推進', 'detail':['放下手，短程向拍攝者靠近。','鏡頭末段輕抬，持續保留頭頂。'], 'l':[0,0.05,0,0.5], 'r':[0,-0.05,0,0.4], 'size':1.30},
 {'t':9.0, 'title':'06  更近地讀表情與西外', 'detail':['以頭至膝附近收尾，笑容有起落。','下腿出畫是預定景別，並非藏滑步。'], 'l':[0,0,0,0], 'r':[0,0,0,0], 'size':1.52},
]
put(P/'screen_targets.json', {'version':1,'units':'output pixels, schematic','canvas':[720,1280],
    'panel_rects':[[0,180,356,920],[364,180,356,920]], 'source_crop_720':[180,130,400,1034],
    'initial_figure_height_target':830,'camera':'stationary viewpoint; slight upward re-aim during approach, magnitude not measured',
    'limits':'Screen-space targets, not world projection, collision check, physical trajectory or gait simulation.', 'keys':keys})

def arrow(d, a, b, fill=ACCENT, width=4):
    d.line([a,b],fill=fill,width=width)
    ang=math.atan2(b[1]-a[1],b[0]-a[0]); L=13
    pts=[b,(b[0]-L*math.cos(ang-.5),b[1]-L*math.sin(ang-.5)),(b[0]-L*math.cos(ang+.5),b[1]-L*math.sin(ang+.5))]
    d.polygon(pts,fill=fill)

def actor(tile, look, pose, scale):
    d=ImageDraw.Draw(tile)
    off, turn, hiphand, step=pose
    h=830*scale; top=48; cx=178+off
    width=1-.35*abs(turn)
    def p(x,y): return (cx+(x*width+turn*.025*(.5-y))*h, top+(y+turn*x*.20)*h)
    def poly(coords, fill, outline=INK, w=3):
        pts=[p(x,y) for x,y in coords]; d.polygon(pts,fill=fill);d.line(pts+[pts[0]],fill=outline,width=w)
    def line(coords,fill=INK,w=4):d.line([p(x,y) for x,y in coords],fill=fill,width=w,joint='curve')
    # Grounded silhouettes are diagrams; interpolation is not a gait simulation.
    legshift=step*.025
    poly([(-.071,.49),(-.006,.49),(-.016-legshift,.72),(-.026-legshift,.97),(-.086-legshift,.97),(-.081-legshift,.73)], '#686d70' if look==0 else '#e1c5af')
    poly([(.006,.49),(.071,.49),(.079+step*.045,.72),(.086+legshift,.97-step*.035),(.026+legshift,.97-step*.035),(.015+step*.045,.72)], '#686d70' if look==0 else '#e1c5af')
    shoefill='#273238' if look==0 else '#eeebe5'
    poly([(-.088-legshift,.957),(-.029-legshift,.957),(-.02-legshift,.982),(-.104-legshift,.986)],shoefill)
    poly([(.026+legshift,.957-step*.035),(.083+legshift,.957-step*.035),(.118+legshift,.986-step*.035),(.019+legshift,.982-step*.035)],shoefill)
    if look==1:
        flare=.115+step*.012
        poly([(-.079,.46),(.079,.46),(flare,.84),(.005,.86),(-flare,.84)],'#eee6d4')
        for x in [-.06,-.02,.025,.06]:line([(x,.5),(x*1.5,.825)],'#b9b4a8',2)
    # Hair behind the jacket / head, never over the central shirt panel.
    poly([(-.065,.05),(.065,.05),(.079,.33),(.049,.38),(-.06,.32),(-.078,.16)],'#78634f')
    poly([(-.09,.20),(.09,.20),(.075,.47),(-.075,.47)],'#eeeae1')
    poly([(-.096,.20),(-.038,.18),(-.018,.31),(-.038,.53),(-.103,.51)],NAVY)
    poly([(.038,.18),(.096,.20),(.103,.51),(.038,.53),(.018,.31)],NAVY)
    if turn>.3:poly([(-.096,.20),(-.067,.21),(-.067,.51),(-.103,.51)],'#41515e')
    if turn<-.3:poly([(.067,.21),(.096,.20),(.103,.51),(.067,.51)],'#41515e')
    line([(-.038,.19),(-.071,.25),(-.032,.29),(-.02,.34)],'#b9c2c4',2)
    line([(.038,.19),(.071,.25),(.032,.29),(.02,.34)],'#b9c2c4',2)
    poly([(-.024,.146),(.024,.146),(.028,.20),(-.028,.20)],'#e1c5af')
    # Arms. Hand at waist opens the side silhouette without fingering the clothes.
    left=[(-.095,.22),(-.145,.36),(-.078,.43)] if hiphand>.4 else [(-.095,.22),(-.112,.39),(-.118,.56)]
    right=[(.095,.22),(.121,.36),(.092,.50)] if abs(turn)>.5 else [(.095,.22),(.115,.39),(.12,.56)]
    for arm in [left,right]:
        line(arm[:2],NAVY,max(8,int(h*.035)))
        line(arm[1:], '#e1c5af',max(7,int(h*.024)))
        endpoint=p(*arm[-1]); rr=max(4,int(h*.012))
        d.ellipse((endpoint[0]-rr,endpoint[1]-rr*1.5,endpoint[0]+rr,endpoint[1]+rr*1.5),fill='#e1c5af',outline=INK,width=2)
    # Existing small bag stays on model's left shoulder (screen right).
    line([(.075,.20),(.106,.44)],'#101d28',max(2,int(h*.007)))
    poly([(.081,.44),(.119,.44),(.12,.53),(.085,.54)],'#1f2c32')
    # Face and expressive eye direction are conceptual, not identity QA.
    headx=cx+turn*h*.025
    box=(headx-.051*h,top+.012*h,headx+.051*h,top+.158*h)
    d.ellipse(box,fill='#ead1bb',outline=INK,width=3)
    d.arc((box[0]-.008*h,box[1]-.012*h,box[2]+.006*h,box[3]),177,355,fill='#705b49',width=max(5,int(h*.017)))
    eye_y=top+.085*h
    for x in [-.021,.023]:
        ex=headx+x*h;d.arc((ex-.01*h,eye_y-.003*h,ex+.01*h,eye_y+.006*h),175,355,fill=INK,width=2)
        d.ellipse((ex-.0025*h,eye_y,ex+.0025*h,eye_y+.005*h),fill=INK)
    smile_depth=.018 if abs(turn)>.5 else (.027 if hiphand>.4 else .022)
    d.arc((headx-.02*h,top+.108*h,headx+.025*h,top+(.108+smile_depth)*h),5,170,fill=INK,width=2)
    if hiphand>.4:
        arrow(d,p(-.12,.50),p(-.08,.43),width=3)
    if abs(turn)>.25:
        y=top+.60*h;d.arc((cx-65,y,cx+65,y+35),5,160,fill=ACCENT,width=4)
    if step>.8:
        arrow(d,p(-.12,.94),p(-.15,.98),width=3)
    return {'hair_top':top,'shoe_bottom':top+.986*h,'shoulder_width':.192*h*width,
            'arm_envelope_x':[cx-.163*h*width if hiphand>.4 else cx-.132*h*width,cx+.134*h*width],
            'full_outfit_visible':top+.986*h<920,'head_inside':top>0 and top+.158*h<920}

def render_frame(key, labels=True):
    im=Image.new('RGB',(720,1280),PAPER);d=ImageDraw.Draw(im)
    reports=[]
    for side in range(2):
        tile=Image.new('RGB',(356,920),'#ece9e0');td=ImageDraw.Draw(tile)
        # Neutral location lines provide orientation only, no reconstructed site claim.
        for xx in [38,303]:td.line([(xx,0),(xx,920)],fill='#cbd0cb',width=2)
        for yy in [180,580,870]:td.line([(0,yy),(356,yy)],fill='#d6d8d0',width=2)
        rep=actor(tile,side,key['l' if side==0 else 'r'],key['size']);reports.append(rep)
        im.paste(tile,(side*364,180))
    if labels:
        d.text((30,35),'同一件西外，兩種穿法',font=font(31),fill=INK)
        d.text((30,90),f'{key["t"]:04.1f} s  /  09.0 s  ·  構圖與節奏示意',font=font(22),fill=MUTED)
        d.text((70,1135),'直褲・樂福鞋',font=font(23),fill=INK)
        d.text((425,1135),'淺裙・球鞋',font=font(23),fill=INK)
        d.line((30,1205,690,1205),fill='#c9c9bd',width=4)
        d.line((30,1205,30+660*key['t']/9,1205),fill=ACCENT,width=6)
        d.text((30,1230),'線稿預演｜不是生成結果或步態驗證',font=font(20),fill=MUTED)
    return im,reports

# Six connected views, same actual 9:16 output proportions.
board=Image.new('RGB',(1560,2020),PAPER);d=ImageDraw.Draw(board)
d.text((45,28),'M03｜把參考變成可見的畫面發展',font=font(42),fill=INK)
d.text((45,91),'全身比較 → 短步與角度呈現輪廓 → 靠近讀表情與西外層次',font=font(27),fill=MUTED)
d.text((45,138),'9秒提案・A左右並排・一人兩套・先完整讀衣，再進較近景別',font=font(23),fill=MUTED)
report=[]
for i,k in enumerate(keys):
    x=35+(i%3)*515;y=207+(i//3)*846
    d.text((x,y),k['title'],font=font(23),fill=INK)
    im,reps=render_frame(k,False);im=im.resize((369,656),Image.Resampling.LANCZOS)
    board.paste(im,(x+55,y+35));d.rectangle((x+55,y+35,x+424,y+691),outline='#b7b9b0',width=2)
    d.rounded_rectangle((x+63,y+46,x+146,y+80),radius=7,fill=PAPER)
    d.text((x+73,y+49),f'{k["t"]:g} 秒',font=font(20),fill=ACCENT)
    for j,txt in enumerate(k['detail']):d.text((x+8,y+710+j*34),txt,font=font(22),fill=INK)
    report.append({'time':k['t'],'panels':reps})
d.text((45,1918),'借用：leeharin 的姿態連動｜momoko 的角度展示與靠近｜mika 的注意與回應',font=font(23),fill=INK)
d.text((45,1962),'線稿只驗構圖、資訊順序與節奏；動作自然度、接地及頭身仍須實片驗收。',font=font(22),fill=MUTED)
board.save(P/'storyboard.png')
for i,k in enumerate(keys):render_frame(k)[0].save(P/f'key_{i+1:02d}.png')

# A timing animatic interpolates screen-space sketches; it is explicitly not a walk simulator.
frames=[]
for fi in range(72):
    t=9*fi/71
    a,b=keys[-2:]
    for ka,kb in zip(keys,keys[1:]):
        if ka['t']<=t<=kb['t']:a,b=ka,kb;break
    u=(t-a['t'])/(b['t']-a['t']);k={'t':t,'size':a['size']+(b['size']-a['size'])*u}
    for side in ['l','r']:k[side]=[va+(vb-va)*u for va,vb in zip(a[side],b[side])]
    frames.append(render_frame(k)[0].resize((540,960),Image.Resampling.LANCZOS))
frames[0].save(P/'timing_animatic.gif',save_all=True,append_images=frames[1:],duration=[120,130]*36,loop=0,optimize=False)

# Approved stills placed in the proposed physical layout; no new AI still or retouched asset.
mock=Image.new('RGB',(720,1280),PAPER);sources=[]
for side,look in enumerate(['L01','L02']):
    receipt=read(W/f'approvals/M03_{look}_still_approval_2026-11-04.json');src=ROOT/receipt['asset_path']
    assert sha(src)==receipt['target_sha256']
    im=Image.open(src).convert('RGB'); w,h=im.size
    # Cropping coordinates scale proportionally from a720x1280 reference raster.
    box=(180*w/720,130*h/1280,580*w/720,1164*h/1280)
    tile=im.crop(box).resize((356,920),Image.Resampling.LANCZOS)
    mock.paste(tile,(side*364,180));sources.append({'look':look,'path':rel(src),'sha256':sha(src),'original_size':[w,h],'crop_box_original':box})
mock.save(P/'approved_stills_layout.png')
put(P/'layout_preflight.json',{'status':'schematic_and_still_preflight_pending_visual_inspection','targets':report,'still_sources':sources,
    'start_picture_rects':[[0,180,356,920],[364,180,356,920]],'start_body_height_approx_percent':65,
    'end_framing':'head to knees, lower legs intentionally outside picture','end_scale_factor_schematic':1.52,
    'limits':['No physical world calibration','Sketch interpolation does not validate gait or hand anatomy','Actual new source needs full motion-envelope and continuous playback review','Original first images already smile; do not claim neutral-to-smile onset']})

# Film plan uses the existing contract, with honest pending storyboard/control evidence.
plan=read(ROOT/'11_skills/mira-reel-director/assets/production_plan.template.json')
plan.update(plan_id='W45_M03_reference_storyboard_v1_20261105',status='in_review',path_base='project',weeks={'source':['2026-W44','2026-W45'],'content':'2026-W45','delivery':None})
plan['editorial']={'audience':'台灣日常穿搭讀者','takeaway':'同件海軍藍西外，直褲的俐落直線與A字裙的展幅；再近看表情、領片與內搭。',
    'visual_theme':'直接對鏡頭展示造型：完整輪廓、連貫的大動作、較近的閱讀收尾','selection_rationale':'保留已選A並排，把11/4參考中的表演連動／角度資訊／靠近轉成三段可見發展；不為禁止舞蹈而凍結人物。'}
plan['presentation']={'layout_id':'parallel_comparison','recipe_id':'parallel_comparison','variant':'front-to-angled-to-near direct outfit presentation','evidence_status':'proposal; not a new mature method'}
plan['film']={'fps':24,'frame_count':216,'duration_seconds':9,'aspect_ratio':'9:16','native_speed':True,'baked_text':False}
original=read(W/'planning/M03/production_plan.json')
plan['models']=copy.deepcopy(original['models']);plan['looks']=copy.deepcopy(original['looks'])
for a in original['assets']:
    if a['kind']=='identity':assert sha(ROOT/a['path'])==a['sha256'];plan['assets'].append(a)
for look,src in zip(plan['looks'],sources):
    aid=src['look']+'_first';look['source_asset_ids']=[aid]
    plan['assets'].append({'id':aid,'kind':'still','path':src['path'],'sha256':src['sha256']})
    original_receipt=read(W/f'approvals/M03_{src["look"]}_still_approval_2026-11-04.json')
    normalized=dict(original_receipt);normalized['scope']='still';normalized['original_scope']=original_receipt['scope']
    normalized['original_receipt_path']=rel(W/f'approvals/M03_{src["look"]}_still_approval_2026-11-04.json')
    dest=P/f'{src["look"]}_existing_still_approval.json';put(dest,normalized)
    plan['approvals'].append({'asset_id':aid,'scope':'still','decision':'approved','target_sha256':src['sha256'],'receipt_path':rel(dest)})
for aid,kind,filename in [('board','storyboard','storyboard.png'),('animatic','previs','timing_animatic.gif'),('targets','source','screen_targets.json')]:
    path=P/filename;plan['assets'].append({'id':aid,'kind':kind,'path':rel(path),'sha256':sha(path)})
plan['shots']=[{'id':'P01','look_ids':[x['id'] for x in plan['looks']],'frames':[0,216],
    'clothing_purpose':'0–5秒完整輪廓與角度，5–9秒連續靠近讀表情、西外領片與內搭。',
    'clear_read_intervals':[[0,120],[168,216]],'storyboard_asset_id':'board','previs_asset_id':'animatic',
    'input_asset_ids':['L01_first','L02_first'],'scene_reference_asset_ids':[],'space_mode':'independent','execution_mode':'generate',
    'camera':'fixed position; slight upward re-aim during approach to retain complete head; no zoom/dolly proposed',
    'panels':[{'id':'left','look_id':plan['looks'][0]['id'],'input_asset_id':'L01_first'},{'id':'right','look_id':plan['looks'][1]['id'],'input_asset_id':'L02_first'}],
    'performance_beats':keys,'source_duration_note':'Request10s per source if currently available; editorial target9s depends on actual useful footage. No stretch, freeze, retime or repeated raw intervals.'}]
plan['missing_assets']=['新連接線稿／構圖節奏示意尚未取得視覺回饋；此前ok授權製作分鏡，不補寫為新圖或成片接受。','生成當下可用控制、額度、單側表演與末段構圖尚待實測。']
plan['existing_identity_authority']={'path':'02_brand/mira_reference_images.csv','status':'approved M03v3 face/full retained','note':'Legacy exact identity receipts are not normalized into this checker; do not request identity approval again solely for schema.'}
plan['reference_mapping']=[
 {'reference':'03_research/ig_feed_study_2026-11-04/REVIEW.md','account':'leeharin.xoxo','url':'https://www.instagram.com/reels/Del9QXDzMdn/','observed_seconds':'approx0–2.8','mapped_film_frames':[0,120],'borrow':'head/gaze/arms/body acting together; changing expression','exclude':'lip-contact and hip-sway choreography'},
 {'reference':'03_research/ig_feed_study_2026-11-04/REVIEW.md','account':'momoko_takasaki','url':'https://www.instagram.com/reels/DfKLi-huVMY/','observed_seconds':'approx3.6–9;9–11.4','mapped_film_frames':[36,216],'borrow':'angle adds garment information; approach adds reading scale','exclude':'two different people, product overlays and exact costume'},
 {'reference':'03_research/ig_reference_Db8AXqwpkef_2026-11-02/REFERENCE_STUDY.md','account':'mika.dono3','url':'https://www.instagram.com/mika.dono3/reel/Db8AXqwpkef/','mapped_film_frames':[120,216],'borrow':'camera-directed attention and an approach with a response','exclude':'crossing story and looking for traffic, which this office setting does not require'}]
plan['generation_scope']={'submitted':0,'first_test':'one L01 source only after this storyboard is resolved','new_stills_planned':0,'total_sources_if_successful':2,'service':'existing Grok; no new service or purchase','retries':'no automatic retries; same mechanism failure twice requires redesign'}
put(P/'production_plan.json',plan)
put(P/'user_continuation.json',{'actor':'user','quote':'ok','recorded_at':'2026-11-05','scope':'Continue concrete reference-mapped storyboard after audit; another ok during the ongoing work reiterates continuation.','limits':'Not acceptance of unseen board, new still, motion source, final film or publication.'})
print(json.dumps({'output':rel(P),'storyboard':True,'animatic_seconds':9,'new_AI_stills':0,'new_Grok_jobs':0}))
