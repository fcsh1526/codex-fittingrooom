"""One emotion-continuity re-cut from unchanged sources, native24fps/full raster."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe'
FP=ROOT/'openmontage/remotion-composer/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
A=HERE.parent/'L01_trial_02/source.mp4';B=HERE.parent/'L02_trial_01/source.mp4'
OLD=HERE.parent/'paired_review_v1/M03_W45_two_looks_review_v1.mp4'
OUT=HERE/'M03_W45_emotion_recut_v2.mp4'
def run(args):
    r=subprocess.run([str(a) for a in args],capture_output=True)
    if r.returncode:raise RuntimeError(r.stderr.decode('utf-8','replace')[-4000:])
    return r.stdout
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def probe(p):return json.loads(run([FP,'-v','error','-show_streams','-show_format','-of','json',p]))
assert sha(OLD)=='40f4644211ab5cac5f42a4be4bd361f66349df35f70e76bc94e7ddee4a62b6f3'
assert sha(A)=='a6dba2c5f6898cb74aa806e701dee535e1fecc2ac97d80832f1b06380a03acda'
assert sha(B)=='ebc028878aeac24b2538c34eab32b191ddbf8b348e3abc0bbea9331be879f2be'
# Smile-to-smile: A[0,66), B[33,162), overlap18f =>177f/7.375s.
graph='[0:v]trim=start_frame=0:end_frame=66,setpts=PTS-STARTPTS,fps=24,settb=1/24,format=yuv420p[a];[1:v]trim=start_frame=33:end_frame=162,setpts=PTS-STARTPTS,fps=24,settb=1/24,format=yuv420p[b];[a][b]xfade=transition=fade:duration=0.75:offset=2.0,format=yuv420p[v]'
run([FF,'-v','error','-y','-i',A,'-i',B,'-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-preset','medium','-crf','18','-movflags','+faststart',OUT])
p=probe(OUT);v=next(s for s in p['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(720,1280,'24/1',177)
assert abs(float(v['duration'])-7.375)<1e-5 and not any(s['codec_type']=='audio' for s in p['streams'])
run([FF,'-v','error','-i',OUT,'-f','null','-'])
(HERE/'probe.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
edl={'date':'2026-11-04','status':'candidate_pending_emotion_review','feedback_receipt':'../paired_review_v1/user_emotion_feedback_2026-11-04.json','fps':24,'raster':[720,1280],'frame_count':177,'duration_seconds':7.375,'sources':[{'role':'A','path':A.relative_to(ROOT).as_posix(),'sha256':sha(A),'range_half_open':[0,66],'source_seconds':[0,2.75],'output_start_frame':0},{'role':'B','path':B.relative_to(ROOT).as_posix(),'sha256':sha(B),'range_half_open':[33,162],'source_seconds':[1.375,6.75],'output_start_frame':48}],'transition':{'type':'linear_cross_dissolve','frames':18,'seconds':0.75,'output_range_half_open':[48,66],'output_seconds':[2,2.75]},'change':'Select one smile/brighten/approach/smile progression. Exclude L02 surprised opening0–1.375s, L01 later big laugh/head tilt, and L02 later speech-like ending. No inferred dialogue narrative.','clear_reading_intervals_estimated':{'A_full_seconds':[0,2],'B_full_seconds':[2.75,4.0],'B_medium_seconds':[5.625,7.375]},'speed':1,'retiming':False,'freeze':False,'crop':False,'rescale':False,'text':False,'audio':False,'new_still_calls':0,'new_video_jobs':0,'old_film_preserved_sha256':sha(OLD),'output_file':OUT.name,'output_sha256':sha(OUT),'complete_decode':'completed','continuous_human_visual_review':False,'user_acceptance':None,'publication_approval':None}
(HERE/'edit_receipt.json').write_text(json.dumps(edl,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
frames=HERE/'review_frames';frames.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',18)
def sheet(times,name,cols,face=False):
    cw,ch=(225,300) if face else (225,430)
    result=Image.new('RGB',(cols*cw,((len(times)+cols-1)//cols)*ch),'#f7f6f0');d=ImageDraw.Draw(result)
    for i,t in enumerate(times):
        out=frames/f'{name}_{i:02d}_{t:.4f}.png';run([FF,'-v','error','-y','-ss',t,'-i',OUT,'-frames:v','1',out])
        im=Image.open(out).convert('RGB')
        if face:im=im.crop((228,170,450,470))
        im.thumbnail((219,ch-38));x=i%cols*cw+3;y=i//cols*ch+32;result.paste(im,(x,y));d.text((x,y-26),f'{t:.3f}s',font=font,fill='#243b41')
    result.save(HERE/(name+'.png'))
sheet([i*.5 for i in range(15)]+[176/24],'whole_film_contact',5)
join=[1.75]+[i/24 for i in range(48,66)]+[2.75,3.0]
sheet(join,'join_contact',5)
sheet(join,'join_faces',6,True)
sheet([i*.25 for i in range(16,30)],'approach_and_ending_contact',5)
run([FF,'-v','error','-y','-ss',1.5,'-i',OUT,'-t',1.75,'-an','-c:v','libx264','-crf','18','-movflags','+faststart',HERE/'join_context_native.mp4'])
def decoded(path):
    data=run([FF,'-v','error','-i',path,'-an','-vf','scale=180:320:flags=area','-pix_fmt','rgb24','-f','rawvideo','-'])
    return np.frombuffer(data,np.uint8).reshape(-1,320,180,3).astype(np.float32)
a,b,out=decoded(A),decoded(B),decoded(OUT)
assert len(out)==177
da=np.abs(out[:48]-a[:48]).mean(axis=(1,2,3));db=np.abs(out[66:]-b[51:162]).mean(axis=(1,2,3))
assert max(da.max(),db.max())<2.5
mapping={'checked_unblended_frames':159,'A_mapping':'output[0,48)=A[0,48)','B_mapping':'output[66,177)=B[51,162)','A_max_MAD':float(da.max()),'B_max_MAD':float(db.max()),'result':'passed_encoder_loss_tolerance','limits':'Technical frame mapping only, not emotional/physical or continuous visual QA.'}
(HERE/'source_mapping_check.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'edit':edl,'mapping':mapping},ensure_ascii=False))
