"""Build a text-free normal-speed review candidate, never user approval."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(root / '10_automation/.video_dependencies'))
import imageio_ffmpeg
reels = root / '10_automation/runs/2026-W37/reels'
work = reels / 'qa/M04_two_looks_review_v1_01'
work.mkdir(exist_ok=True)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

def run(args):
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

def scan(source):
    reader = imageio_ffmpeg.read_frames(str(source))
    meta = next(reader)
    w, h = meta['size']
    black, still, n, previous = [], [], 0, None
    for frame in reader:
        pixels = np.frombuffer(frame, dtype=np.uint8).reshape(h, w, 3)[::8, ::8].astype(np.float32)
        if (pixels < 16).all(axis=2).mean() > .98:
            black.append(n)
        if previous is not None and np.abs(pixels - previous).mean() < .1:
            still.append([n-1, n])
        previous = pixels
        n += 1
    return dict(metadata=meta, decoded_frames=n, black_candidate_frames=black, near_identical_frame_pairs=still)

inputs = [reels / 'videos/M04_A_L01_upload_trial_01.mp4', reels / 'videos/M04_B_L02_motion_v1_01.mp4']
selections = [(0, 90), (6, 108)]
for index, (source, (start, end)) in enumerate(zip(inputs, selections)):
    run(['-i', str(source), '-vf', f'trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1',
         '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '24', str(work / f'segment_{index}.mp4')])
listing = work / 'concat.txt'
listing.write_text("file 'segment_0.mp4'\nfile 'segment_1.mp4'\n", encoding='utf-8')
output = reels / 'videos/M04_two_looks_review_v1_01.mp4'
run(['-f', 'concat', '-safe', '0', '-i', str(listing), '-c', 'copy', '-an', '-movflags', '+faststart', str(output)])
scan_b = scan(inputs[1])
(reels / 'qa/M04_B_L02_motion_v1_01/decode_scan.json').write_text(json.dumps(scan_b, indent=2), encoding='utf-8')
scan_out = scan(output)
(work / 'decode_scan.json').write_text(json.dumps(scan_out, indent=2), encoding='utf-8')
times = [0, 1.5, 3.5, 89/24, 90/24, 4.5, 6, 7, 191/24]
sheet = Image.new('RGB', (288*len(times), 544), 'white')
draw = ImageDraw.Draw(sheet)
for index, seconds in enumerate(times):
    image_path = work / f'frame_{round(seconds*24):03d}.png'
    run(['-ss', str(seconds), '-i', str(output), '-frames:v', '1', str(image_path)])
    with Image.open(image_path) as im:
        im.thumbnail((288, 512))
        sheet.paste(im, (288*index, 24))
    draw.text((288*index+8, 5), f'{seconds:.3f}s', fill='black')
sheet.save(work / 'checkpoints.jpg', quality=95)
record = dict(reel_id='2026-W37-M04-reel', status='review_candidate_pending_continuous_visual_approval', date='2026-10-01',
              output_path=str(output.relative_to(root)).replace('\\','/'), sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
              duration_seconds=8, resolution=[720,1280], fps=24, text='none', audio='none', speed='unchanged',
              transitions='one direct outfit cut at frame 90, 3.75s; no fades or effects',
              aspect_handling='Uniformly scale both 720x1264 sources to cover 720x1280, then center-crop approximately five pixels per side; no stretching, no animated crop.',
              sources=[dict(path=str(src.relative_to(root)).replace('\\','/'), start_frame=s, end_frame_exclusive=e) for src,(s,e) in zip(inputs,selections)],
              technical_scan=scan_out, qa=dict(continuous_watch_done=False,user_approval=None, visual_notes='Pending inspection of output cut frames and user normal-speed full playback.'))
(reels / 'M04_two_looks_review_v1_01.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
trial_path = reels / 'M04_B_L02_motion_v1_01.json'
trial = json.loads(trial_path.read_text(encoding='utf-8-sig'))
trial.update(status='decoded_sampled_review_complete_continuous_qa_pending', output_path=str(inputs[1].relative_to(root)).replace('\\','/'))
trial['video'] = dict(resolution=[720,1264], duration_seconds=145/24, fps=24, sha256=hashlib.sha256(inputs[1].read_bytes()).hexdigest())
trial['qa'].update(decode_scan=scan_b, sampled_visual_review='Nine checkpoints inspected. Face and ivory collar/navy skirt show no obvious sampled jump; retreat reveals black low-heel pumps. Satin folds/hem silhouette and room parallax still require normal-speed full playback.')
trial_path.write_text(json.dumps(trial, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(output=record['output_path'], scan=scan_out)))
