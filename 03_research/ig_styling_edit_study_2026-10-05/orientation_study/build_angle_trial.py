"""Build one independent native-speed angle comparison; preserve prior outputs."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
sys.path.insert(0, str(ROOT / '10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    output = HERE / 'M02_parallel_angle_review_v2.mp4'
    receipt_path = output.with_suffix('.json')
    if output.exists() or receipt_path.exists():
        raise FileExistsError('Keep prior candidates; choose a new version.')
    prior = json.loads((HERE / 'research_manifest.json').read_text(encoding='utf-8-sig'))
    protected = [(ROOT / r['path'], r['sha256']) for r in prior['protected_first_wave']]
    protected += [
        (HERE.parent / 'simultaneous_comparison/M02_parallel_compare_review_v4_size_matched.mp4', 'a383ea81ef1eb8e4b27993954aafe11376b80183bfc4634242370a7e0bdf9499'),
        (ROOT / '10_automation/runs/2026-W37/reels/M02_paired_D_v1/review/M02_paired_D_v1_review_v2_matched.mp4', '3c077e1e05d31db0e92176ec49313ff051ddddfd8e3affb9b431ec88c6b27989'),
    ]
    for p, expected in protected:
        if sha(p) != expected:
            raise ValueError(f'Protected output changed: {p.name}')
    graphs, inputs, sources = [], [], []
    for i, letter in enumerate(('A', 'B')):
        source = HERE / f'grok_{letter}_recovery_01/source.mp4'
        observed = json.loads((HERE / f'qa/recovery_01/{letter}/inspection_receipt.json').read_text(encoding='utf-8'))
        if observed['observed_fps'] != 24 or observed['native_size'] != [720,1280] or observed['decoded_frames'] != 145:
            raise ValueError('Timing/dimensions require a new composition decision.')
        if sha(source) != observed['source_sha256']:
            raise ValueError('Source differs from inspected original.')
        inputs += ['-i', str(source)]
        # Fresh constant window reviewed on all 25 samples; keeps tote and skirt.
        # The same scale is appropriate for these sources, not inherited from v4.
        graphs.append(f'[{i}:v]trim=start_frame=0:end_frame=144,setpts=PTS-STARTPTS,'
                      'crop=490:1280:135:0,scale=352:920:flags=lanczos,'
                      'pad=360:1280:4:180:color=0xe8e2d9,setsar=1,settb=1/24[p'+str(i)+']')
        sources.append(dict(label=letter, path=source.relative_to(ROOT).as_posix(),
                            sha256=observed['source_sha256'], native_frames=145,
                            selected_frames=[0,144], native_fps=24,
                            fixed_window_xywh=[135,0,490,1280], image_rectangle_xywh=[4,180,352,920],
                            speed='unchanged', action='unchanged'))
    graphs.append('[p0][p1]hstack=inputs=2,format=yuv420p[v]')
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg,'-hide_banner','-loglevel','error',*inputs,
                    '-filter_complex',';'.join(graphs),'-map','[v]','-an','-c:v','libx264',
                    '-crf','18','-preset','medium','-r','24','-frames:v','144','-movflags','+faststart',str(output)],check=True)
    decoded = scan(output)
    if decoded['decoded_frames'] != 144 or decoded['metadata']['fps'] != 24 or decoded['metadata']['size'] != (720,1280):
        raise ValueError('Unexpected rendered video metadata.')
    qa = HERE / 'qa/output_v2'
    qa.mkdir()
    reader=imageio_ffmpeg.read_frames(str(output))
    next(reader)
    frames=[]
    selected={0,24,36,72,84,108,143}
    for n, raw in enumerate(reader):
        if n in selected:
            frame=Image.frombytes('RGB',(720,1280),raw)
            frame.save(qa/f'frame_{n:06d}.png')
            frames.append((n,frame))
    board=Image.new('RGB',(1080,408),'white')
    draw=ImageDraw.Draw(board)
    regular_frames=[pair for pair in frames if pair[0] in {0,36,72,108,143}]
    for i,(n,frame) in enumerate(regular_frames):
        frame.thumbnail((216,384),Image.Resampling.LANCZOS)
        board.paste(frame,(i*216,24))
        draw.text((i*216+4,4),f'f{n} / {n/24:.3f}s',fill='black')
    board.save(qa/'checkpoints.jpg',quality=95)
    for p, expected in protected:
        if sha(p) != expected:
            raise ValueError('Protected output changed during render.')
    receipt=dict(status='research_candidate_pending_user_visual_approval',model='M02',
                 look_ids=prior['look_ids'],output=output.relative_to(ROOT).as_posix(),
                 output_sha256=sha(output),size=[720,1280],fps=24,frames=144,seconds=6,
                 sources=sources,technical_scan=decoded,
                 image_scale_note='Common constant near-proportional raster scale; rounding 920px height introduces <0.1% ratio difference. No subject tracking.',
                 informational_change='Front to side-facing torso views add sleeve and dress outline; bags partly obscure shirt side.',
                 actual_turn_note='More side-facing than requested 30 degrees; angle not calibrated. A turns earlier than B.',
                 synchronization='Common start only; no forced gesture phase',baked_text=False,audio=False,
                 output_clock='Explicit native 24fps timebase and encoder frame rate; source frame selection unchanged.',
                 interior_switches=[],transition_rule='Any future switch needs approximately 0.75s dissolve.',
                 retime_freeze_reverse_replay=False,assistant_sampled_review='pending',
                 assistant_continuous_review=False,user_approval=None,publishable=False,
                 protected_media_hashes_matched=True,cloud_writes=False,publication=False,audience_metrics=None)
    save(receipt_path,receipt)
    print(json.dumps({'output':str(output),'sha256':receipt['output_sha256'],'seconds':6,
                      'qa_board':str(qa/'checkpoints.jpg'),'protected_media_unchanged':True},ensure_ascii=False))

if __name__=='__main__':
    main()
