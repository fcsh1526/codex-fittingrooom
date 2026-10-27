"""Render a separately versioned, native-speed matched-start trial after source review."""
import argparse
import json
from datetime import date
from pathlib import Path
from PIL import Image, ImageDraw
from build_distance_review import ROOT, HERE, sha, save, selected_frames, imageio_ffmpeg, scan


def board(items, target, title):
    columns, tw, th = 5, 208, 368
    canvas = Image.new('RGB', (columns * tw, 30 + ((len(items) + columns - 1) // columns) * (th + 25)), '#f5f3ef')
    draw = ImageDraw.Draw(canvas)
    draw.text((5, 7), title, fill='black')
    for slot, (index, im) in enumerate(items):
        im = im.copy()
        im.thumbnail((tw - 8, th - 6), Image.Resampling.LANCZOS)
        x, y = slot % columns * tw, 30 + slot // columns * (th + 25)
        draw.text((x + 4, y + 4), f'f{index} / {index/24:.3f}s', fill='black')
        canvas.paste(im, (x + (tw - im.width) // 2, y + 25 + (th - im.height) // 2))
    canvas.save(target, quality=95)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True, choices=('v2', 'v3', 'v4'))
    parser.add_argument('--b-folder', required=True)
    parser.add_argument('--b-sha', required=True)
    parser.add_argument('--a-count', type=int, default=96)
    parser.add_argument('--b-count', type=int, default=144)
    parser.add_argument('--date', default=date.today().isoformat())
    args = parser.parse_args()
    A = HERE / 'near_start_A_attempt_01/source.mp4'
    B = (HERE / args.b_folder / 'source.mp4').resolve()
    if not B.is_relative_to(HERE) or not B.is_file():
        raise ValueError('New reviewed B source must exist inside this trial')
    output = HERE / f'M02_body_distance_review_{args.version}.mp4'
    receipt = output.with_suffix('.json')
    qa = HERE / f'qa/output_{args.version}'
    if output.exists() or receipt.exists() or qa.exists():
        raise FileExistsError('Preserve all earlier versions and QA')
    a_sha = 'be49906fa1ec7397bb456acc1ce7947325e71b4ce5a0692d7235d878ad6017ea'
    a_count, b_count, overlap = args.a_count, args.b_count, 18
    if min(a_count, b_count) <= overlap or max(a_count, b_count) > 145:
        raise ValueError('Source interval must be a reviewed native selection')
    original = json.loads((HERE / 'M02_body_distance_review_v1.json').read_text(encoding='utf-8'))
    protected = [(ROOT / item['path'], item['sha256']) for item in original['protected_media']]
    protected.append((HERE / 'M02_body_distance_review_v1.mp4', '170caa07b1f385562c93151ce1d03c3689504be8503dfb701d79d7c48c70acc6'))
    for path, expected in protected:
        if sha(path) != expected:
            raise ValueError('Protected media differs: ' + str(path))
    a = selected_frames(A, a_count, a_sha)
    b = selected_frames(B, b_count, args.b_sha)
    writer = imageio_ffmpeg.write_frames(str(output), (720, 1280), fps=24, codec='libx264',
        pix_fmt_in='rgb24', pix_fmt_out='yuv420p', quality=None, macro_block_size=1,
        ffmpeg_log_level='error', output_params=['-crf', '18', '-preset', 'medium', '-movflags', '+faststart'])
    writer.send(None)
    mapping = []
    try:
        for index in range(a_count - overlap):
            writer.send(next(a).tobytes())
            mapping.append({'output_frame': len(mapping), 'A_native_frame': index, 'B_native_frame': None, 'B_alpha': 0})
        for index in range(overlap):
            alpha = (index + 1) / overlap
            writer.send(Image.blend(next(a), next(b), alpha).tobytes())
            mapping.append({'output_frame': len(mapping), 'A_native_frame': a_count - overlap + index, 'B_native_frame': index, 'B_alpha': alpha})
        for index in range(overlap, b_count):
            writer.send(next(b).tobytes())
            mapping.append({'output_frame': len(mapping), 'A_native_frame': None, 'B_native_frame': index, 'B_alpha': 1})
    finally:
        writer.close()
        a.close()
        b.close()
    count = a_count + b_count - overlap
    decoded = scan(output)
    if decoded['decoded_frames'] != count or decoded['metadata']['fps'] != 24 or tuple(decoded['metadata']['size']) != (720, 1280):
        raise ValueError('Render clock/dimensions/frame count mismatch')
    qa.mkdir(parents=True)
    (qa / 'full').mkdir()
    points = {round(i * (count - 1) / 24) for i in range(25)}
    join_range = range(max(0, a_count - overlap - 8), min(count, a_count + 8))
    keep = points | set(join_range)
    reader = imageio_ffmpeg.read_frames(str(output), pix_fmt='rgb24')
    next(reader)
    full, joins = [], []
    for index, raw in enumerate(reader):
        if index not in keep:
            continue
        im = Image.frombytes('RGB', (720, 1280), raw)
        im.save(qa / 'full' / f'frame_{index:06d}.png')
        if index in points:
            full.append((index, im))
        if index in join_range:
            joins.append((index, im))
    board(full, qa / 'full_25_checkpoints.jpg', 'Matched distance output samples; continuous review separate')
    board(joins, qa / 'transition_all_boundary_frames.jpg', 'Every transition frame with eight native frames on each side')
    for path, expected in protected + [(A, a_sha), (B, args.b_sha)]:
        if sha(path) != expected:
            raise ValueError('Reviewed/protected source changed during composition')
    save(qa / 'decode_scan.json', decoded)
    save(qa / 'frame_mapping.json', mapping)
    info = {
        'status': 'research_candidate_pending_visual_review', 'date': args.date, 'model': 'M02',
        'look_ids': ['2026-W37-001-L01', '2026-W37-001-L02'],
        'output': output.relative_to(ROOT).as_posix(), 'output_sha256': sha(output),
        'native_size': [720, 1280], 'fps': 24, 'frames': count, 'seconds': count / 24,
        'sources': [
            {'role': 'A_near_to_full', 'path': A.relative_to(ROOT).as_posix(), 'sha256': a_sha, 'selected_native_frames_half_open': [0, a_count]},
            {'role': 'B_matched_full_to_near', 'path': B.relative_to(ROOT).as_posix(), 'sha256': args.b_sha, 'selected_native_frames_half_open': [0, b_count]},
        ],
        'transition': {'type': 'linear_cross_dissolve', 'seconds': .75, 'frames': overlap,
                       'output_frames_half_open': [a_count - overlap, a_count], 'B_weight': '(overlap_index+1)/18'},
        'frame_mapping': str((qa / 'frame_mapping.json').relative_to(HERE)),
        'framing_transform': 'none; native full raster both sources',
        'retime_freeze_reverse_replay': False, 'forced_action_synchronization': False,
        'text': 'none', 'audio': 'none; frame-only encode',
        'technical_scan': str((qa / 'decode_scan.json').relative_to(HERE)),
        'transition_boundary_QA_indices': list(join_range),
        'assistant_sampled_review': 'pending', 'assistant_continuous_review': False,
        'user_approval': None, 'publishable': False,
        'limitations': ['Starting-still approval does not establish native motion, paired overlap or continuous comfort.',
                        'Actual clothing clarity and 18 paired dissolve frames must be reviewed before showing as a candidate.'],
        'protected_media_hashes_matched': True,
        'protected_media': [{'path': p.relative_to(ROOT).as_posix(), 'sha256': v} for p, v in protected],
        'cloud_write': False, 'publication': False, 'global_template_adopted': False, 'audience_performance': None,
    }
    save(receipt, info)
    print(json.dumps({k: info[k] for k in ('output', 'output_sha256', 'seconds', 'frames', 'protected_media_hashes_matched')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
