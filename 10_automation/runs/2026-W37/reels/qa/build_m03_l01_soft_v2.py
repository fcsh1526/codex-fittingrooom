"""Short dissolve experiment requested by user; retain the hard-cut baseline."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(root/'10_automation'))
sys.path.insert(0,str(root/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from scan_reel_video import scan
reels=root/'10_automation/runs/2026-W37/reels'
work=reels/'qa/M03_L01_full_detail_review_v2_soft_01'
work.mkdir(exist_ok=True)
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
def rel(p):return str(p.relative_to(root)).replace('\\','/')
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(a):subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y',*a],check=True)
a=reels/'videos/M03_A1_L01_motion_v1_01.mp4'
b=reels/'videos/M03_A2_L01_motion_v1_01.mp4'
out=reels/'videos/M03_L01_full_detail_review_v2_soft_01.mp4'
common='scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=24,settb=1/24'
graph=f'[0:v]trim=start_frame=18:end_frame=72,setpts=PTS-STARTPTS,{common}[a];[1:v]trim=start_frame=6:end_frame=55,setpts=PTS-STARTPTS,{common}[b];[a][b]xfade=transition=fade:duration=0.25:offset=2,format=yuv420p[v]'
run(['-i',str(a),'-i',str(b),'-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-crf','18','-r','24','-frames:v','96','-movflags','+faststart',str(out)])
decoded=scan(out)
save(work/'decode_scan.json',decoded)
times=[0,1.5,47/24,2,49/24,50/24,51/24,52/24,53/24,54/24,3,95/24]
sheet=Image.new('RGB',(288*6,544*2),'white');draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    p=work/f'frame_{round(t*24):03d}.png'
    run(['-ss',str(t),'-i',str(out),'-frames:v','1',str(p)])
    x=(i%6)*288;y=(i//6)*544
    with Image.open(p) as im:
        im.thumbnail((288,512));sheet.paste(im,(x,y+24))
    draw.text((x+8,y+5),f'{t:.3f}s',fill='black')
sheet.save(work/'checkpoints.jpg',quality=95)
record=dict(reel_id='2026-W37-M03-reel',date='2026-10-01',scope='L01 full/detail transition experiment only',status='candidate_pending_continuous_user_review',output_path=rel(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),duration_seconds=4,resolution=[720,1280],fps=24,text='none',audio='none',speed='source timing unchanged; generated slow-motion impression remains unresolved',transition=dict(type='short cross dissolve',start_seconds=2,end_seconds=2.25,duration_seconds=.25,frame_intervals=6,zoom_blur_morph='none'),sources=[dict(path=rel(a),start_frame=18,end_frame_exclusive=72),dict(path=rel(b),start_frame=6,end_frame_exclusive=54)],baseline=rel(reels/'videos/M03_L01_full_detail_review_v1_01.mp4'),technical_scan=decoded,qa=dict(continuous_watch_done=False,user_approval=None,visual_sample_review=None,open_issues=['Different scales inevitably overlap briefly; check whether ghosting distracts.','Short dissolve can soften the discontinuity but does not fix source action pacing or spatial continuity.']),user_feedback='Hard cuts feel uncomfortable against the slow-looking generated motion, across previous trials; user requests softer transition.',time=dict(active_minutes=None,generation_wait_minutes=0))
record['sources'][1]['end_frame_exclusive']=55
record['qa']['visual_sample_review']='Start, ending and every transition-frame interval inspected. Full hair/shoes remain in the full shot; face excluded in detail. Brief double-scale overlap visible inside the dissolve, not a morph or a clean spatially continuous move. Continuous comfort remains pending.'
save(reels/'M03_L01_full_detail_review_v2_soft_01.json',record)
manifest_path=reels/'production_manifest.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig'))
m03=next(x for x in manifest['reels'] if x['model_profile_id']=='M03')
m03['status']='L01_soft_transition_v2_pending_review_L02_unstarted'
m03['partial_review_output_path']=rel(out)
m03['edit_feedback_2026_10_01']=dict(user_feedback=record['user_feedback'],test=rel(reels/'M03_L01_full_detail_review_v2_soft_01.json'),adopted_globally=False,slow_motion_impression='user reported; unresolved')
save(manifest_path,manifest)
print(json.dumps(dict(output=rel(out),scan=decoded),ensure_ascii=False))
