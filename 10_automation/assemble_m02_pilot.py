"""Build a review-only M02 pilot; never promotes footage to accepted QA."""
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
import imageio_ffmpeg

PILOT = ROOT / '10_automation/runs/2026-W37/reels/pilot_M02'
OUT = PILOT / 'edit_v1'
OUT.mkdir(exist_ok=True)
manifest = json.loads((PILOT.parent / 'production_manifest.json').read_text(encoding='utf-8'))
reel = next(r for r in manifest['reels'] if r['model_profile_id'] == 'M02')
proofs = [ROOT / v['source_path'] for v in reel['views'] if v['role'] == 'proof']
clips = [PILOT / 'videos/T07_01.mp4', PILOT / 'videos/T08_01.mp4']
captions = [r['subtitle'] for r in reel['storyboard']]
segments = [(clips[0], .75, 0), (clips[1], .75, 0),
            (clips[0], 3, 1), (proofs[0], 2, 2),
            (clips[1], 3, 3), (proofs[1], 2, 4),
            (clips[0], 1.75, 5), (clips[1], 1.75, 5)]
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
font = ImageFont.truetype('C:/Windows/Fonts/msjhbd.ttc', 32)
for n, text in enumerate(captions):
    im = Image.new('RGBA', (720, 1280))
    draw = ImageDraw.Draw(im)
    width = draw.textlength(text, font=font)
    x = (720-width)/2
    draw.rounded_rectangle((x-20, 1008, x+width+20, 1074), radius=12, fill=(28, 31, 30, 210))
    draw.text((x, 1018), text, font=font, fill=(255, 253, 247, 255))
    im.save(OUT / f'caption_{n}.png')

def run(args):
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

records = []
for n, (source, duration, caption) in enumerate(segments):
    args = ['-loop', '1', '-framerate', '24'] if source.suffix == '.png' else []
    clean = OUT / f'clean_{n}.mp4'
    run([*args, '-i', str(source), '-t', str(duration), '-vf',
         'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24',
         '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', str(clean)])
    run(['-i', str(clean), '-i', str(OUT / f'caption_{caption}.png'), '-filter_complex',
         '[0:v][1:v]overlay=0:0', '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
         str(OUT / f'captioned_{n}.mp4')])
    records.append(dict(source=str(source.relative_to(ROOT)), source_start=0,
                        source_end=duration, subtitle=captions[caption], qa='pending'))
for kind, filename in [('clean', 'M02_two_looks_clean_review_v1.mp4'),
                       ('captioned', 'M02_two_looks_captioned_review_v1.mp4')]:
    listing = OUT / f'{kind}_concat.txt'
    listing.write_text(''.join(f"file '{kind}_{n}.mp4'\n" for n in range(len(segments))), encoding='utf-8')
    run(['-f', 'concat', '-safe', '0', '-i', str(listing), '-c', 'copy', '-movflags', '+faststart', str(OUT / filename)])
(OUT / 'edit_manifest.json').write_text(json.dumps(dict(status='review_only_pending_dynamic_QA',
    duration_seconds=15, actual_size=[720,1280], fps=24, music=None,
    note='No music or generated source audio. Repeated full shots are intentional opening/closing recaps. Segment selection is provisional, not certified usable intervals.',
    segments=records), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(OUT / 'M02_two_looks_captioned_review_v1.mp4')
