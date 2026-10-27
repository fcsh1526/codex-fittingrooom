"""Keep M01 source selection/action, replace its cut with0.75s overlap."""
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
work = reels / 'qa/M01_two_looks_soft_review_v2_01'
work.mkdir(exist_ok=True)
baseline = json.loads((reels / 'M01_two_looks_review_v1_01.json').read_text(encoding='utf-8-sig'))
out = reels / 'videos/M01_two_looks_soft_review_v2_01.mp4'

def rel(path):
    return path.relative_to(root).as_posix()

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def run(args):
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

chains = []
for i, source in enumerate(baseline['sources']):
    chains.append(f"[{i}:v]trim=start_frame={source['start_frame']}:end_frame={source['end_frame_exclusive']},"
                  f"setpts=PTS-STARTPTS,{source['framing']},setsar=1,fps=24,settb=1/24[v{i}]")
graph = ';'.join(chains) + ';[v0][v1]xfade=transition=fade:duration=0.75:offset=2.75,format=yuv420p[v]'
inputs = []
for source in baseline['sources']:
    inputs.extend(['-i', str(root / source['path'])])
run([*inputs, '-filter_complex', graph, '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '18',
     '-r', '24', '-frames:v', '162', '-movflags', '+faststart', str(out)])
decoded = scan(out)
save(work / 'decode_scan.json', decoded)
assert 161 <= decoded['decoded_frames'] <= 162 and tuple(decoded['metadata']['size']) == (720, 1280)
times = [0, 1.5, 65/24, 66/24, 2.9375, 3.125, 3.3125, 83/24, 3.5, 4.5, 5.75, (decoded['decoded_frames']-1)/24]
sheet = Image.new('RGB', (4*240, 3*452), 'white')
draw = ImageDraw.Draw(sheet)
for i, t in enumerate(times):
    frame = work / f'checkpoint_{i:02d}.png'
    run(['-ss', str(t), '-i', str(out), '-frames:v', '1', str(frame)])
    x, y = i % 4 * 240, i // 4 * 452
    with Image.open(frame) as img:
        img.thumbnail((240, 426))
        sheet.paste(img, (x, y+24))
    draw.text((x+8, y+5), f'{t:.3f}s', fill='black')
sheet.save(work / 'checkpoints.jpg', quality=95)
record = dict(baseline)
record.update(date='2026-10-02', status='soft_candidate_pending_continuous_user_approval',
    output_path=rel(out), sha256=hashlib.sha256(out.read_bytes()).hexdigest(), duration_seconds=decoded['decoded_seconds'],
    baseline=baseline['output_path'], transitions=[dict(type='cross_dissolve', duration_seconds=0.75,
        start_seconds=2.75, end_seconds=3.5)],
    change_scope='Only overlap changed; original selected source intervals, framing and source speed retained. Nominal duration6.75s, encoded duration measured separately; xfade endpoint omits one final frame at24fps. No added freeze or retiming.',
    qa=dict(continuous_watch_done=False, user_approval=None, sampled_review='pending',
        technical_scan=decoded, sample_sheet=rel(work / 'checkpoints.jpg')))
save(reels / 'M01_two_looks_soft_review_v2_01.json', record)
print(json.dumps(dict(output=rel(out), frames=decoded['decoded_frames'], duration=decoded['decoded_seconds'],
    black_frames=decoded['black_candidate_frames'], still_pairs=decoded['near_identical_frame_pairs']), ensure_ascii=False))
