"""Append only the new, scene-corrected F04 source to the accepted prefix.

Preparation does not inspect/build media. Invoke after exact new-source visual
review; --f04-sha is mandatory. The superseded d83c source is rejected.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
F04 = HERE.parent
BASE_HELPER = F04 / "build_four_shot_review.py"
spec = importlib.util.spec_from_file_location("mira_scene_corrected_f04_base", BASE_HELPER)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load append helper: {BASE_HELPER}")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
native = base.native
REJECTED_SHA = "d83c6c18fa7d058c3eb3b374afad70db0a51cf0c561ba2c6bd4a255041d0bb50"
SOURCE = HERE / "F04_source.mp4"
END = HERE / "F04_M03_L02_end_scene_correction_v3.png"
END_SHA = "fe97ba462401f7df3ef286a348853b65f54c51703980b402174c0a59ed605139"
PROTECTED = [
    (base.PREFIX, base.PREFIX_SHA),
    (F04 / "F04_M03_L02_start_candidate_A.png", "98687eb8365828d67850ddc03d57e48d9d28ad4628f9f62c727bcb166e002457"),
    (END, END_SHA),
]


def require_new_source_sha(digest: str) -> None:
    if digest == REJECTED_SHA:
        raise ValueError("Reject superseded F04 d83c source; use only the newly downloaded scene-corrected source")
    # This also validates lowercase SHA format and exact file bytes.
    native.verified_source(SOURCE, digest)


def full_decode(path):
    return native.full_decode(path)


def stream_inventory(path):
    return native.stream_inventory(path)


def build(f04_sha: str, version: str = "v1") -> dict:
    require_new_source_sha(f04_sha)
    # Reuse immutable algorithm, replacing only this execution's bounded paths
    # and exact still protections. No older code/media is rewritten.
    base.HERE = HERE
    base.SOURCE = SOURCE
    base.PROTECTED = PROTECTED
    result = base.build(f04_sha, version)
    destination = Path(result["output"]).parent
    native.json_new(destination / "scene_correction_execution.json", {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "wrapper": str(Path(__file__).resolve()),
        "wrapper_sha256": native.sha256(Path(__file__).resolve()),
        "borrowed_algorithm": str(BASE_HELPER), "borrowed_algorithm_sha256": native.sha256(BASE_HELPER),
        "source": str(SOURCE), "source_sha256": f04_sha,
        "approved_endpoint": str(END), "approved_endpoint_sha256": END_SHA,
        "superseded_d83c_source_rejected": True,
        "accepted_prefix_used_as_media_input": True, "prior_joins_rebuilt": False,
        "technical_success_is_visual_approval": False,
        "user_video_approval": None, "publication": False,
    })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f04-sha", required=True, help="Exact new scene-corrected source SHA256 after inspection")
    parser.add_argument("--version", default="v1", help="Exclusive new four_shot_review_v1/v2/... output")
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.f04_sha, args.version), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
