"""Schematic directing boards and diagnostic layout; never modifies source stills."""
import copy, hashlib, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[6]
HERE=Path(__file__).resolve().parent
TRIAL=ROOT/'10_automation/runs/2026-W45/reels/M03/expressive_parallel_2026-11-05/trial_01'
TRIAL.mkdir(parents=True,exist_ok=True)
if (TRIAL/'submission.json').exists():
    raise SystemExit('Provider result exists. Preserve frozen prompts/shot record; create a separate revision before rebuilding.')
FONT='C:/Windows/Fonts/msjh.ttc'
def font(n):return ImageFont.truetype(FONT,n)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def savej(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
old=json.loads((HERE.parent/'production_plan.json').read_text(encoding='utf-8-sig'))
stillpaths=[ROOT/f'10_automation/runs/2026-W45/generated_images/2026-W45-003/looks/2026-W45-003-L0{i}/reel/2026-W45-003-L0{i}_M03_reel_candidate_A{suffix}.png' for i,suffix in [(1,'_framing_v2'),(2,'')]]
assert sha(stillpaths[0])=='d62277fdb318f1e799f534f3b610d092895585ffa769338f222cddb090f618dd'
assert sha(stillpaths[1])=='2a7069a0ce028a1c3a80aa5e0800b67369c9f5ecd8ec3a60c1bf26d032cf2c6d'

# Normalized positions in each NARROW output panel, not a measured 3D camera model.
base={'head':(.5,.205),'hip':(.5,.565),'shoulderL':(.29,.31),'shoulderR':(.71,.31),'elbowL':(.24,.43),'handL':(.27,.55),'elbowR':(.76,.43),'handR':(.73,.55),'footL':(.39,.88),'footR':(.61,.88)}
def pose(**changes):return dict(base,**changes)
left=[(0,pose()),(1.0,pose(hip=(.47,.565),footL=(.32,.88),footR=(.60,.88))),
 (2.5,pose(head=(.47,.20),hip=(.47,.565),shoulderL=(.27,.31),elbowL=(.16,.205),handL=(.32,.08),footL=(.32,.88),footR=(.60,.88))),
 (3.6,pose(hip=(.47,.565),footL=(.32,.88))),
 (5,pose(head=(.47,.205),hip=(.48,.565),shoulderL=(.36,.31),shoulderR=(.67,.31),elbowL=(.24,.44),handL=(.39,.54))),
 (7,pose(head=(.46,.205),shoulderL=(.39,.31),shoulderR=(.62,.31),hip=(.46,.565),footL=(.36,.88),footR=(.57,.88))),
 (9.25,pose(head=(.48,.205),elbowL=(.17,.43),handL=(.38,.55),hip=(.48,.565)))]
right=[(0,pose()),(1.5,pose(hip=(.54,.565),footL=(.40,.88),footR=(.69,.88))),
 (2.5,pose(head=(.52,.205),hip=(.55,.565),elbowL=(.17,.43),handL=(.38,.55),elbowR=(.83,.43),handR=(.64,.55),footR=(.69,.88))),
 (5,pose(head=(.54,.205),hip=(.52,.565),shoulderL=(.38,.31),shoulderR=(.64,.31))),
 (7,pose(head=(.53,.20),hip=(.53,.565),elbowL=(.19,.20),handL=(.34,.085),elbowR=(.83,.43),handR=(.64,.55))),
 (9.25,pose(head=(.54,.205),hip=(.55,.565),elbowL=(.18,.44),handL=(.39,.55),footR=(.68,.88)))]
def at(keys,t):
 for (a,p),(b,q) in zip(keys,keys[1:]):
  if a<=t<=b:
   u=(t-a)/(b-a);u=u*u*(3-2*u)
   return {k:(p[k][0]*(1-u)+q[k][0]*u,p[k][1]*(1-u)+q[k][1]*u) for k in p}
 return keys[-1][1]
def figure(d,box,p,skirt=False):
 x,y,w,h=box
 def pt(v):return (int(x+v[0]*w),int(y+v[1]*h))
 navy='#213a55';skin='#d5a890';ink='#34434b'
 head=pt(p['head']);rx=int(w*.108);ry=int(h*.050)
 d.ellipse((head[0]-rx,head[1]-ry,head[0]+rx,head[1]+ry),fill=skin,outline=ink,width=2)
 d.line([pt((p['head'][0],p['head'][1]+.05)),pt((p['head'][0],.30))],fill=ink,width=4)
 sl,sr=p['shoulderL'],p['shoulderR'];hx,hy=p['hip']
 d.polygon([pt(sl),pt(sr),pt((hx+.14,hy)),pt((hx-.14,hy))],fill=navy)
 if skirt:d.polygon([pt((hx-.13,hy)),pt((hx+.13,hy)),pt((hx+.27,.77)),pt((hx-.27,.77))],fill='#e5ddc9',outline=ink)
 else:
  for a,b in [((hx-.09,hy),p['footL']),((hx+.09,hy),p['footR'])]:d.line([pt(a),pt((b[0],b[1]-.025))],fill='#575b60',width=max(5,int(w*.12)))
 for side in ['L','R']:
  d.line([pt(p['shoulder'+side]),pt(p['elbow'+side]),pt(p['hand'+side])],fill=navy,width=max(4,int(w*.07)))
  q=pt(p['hand'+side]);d.ellipse((q[0]-4,q[1]-5,q[0]+4,q[1]+5),fill=skin)
  f=pt(p['foot'+side]);d.line([(f[0]-8,f[1]),(f[0]+10,f[1])],fill=ink,width=5)
 # Same physical left shoulder bag, on image-right. Graphic only.
 d.line([pt(sr),pt((hx+.21,.53))],fill='#191e24',width=2)
 bx,by=pt((hx+.20,.54));d.rounded_rectangle((bx-10,by-5,bx+10,by+28),radius=3,fill='#191e24')
def frame(t,size=(360,640),labels=True):
 im=Image.new('RGB',size,'#f5f3ec');d=ImageDraw.Draw(im);w,h=size;gap=6;pw=(w-gap)//2
 for n,(keys,skirt) in enumerate([(left,False),(right,True)]):
  x=n*(pw+gap);d.rectangle((x,0,x+pw-1,h-1),outline='#b5bab6',width=1)
  d.rectangle((x+.08*pw,.055*h,x+.92*pw,.94*h),outline='#b9cabd',width=1)
  figure(d,(x,0,pw,h),at(keys,t),skirt)
 d.rectangle((pw,0,pw+gap,h),fill='#f5f3ec')
 if labels:
  d.text((8,h-47),'褲裝',font=font(15),fill='#293a43');d.text((pw+gap+8,h-47),'裙裝',font=font(15),fill='#293a43')
  d.text((8,h-25),f'{t:04.2f}s｜示意，非生成影片',font=font(13),fill='#576165')
 return im
times=[0,2.5,4.2,5,7,9.25]
titles=['亮相｜完整兩套','動作高點｜抬臂／叉腰','收手後轉向','第二段銜接','換另一側成為動作主角','自然收姿｜完整讀衣']
board=Image.new('RGB',(1200,1640),'#f5f3ec');d=ImageDraw.Draw(board)
d.text((28,18),'M03｜同件西外，兩種穿法 × 完整換姿表演',font=font(32),fill='#203846')
d.text((28,64),'9.25秒剪輯草圖｜固定鏡位｜兩段各5秒，重疊0.75秒｜本輪只測左側第一段',font=font(20),fill='#596465')
for i,(t,title) in enumerate(zip(times,titles)):
 x=22+(i%3)*398;y=112+(i//3)*748
 d.text((x,y),f'{i+1}. {t:g}s  {title}',font=font(18),fill='#203846')
 board.paste(frame(t),(x+8,y+36))
 d.text((x+8,y+687),'綠框：預留動作區；非實測人物邊界',font=font(15),fill='#56675b')
board.save(HERE/'storyboard.png')
frames=[frame(i/12) for i in range(112)]
frames[0].save(HERE/'motion_previs.gif',save_all=True,append_images=frames[1:],duration=83,loop=0)

layout=Image.new('RGB',(720,1280),'#f5f3ec')
for i,p in enumerate(stillpaths):
 source=Image.open(p).convert('RGB');crop=source.crop((236,0,701,1672));crop.thumbnail((356,1280),Image.Resampling.LANCZOS)
 layout.paste(crop,(i*364,0))
layout.save(HERE/'approved_stills_layout.png')
savej(HERE/'layout_review.json',{'purpose':'diagnostic composition only; not a new AI source still','output':[720,1280],'source_crop':[236,0,701,1672],'panel_width':356,'gutter':8,'sources':[{'path':rel(p),'sha256':sha(p),'size':list(Image.open(p).size)} for p in stillpaths],'human_estimated_head_to_sole_height_fraction':[.735,.735],'limits':'Source first-frame bounds visually checked; future arm/bag/foot bounds require actual generated motion review. No measured3D route or motion guarantee.'})
savej(HERE/'choreography.json',{'coordinates':'normalized per output panel, top-left origin; schematic/unmeasured','left':left,'right':right,'film_seconds':9.25,'source_timing_note':'Graphic interpolations explain planned poses, not physically simulated human movement. S01/S02 have0.75s overlap; pose continuity must be revised from actual source endpoints.'})

plan=copy.deepcopy(old);plan.update(plan_id='W45_M03_expressive_parallel_draft_2026-11-05',status='draft')
plan['editorial'].update(takeaway='同件海軍藍西外，直接比較俐落褲裝與柔和裙裝，觀看有起落的換姿展示',visual_theme='自在自信、帶玩心的全身時裝展示',selection_rationale='使用者要求明顯且多樣的表演，而非僅微幅擺身；借參考的角度與姿態發展，不推定原片製作方法')
plan['presentation']={'layout_id':'parallel_comparison','recipe_id':'parallel_comparison'}
plan['film'].update(frame_count=222,duration_seconds=9.25)
plan['assets']=[a for a in plan['assets'] if a['kind']=='identity']
for i,p in enumerate(stillpaths,1):plan['assets'].append({'id':f'still_L0{i}','kind':'still','path':rel(p),'sha256':sha(p)})
for i,look in enumerate(plan['looks'],1):look['source_asset_ids']=[f'still_L0{i}']
plan['assets'].append({'id':'new_board','kind':'storyboard','path':rel(HERE/'storyboard.png'),'sha256':sha(HERE/'storyboard.png')})
plan['shots']=[]
for sid,bounds,reads,perf in [('P01',[0,120],[[0,102]],'左右完整亮相，先左抬臂右叉腰；收手後轉向'),('P02',[102,222],[[120,222]],'左側轉後回正，右側抬臂／換姿，完整收束')]:
 plan['shots'].append({'id':sid,'look_ids':[x['id'] for x in plan['looks']],'frames':bounds,'clothing_purpose':'並排看同件西外下的褲裙及鞋款差異，動作展現輪廓','clear_read_intervals':reads,'storyboard_asset_id':'new_board','previs_asset_id':None,'input_asset_ids':['still_L01','still_L02'] if sid=='P01' else [],'scene_reference_asset_ids':[],'space_mode':'independent','execution_mode':'generate','camera':'fixed','panels':[{'id':'left','look_id':plan['looks'][0]['id']},{'id':'right','look_id':plan['looks'][1]['id']}],'performance':perf})
plan['transitions']=[{'from_shot':'P01','to_shot':'P02','frames':[102,120],'overlap_frames':18,'method':'cross_dissolve'}]
plan['approvals']=[]
plan['missing_assets']=['完整並排片仍需兩側來源與第二段可用起點／相鄰接點證據；不得用6秒來源延長為9.25秒','本圖為助理新繪製分鏡，使用者尚未看過精確圖；既有ok授權規劃及一側短測，非整片視覺接受','完整計畫的身份／首圖核准收據需依現有精確紀錄連接，不能補造核准']
savej(HERE/'production_plan.json',plan)

prompt="""She is playfully and confidently showing her outfit to the camera, flowing through a clear full-body posing phrase. Start from the exact approved image. First she takes one small side-step to her right (image-left) and settles her weight, lifting her free right arm with a bent elbow so her hand reaches just above her hair. Her chest opens and her hips angle naturally; the other arm stays comfortably beside the bag. Let the lifted pose read briefly. She then lowers that arm before making a clear quarter-turn toward image-left, and finishes looking back to the lens in an easy, self-assured pose. Her head, gaze, expression, arms and fabric respond together, with ordinary pauses and a relaxed changing smile. This is an intentional, lively outfit demonstration with visible pose changes.

One continuous six-second real-time full-person shot from the original fixed, level chest-height 50mm camera. Keep her at the original distance, complete hair, raised hand and both shoes visible. Keep the action compact across the frame, with no horizontal arm spread; leave both side margins for a later narrow-panel layout. Preserve the same M03 face, long wavy brown hair, open deep-navy blazer, white crewneck tee, charcoal straight trousers, black loafers, small black bag on her left shoulder and silver necklace. Keep the shaded office wall, windows, bench, paving and daylight coherent. Natural grounded foot repositioning and responsive cloth. No camera move, full spin, outfit change, slow motion or text."""
(TRIAL/'video_prompt.txt').write_text(prompt+'\n',encoding='utf-8')
request='''本輪只生成一支全新 M03 W45 褲裝「完整換姿表演」短測，不是11/4微幅轉身退件片。使用者已同意先完成動作分鏡與雙欄活動空間，再測一側；本機圖已畫好。只此一次6秒720p原生9:16，不生成照片、不重試、不製作右側或整片、不加購／換服務、不改刪舊媒體。
精確First frame: 2e8df556-7034-4788-92d8-3a769fcdfed3（核准framing_v2，長棕捲髮M03，深藍西外／白T／炭灰直褲／黑樂福／黑左肩包，辦公樓遮簷長凳，全身約74%畫高）。
身份參照asset_ids: ["26e03f42-2907-488c-b75c-239a2a19b9c8","15c720b2-46b6-45e0-a150-60290e3290e6"]，M03 v3臉及全身只鎖身份／普通比例，不複製棚拍衣服。
先實際查看三個UUID及當下可用設定；若找不到、內容不符、額度不足或6秒設定拒絕，停下回報，不能代換。duration:"6", resolution_name:"720p", aspect_ratio:"9:16"；不設last或keyframes。畫布舊選取不是輸入。注意包在她左肩，抬的是沒有背包的右臂；先落臂再轉身，避免同時扭轉與展臂。
以下英文逐字作prompt，標記不傳入：
PROMPT_BEGIN
'''+prompt+'''
PROMPT_END
音訊有實際開關才關，否則如實回報，別為聲音重生。完成保留唯一原片，列實際First/identity IDs、新影片UUID、設定與輸出時長／尺寸／音軌。參數接受、抽樣觀察、真人感與物理驗收分開；不要自行宣稱通過。
'''
(TRIAL/'grok_request.txt').write_text(request,encoding='utf-8')
savej(TRIAL/'shot_plan.json',{'date':'2026-11-05','status':'prepared_not_submitted','user_authorization_quote':'ok','authorization_context':'Direct assent to draw action onset/peak/settle and dual-panel space, then test one more expressive motion segment; no unseen still or finished-film approval.','first_frame_asset_id':'2e8df556-7034-4788-92d8-3a769fcdfed3','identity_asset_ids':['26e03f42-2907-488c-b75c-239a2a19b9c8','15c720b2-46b6-45e0-a150-60290e3290e6'],'source_still':rel(stillpaths[0]),'source_still_sha256':sha(stillpaths[0]),'still_approval':'10_automation/runs/2026-W45/approvals/M03_L01_still_approval_2026-11-04.json','storyboard':rel(HERE/'storyboard.png'),'storyboard_sha256':sha(HERE/'storyboard.png'),'schematic_poses_are_not_new_AI_stills':True,'prompt_sha256':sha(TRIAL/'video_prompt.txt'),'max_new_jobs':1,'full_film_generation_authorized':False,'new_still_calls':0,'new_jobs_submitted':0,'native_speed_required':True,'remaining_quota':'unknown','model_version':'unknown','seed':'unknown'})
print(json.dumps({'boards':rel(HERE/'storyboard.png'),'source_stills_unchanged':True,'trial_prepared':True,'new_jobs':0}))
