"""Render two review-only edits from identical selected source frames."""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
sys.path.insert(0, str(ROOT / '10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan

OUT = Path(__file__).resolve().parent / 'M03_edit_trial_01'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
COMMON = 'scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=24,settb=1/24'
SHOTS = {
    'A1': ('M03_A1_L01_motion_v1_01.mp4', 18, 96, '2026-W37-005-L01'),
    'A2': ('M03_A2_L01_motion_v1_01.mp4', 6, 84, '2026-W37-005-L01'),
    'B1': ('M03_B1_L02_motion_v1_01.mp4', 18, 96, '2026-W37-005-L02'),
    'B2': ('M03_B2_L02_motion_v1_01.mp4', 6, 84, '2026-W37-005-L02'),
}

def rel(path):
    return path.relative_to(ROOT).as_posix()

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def run(args):
    subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

def selected_graph(start, end):
    # Supply one following source frame to fps as an endpoint timestamp,
    # then exclude it. This preserves the requested frames without a freeze.
    return (f'trim=start_frame={start}:end_frame={end+1},setpts=PTS-STARTPTS,'
            f'{COMMON},trim=end_frame={end-start}')

def checkpoints(source, folder, times, name):
    folder.mkdir(parents=True, exist_ok=True)
    cols, w, h = 6, 216, 408
    board = Image.new('RGB', (cols*w, ((len(times)+cols-1)//cols)*h), 'white')
    draw = ImageDraw.Draw(board)
    for index, seconds in enumerate(times):
        dest = folder / f'frame_{index:02d}_{seconds:.3f}.png'
        run(['-ss', str(seconds), '-i', str(source), '-frames:v', '1', str(dest)])
        x, y = index % cols*w, index // cols*h
        with Image.open(dest) as im:
            im.thumbnail((w, h-24))
            board.paste(im, (x, y+24))
        draw.text((x+5, y+5), f'{seconds:.3f}s', fill='black')
    board.save(folder / name, quality=95)
    return rel(folder / name)

def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for shot_id, (filename, start, end, look_id) in SHOTS.items():
        source = ROOT / '10_automation/runs/2026-W37/reels/videos' / filename
        if not source.is_file():
            raise FileNotFoundError(source)
        source_meta = imageio_ffmpeg.read_frames(str(source)).__next__()
        if source_meta['fps'] != 24:
            raise ValueError(f'{shot_id}: source fps requires a separate timing decision')
        selected = OUT / f'{shot_id}_selected.mp4'
        graph = f'{selected_graph(start,end)},format=yuv420p'
        run(['-i', str(source), '-vf', graph, '-an', '-c:v', 'libx264', '-crf', '18',
             '-preset', 'medium', '-r', '24', '-movflags', '+faststart', str(selected)])
        decoded = scan(selected)
        save(OUT / f'{shot_id}_scan.json', decoded)
        if decoded['decoded_frames'] != end-start:
            raise ValueError(f'{shot_id}: insufficient selected frames')
        if decoded['black_candidate_frames'] or decoded['near_identical_frame_pairs']:
            raise ValueError(f'{shot_id}: technical signal requires inspection')
        board = checkpoints(selected, OUT / 'qa' / shot_id,
                            [0, .65, 1.3, 1.95, 2.6, 77/24], 'source_checkpoints.jpg')
        records.append(dict(shot_id=shot_id, look_id=look_id, path=rel(source),
                            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                            start_frame=start, end_frame_exclusive=end, selected_frames=end-start,
                            selected_preview=rel(selected), technical_scan=decoded, checkpoint_board=board,
                            sampled_visual_review='pending', continuous_review='pending'))
    save(OUT / 'source_selection.json', dict(date='2026-10-02', sources=records,
         scope='Candidate extended intervals; historical approval is not extended automatically'))
    print(json.dumps({'prepared_sources':len(records),'folder':str(OUT)}, ensure_ascii=False))

def assemble():
    selection = json.loads((OUT / 'source_selection.json').read_text(encoding='utf-8'))
    versions = [('C', ['A1','A2','B2','B1']), ('D', ['A2','A1','B1','B2'])]
    receipts = []
    for version, order in versions:
        inputs, graphs = [], []
        for i, shot_id in enumerate(order):
            filename, start, end, _ = SHOTS[shot_id]
            inputs += ['-i', str(ROOT / '10_automation/runs/2026-W37/reels/videos' / filename)]
            graphs.append(f'[{i}:v]{selected_graph(start,end)}[s{i}]')
        graphs += ['[s0][s1]xfade=transition=fade:duration=0.75:offset=2.5[x1]',
                   '[x1][s2]xfade=transition=fade:duration=0.75:offset=5[x2]',
                   '[x2][s3]xfade=transition=fade:duration=0.75:offset=7.5,format=yuv420p[v]']
        output = OUT / f'M03_order_{version}_review_v1.mp4'
        run([*inputs, '-filter_complex', ';'.join(graphs), '-map', '[v]', '-an',
             '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-r', '24',
             '-frames:v', '258', '-movflags', '+faststart', str(output)])
        decoded = scan(output)
        save(OUT / f'{version}_scan.json', decoded)
        end = (decoded['decoded_frames']-1)/24
        times = sorted(set([0, 1.25, 3.75, 6.25, 8.75, end] +
                       [x+d for x in (2.5, 5, 7.5) for d in (-1/24, 0, .375, .75, .75+1/24)]))
        board = checkpoints(output, OUT / 'qa' / version, times, 'output_checkpoints.jpg')
        receipt = dict(version=version, date='2026-10-02', status='candidate_pending_user_continuous_review',
                       output_path=rel(output), sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                       shot_order=order, sources=[next(s for s in selection['sources'] if s['shot_id']==shot_id) for shot_id in order],
                       theoretical_seconds=10.75, actual_seconds=decoded['decoded_seconds'],
                       fps=24, resolution=[720,1280], audio='none', baked_text='none',
                       character_speed='unchanged', crop='static cover-scale and center crop, no stretching',
                       transitions=[dict(start=x,end=x+.75,duration=.75,type='cross dissolve') for x in (2.5,5,7.5)],
                       technical_scan=decoded, checkpoint_board=board,
                       assistant_sampled_visual_review='pending', assistant_continuous_review=False,
                       user_approval=None, audience_performance=None)
        save(OUT / f'M03_order_{version}_review_v1.json', receipt)
        receipts.append(receipt)
    if receipts[0]['technical_scan']['decoded_frames'] != receipts[1]['technical_scan']['decoded_frames']:
        raise ValueError('Versions differ in actual length')
    print(json.dumps({'outputs':[dict(version=r['version'],path=r['output_path'],duration=r['actual_seconds'],
                         frames=r['technical_scan']['decoded_frames']) for r in receipts]}, ensure_ascii=False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare','assemble'])
    args = parser.parse_args()
    start = time.monotonic()
    (prepare if args.stage == 'prepare' else assemble)()
    print(f'Processing wall seconds: {time.monotonic()-start:.2f}')
