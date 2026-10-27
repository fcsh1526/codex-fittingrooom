"""Build a non-generative layout diagnostic from accepted full-person masters."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
size = (720, 1280)
canvas = Image.new('RGB', size, '#e8e2d9')
records = []
for i, look in enumerate(('L01', 'L02')):
    path = ROOT / f'10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-{look}/reel/paired_scene_v1/2026-W37-001-{look}_M02_reel_full_master_candidate_v1.png'
    with Image.open(path) as source:
        assert source.size == (941, 1672), source.size
        # Full-height, fixed window; retains the visible head, shoes and bag.
        # This diagnostic does not establish a safe moving-video crop.
        box = (245, 0, 770, 1672)
        tile = source.crop(box).convert('RGB')
        tile.thumbnail((352, 1280), Image.Resampling.LANCZOS)
        x = 4 + i * 360 + (352 - tile.width) // 2
        y = (1280 - tile.height) // 2
        canvas.paste(tile, (x, y))
    records.append(dict(look_id=f'2026-W37-001-{look}', source_path=path.relative_to(ROOT).as_posix(), source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), source_size=[941, 1672], fixed_window=list(box), output_position=[x, y], output_size=list(tile.size)))
target = OUT / 'M02_parallel_layout_diagnostic_v1.png'
if target.exists():
    raise FileExistsError('Preserve earlier diagnostics; use a new filename for a revision.')
canvas.save(target)
canvas.resize((360, 640), Image.Resampling.LANCZOS).save(OUT / 'M02_parallel_layout_mobile_360px_v1.png')
(OUT / 'layout_receipt.json').write_text(json.dumps(dict(status='layout_diagnostic_only', sources=records, output_path=target.relative_to(ROOT).as_posix(), output_sha256=hashlib.sha256(target.read_bytes()).hexdigest(), output_size=list(size), source_images_changed=False, generated_stills=False, dynamic_crop_qa='not_started', user_layout_approval=None, publishable=False), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'output':str(target),'dimensions':size,'status':'layout_diagnostic_only'},ensure_ascii=False))
