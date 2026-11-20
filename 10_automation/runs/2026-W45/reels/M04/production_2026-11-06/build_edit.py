from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;ROOT=P.parents[5];FF=ROOT/'openmontage/.local/bin/ffmpeg.exe';PROBE=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
src=P/'S01_source.mp4';out=P/'M04_W45_floral_single_review_v1.mp4'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='c6380ee2cac2a9b731e1a4bc07d034462a30efb04d380cff72dc5ec310265595'
def run(args):
 r=subprocess.run([str(x) for x in args],capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-3000:])
 return r.stdout
f='[0:v]fps=24,split=3[x][y][z];[x]trim=start_frame=0:end_frame=96,setpts=PTS-STARTPTS,settb=1/24,fps=24[a];[y]trim=start_frame=96:end_frame=174,setpts=PTS-STARTPTS,crop=360:640:185:250,scale=720:1280,settb=1/24,fps=24[b];[z]trim=start_frame=174:end_frame=241,setpts=PTS-STARTPTS,settb=1/24,fps=24[c];[a][b]xfade=transition=fade:duration=0.75:offset=3.25,fps=24,settb=1/24[ab];[ab][c]xfade=transition=fade:duration=0.75:offset=5.75[v]'
run([FF,'-v','error','-y','-i',src,'-filter_complex',f,'-map','[v]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-frames:v','205','-movflags','+faststart',out])
probe=json.loads(run([PROBE,'-v','error','-show_streams','-show_format','-of','json',out]));video=next(x for x in probe['streams'] if x['codec_type']=='video');assert video['nb_frames']=='205'
run([FF,'-v','error','-i',out,'-f','null','-'])
qa=P/'edit_qa';qa.mkdir(exist_ok=True)
run([FF,'-v','error','-y','-i',out,'-vf','select=not(mod(n\\,3))','-fps_mode','vfr','-q:v','2',qa/'frame_%03d.jpg'])
files=sorted(qa.glob('frame_*.jpg'));font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',17)
for name,selected,cols,cell in [('edit_contact',list(range(0,len(files),4)),6,(230,425)),('join_contact',[i for i in range(len(files)) if 3.125<=i*.125<=4.125 or 5.625<=i*.125<=6.625],7,(180,340))]:
 cw,ch=cell;im=Image.new('RGB',(cols*cw,((len(selected)+cols-1)//cols)*ch),'#f5f3ec');d=ImageDraw.Draw(im)
 for j,k in enumerate(selected):
  pic=Image.open(files[k]);pic.thumbnail((cw-4,ch-28));x=j%cols*cw;y=j//cols*ch;im.paste(pic,(x,y+25));d.text((x+2,y),f'{k*.125:.3f}s',font=font,fill='#123')
 im.save(P/(name+'.jpg'),quality=96)
receipt={'date':'2026-11-06','status':'initial_edit_sampled_pending_user_review','source_uuid':'0c3fed58-b7bf-45c3-a4c5-ecc70793c1bb','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'film_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source_intervals_frames':{'full_open':[0,96],'detail':[96,174],'full_end':[174,241]},'detail_crop_xywh':[185,250,360,640],'detail_upscale_factor':2,'detail_note':'Digital reframing from same continuous source, no newly generated fabric; print arrangement readable, fine cotton weave not established.','join_output_frames':[[78,96],[138,156]],'join_frames_each':18,'fps':24,'frame_count':205,'seconds':205/24,'full_decode':True,'audio':False,'baked_text':False,'native_source_speed':True,'source_raw_intervals_disjoint':True,'no_freeze_retime_reverse_repeat_or_flow':True,'continuous_native_speed_review':False,'user_film_approval':None,'publication_approval':None}
(P/'edit_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');(P/'edit_probe.json').write_text(json.dumps(probe,indent=2),encoding='utf-8');print(json.dumps(receipt))
