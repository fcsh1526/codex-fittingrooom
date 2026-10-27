"""Normal-speed two-look review. No visual approval is assigned here."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(root / '10_automation/.video_dependencies'))
import imageio_ffmpeg

reels = root / '10_automation/runs/2026-W37/reels'
work = reels / 'qa/M01_two_looks_review_v1_01'
work.mkdir(exist_ok=True)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
sources = [reels / 'videos/M01_A_L01_fixed_full_v1_01.mp4', reels / 'videos/M01_B_L02_fixed_full_v1_01.mp4']
selections = [(18, 102), (18, 114)]
framing = ['scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280', 'crop=642:1140:39:20,scale=720:1280']

def run(args):
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

for index, (source, (start, end), crop) in enumerate(zip(sources, selections, framing)):
    run(['-i', str(source), '-vf', f'trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,{crop},setsar=1', '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '24', str(work / f'segment_{index}.mp4')])
listing = work / 'concat.txt'
listing.write_text("file 'segment_0.mp4'\nfile 'segment_1.mp4'\n", encoding='utf-8')
output = reels / 'videos/M01_two_looks_review_v1_01.mp4'
run(['-f', 'concat', '-safe', '0', '-i', str(listing), '-c', 'copy', '-an', '-movflags', '+faststart', str(output)])
record = dict(reel_id='2026-W37-M01-reel', date='2026-10-01', status='review_candidate_pending_continuous_visual_approval', output_path=output.relative_to(root).as_posix(), sha256=hashlib.sha256(output.read_bytes()).hexdigest(), duration_seconds=7.5, resolution=[720,1280], fps=24, text='none', audio='none', speed='unchanged', transitions='one direct outfit cut at frame84 / 3.5s; no effects', aspect_handling='A uniform cover scale and narrow side crop. B constant 642x1140 crop at x39,y20, uniform resize to720x1280; no animated zoom or stretching. Subject scale/head/shoe placement reviewed separately.', sources=[dict(path=p.relative_to(root).as_posix(), start_frame=s, end_frame_exclusive=e, framing=f) for p,(s,e),f in zip(sources,selections,framing)], qa=dict(continuous_watch_done=False, user_approval=None, sampled_review='pending', technical_scan='pending'))
(reels / 'M01_two_looks_review_v1_01.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(output)
