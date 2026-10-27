"""Inspect one SHA-bound F03 native gait trial and both proposed overlaps.

Prepare only until root supplies the exact downloaded --source-sha. All frame
indices are zero based. QA contact sheets do not alter any source or film.
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
    frames, total = {}, 0
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
    draw.text((5, 23), 'QA only; native frame order; not continuous playback or an accepted film', fill='black')
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
    parser.add_argument('--source-sha', required=True, help='Exact SHA256 supplied by root after download')
    parser.add_argument('--source', default=str(HERE.parent / 'F03_pace_source.mp4'))
    parser.add_argument('--silent', action='store_true', help='Create a separate stream-copy silent diagnostic')
    args = parser.parse_args()
    assert re.fullmatch('[0-9a-fA-F]{64}', args.source_sha), 'Exact 64-character SHA256 required'
    source = Path(args.source).resolve()
    assert source.parent == HERE.parent and source.name == 'F03_pace_source.mp4'
    assert source.is_file(), f'Source not downloaded: {source}'
    assert sha(source) == args.source_sha.lower(), 'New source SHA mismatch'
    assert not (HERE / 'technical_report.json').exists(), 'QA already completed; do not overwrite'

    f01 = BRIDGE / 'F01/F01_source.mp4'
    f02 = RESET / 'pace_rebuild_2026-10-22/F02/F02_pace_source.mp4'
    original_f03 = BRIDGE / 'F03/F03_source.mp4'
    f04 = RESET / 'F04_motion_01/F04_source.mp4'
    f05 = RESET / 'F05_half_motion_01/F05_half_source.mp4'
    old_film = RESET / 'F05_half_motion_01/five_look_review_2026-10-22/v1/review.mp4'
    context = RESET / 'pace_rebuild_2026-10-22/context_review_v1/review.mp4'
    first = BRIDGE / 'F03/F03_M03_L03_start_candidate_A.png'
    anchor = RESET / 'source_audit/F03_f091.png'
    original_end_overlap = RESET / 'source_audit/F03_f108.png'
    expected = {
        f01: '6a9bf3204aadad28dc710aa914592e26851a03e47209c5bd9b682286b184fa50',
        f02: 'f6fcd8e02e99a6dd1b6282d5b5eb5e2b0eeca0bacc10c54d83940cfa4a0bbdf6',
        original_f03: '26087d5c7f4fd7dd8153b9c0c5a70fcdeea0429c0e8def12dc672632a9b499d5',
        f04: 'e32ee2f282b80dec8b8666d6755c9d2e77e5def6850bc53c89b5333927cd2208',
        f05: 'c2d9f0442ea0d9b9c50674fb959b96ae53a8264c3947c509aa91f05e4bec9aa9',
        old_film: 'e4ed855809463e9c8421c5c7d4292f62bdf3f12f1c5f30af8f5c0e0a4edd32dc',
        context: '799911d2a7637c7920c0d2ecec47cc36bea670142a57c9c947dacd256b24d819',
        first: 'a7b6e33248b5e90c9c63ba0cda1264f23b8ebe8a3dabcb5baeab017c0b30db9e',
        anchor: '915d8618c9dca7bd16482ec37ee8fca64aa6d3b6177f210de36a032f791e6526',
        original_end_overlap: '62517bccb2d6d47c32666bcaab4734690eaf29567a9133f61c260cebd3861c44',
        MASTER: '9707b42d230466ef2c2088a926ec45745d546d717c0fa9756d1b8e52ac0ab21d',
    }
    protected_before = {str(p): sha(p) for p in expected}
    assert protected_before == {str(p): h for p, h in expected.items()}, 'Protected input identity mismatch'

    metadata, frames, count = decode(source)
    assert 145 <= count <= 146, f'Unexpected six-second length: {count}; reassess mapping'
    meta_f02, frames_f02, count_f02 = decode(f02, set(range(127, 145)))
    meta_f04, frames_f04, count_f04 = decode(f04, set(range(18)))
    master_indices = sorted(set(range(0, 145, 3)) | {144})
    original_indices = sorted(set(range(0, 145, 3)) | {1, 91, 108, 144})
    meta_master, frames_master, count_master = decode(MASTER, set(master_indices))
    meta_original, frames_original, count_original = decode(original_f03, set(original_indices))
    assert count_f02 > 144 and count_f04 > 17 and count_master > 144 and count_original > 144

    artifacts = []
    checkpoints = [round(i * (count - 1) / 24) for i in range(25)]
    every3 = sorted(set(range(0, count, 3)) | {count - 1})
    every6 = sorted(set(range(0, count, 6)) | {count - 1})
    artifacts.append(board(frame_items(frames, checkpoints, 'new F03'), 'checkpoints_25.jpg', 'New F03: 25 whole-frame checkpoints; selected [1,109)'))
    artifacts.append(board(frame_items(frames, every3, 'new F03'), 'new_F03_every3_foot.jpg', 'New F03 feet: every 3 native frames; QA-only y740:1280 crop', crop=FOOT, width=230))
    artifacts.append(board(frame_items(frames, every6, 'new F03'), 'new_F03_every6_whole.jpg', 'New F03: every 6 native frames; full raster'))
    artifacts.append(board(frame_items(frames_master, master_indices, 'pace master'), 'selected_master_every3_foot.jpg', 'Selected pace master: every 3 native frames; QA-only feet crop', crop=FOOT, width=230))
    artifacts.append(board(frame_items(frames_original, original_indices, 'old F03'), 'original_F03_every3_foot.jpg', 'Original F03 native feet; only [1,109) used in current film', crop=FOOT, width=230))

    sample_indices = sorted(set([0, 1, 18, 36, 72, 90, 91, 108, 109, 127, 144, count - 1]))
    for i in sorted(set(sample_indices) | set(range(1, 19)) | set(range(91, 109))):
        artifacts.append(save_new(HERE / 'frames' / f'new_F03_f{i:06d}.png', frames[i]))
    first_image = Image.open(first).convert('RGB')
    anchor_image = Image.open(anchor).convert('RGB')
    assert anchor_image.size == SIZE
    anchor_pixel_identical = anchor_image.tobytes() == frames_original[91].tobytes()
    assert anchor_pixel_identical, 'Saved f91 anchor is not the exact decoded original f91'
    artifacts.append(board([
        ('approved F03 first\nphoto normalized for QA', first_image),
        ('new source f000\nfirst comparison only', frames[0]),
        ('original F03 f001\nold selected incoming', frames_original[1]),
        ('new F03 f001\nproposed selected incoming', frames[1]),
    ], 'first_comparison.jpg', 'Approved first photo and actual old/new selected entry; not a motion pass', cols=4, width=300))
    artifacts.append(board([
        ('old source f091\nexact extracted anchor', anchor_image),
        ('new source f091\nkeyframe target 91/24s', frames[91]),
        ('old source f108\nold overlap end, NOT control', frames_original[108]),
        ('new source f108\nproposed selected last frame', frames[108]),
    ], 'anchor_f091_and_overlap_end_comparison.jpg', 'Original f91 is accepted-video extract, NOT separately approved AI photo', cols=4, width=300))

    joins = []
    for name, outgoing, start_out, incoming, start_in, roles, timeline in [
        ('J23', frames_f02, 127, frames, 1, ('accepted new F02', 'new F03'), [187, 205]),
        ('J34', frames, 91, frames_f04, 0, ('new F03', 'original F04'), [277, 295]),
    ]:
        items, mapping = [], []
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
        joins.append({'id': name, 'status': 'proposed_new_overlap_not_approved_or_rendered_film', 'frames': 18, 'seconds': 0.75, 'outgoing': roles[0], 'incoming': roles[1], 'outgoing_half_open': [start_out, start_out + 18], 'incoming_half_open': [start_in, start_in + 18], 'proposed_whole_context_half_open': timeline, 'rows': mapping})

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    info = subprocess.run([ffmpeg, '-hide_banner', '-i', str(source)], capture_output=True, check=False)
    artifacts.append(save_new(HERE / 'source_stream_info.txt', info.stderr.decode('utf-8', errors='replace')))
    silent_record = None
    if args.silent:
        silent = HERE / 'F03_pace_silent.mp4'
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
        'purpose': 'SHA-bound source and proposed J23/J34 inspection only; no full film render or replacement',
        'source': {'path': str(source), 'sha256': sha(source), 'bytes': source.stat().st_size, 'metadata': metadata, 'fully_decoded': True, 'frames': count, 'native_fps': FPS, 'pixels': list(SIZE), 'derived_frame_duration_seconds': count / FPS, 'individual_source_PTS_measured': False, 'proposed_selected_half_open': [1, 109]},
        'references': {'accepted_F02': {'path': str(f02), 'metadata': meta_f02, 'frames': count_f02}, 'original_F03': {'path': str(original_f03), 'metadata': meta_original, 'frames': count_original}, 'original_F04': {'path': str(f04), 'metadata': meta_f04, 'frames': count_f04}, 'selected_pace_master': {'path': str(MASTER), 'metadata': meta_master, 'frames': count_master, 'role': 'human-selected visual pace standard only; NOT engine motion conditioning'}},
        'anchor': {'path': str(anchor), 'sha256': sha(anchor), 'original_source_frame': 91, 'requested_timestamp_seconds': 91 / FPS, 'decoded_original_f91_pixel_identical': anchor_pixel_identical, 'role': 'exact original accepted-video extract; no separate still-photograph approval claimed', 'exact_new_f91_hit_claim': False},
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
        'limits': ['Contact sheets are sampled visual evidence, not precise foot-ground tracking.', 'Assess selected [1,109) separately from unused new f109..144 tail.', 'Compare observed phase spacing, body progression and foot plant against actual adjacent sources; prompt and keyframe request are not success evidence.', 'Original f91 anchors only the beginning of J34; all 18 overlap frames and both boundaries need fresh QA.', 'Expected image blends are diagnostics, not a rendered, accepted or publishable whole film.'],
    }
    save_new(HERE / 'technical_report.json', json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({'source_sha256': report['source']['sha256'], 'frames': count, 'fps': FPS, 'pixels': SIZE, 'qa_artifacts': len(artifacts), 'report': str(HERE / 'technical_report.json'), 'visual_pass': None}, ensure_ascii=False))


if __name__ == '__main__':
    main()
