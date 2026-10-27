"""Build the approved-still motion test; never grant subjective approval."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(root / '10_automation'))
sys.path.insert(0, str(root / '10_automation/.video_dependencies'))
import imageio_ffmpeg
from scan_reel_video import scan

reels = root / '10_automation/runs/2026-W37/reels'
work = reels / 'qa/M03_L01_full_detail_review_v1_01'
work.mkdir(exist_ok=True)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
def rel(p): return str(p.relative_to(root)).replace('\\', '/')
def save(p, value): p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def run(args): subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

specs = [
    ('A1', 'full_start_candidate_v2', 18, 66,
     'https://grok.com/imagine/post/75e7eda5-4051-4798-a909-fec73ef69006?conversation=a5650c8a-b2ab-4401-a857-2906812df204',
     'Nine checkpoints: face/hair and full loafers remain visible; cream shirt, coffee trousers and bag persist. Subject makes a short step then rotates slightly, exceeding a pure weight shift. No obvious sampled background morph. Continuous QA pending.'),
    ('A2', 'detail_start_candidate_v4', 6, 54,
     'https://grok.com/imagine/post/eceec701-1dc9-4c90-9a71-c9f9e0662be3?conversation=292e6d74-de12-4fe9-9421-1304cc4e0520',
     'Nine checkpoints: face remains excluded, bag panel/strap and plain shirt/trouser waist readable. Later source turns more than requested; use only early near-frontal interval. No obvious sampled wall/window/bench morph. Continuous QA pending.')
]
trials = []
for i, (shot, suffix, start, end, url, note) in enumerate(specs):
    source = reels / f'videos/M03_{shot}_L01_motion_v1_01.mp4'
    qa = reels / f'qa/M03_{shot}_L01_motion_v1_01'
    decoded = scan(source)
    save(qa/'decode_scan.json', decoded)
    run(['-i', str(source), '-vf', f'trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1', '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '24', str(work/f'segment_{i}.mp4')])
    still = root / f'10_automation/runs/2026-W37/generated_images/2026-W37-005/looks/2026-W37-005-L01/reel/2026-W37-005-L01_M03_{shot}_{suffix}.png'
    trial = dict(reel_id='2026-W37-M03-reel', look_id='2026-W37-005-L01', trial_id=f'M03_{shot}_L01_motion_v1_01', date='2026-10-01', status='decoded_sampled_review_complete_continuous_qa_pending', source_post_url=url, input_still=rel(still), still_user_approval='ok; explicitly approved for motion on 2026-10-01', input_role='single First frame; exact filename checkbox selected; Add last frame visible; no Last frame', identity_reference='No separate saved character selected. A1 approved near-frontal face is identity input; A2 is approved faceless detail.', prompt_path=rel(reels/f'prompts/M03_{shot}_L01_motion_v1.md'), ui_settings=dict(resolution='720p', duration='6s', audio='off; checkbox0 observed', model='unnamed in visible UI'), video=dict(output_path=rel(source), sha256=hashlib.sha256(source.read_bytes()).hexdigest(), resolution=[720,1264], fps=24, duration_seconds=decoded['decoded_seconds']), qa=dict(decode_scan=decoded, sampled_review=note, provisional_selection_frames=[start,end], end_frame_exclusive=True, usable_seconds=None, continuous_watch_done=False, user_visual_approval=None), time=dict(active_minutes=None,generation_wait_minutes=None), upload=dict(status='assistant_upload_success',method='filechooser registered before actual AX Upload media click, setFiles, exact selected filename verified'))
    save(reels/f'M03_{shot}_L01_motion_v1_01.json',trial)
    trials.append(dict(trial_id=trial['trial_id'], output_path=rel(source), source_url=url, qa='sampled_only_continuous_pending', record_path=rel(reels/f'M03_{shot}_L01_motion_v1_01.json')))
    prompt = reels/f'prompts/M03_{shot}_L01_motion_v1.md'
    prompt.write_text(prompt.read_text(encoding='utf-8-sig').replace('# Prepared only; not submitted','# Submitted 2026-10-01; single approved First frame, 720p / 6s / audio off'),encoding='utf-8')
    gen = still.parent / ('A1_full_start_generation_v2.json' if shot=='A1' else 'A2_detail_generation_v4.json')
    data=json.loads(gen.read_text(encoding='utf-8-sig'))
    data['grok_submitted']=True
    data['motion_record_path']=rel(reels/f'M03_{shot}_L01_motion_v1_01.json')
    save(gen,data)

(work/'concat.txt').write_text("file 'segment_0.mp4'\nfile 'segment_1.mp4'\n",encoding='utf-8')
output=reels/'videos/M03_L01_full_detail_review_v1_01.mp4'
run(['-f','concat','-safe','0','-i',str(work/'concat.txt'),'-c','copy','-an','-movflags','+faststart',str(output)])
decoded=scan(output)
save(work/'decode_scan.json',decoded)
times=[0,.75,1.5,47/24,2,2.75,3.5,95/24]
sheet=Image.new('RGB',(288*len(times),544),'white')
draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    frame=work/f'frame_{round(t*24):03d}.png'
    run(['-ss',str(t),'-i',str(output),'-frames:v','1',str(frame)])
    with Image.open(frame) as im:
        im.thumbnail((288,512));sheet.paste(im,(i*288,24))
    draw.text((i*288+8,5),f'{t:.3f}s',fill='black')
sheet.save(work/'checkpoints.jpg',quality=95)
record=dict(reel_id='2026-W37-M03-reel',scope='L01 full-to-detail junction only; not a complete two-look Reel',status='review_candidate_pending_continuous_user_approval',date='2026-10-01',output_path=rel(output),sha256=hashlib.sha256(output.read_bytes()).hexdigest(),duration_seconds=4,resolution=[720,1280],fps=24,text='none',audio='none',speed='unchanged',transitions='one direct cut at 2s; no fades/effects/animated crop',aspect_handling='Uniform cover-scale 720x1264 to 720x1280 and narrow center side crop; no stretching. Preserve original shot framing to test actual junction.',sources=[dict(path=rel(reels/f'videos/M03_{s[0]}_L01_motion_v1_01.mp4'),start_frame=s[2],end_frame_exclusive=s[3]) for s in specs],technical_scan=decoded,qa=dict(continuous_watch_done=False,user_approval=None,open_issue='Bag position shifts horizontally and scales up at full/detail cut; comfort must be checked by normal-speed viewing.'))
save(reels/'M03_L01_full_detail_review_v1_01.json',record)
manifest_path=reels/'production_manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig'))
m03=next(x for x in manifest['reels'] if x['model_profile_id']=='M03')
m03['generation']['trials'].extend(x for x in trials if x['trial_id'] not in {y['trial_id'] for y in m03['generation']['trials']})
m03['generation']['settings']=dict(resolution='720p',duration='6s',audio='off',input='single First frame per shot',saved_character_selected=False)
m03['generation']['prompt_version']='M03_A1_A2_motion_v1'
m03['status']='L01_full_detail_cut_pending_user_review_L02_unstarted'
m03['partial_review_output_path']=rel(output)
m03['qa']['status']='L01_sampled_technical_complete_junction_continuous_pending'
for shot in m03['storyboard']:
    if shot['shot_id'] in ['A1','A2']:shot['status']='motion_generated_sampled_pending_cut_review'
save(manifest_path,manifest)
print(json.dumps(dict(output=rel(output),scan=decoded),ensure_ascii=False))
