from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,csv,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent;P=RUN/'planning'
J1=RUN/'generated_images/2026-W44-001/looks/2026-W44-001-L01/reel'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
proof=J1/'2026-W44-001-L01_M02_reel_styling_proof_candidate_A.png'
assert sha(proof)=='b971d913fd7fa9974e3c922dda568b70a939f68b48b720e25233b1ffc293b1c9'
approval=J1/'user_proof_still_approval_2026-10-28.json'
write(approval,{'actor':'user','decision':'approved','scope':'still','target_sha256':sha(proof),'quote':'ok','recorded_at':'2026-10-28','context':'Direct reply to displayed L01 styling proof and explicit question whether it may be retained','limits':'Exact independent styling-proof still, not a later route frame, generated motion or publication approval'})
p=J1/'styling_proof_receipt_2026-10-28.json';v=read(p);v['status']='user_approved_still';v['new_still_approved']=True;v['approval_receipt']=approval.name;write(p,v)
pp=P/'series_01/production_plan.json';plan=read(pp)
if not any(a.get('asset_id')=='L01_styling_proof_candidate' for a in plan['approvals']):
 plan['approvals'].append({'asset_id':'L01_styling_proof_candidate','scope':'still','decision':'approved','target_sha256':sha(proof),'receipt_path':approval.relative_to(R).as_posix()})
plan['status']='L01_full_and_proof_approved_L02_entry_prepared';write(pp,plan)

def raster(svg,width):
 root=ET.fromstring(svg);vw,vh=map(float,root.attrib['viewBox'].split()[2:]);scale=width/vw
 im=Image.new('RGB',(width,round(vh*scale)),'#faf9f4');d=ImageDraw.Draw(im)
 def pts(val):return [tuple(float(c)*scale for c in p.split(',')) for p in val.split()]
 for el in root:
  a=el.attrib;tag=el.tag.split('}')[-1];fill=a.get('fill');fill=None if fill in [None,'none'] else fill;stroke=a.get('stroke');lw=max(1,round(float(a.get('stroke-width',1))*scale))
  if tag=='polygon':
   ps=pts(a['points']);d.polygon(ps,fill=fill)
   if stroke:d.line(ps+[ps[0]],fill=stroke,width=lw)
  elif tag=='polyline':d.line(pts(a['points']),fill=stroke,width=lw)
  elif tag=='line':d.line([(float(a['x1'])*scale,float(a['y1'])*scale),(float(a['x2'])*scale,float(a['y2'])*scale)],fill=stroke,width=lw)
  elif tag in ['circle','rect']:
   if tag=='circle':x,y,r=[float(a[k])*scale for k in ['cx','cy','r']];box=[x-r,y-r,x+r,y+r];d.ellipse(box,fill=fill,outline=stroke,width=lw)
   else:x,y,w,h=[float(a.get(k,0))*scale for k in ['x','y','width','height']];d.rectangle([x,y,x+w,y+h],fill=fill,outline=stroke,width=lw)
 return im
frames=read(P/'previs_frames.json');chosen=next(x for x in frames if x['frame']==150)
cam=P/'L02_entry_f150_camera.png';raster(chosen['camera'],540).save(cam)
combined=[];font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',18)
for f in frames[:-1]:
 overhead=raster(f['overhead'],325);camera=raster(f['camera'],225)
 im=Image.new('RGB',(600,490),'#f5f3ed');im.paste(overhead,(10,55));im.paste(camera,(360,55));d=ImageDraw.Draw(im)
 d.text((12,10),f"W44 示意預演  {f['seconds']:.3f}s  / f{f['frame']}",font=font,fill='#26313b');d.text((12,460),'人物棕／相機藍；非生成影片或物理步態驗證',font=font,fill='#26313b');combined.append(im)
combined[0].save(P/'route_previs_schematic_13p25s.gif',save_all=True,append_images=combined[1:],duration=[120,130]*53,loop=0)
# 106 samples x 0.125s average = 13.25s. No claim of continuous human playback review.
write(P/'L02_entry_requirement.json',{'date':'2026-10-28','shot':'S02','entry_global_frame':150,'entry_seconds':6.25,'overlap_global_frames':[150,168],'source_space_sha256':sha(P/'shared_space.json'),'source_previs_frames_sha256':sha(P/'previs_frames.json'),'camera_key_view':cam.relative_to(R).as_posix(),'key_view_sha256':sha(cam),'motion_preview':(P/'route_previs_schematic_13p25s.gif').relative_to(R).as_posix(),'correction':'Prior generic weekly look scene mistakenly said S01f0 for L02. Corrected below; garment change alone is not S02 route progress.','limits':'Key view derived from already approved schematic. Static f150 view checked; full timed native playback not visually verified. Approved photoreal L01 scene is uncalibrated and does not prove precise shared-space reprojection; new L02 remains a candidate.'})
lookpath=RUN/'weekly_look_plan.csv'
with lookpath.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for row in rows:
 if row['look_id']=='2026-W44-001-L02':
  row['scene']='同一辦公街廓路線S02 global f150／6.25秒接入；人物已沿路前進，相機按共同場地曲線移動。依planning/L02_entry_f150_camera.png核對；L01照片場地未校準，不能宣稱精確投影重建。'
  row['visible_action']='沿共同路線持續前進的接入姿態；不是返回S01f0原地換褲；步相需在實際影片與前鏡重疊18幀逐段驗收'
with lookpath.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
for surface in ['reel','carousel']:
 subprocess.run([sys.executable,str(R/'11_skills/mira-image-daily/scripts/prepare_daily_image_job.py'),'--project-root',str(R),'--run-dir',str(RUN),'--look-id','2026-W44-001-L02','--surface',surface],cwd=R,check=True,capture_output=True)
print(cam)
