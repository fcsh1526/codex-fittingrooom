"""Read-only source QA: B[24,126) then A[0,120), 18 native overlap frames.

Writes inspection PNG/JPEG/JSON only; never encodes a delivery video.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw
import native_pair_tools as native

HERE = Path(__file__).resolve().parent
A_SHA = "5baaa223b437e6fde482545cc64a0d2b8c85dffec14df6397735b71c7e0b7d49"
B_SHA = "25b8bd59b95c46dcef8c30ca9847ca4fcdc892581899aea0f804c8375d388a54"
HEAD = (158, 0, 562, 448)


def kept(source, indices):
    selected = {}
    with native.native_reader(source) as reader:
        for index, raw in enumerate(reader):
            if index in indices:
                selected[index] = Image.frombytes("RGB", native.SIZE, raw)
            if index >= max(indices):
                break
    if set(selected) != set(indices):
        raise ValueError("Source lacks a requested original frame")
    return selected


def pair_board(rows, path, title, head=False):
    tw, th = 232, (280 if head else 410)
    canvas = Image.new("RGB", (3 * tw, 34 + len(rows) * (th + 30)), "#f5f3ef")
    draw = ImageDraw.Draw(canvas)
    draw.text((5, 8), title, fill="black")
    for row, item in enumerate(rows):
        for col, role in enumerate(("B", "A", "blend")):
            image = item[role].crop(HEAD) if head else item[role].copy()
            image.thumbnail((tw - 8, th - 6), Image.Resampling.LANCZOS)
            x, y = col * tw, 34 + row * (th + 30)
            draw.text((x + 4, y + 4), item[role + "_label"], fill="black")
            canvas.paste(image, (x + (tw - image.width) // 2, y + 28))
    native.image_new(path, canvas)


def boundary_board(rows, path):
    tw, th = 208, 368
    canvas = Image.new("RGB", (4 * tw, 34 + 4 * (th + 32)), "#f5f3ef")
    draw = ImageDraw.Draw(canvas)
    draw.text((5, 8), "Eight pure frames B before overlap; eight pure A after overlap", fill="black")
    for index, item in enumerate(rows):
        x, y = (index % 4) * tw, 34 + (index // 4) * (th + 32)
        draw.text((x + 4, y + 4), item["label"], fill="black")
        image = item["image"].copy()
        image.thumbnail((tw - 8, th - 6), Image.Resampling.LANCZOS)
        canvas.paste(image, (x + (tw - image.width) // 2, y + 28))
    native.image_new(path, canvas)


def main():
    source_b = native.verified_source(HERE / "B_attempt_01/source.mp4", B_SHA)
    source_a = native.verified_source(HERE / "A_attempt_01/source.mp4", A_SHA)
    protected = native.protected_inputs()
    scans = {"B": native.full_decode(source_b), "A": native.full_decode(source_a)}
    native.require_interval(24, 126, scans["B"]["decoded_frames"], 19)
    native.require_interval(0, 120, scans["A"]["decoded_frames"], 19)
    output = native.destination("QA_join_B126_A0_2026-10-08")
    b = kept(source_b, set(range(100, 126)))
    a = kept(source_a, set(range(26)))
    output.mkdir()
    frames = output / "native_pairs"
    heads = output / "head_blends_QA_only"
    edges = output / "native_boundary"
    frames.mkdir()
    heads.mkdir()
    edges.mkdir()
    rows, mapping = [], []
    for index in range(18):
        bi, ai, oi = 108 + index, index, 84 + index
        alpha = (index + 1) / 18
        blend = Image.blend(b[bi], a[ai], alpha)
        native.image_new(frames / f"B_{bi:06d}.png", b[bi])
        native.image_new(frames / f"A_{ai:06d}.png", a[ai])
        native.image_new(frames / f"blend_output_{oi:06d}.png", blend)
        native.image_new(heads / f"head_blend_output_{oi:06d}.png", blend.crop(HEAD))
        rows.append({"B": b[bi], "A": a[ai], "blend": blend,
                     "B_label": f"B f{bi} / {bi/24:.3f}s",
                     "A_label": f"A f{ai} / {ai/24:.3f}s",
                     "blend_label": f"out f{oi}; A {alpha:.3f}"})
        mapping.append({"output_frame": oi, "B_native_frame": bi,
                        "A_native_frame": ai, "A_alpha": alpha})
    for first in range(0, 18, 6):
        part = rows[first:first + 6]
        pair_board(part, output / f"paired_full_{first+1:02d}_{first+6:02d}.jpg",
                   f"QA only B/A/blend; native overlap {first+1}-{first+6}")
        pair_board(part, output / f"paired_head_{first+1:02d}_{first+6:02d}.jpg",
                   f"QA only common head window; overlap {first+1}-{first+6}", head=True)
    pure, boundary_mapping = [], []
    for bi in range(100, 108):
        oi = bi - 24
        native.image_new(edges / f"output_{oi:06d}_B{bi}.png", b[bi])
        pure.append({"image": b[bi], "label": f"out{oi}; B f{bi} / {bi/24:.3f}s"})
        boundary_mapping.append({"output_frame": oi, "source_role": "B", "native_frame": bi})
    for ai in range(18, 26):
        oi = 102 + ai - 18
        native.image_new(edges / f"output_{oi:06d}_A{ai}.png", a[ai])
        pure.append({"image": a[ai], "label": f"out{oi}; A f{ai} / {ai/24:.3f}s"})
        boundary_mapping.append({"output_frame": oi, "source_role": "A", "native_frame": ai})
    boundary_board(pure, output / "pure_boundary_8_each_side.jpg")
    native.verified_source(source_a, A_SHA)
    native.verified_source(source_b, B_SHA)
    native.protected_inputs()
    receipt = {"date": "2026-10-08", "scope": "QA derivatives only; no new video or global-status changes",
               "status": "actual_native_join_QA_assets_ready_visual_review_pending",
               "source_order": ["B", "A"],
               "sources": [{"role": "B", "look": "L02", "path": str(source_b), "sha256": B_SHA},
                           {"role": "A", "look": "L01", "path": str(source_a), "sha256": A_SHA}],
               "full_decode": scans,
               "candidate_source_intervals_half_open": {"B": [24, 126], "A": [0, 120]},
               "candidate_if_composed": {"frames": 204, "seconds": 8.5, "fps": 24,
                                         "native_size": [720, 1280]},
               "overlap": {"frames": 18, "seconds": .75,
                           "output_half_open": [84, 102], "B_native_half_open": [108, 126],
                           "A_native_half_open": [0, 18], "incoming_A_weight": "(index+1)/18"},
               "boundary_output_half_open": [76, 110], "mapping": mapping,
               "boundary_mapping": boundary_mapping,
               "head_window_native_xyxy": list(HEAD),
               "inspection_crops_are_delivery_transforms": False,
               "retime_freeze_reverse_replay": False, "delivery_written": False,
               "protected_inputs_verified": protected, "user_video_approval": None,
               "assistant_continuous_visual_review": False}
    native.json_new(output / "qa_receipt.json", receipt)
    print(json.dumps({"QA_folder": str(output), "delivery_written": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
