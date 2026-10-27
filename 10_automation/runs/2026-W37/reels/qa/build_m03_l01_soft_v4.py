"""0.75s dissolve comparison; same source intervals as 0.5s version."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(root/'10_automation'))
sys.path.insert(0,str(root/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from scan_reel_video import scan
reels=root/'10_automation/runs/2026-W37/reels'
work=reels/'qa/M03_L01_full_detail_review_v4_soft_075s_01';work.mkdir(exist_ok=True)
def rel(p):return str(p.relative_to(root)).replace('\\','/')
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args):subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-y',*args],check=True)
a=reels/'videos/M03_A1_L01_motion_v1_01.mp4';b=reels/'videos/M03_A2_L01_motion_v1_01.mp4'
out=reels/'videos/M03_L01_full_detail_review_v4_soft_075s_01.mp4'
common='scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=24,settb=1/24'
graph=f'[0:v]trim=start_frame=18:end_frame=72,setpts=PTS-STARTPTS,{common}[a];[1:v]trim=start_frame=6:end_frame=55,setpts=PTS-STARTPTS,{common}[b];[a][b]xfade=transition=fade:duration=0.75:offset=1.5,format=yuv420p[v]'
run(['-i',str(a),'-i',str(b),'-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-crf','18','-r','24','-frames:v','84','-movflags','+faststart',str(out)])
decoded=scan(out);save(work/'decode_scan.json',decoded)
times=[0]+[n/24 for n in range(35,55)]+[2.75,83/24]
sheet=Image.new('RGB',(240*6,452*4),'white');draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    p=work/f'frame_{round(t*24):03d}.png';run(['-ss',str(t),'-i',str(out),'-frames:v','1',str(p)])
    x=i%6*240;y=i//6*452
    with Image.open(p) as im:
        im.thumbnail((240,426));sheet.paste(im,(x,y+24))
    draw.text((x+8,y+5),f'{t:.3f}s',fill='black')
sheet.save(work/'checkpoints.jpg',quality=95)
previous=reels/'M03_L01_full_detail_review_v3_soft_05s_01.json'
record=json.loads(previous.read_text(encoding='utf-8-sig'))
record.update(status='candidate_pending_continuous_user_review',output_path=rel(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),duration_seconds=decoded['decoded_seconds'],transition=dict(type='cross dissolve',start_seconds=1.5,end_seconds=2.25,duration_seconds=.75,frame_intervals=18,zoom_blur_morph='none'),baseline=record['output_path'],technical_scan=decoded,user_feedback='User: 好多了，0.75秒呢. Requests longer comparison, same source action and timing.',qa=dict(continuous_watch_done=False,user_approval=None,visual_sample_review=None,open_issues=['Longer double-scale overlap; subjective comfort and duration preference pending.']))
save(reels/'M03_L01_full_detail_review_v4_soft_075s_01.json',record)
v3=json.loads(previous.read_text(encoding='utf-8-sig'));v3['status']='user_reviewed_positive_comparing_longer_transition'
v3['qa']['user_feedback']='好多了，0.75秒呢';v3['qa']['user_approval']=None;save(previous,v3)
p=reels/'production_manifest.json';manifest=json.loads(p.read_text(encoding='utf-8-sig'))
m03=next(x for x in manifest['reels'] if x['model_profile_id']=='M03')
m03.update(status='L01_soft_transition_v4_075s_pending_comparison_L02_unstarted',partial_review_output_path=rel(out))
m03['edit_feedback_2026_10_01'].update(user_feedback=record['user_feedback'],test=rel(reels/'M03_L01_full_detail_review_v4_soft_075s_01.json'),adopted_globally=False);save(p,manifest)
print(json.dumps(dict(output=rel(out),scan=decoded),ensure_ascii=False))
