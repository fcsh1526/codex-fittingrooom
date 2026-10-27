"""One earlier native A96-113/B0-17 QA comparison; no video output."""
from pathlib import Path
import json
from PIL import Image
import native_pair_tools as native
from build_A126_B0_join_QA import A_SHA, B_SHA, kept, pair_board

HERE = Path(__file__).resolve().parent


def main():
    source_a = native.verified_source(HERE / "A_attempt_01/source.mp4", A_SHA)
    source_b = native.verified_source(HERE / "B_attempt_01/source.mp4", B_SHA)
    protected = native.protected_inputs()
    scans = {"A": native.full_decode(source_a), "B": native.full_decode(source_b)}
    native.require_interval(24, 114, scans["A"]["decoded_frames"], 19)
    native.require_interval(0, 120, scans["B"]["decoded_frames"], 19)
    output = native.destination("QA_join_A114_B0_2026-10-08")
    a, b = kept(source_a, set(range(88, 114))), kept(source_b, set(range(26)))
    output.mkdir()
    frames, edges = output / "native_pairs", output / "native_boundary"
    frames.mkdir()
    edges.mkdir()
    rows, mapping = [], []
    for index in range(18):
        ai, bi, oi = 96 + index, index, 72 + index
        alpha = (index + 1) / 18
        blend = Image.blend(a[ai], b[bi], alpha)
        native.image_new(frames / f"A_{ai:06d}.png", a[ai])
        native.image_new(frames / f"B_{bi:06d}.png", b[bi])
        native.image_new(frames / f"blend_output_{oi:06d}.png", blend)
        rows.append({"A": a[ai], "B": b[bi], "blend": blend,
                     "A_label": f"A f{ai} / {ai/24:.3f}s",
                     "B_label": f"B f{bi} / {bi/24:.3f}s",
                     "blend_label": f"out f{oi}; B {alpha:.3f}"})
        mapping.append({"output_frame": oi, "A_native_frame": ai,
                        "B_native_frame": bi, "B_alpha": alpha})
    for first in range(0, 18, 6):
        part = rows[first:first + 6]
        pair_board(part, output / f"paired_full_{first+1:02d}_{first+6:02d}.jpg",
                   f"QA only earlier A/B/blend; native overlap {first+1}-{first+6}")
        pair_board(part, output / f"paired_head_{first+1:02d}_{first+6:02d}.jpg",
                   f"QA only earlier common head window; overlap {first+1}-{first+6}", head=True)
    pure = []
    for ai in range(88, 96):
        oi = ai - 24
        native.image_new(edges / f"output_{oi:06d}_A{ai}.png", a[ai])
        pure.append((oi, a[ai]))
    for bi in range(18, 26):
        oi = 90 + bi - 18
        native.image_new(edges / f"output_{oi:06d}_B{bi}.png", b[bi])
        pure.append((oi, b[bi]))
    native.sheet(pure, output / "pure_boundary_8_each_side.jpg", "Earlier join: eight pure-source frames before/after")
    native.verified_source(source_a, A_SHA)
    native.verified_source(source_b, B_SHA)
    native.protected_inputs()
    native.json_new(output / "qa_receipt.json", {
        "date": "2026-10-08", "scope": "One earlier native join comparison; QA derivatives only",
        "status": "actual_native_join_QA_assets_ready_visual_review_pending",
        "sources": [{"role": "A", "path": str(source_a), "sha256": A_SHA},
                    {"role": "B", "path": str(source_b), "sha256": B_SHA}],
        "full_decode": scans, "candidate_source_intervals_half_open": {"A": [24, 114], "B": [0, 120]},
        "candidate_if_composed": {"frames": 192, "seconds": 8.0, "fps": 24, "native_size": [720, 1280]},
        "overlap": {"frames": 18, "seconds": .75, "output_half_open": [72, 90],
                    "A_native_half_open": [96, 114], "B_native_half_open": [0, 18], "B_weight": "(index+1)/18"},
        "boundary_output_half_open": [64, 98], "mapping": mapping,
        "head_window_native_xyxy": [158, 0, 562, 448],
        "inspection_crops_are_delivery_transforms": False, "retime_freeze_reverse_replay": False,
        "delivery_written": False, "protected_inputs_verified": protected,
        "user_video_approval": None, "assistant_continuous_visual_review": False,
        "comparison_count": 1, "further_selection_if_failed": "stop"})
    print(json.dumps({"QA_folder": str(output), "delivery_written": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
