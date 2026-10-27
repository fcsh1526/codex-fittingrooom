from pathlib import Path
import hashlib
import json
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
sys.path.insert(0, str(ROOT / '10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

a = OUT / 'A_attempt_02/source.mp4'
b = OUT / 'B_attempt_01/source.mp4'
assert sha(a) == '8e9deb287f3d0eef8055a0fd2e0bf3b05e51a04fdfb767e766ea5d2b084dfa20'
assert sha(b) == '861120d4da0f62cac657225b37be7a1fcc00d72bd401505efe08d6cdcc850fb8'
review = {
    'method': 'All 241 whole-frame thumbnails plus25 larger whole samples, five native face windows and native whole frames60/90/110/210 viewed; not continuous normal-speed playback.',
    'actual_motion': 'Front hold through about1.7s; side turn about2-3s; near-profile stance through about4s; front again about4.5-5s; approach begins around8s and continues at end. Does not achieve planned settled near ending.',
    'identity_clothing_background': 'Recognizable identity/hair and navy blazer, gray tee, cream trousers retained in reviewed views. Blank right wall, bench, left window and floor broadly stationary; no new architecture detected.',
    'feet_bag': 'No obvious gross foot/hand distortion in reviewed views; black bag becomes far-side occluded during profile and visible again on return. Tiny shoe/strap details not certified on every native frame.',
    'limits': 'Side turn exceeds planned35deg; front hold is longer than prompt target. End remains walking; feet progressively leave frame with approach. Source naturalness and final transition comfort await user playback.'
}
p = OUT / 'B_attempt_01/technical_receipt.json'
d = json.loads(p.read_text(encoding='utf-8'))
d.update({'visual_review': 'sampled_candidate_usable_for_provisional_edit', 'review_observations': review, 'continuous_playback': False, 'user_film_approval': None})
save(p, d)

delivery = OUT / 'M03_continuous_distance_pose_two_looks_v1.mp4'
if delivery.exists() and delivery.stat().st_size == 0:
    attempt = 1
    failed = OUT / f'render_attempt_{attempt}_failed_empty.mp4'
    while failed.exists():
        attempt += 1
        failed = OUT / f'render_attempt_{attempt}_failed_empty.mp4'
    delivery.rename(failed)
assert not delivery.exists(), 'Create a new version rather than overwrite.'
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
filters = ('[0:v]trim=end_frame=204,settb=1/24,setpts=N,format=yuv420p,fps=24[a];'
           '[1:v]trim=end_frame=240,settb=1/24,setpts=N,format=yuv420p,fps=24[b];'
           '[a][b]xfade=transition=fade:duration=0.75:offset=7.75,format=yuv420p[v]')
cmd = [ffmpeg, '-hide_banner', '-i', str(a), '-i', str(b), '-filter_complex', filters,
       '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium',
       '-pix_fmt', 'yuv420p', '-r', '24', '-frames:v', '426', '-movflags', '+faststart', str(delivery)]
r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
(OUT / 'two_looks_render_log.txt').write_text(r.stderr, encoding='utf-8')
r.check_returncode()
result = scan(delivery)
assert result['decoded_frames'] == 426 and result['metadata']['fps'] == 24
assert list(result['metadata']['size']) == [720, 1280]
probe = subprocess.run([ffmpeg, '-hide_banner', '-i', str(delivery)], capture_output=True, text=True, encoding='utf-8', errors='replace')
assert 'Audio:' not in probe.stderr

qa = OUT / 'two_looks_qa'; qa.mkdir(exist_ok=True)
indices = np.linspace(0, 425, 25, dtype=int).tolist()
transition_indices = list(range(184, 209, 2))
whole = Image.new('RGB', (1000, 1900), 'white'); wd = ImageDraw.Draw(whole)
transition = Image.new('RGB', (1400, 760), 'white'); td = ImageDraw.Draw(transition)
reader = imageio_ffmpeg.read_frames(str(delivery)); next(reader)
boards = {}
for i, data in enumerate(reader):
    frame = Image.frombytes('RGB', (720, 1280), data)
    if i in indices:
        k=indices.index(i); x=k%5*200; y=k//5*380
        wd.text((x+3,y+3), f'{i/24:.2f}s / {i}', fill='black')
        whole.paste(frame.resize((200,356), Image.Resampling.LANCZOS),(x,y+24))
    if i in transition_indices:
        k=transition_indices.index(i); x=k%7*200; y=k//7*380
        td.text((x+3,y+3), f'{i/24:.2f}s / {i}', fill='black')
        transition.paste(frame.resize((200,356), Image.Resampling.LANCZOS),(x,y+24))
        frame.save(qa / f'join_{i:03d}.png')
    block=i//48; k=i%48
    if block not in boards: boards[block]=Image.new('RGB',(1280,1854),'white')
    x=k%8*160; y=k//8*309
    ImageDraw.Draw(boards[block]).text((x+3,y+3),str(i),fill='black')
    boards[block].paste(frame.resize((160,285),Image.Resampling.LANCZOS),(x,y+24))
whole.save(qa/'whole_25.jpg',quality=95)
transition.save(qa/'transition_13.jpg',quality=95)
for block, board in boards.items(): board.save(qa/f'all_{block:02d}.jpg',quality=95)

protected = json.loads((ROOT / '10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json').read_text(encoding='utf-8-sig'))
unchanged = []
for reel in protected['reels']:
    actual=sha(ROOT/reel['source_path']); assert actual==reel['sha256']
    unchanged.append({'model':reel['model'],'sha256':actual,'unchanged':True})
save(OUT / 'two_looks_receipt.json', {
    'status':'combined_candidate_exported_visual_review_pending',
    'file':delivery.relative_to(ROOT).as_posix(),'sha256':sha(delivery),'scan':result,
    'sources':[{'file':a.relative_to(ROOT).as_posix(),'sha256':sha(a),'frames':[0,204],'end_exclusive':True},
               {'file':b.relative_to(ROOT).as_posix(),'sha256':sha(b),'frames':[0,240],'end_exclusive':True}],
    'transition':{'type':'cross_dissolve','seconds':0.75,'frames':18,'start_seconds':7.75,'end_seconds':8.5},
    'editing':'Remove redundant A ending hold; same native24fps and source speed, no crop/zoom/reverse/freeze/text. No internal cut in either retained source.',
    'audio_streams_verified':0,'b_review':review,'all_frame_thumbnails_exported':426,
    'assistant_continuous_playback':False,'user_film_approval':None,
    'protected_w41_originals':unchanged,'drive_uploaded':False,'published':False
})
print(json.dumps({'file':str(delivery),'frames':426,'seconds':result['decoded_seconds'],'sha256':sha(delivery)},ensure_ascii=False))
