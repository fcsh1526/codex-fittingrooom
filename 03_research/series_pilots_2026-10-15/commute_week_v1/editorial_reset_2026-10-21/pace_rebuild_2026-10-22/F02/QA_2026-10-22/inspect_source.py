"""Inspect one SHA-identified F02 pace trial. QA outputs only; never replace films.

Run after the source arrives, with --source-sha EXACT_SHA256. All frame numbers
are zero based. Proposed overlaps are image diagnostics, not accepted edits.
"""
from pathlib import Path
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import json
import math
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / '10_automation/CANONICAL_WORKFLOW.md').is_file())
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
import imageio_ffmpeg
from PIL import Image, ImageDraw

BASE = ROOT / '03_research/series_pilots_2026-10-15/commute_week_v1'
BRIDGE = BASE / 'production_bridge_2026-10-19'
RESET = BASE / 'editorial_reset_2026-10-21'
MASTER = RESET / 'gait_continuity_2026-10-22/cadence_master_trial_01/cadence_source.mp4'
FPS = 24
SIZE = (720, 1280)
FOOT = (0, 740, 720, 1280)
OFFSETS = [0, 3, 6, 9, 12, 15, 17]


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save_new(path, data):
    assert path.parent == HERE or HERE in path.parents, 'Outside QA output directory'
    assert not path.exists(), f'Refuse overwrite: {path}'
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, Image.Image):
        data.save(path, quality=95)
    else:
        path.write_text(data, encoding='utf-8')
    return {'path': str(path), 'sha256': sha(path), 'bytes': path.stat().st_size}


def decode(path, select=None):
    reader = imageio_ffmpeg.read_frames(str(path), pix_fmt='rgb24', output_params=['-vsync', '0'])
    metadata = next(reader)
    assert tuple(metadata['size']) == SIZE, (str(path), metadata)
    assert metadata['fps'] == FPS, (str(path), metadata)
    frames = {}
    total = 0
    try:
        for i, raw in enumerate(reader):
            if select is None or i in select:
                frames[i] = Image.frombytes('RGB', SIZE, raw)
            total = i + 1
    finally:
        reader.close()
    return metadata, frames, total


def board(items, filename, title, cols=5, width=216, crop=None):
    region = (crop[2] - crop[0], crop[3] - crop[1]) if crop else SIZE
    height = round(region[1] * width / region[0])
    row_height = height + 40
    canvas = Image.new('RGB', (cols * width, 56 + math.ceil(len(items) / cols) * row_height), '#f5f3ef')
    draw = ImageDraw.Draw(canvas)
    draw.text((5, 5), title, fill='black')
    draw.text((5, 23), 'QA only; native frame order; not full-speed playback or an accepted film', fill='black')
    for j, (label, frame) in enumerate(items):
        x, y = j % cols * width, 56 + j // cols * row_height
        image = frame.crop(crop) if crop else frame
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        canvas.paste(image, (x, y + 35))
        for line_no, line in enumerate(label.split('\n')):
            draw.text((x + 3, y + line_no * 14), line, fill='black')
    return save_new(HERE / filename, canvas)


def frame_items(frames, indices, role):
    return [(f'{role} f{i:03d} / {i / FPS:.3f}s', frames[i]) for i in indices]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-sha', required=True, help='Expected exact downloaded source SHA256')
    parser.add_argument('--source', default=str(HERE.parent / 'F02_pace_source.mp4'))
    parser.add_argument('--silent', action='store_true', help='Also create a stream-copy silent diagnostic')
    args = parser.parse_args()
    assert re.fullmatch('[0-9a-fA-F]{64}', args.source_sha), 'Exact 64-character SHA256 required'
    source = Path(args.source).resolve()
    assert source.parent == HERE.parent and source.name == 'F02_pace_source.mp4'
    assert source.is_file(), f'Source not downloaded: {source}'
    assert sha(source) == args.source_sha.lower(), 'New source SHA mismatch'
    assert not (HERE / 'technical_report.json').exists(), 'QA was already completed; do not overwrite'

    first = BRIDGE / 'F02/F02_M03_L05_start_candidate_A.png'
    last = BRIDGE / 'F02/F02_M03_L05_end_candidate_A.png'
    f01 = BRIDGE / 'F01/F01_source.mp4'
    old_f02 = BRIDGE / 'F02/motion_retry_01/F02_source.mp4'
    f03 = BRIDGE / 'F03/F03_source.mp4'
    f03_first = BRIDGE / 'F03/F03_M03_L03_start_candidate_A.png'
    accepted_prefix = RESET / 'four_look_review/v1/review.mp4'
    old_film = RESET / 'F05_half_motion_01/five_look_review_2026-10-22/v1/review.mp4'
    expected = {
        first: '99aadb4495132c29d816b51e6bd17238b827b9975746802cadb96d37cabce987',
        last: '10b9a0fd248ae13c1a4409cb9ed3d322c2ea00cc9eb49d7d4cfd052789cb47c7',
        f01: '6a9bf3204aadad28dc710aa914592e26851a03e47209c5bd9b682286b184fa50',
        old_f02: 'cc23a3e22b5d51b2db42cc87b33371f73189b25b101cc37fff3a070dd68800b0',
        f03: '26087d5c7f4fd7dd8153b9c0c5a70fcdeea0429c0e8def12dc672632a9b499d5',
        f03_first: 'a7b6e33248b5e90c9c63ba0cda1264f23b8ebe8a3dabcb5baeab017c0b30db9e',
        accepted_prefix: '3c0f3fa5bb0c90d0d9b5d434ada37cd5dbe130658d5bff24c01143feb77f1f94',
        old_film: 'e4ed855809463e9c8421c5c7d4292f62bdf3f12f1c5f30af8f5c0e0a4edd32dc',
        MASTER: '9707b42d230466ef2c2088a926ec45745d546d717c0fa9756d1b8e52ac0ab21d',
    }
    protected_before = {str(p): sha(p) for p in expected}
    assert protected_before == {str(p): h for p, h in expected.items()}, 'Protected input identity mismatch'

    metadata, frames, count = decode(source)
    assert count >= 145, f'Need f127..144 for the proposed J23, got {count} frames'
    assert count <= 146, f'Unexpected six-second length: {count}; reassess mapping before QA'
    meta_f01, frames_f01, count_f01 = decode(f01, set(range(60, 78)))
    meta_f03, frames_f03, count_f03 = decode(f03, set(range(1, 19)))
    master_indices = sorted(set(range(0, 145, 3)) | {144})
    meta_master, frames_master, count_master = decode(MASTER, set(master_indices))
    assert count_f01 > 77 and count_f03 > 18 and count_master > 144

    artifacts = []
    checkpoints = [round(i * (count - 1) / 24) for i in range(25)]
    every3 = sorted(set(range(0, count, 3)) | {count - 1})
    every6 = sorted(set(range(0, count, 6)) | {count - 1})
    artifacts.append(board(frame_items(frames, checkpoints, 'new F02'), 'checkpoints_25.jpg', 'New F02: 25 whole-frame checkpoints'))
    artifacts.append(board(frame_items(frames, every3, 'new F02'), 'new_F02_every3_foot.jpg', 'New F02 feet: every 3 native frames; QA-only y740:1280 crop', crop=FOOT, width=230))
    artifacts.append(board(frame_items(frames, every6, 'new F02'), 'new_F02_every6_whole.jpg', 'New F02: every 6 native frames; full raster'))
    artifacts.append(board(frame_items(frames_master, master_indices, 'pace master'), 'selected_master_every3_foot.jpg', 'Selected pace master: every 3 native frames; QA-only feet crop', crop=FOOT, width=230))

    sample_indices = sorted(set([0, round((count - 1) / 4), round((count - 1) / 2), round(3 * (count - 1) / 4), count - 1, 127, 144]))
    for i in sorted(set(sample_indices) | set(range(18)) | set(range(127, 145))):
        artifacts.append(save_new(HERE / 'frames' / f'new_F02_f{i:06d}.png', frames[i]))
    first_image = Image.open(first).convert('RGB')
    last_image = Image.open(last).convert('RGB')
    f03_first_image = Image.open(f03_first).convert('RGB')
    artifacts.append(board([
        ('approved F02 first\nphoto normalized for QA', first_image),
        ('new source f000\nfirst comparison only', frames[0]),
        ('approved F02 last\nphoto normalized for QA', last_image),
        (f'new source f{count - 1:03d}\nlast comparison only', frames[count - 1]),
    ], 'first_last_comparison.jpg', 'Approved photographs vs new source endpoints; not a motion pass', cols=4, width=300))
    artifacts.append(board([
        ('new F02 f127\nproposed overlap START', frames[127]),
        ('approved F03 first\ncreated from OLD F02 f127', f03_first_image),
        ('original F03 f001\nactual proposed incoming', frames_f03[1]),
    ], 'proposed_J23_start_comparison.jpg', 'Proposed NEW J23 boundary; old still approval does not approve new overlap', cols=3, width=300))

    joins = []
    for name, outgoing, start_out, incoming, start_in, roles in [
        ('J12', frames_f01, 60, frames, 0, ('old F01', 'new F02')),
        ('J23', frames, 127, frames_f03, 1, ('new F02', 'old F03')),
    ]:
        items = []
        mapping = []
        for offset in OFFSETS:
            out_i, in_i = start_out + offset, start_in + offset
            weight = (offset + 1) / 18
            out_image, in_image = outgoing[out_i], incoming[in_i]
            mix = Image.blend(out_image, in_image, weight)
            items.extend([
                (f'OUT {roles[0]} f{out_i:03d}\n{out_i / FPS:.3f}s; o{offset}', out_image),
                (f'IN {roles[1]} f{in_i:03d}\n{in_i / FPS:.3f}s; o{offset}', in_image),
                (f'PROPOSED blend o{offset}\nin-weight {weight:.4f}', mix),
            ])
            mapping.append({'overlap_offset': offset, 'outgoing_frame': out_i, 'incoming_frame': in_i, 'incoming_blend_weight': weight})
        artifacts.append(board(items, f'proposed_{name}_whole.jpg', f'{name} PROPOSED NEW overlap, not approved film: OUT / IN / expected 18f blend', cols=3, width=300))
        artifacts.append(board(items, f'proposed_{name}_foot.jpg', f'{name} PROPOSED NEW overlap, QA-only feet crop: OUT / IN / expected blend', cols=3, width=240, crop=FOOT))
        joins.append({'id': name, 'status': 'proposed_new_overlap_not_approved_or_rendered_film', 'frames': 18, 'seconds': 0.75, 'outgoing': roles[0], 'incoming': roles[1], 'outgoing_half_open': [start_out, start_out + 18], 'incoming_half_open': [start_in, start_in + 18], 'rows': mapping})

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    info = subprocess.run([ffmpeg, '-hide_banner', '-i', str(source)], capture_output=True, check=False)
    artifacts.append(save_new(HERE / 'source_stream_info.txt', info.stderr.decode('utf-8', errors='replace')))
    silent_record = None
    if args.silent:
        silent = HERE / 'F02_pace_silent.mp4'
        assert not silent.exists(), 'Refuse existing silent output'
        result = subprocess.run([ffmpeg, '-hide_banner', '-n', '-i', str(source), '-map', '0:v:0', '-an', '-c:v', 'copy', '-movflags', '+faststart', str(silent)], capture_output=True, check=False)
        artifacts.append(save_new(HERE / 'silent_remux_log.txt', result.stderr.decode('utf-8', errors='replace')))
        assert result.returncode == 0, 'Silent stream-copy failed'
        bitstream_hashes = []
        for path in [source, silent]:
            result = subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-i', str(path), '-map', '0:v:0', '-c:v', 'copy', '-bsf:v', 'h264_mp4toannexb', '-f', 'h264', 'pipe:1'], capture_output=True, check=False)
            assert result.returncode == 0, f'Bitstream comparison failed: {path}'
            bitstream_hashes.append(hashlib.sha256(result.stdout).hexdigest())
        assert bitstream_hashes[0] == bitstream_hashes[1], 'Silent copy video bitstream differs'
        silent_record = {'path': str(silent), 'sha256': sha(silent), 'bytes': silent.stat().st_size, 'stream_copy': True, 'audio_removed': True, 'retimed': False, 'cropped': False, 'reencoded': False, 'source_h264_annexb_sha256': bitstream_hashes[0], 'silent_h264_annexb_sha256': bitstream_hashes[1], 'identical_video_bitstream': True}

    protected_after = {str(p): sha(p) for p in expected}
    assert protected_before == protected_after, 'Protected input changed while inspecting'
    assert sha(source) == args.source_sha.lower(), 'New source mutated while inspecting'
    report = {
        'recorded_at_taipei': datetime.now(timezone(timedelta(hours=8))).isoformat(),
        'purpose': 'SHA-bound source and proposed boundary inspection only; no full film render or replacement',
        'source': {'path': str(source), 'sha256': sha(source), 'bytes': source.stat().st_size, 'metadata': metadata, 'fully_decoded': True, 'frames': count, 'native_fps': FPS, 'pixels': list(SIZE), 'derived_frame_duration_seconds': count / FPS, 'individual_source_PTS_measured': False},
        'references': {'F01': {'path': str(f01), 'metadata': meta_f01, 'frames': count_f01}, 'F03': {'path': str(f03), 'metadata': meta_f03, 'frames': count_f03}, 'selected_pace_master': {'path': str(MASTER), 'metadata': meta_master, 'frames': count_master, 'role': 'human-selected visual pace standard only; NOT an engine video-motion input'}},
        'proposed_joins': joins,
        'source_sample_frame_indices': sample_indices,
        'whole_frame_checkpoints': checkpoints,
        'feet_crop_QA_only_xyxy': list(FOOT),
        'artifacts': artifacts,
        'silent': silent_record,
        'protected_hashes_before': protected_before,
        'protected_hashes_after': protected_after,
        'all_source_hashes_unchanged': True,
        'full_film_rendered_or_replaced': False,
        'source_speed_factor': 1,
        'source_frame_order_changed': False,
        'visual_pass': None,
        'user_motion_approval': None,
        'normal_speed_continuous_visual_review': False,
        'footfall_measurement': None,
        'slide_free_claim': False,
        'limits': ['Contact sheets are sampled visual evidence, not precise foot-ground tracking.', 'Compare observed front/middle/end phase spacing against selected master 12-15 frame range; the prompt is not evidence of success.', 'Both J12 and J23 need fresh visual QA; old first/last still approval does not transfer motion or overlap approval.', 'Expected blends are diagnostic images, not a rendered, accepted or publishable film.'],
    }
    save_new(HERE / 'technical_report.json', json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({'source_sha256': report['source']['sha256'], 'frames': count, 'fps': FPS, 'pixels': SIZE, 'qa_artifacts': len(artifacts), 'report': str(HERE / 'technical_report.json'), 'visual_pass': None}, ensure_ascii=False))


if __name__ == '__main__':
    main()
