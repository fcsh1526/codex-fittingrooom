from pathlib import Path
import sys, math, json, hashlib
from datetime import datetime, timezone, timedelta
ROOT=Path.cwd()
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
from PIL import Image, ImageDraw
import imageio_ffmpeg
BASE=ROOT/'03_research/series_pilots_2026-10-15/commute_week_v1'
OUT=BASE/'editorial_reset_2026-10-21/gait_continuity_2026-10-22'
FRONT=OUT/'front_sources'; JOINS=OUT/'joins'
FRONT.mkdir(parents=True,exist_ok=True); JOINS.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
S={
 'F01':(BASE/'production_bridge_2026-10-19/F01/F01_source.mp4','6a9bf3204aadad28dc710aa914592e26851a03e47209c5bd9b682286b184fa50'),
 'F02':(BASE/'production_bridge_2026-10-19/F02/motion_retry_01/F02_source.mp4','cc23a3e22b5d51b2db42cc87b33371f73189b25b101cc37fff3a070dd68800b0'),
 'F03':(BASE/'production_bridge_2026-10-19/F03/F03_source.mp4','26087d5c7f4fd7dd8153b9c0c5a70fcdeea0429c0e8def12dc672632a9b499d5'),
 'F04':(BASE/'editorial_reset_2026-10-21/F04_motion_01/F04_source.mp4','e32ee2f282b80dec8b8666d6755c9d2e77e5def6850bc53c89b5333927cd2208'),
 'F05':(BASE/'editorial_reset_2026-10-21/F05_half_motion_01/F05_half_source.mp4','c2d9f0442ea0d9b9c50674fb959b96ae53a8264c3947c509aa91f05e4bec9aa9'),
 'film':(BASE/'editorial_reset_2026-10-21/F05_half_motion_01/five_look_review_2026-10-22/v1/review.mp4','e4ed855809463e9c8421c5c7d4292f62bdf3f12f1c5f30af8f5c0e0a4edd32dc')}
CACHE={}; RECORD={}
for k,(p,h) in S.items():
 assert sha(p)==h,(k,'hash mismatch')
 rr=imageio_ffmpeg.read_frames(str(p),pix_fmt='rgb24'); meta=next(rr)
 assert tuple(meta['size'])==(720,1280) and meta['fps']==24
 frames=[]
 for raw in rr: frames.append(Image.frombytes('RGB',(720,1280),raw))
 rr.close(); CACHE[k]=frames
 RECORD[k]={'path':str(p),'sha256':h,'fps':24,'decoded_frames':len(frames),'PTS_measured':False}
def save_sheet(items,path,title,columns=5):
 w=230; h=205
 im=Image.new('RGB',(columns*w,40+math.ceil(len(items)/columns)*h),'#f5f3ef'); d=ImageDraw.Draw(im)
 d.text((5,7),title,fill='black')
 for j,(label,frame) in enumerate(items):
  x=(j%columns)*w; y=40+(j//columns)*h
  d.text((x+3,y+2),label,fill='black')
  cr=frame.crop((0,740,720,1280)); cr.thumbnail((224,168),Image.Resampling.LANCZOS)
  im.paste(cr,(x+(w-cr.width)//2,y+28))
 assert not path.exists(),path
 im.save(path)
 return {'path':str(path),'sha256':sha(path),'labels':[a for a,b in items]}
boards=[]
for k,a,b in [('F01',0,78),('F02',0,145),('F03',1,109)]:
 ii=sorted(set(range(a,b,3))|{b-1})
 boards.append(save_sheet([(f'{k} f{i} / {i/24:.3f}s',CACHE[k][i]) for i in ii],FRONT/f'{k}_every3_foot.png',f'{k} native-frame QA ONLY; crop y740:1280; unretimed'))
joins=[]
for name,a,ao,b,bi,fo in [('J12','F01',60,'F02',0,60),('J23','F02',127,'F03',1,187),('J34','F03',91,'F04',0,277),('J45','F04',90,'F05',0,367)]:
 items=[]; mapping=[]
 for o in [0,3,6,9,12,15,17]:
  items.extend([(f'OUT {a} f{ao+o}/{(ao+o)/24:.3f}s',CACHE[a][ao+o]),(f'IN {b} f{bi+o}/{(bi+o)/24:.3f}s',CACHE[b][bi+o]),(f'MIX f{fo+o}/{(fo+o)/24:.3f}s',CACHE['film'][fo+o])])
  mapping.append({'overlap_offset':o,'outgoing_source':a,'outgoing_frame':ao+o,'incoming_source':b,'incoming_frame':bi+o,'film_frame':fo+o,'film_second':(fo+o)/24})
 boards.append(save_sheet(items,JOINS/f'{name}_paired_foot.png',f'{name} OUT / IN / actual current mix; QA-only crop',3))
 joins.append({'name':name,'map':mapping})
rec={'date_taipei':datetime.now(timezone(timedelta(hours=8))).isoformat(),'purpose':'read-only motion diagnostic; no movie creation or source mutation','crop_QA_only_xyxy':[0,740,720,1280],'source_records':RECORD,'source_selection_half_open':{'F01':[0,78],'F02':[0,145],'F03':[1,109]},'boards':boards,'join_mapping':joins,'no_speed_change':True,'visual_measurement_not_established':True}
(FRONT/'diagnostic_receipt.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'boards':len(boards),'status':'inspection-only ready'},ensure_ascii=False))
