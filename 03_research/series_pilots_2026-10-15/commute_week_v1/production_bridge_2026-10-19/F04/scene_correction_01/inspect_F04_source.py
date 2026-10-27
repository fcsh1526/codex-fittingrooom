"""Inspect only the newly downloaded scene-corrected F04; never approve quality.

Requires --f04-sha and rejects the superseded d83c source. Outputs are exclusive
source_inspection_v1/v2/... under this scene_correction_01 folder.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE_HELPER = HERE.parent / "inspect_F04_source.py"
spec = importlib.util.spec_from_file_location("mira_scene_corrected_f04_inspection_base", BASE_HELPER)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load inspection helper: {BASE_HELPER}")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
builder_spec = importlib.util.spec_from_file_location("mira_scene_corrected_f04_builder", HERE / "build_four_shot_review.py")
if builder_spec is None or builder_spec.loader is None:
    raise ImportError("Cannot load scene-corrected builder protections")
builder = importlib.util.module_from_spec(builder_spec)
builder_spec.loader.exec_module(builder)


def inspect(f04_sha: str, version: str = "v1") -> dict:
    builder.require_new_source_sha(f04_sha)
    base.HERE = HERE
    base.builder = builder
    result = base.inspect(f04_sha, version)
    output = Path(result["output_QA"])
    base.native.json_new(output / "scene_correction_execution.json", {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "wrapper": str(Path(__file__).resolve()),
        "wrapper_sha256": base.native.digest(Path(__file__).resolve()),
        "borrowed_inspection": str(BASE_HELPER), "borrowed_inspection_sha256": base.native.digest(BASE_HELPER),
        "new_source_sha256": f04_sha, "superseded_d83c_source_rejected": True,
        "approved_endpoint": str(builder.END), "approved_endpoint_sha256": builder.END_SHA,
        "visual_qa_pass": None, "normal_speed_full_playback": None,
    })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f04-sha", required=True, help="Exact newly downloaded scene-corrected source SHA256")
    parser.add_argument("--version", default="v1", help="Exclusive new inspection directory version:v1,v2,...")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.f04_sha, args.version), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
