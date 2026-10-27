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
OUT = PILOT / 'edit_v2'
OUT.mkdir(exist_ok=True)
manifest = json.loads((PILOT.parent / 'production_manifest.json').read_text(encoding='utf-8'))
reel = next(r for r in manifest['reels'] if r['model_profile_id'] == 'M02')
proofs = [ROOT / v['source_path'] for v in reel['views'] if v['role'] == 'proof']
clips = [PILOT / 'videos/T07_01.mp4', PILOT / 'videos/T08_01.mp4']
captions = ['冷氣房的兩套薄襯衫穿搭', '敞開襯衫，保留內搭層次', '霧藍襯衫搭深藍洋裝', '進室內加薄襯衫，外出可脫']
segments = [(clips[0], 4.5, 0), (proofs[0], 3.5, 1),
            (clips[1], 4.5, 2), (proofs[1], 4, 3)]
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
    records.append(dict(source=str(source.relative_to(ROOT)), source_start=0,
                        source_end=duration, subtitle=captions[caption], qa='pending'))
inputs = []
for n in range(4): inputs += ['-i', str(OUT / f'clean_{n}.mp4')]
filters = ';'.join(f'[{n}:v]settb=AVTB,setpts=PTS-STARTPTS,fps=24[v{n}]' for n in range(4))
filters += ';[v0][v1]xfade=transition=fade:duration=0.5:offset=4,fps=24[x1]'
filters += ';[x1][v2]xfade=transition=fade:duration=0.5:offset=7,fps=24[x2]'
filters += ';[x2][v3]xfade=transition=fade:duration=0.5:offset=11[v]'
clean_master = OUT / 'M02_two_looks_clean_review_v2.mp4'
run([*inputs, '-filter_complex', filters, '-map', '[v]', '-t', '15', '-an',
     '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(clean_master)])
inputs = ['-i', str(clean_master)]
for n in range(4): inputs += ['-loop', '1', '-i', str(OUT / f'caption_{n}.png')]
# Captions fade separately so two lines never overlap during a picture dissolve.
windows = [(0,4), (4.5,7), (7.5,11), (11.5,15)]
filters = []
last = '0:v'
for n,(start,end) in enumerate(windows):
    filters.append(f'[{n+1}:v]format=rgba,fade=t=in:st={start}:d=0.15:alpha=1,fade=t=out:st={end-0.15}:d=0.15:alpha=1[c{n}]')
    filters.append(f'[{last}][c{n}]overlay=0:0[o{n}]')
    last = f'o{n}'
run([*inputs, '-filter_complex', ';'.join(filters), '-map', f'[{last}]', '-t', '15', '-r', '24', '-an',
     '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
     str(OUT / 'M02_two_looks_captioned_review_v2.mp4')])
(OUT / 'edit_manifest.json').write_text(json.dumps(dict(status='review_only_pending_dynamic_QA',
    duration_seconds=15, actual_size=[720,1280], fps=24, music=None,
    note='V2 responds to user discomfort: four ordered shots; no rapid opening or closing recaps; 0.5s editorial dissolves at4,7,11s. Captions fade separately. No music. Full dynamic review pending.',
    segments=records), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(OUT / 'M02_two_looks_captioned_review_v2.mp4')
