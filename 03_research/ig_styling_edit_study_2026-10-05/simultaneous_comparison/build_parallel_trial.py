"""Assemble a separate side-by-side research cut; never write publishing files."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
sys.path.insert(0, str(ROOT / '10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def relative(path):
    return path.relative_to(ROOT).as_posix()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(args):
    subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def checkpoints(path, name):
    folder = OUT / 'qa' / name
    folder.mkdir(parents=True, exist_ok=True)
    times = [0, 1.5, 3, 4.5, 143/24]
    board = Image.new('RGB', (5*180, 344), '#ffffff')
    draw = ImageDraw.Draw(board)
    for index, seconds in enumerate(times):
        image_path = folder / f'frame_{index:02d}.png'
        run(['-ss', str(seconds), '-i', str(path), '-frames:v', '1', str(image_path)])
        with Image.open(image_path) as frame:
            frame.thumbnail((180, 320), Image.Resampling.LANCZOS)
            board.paste(frame, (index*180, 24))
        draw.text((index*180+4, 4), f'{seconds:.3f}s', fill='black')
    board.save(folder / 'checkpoints.jpg', quality=95)
    return relative(folder / 'checkpoints.jpg')

def main():
    output = OUT / 'M02_parallel_compare_review_v2.mp4'
    if output.exists():
        raise FileExistsError('Keep the earlier version; select a new output name.')
    original_receipt = json.loads((ROOT / '10_automation/runs/2026-W37/reels/google_drive_update_2026-10-02.json').read_text(encoding='utf-8-sig'))
    protected = {r['model']: (ROOT / r['source_video_path'], r['local_sha256']) for r in original_receipt['files']}
    for model, (path, expected) in protected.items():
        if sha(path) != expected:
            raise ValueError(f'{model}: protected first-wave local hash differs')
    graphs = []
    inputs = []
    source_records = []
    for i, letter in enumerate(('A', 'B')):
        source = OUT / f'grok_{letter}_attempt_01/source.mp4'
        result = scan(source)
        save(f'{letter}_source_scan.json', result)
        if result['metadata']['fps'] != 24 or result['decoded_frames'] < 144:
            raise ValueError('New timing decision required; do not retime or freeze the source.')
        w, h = result['metadata']['size']
        # The static narrow window cropped A's moving hem and was rejected.
        # Use one wider fixed window and common scale in both panels;
        # moving boundaries in B and the combined film still require review.
        if (w, h) != (720, 1280):
            raise ValueError('Crop needs a new boundary review for this native size.')
        x, crop_w = 145, 470
        inputs += ['-i', str(source)]
        graph = (f'[{i}:v]trim=start_frame=0:end_frame=144,setpts=PTS-STARTPTS,'
                 f'crop={crop_w}:{h}:{x}:0,scale=352:1280:force_original_aspect_ratio=decrease,'
                 'pad=360:1280:(ow-iw)/2:(oh-ih)/2:color=0xe8e2d9,setsar=1,'
                 f'settb=1/24[p{i}]')
        graphs.append(graph)
        source_records.append(dict(look_id=f'2026-W37-001-L0{i+1}', source_path=relative(source), source_sha256=sha(source), native_size=[w,h], start_frame=0, end_frame_exclusive=144, native_fps=24, speed='unchanged', fixed_crop=[x,0,crop_w,h], fixed_proportional_contain=True, source_scan=result, checkpoint_board=checkpoints(source, f'source_{letter}'), sampled_qa='pending', continuous_qa='pending'))
    graphs.append('[p0][p1]hstack=inputs=2,format=yuv420p[v]')
    run([*inputs,'-filter_complex',';'.join(graphs),'-map','[v]','-an','-c:v','libx264','-crf','18','-preset','medium','-r','24','-frames:v','144','-movflags','+faststart',str(output)])
    decoded = scan(output)
    if decoded['decoded_frames'] != 144 or decoded['metadata']['size'] != (720,1280):
        raise ValueError(f'Unexpected output: {decoded}')
    board = checkpoints(output, 'output_v2')
    for model, (path, expected) in protected.items():
        if sha(path) != expected:
            raise ValueError(f'{model}: protected first-wave file changed')
    receipt = dict(status='research_candidate_pending_visual_review', model_id='M02', output_path=relative(output), output_sha256=sha(output), actual_seconds=decoded['decoded_seconds'], frames=144, fps=24, output_size=[720,1280], sources=source_records, composition='same identity, two weekly looks simultaneously in separate panels', character_actions='native generated actions unchanged in editing', synchronization='common playback start only; gestures are not forced into phase', transitions=[], transition_rule='No interior shot/outfit switches; any later switch must use approximately0.75s dissolve and be reviewed.', baked_text='none', audio='none', no_freeze_reverse_retime=True, checkpoint_board=board, technical_scan=decoded, assistant_sampled_visual_review='pending', assistant_continuous_review=False, user_video_approval=None, cloud_upload=False, publication=False, audience_performance=None, protected_first_wave_local_hashes_match=True, publishable=False)
    save('M02_parallel_compare_review_v2.json',receipt)
    print(json.dumps({'output':str(output),'seconds':receipt['actual_seconds'],'frames':144,'checkpoint_board':board,'first_wave_preserved':True},ensure_ascii=False))

if __name__ == '__main__':
    main()
