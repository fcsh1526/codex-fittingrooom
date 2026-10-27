from pathlib import Path
import sys, json, subprocess, hashlib
import numpy as np
from PIL import Image

base=Path(__file__).resolve().parent;root=base.parents[1]
sys.path.insert(0,str(root/'10_automation/.video_dependencies'))
import imageio_ffmpeg
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
a=base/'A_motion_attempt_01/source.mp4';b=base/'B_motion_attempt_01/source.mp4'
out=base/'joined_review_v1';out.mkdir(exist_ok=True)
silent=base/'B_motion_attempt_01/review_silent.mp4'
subprocess.run([ffmpeg,'-y','-i',str(b),'-map','0:v:0','-c:v','copy','-an','-movflags','+faststart',str(silent)],check=True,capture_output=True)
def get_frame(path,index):
    reader=imageio_ffmpeg.read_frames(str(path));meta=next(reader)
    for i,data in enumerate(reader):
        if i==index:
            image=Image.frombytes('RGB',tuple(meta['size']),data);reader.close();return image
af=get_frame(a,144);bf=get_frame(b,0)
af=af.resize(bf.size,Image.Resampling.LANCZOS)
mae=float(np.abs(np.asarray(af,dtype=float)-np.asarray(bf,dtype=float)).mean())
target=out/'M02_cafe_wall_two_looks_trial_v1.mp4'
filtergraph='[0:v:0]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,setpts=PTS-STARTPTS,fps=24[a];[1:v:0]setsar=1,setpts=PTS-STARTPTS,fps=24[b];[a][b]xfade=transition=fade:duration=0.75:offset=5.291666667[v]'
subprocess.run([ffmpeg,'-y','-i',str(a),'-i',str(b),'-filter_complex',filtergraph,'-map','[v]','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],check=True,capture_output=True)
r={
 'date':'2026-10-14','model':'M02','look_ids':['2026-W41-003-L01','2026-W41-003-L02'],
 'concept':'camera passes cafe wall corner between two everyday looks; physical occlusion plus default soft join',
 'source_a':a.relative_to(root).as_posix(),'source_b':b.relative_to(root).as_posix(),
 'source_a_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),'source_b_sha256':hashlib.sha256(b.read_bytes()).hexdigest(),
 'output':target.relative_to(root).as_posix(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
 'speed':'original 1x for both','text':False,'audio':False,
 'join_seconds':[5.291666667,6.041666667],'join_duration':0.75,
 'framing':'A 720x1264 proportionally scaled to cover 720x1280 and centre-cropped about 8px total horizontal; B native720x1280 unchanged. No stretch or letterbox.',
 'endpoint_comparison':{'method':'A last decoded frame resized to B first frame dimensions for comparison only','mean_absolute_rgb_difference_0_to_255':mae,'not_pixel_identical':True},
 'B_review':{'samples_viewed':['whole_25.jpg','face_5.jpg','all_00.jpg','all_01.jpg','all_02.jpg','all_03.jpg'],'findings':['Starts on opaque wall; reveal edge moves left and figure emerges on right.','Face and shirt/denim/shoes/bag readable in samples.','Wall becomes coarser/sharper before revealing, then settles toward finer plaster; exact fixed material continuity is not proven.','Subject changes weight and makes a short forward step near ending; not perfectly standing still.'],'assistant_continuous_playback':False,'user_dynamic_approval':None},
 'full_film_user_approval':None,'published':False,'publishing_replacement':False
}
(out/'edit_receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(target),'endpoint_mae':mae}))
