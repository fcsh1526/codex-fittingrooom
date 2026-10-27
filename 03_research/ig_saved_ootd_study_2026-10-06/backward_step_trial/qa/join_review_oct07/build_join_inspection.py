"""QA-only native A/B overlap boards; never edits a delivery video or status."""
import argparse
from datetime import date
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / '10_automation').is_dir())
TRIAL = HERE.parent.parent
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
import imageio_ffmpeg

A_PATH = TRIAL / 'near_start_A_attempt_01/source.mp4'
A_SHA = 'be49906fa1ec7397bb456acc1ce7947325e71b4ce5a0692d7235d878ad6017ea'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_kept(path, expected_hash, indices):
    if sha(path) != expected_hash:
        raise ValueError('Unreviewed source hash: ' + str(path))
    reader = imageio_ffmpeg.read_frames(str(path), pix_fmt='rgb24')
    meta = next(reader)
    if meta['fps'] != 24 or tuple(meta['size']) != (720, 1280):
        reader.close()
        raise ValueError('Source clock/dimensions differ from the plan')
    kept = {}
    try:
        for index, raw in enumerate(reader):
            if index in indices:
                kept[index] = Image.frombytes('RGB', (720, 1280), raw)
            if index >= max(indices):
                break
    finally:
        reader.close()
    if set(kept) != set(indices):
        raise ValueError('Requested native frames unavailable')
    if sha(path) != expected_hash:
        raise ValueError('Source changed during QA')
    return kept


def save_group(items, path, title, crop=None):
    thumb = (216, 384) if crop is None else (216, 270)
    row_height = thumb[1] + 30
    canvas = Image.new('RGB', (3 * 224, 34 + len(items) * row_height), '#f5f3ef')
    draw = ImageDraw.Draw(canvas)
    draw.text((6, 8), title, fill='black')
    for row, item in enumerate(items):
        for col, role in enumerate(('A', 'B', 'blend')):
            im = item[role]
            if crop:
                im = im.crop(crop)
            im = im.copy()
            im.thumbnail(thumb, Image.Resampling.LANCZOS)
            x, y = col * 224, 34 + row * row_height
            draw.text((x + 4, y + 4), item[role + '_label'], fill='black')
            canvas.paste(im, (x + (224 - im.width) // 2, y + 28))
    canvas.save(path, quality=96)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--b-source', required=True)
    parser.add_argument('--b-sha256', required=True)
    parser.add_argument('--a-end', type=int, default=96)
    parser.add_argument('--b-start', type=int, default=0)
    parser.add_argument('--label', default='new_B_A96')
    parser.add_argument('--date', default=date.today().isoformat())
    args = parser.parse_args()
    if args.a_end not in (90, 96, 102):
        raise ValueError('Use the documented first join or a small actual-tail comparison')
    if args.b_start < 0 or args.b_start + 26 > 145:
        raise ValueError('B native inspection window unavailable')
    if Path(args.label).name != args.label:
        raise ValueError('Label must be a filename component')
    out = HERE / args.label
    if out.exists():
        raise FileExistsError('Keep the previous QA inspection')
    b_path = Path(args.b_source).resolve()
    overlap = 18
    start = args.a_end - overlap
    a_indices = set(range(max(0, start - 8), args.a_end))
    b_indices = set(range(args.b_start, args.b_start + 26))
    a = read_kept(A_PATH, A_SHA, a_indices)
    b = read_kept(b_path, args.b_sha256.lower(), b_indices)
    out.mkdir()
    native = out / 'transition_native_full'
    native.mkdir()
    rows = []
    mapping = []
    for k in range(overlap):
        alpha = (k + 1) / overlap
        ai = start + k
        bi = args.b_start + k
        blended = Image.blend(a[ai], b[bi], alpha)
        blended.save(native / f'output_{ai:06d}_A{ai}_B{bi}.png')
        rows.append({'A': a[ai], 'B': b[bi], 'blend': blended,
                     'A_label': f'A f{ai} / {ai / 24:.3f}s',
                     'B_label': f'B f{bi} / {bi / 24:.3f}s',
                     'blend_label': f'output f{ai}; B {alpha:.3f}'})
        mapping.append({'output_frame': ai, 'A_native_frame': ai,
                        'B_native_frame': bi, 'B_alpha': alpha})
    for first in range(0, overlap, 6):
        save_group(rows[first:first + 6], out / f'paired_full_{first + 1:02d}_{first + 6:02d}.jpg',
                   f'QA only: native A/B and blend; overlap {first + 1}-{first + 6}')
        # These common fixed windows are inspection crops only, not delivery transforms.
        save_group(rows[first:first + 6], out / f'paired_head_{first + 1:02d}_{first + 6:02d}.jpg',
                   f'QA only: common head/shoulder window; overlap {first + 1}-{first + 6}',
                   crop=(220, 100, 500, 450))
        save_group(rows[first:first + 6], out / f'paired_lower_{first + 1:02d}_{first + 6:02d}.jpg',
                   f'QA only: common hem/feet window; overlap {first + 1}-{first + 6}',
                   crop=(200, 780, 530, 1190))
    # Eight actual native frames on each side remain separate pure-source QA images.
    edge = out / 'boundary_native_full'
    edge.mkdir()
    for ai in range(start - 8, start):
        a[ai].save(edge / f'output_{ai:06d}_A{ai}.png')
    for bi in range(args.b_start + 18, args.b_start + 26):
        output_index = args.a_end + bi - args.b_start - overlap
        b[bi].save(edge / f'output_{output_index:06d}_B{bi}.png')
    receipt = {'date': args.date, 'scope': 'QA derivatives only; no delivery video',
               'sources': [{'path': A_PATH.relative_to(ROOT).as_posix(), 'sha256': A_SHA},
                           {'path': str(b_path), 'sha256': args.b_sha256.lower()}],
               'A_selected_native_half_open': [0, args.a_end],
               'B_start_native_frame': args.b_start,
               'transition_output_half_open': [start, args.a_end],
               'transition_frames': overlap, 'fps': 24,
               'mapping': mapping,
               'boundary_output_half_open': [start - 8, args.a_end + 8],
               'head_QA_window': [220, 100, 500, 450],
               'lower_QA_window': [200, 780, 530, 1190],
               'delivery_transform': 'none', 'visual_review': 'pending',
               'assistant_continuous_review': False, 'user_approval': None}
    (out / 'qa_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'QA_folder': str(out), 'delivery_written': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
