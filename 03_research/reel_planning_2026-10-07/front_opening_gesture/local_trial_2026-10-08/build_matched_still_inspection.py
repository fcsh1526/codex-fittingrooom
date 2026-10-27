"""Inspection-only comparisons; never edits or replaces delivered stills."""
from pathlib import Path
import hashlib
import json
import sys
import argparse

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "10_automation").is_dir())
sys.path.insert(0, str(ROOT / "10_automation/.video_dependencies"))
from PIL import Image, ImageDraw

asset_dir = ROOT / "10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/front_opening_matched_start_v1"
parser = argparse.ArgumentParser()
parser.add_argument("--variant", choices=("v1", "v2"), default="v1")
args = parser.parse_args()
out = asset_dir / ("QA" if args.variant == "v1" else "QA_v2")
out.mkdir(exist_ok=False)
inputs = {
    "A native f116": HERE / "QA_join_A126_B0_2026-10-08/native_pairs/A_000116.png",
    f"New B still {args.variant}": asset_dir / f"2026-W37-001-L02_M02_front_opening_matched_start_candidate_{args.variant}.png",
    "Approved B proof": ROOT / "10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/paired_scene_v1/2026-W37-001-L02_M02_reel_proof_candidate_v1.png",
    "Old B motion f8": HERE / "QA_join_A126_B0_2026-10-08/native_pairs/B_000008.png",
}
records, images = [], {}
for label, path in inputs.items():
    raw = path.read_bytes()
    im = Image.open(path).convert("RGB")
    records.append({"role": label, "path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(), "size": list(im.size)})
    images[label] = im.resize((720, 1280), Image.Resampling.LANCZOS)

def board(entries, name, crop=None):
    tiles = []
    for label, im in entries:
        tile = im.crop(crop) if crop else im.copy()
        tile.thumbnail((360, 640), Image.Resampling.LANCZOS)
        tiles.append((label, tile))
    height = max(im.height for _, im in tiles) + 28
    canvas = Image.new("RGB", (360 * len(tiles), height), "#eeeae4")
    draw = ImageDraw.Draw(canvas)
    for i, (label, im) in enumerate(tiles):
        draw.text((i * 360 + 6, 6), label, fill="black")
        canvas.paste(im, (i * 360 + (360 - im.width) // 2, 28))
    with (out / name).open("xb") as stream:
        canvas.save(stream, "JPEG", quality=96)

board(list(images.items()), "full_comparison.jpg")
board(list(images.items()), "head_comparison.jpg", (180, 45, 530, 385))
a = images["A native f116"]
blends = [(label, Image.blend(a, images[label], 0.5)) for label in (f"New B still {args.variant}", "Approved B proof", "Old B motion f8")]
board(blends, "half_blend_full.jpg")
board(blends, "half_blend_head.jpg", (180, 45, 530, 385))
with (out / "inspection_inputs.json").open("x", encoding="utf-8") as stream:
    json.dump({"date": "2026-10-08", "inputs": records, "normalized_inspection_size": [720, 1280], "normalization_is_QA_only": True, "delivery_asset_modified": False, "static_visual_result": "pending", "dynamic_join_result": "not_tested", "user_approval": None}, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
print(json.dumps({"QA": str(out), "inputs": records}, ensure_ascii=False))
