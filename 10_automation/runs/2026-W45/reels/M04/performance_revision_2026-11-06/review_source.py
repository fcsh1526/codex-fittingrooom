from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw,ImageFont
ROOT=Path.cwd();P=Path(__file__).resolve().parent
ff=ROOT/'openmontage/.local/bin/ffmpeg.exe'
fp=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
def run(args):return subprocess.run([str(a) for a in args],check=True,capture_output=True,text=True,encoding='utf-8')
src=P/'S01_source.mp4'
probe=json.loads(run([fp,'-v','error','-show_streams','-show_format','-of','json',src]).stdout)
(P/'source_probe.json').write_text(json.dumps(probe,indent=2),encoding='utf-8')
v=next(s for s in probe['streams'] if s['codec_type']=='video')
run([ff,'-v','error','-i',src,'-f','null','-'])
out=P/'M04_W45_performance_revision_silent.mp4'
run([ff,'-v','error','-y','-i',src,'-map','0:v:0','-c:v','copy','-an',out])
frames=P/'qa';frames.mkdir(exist_ok=True)
run([ff,'-v','error','-y','-i',src,'-vf',r'select=not(mod(n\,3))','-fps_mode','vfr',frames/'f_%03d.jpg'])
files=sorted(frames.glob('f_*.jpg'));font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',18)
def sheet(name,selected,crop,tw,th,cols):
 im=Image.new('RGB',(cols*tw,((len(selected)+cols-1)//cols)*(th+27)), '#f4f1eb');d=ImageDraw.Draw(im)
 for k,(idx,path) in enumerate(selected):
  pic=Image.open(path).convert('RGB')
  if crop:pic=pic.crop(crop)
  pic.thumbnail((tw,th))
  x=k%cols*tw;y=k//cols*(th+27)
  im.paste(pic,(x+(tw-pic.width)//2,y+27));d.text((x+3,y+2),f'{idx*3/24:.3f}s',font=font,fill='black')
 im.save(P/name)
sheet('whole_contact.jpg',[(i,f) for i,f in enumerate(files) if i%4==0],None,180,320,7)
sheet('face_contact.jpg',list(enumerate(files)),(170,20,520,430),155,181,7)
sheet('lower_contact.jpg',list(enumerate(files)),(100,620,680,1280),155,177,7)
report={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'preview_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'frame_count':v.get('nb_frames'),'seconds':probe['format']['duration'],'original_audio':any(s['codec_type']=='audio' for s in probe['streams']),'full_decode':True,'sample_every_frames':3,'sample_count':len(files),'preview':'Full-length video streamcopy with audio removed; no crop/cut/retiming.','continuous_native_speed_visual_pass':False,'user_acceptance':None}
(P/'technical_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
