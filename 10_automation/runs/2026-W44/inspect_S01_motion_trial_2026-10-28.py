from pathlib import Path
import sys,json,hashlib,subprocess
from PIL import Image,ImageDraw
root=Path.cwd();sys.path.insert(0,str(root/'10_automation/.video_dependencies'))
import imageio_ffmpeg
out=root/'10_automation/runs/2026-W44/editorial_reset_v3_2026-10-28/S01_motion_trial_01'
source=out/'S01_source.mp4'
reader=imageio_ffmpeg.read_frames(str(source),pix_fmt='rgb24');meta=next(reader)
fps=meta['fps'];size=tuple(meta['size']);frames=[]
for raw in reader:frames.append(Image.frombytes('RGB',size,raw))
reader.close();n=len(frames)
qa=out/'QA';qa.mkdir(exist_ok=True)
def sheet(indices,name,cols=4):
 indices=sorted(set(max(0,min(n-1,int(i))) for i in indices));tw=200;th=round(tw*size[1]/size[0]);h=th+26
 im=Image.new('RGB',(cols*tw,((len(indices)+cols-1)//cols)*h),'#eeeeea');d=ImageDraw.Draw(im)
 for k,i in enumerate(indices):
  x=(k%cols)*tw;y=(k//cols)*h;im.paste(frames[i].resize((tw,th)),(x,y+24));d.text((x+4,y+5),f'f{i:03} / {i/fps:.3f}s',fill='black')
 im.save(qa/name,quality=93)
 return indices
main=sheet([round(t*fps) for t in [0,1,2,2.5,3,4,5,6,6.5,7,7.5,8,8.25,8.5,9]]+[n-1],'whole_source.jpg')
dense=sheet(range(round(7*fps),min(n,round(8.5*fps)+1),3),'column_7_to_8p5.jpg',5)
for i in set([0,round(8*fps),min(n-1,round(8.25*fps)),n-1]):frames[i].save(qa/f'frame_{i:03}.png')
ff=imageio_ffmpeg.get_ffmpeg_exe()
probe=subprocess.run([ff,'-hide_banner','-i',str(source)],capture_output=True,text=True,encoding='utf-8',errors='replace')
(qa/'ffmpeg_probe.txt').write_text(probe.stderr,encoding='utf-8')
preview=out/'S01_silent_review.mp4'
if not preview.exists():subprocess.run([ff,'-hide_banner','-loglevel','error','-n','-i',str(source),'-map','0:v:0','-c:v','copy','-an','-movflags','+faststart',str(preview)],check=True)
record={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_bytes':source.stat().st_size,'metadata':meta,'decoded_frames':n,'frame_count_over_fps_seconds':n/fps,'full_decode_completed':True,'sample_indices':main,'column_dense_indices':dense,'inspection_limits':'Prepared samples only. Continuous human playback not performed by this script; no visual or motion pass inferred.','silent_preview_sha256':hashlib.sha256(preview.read_bytes()).hexdigest()}
(qa/'technical_scan.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
