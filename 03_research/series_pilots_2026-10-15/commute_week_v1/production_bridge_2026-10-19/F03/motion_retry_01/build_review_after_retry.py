"""Build an isolated three-shot preview after inspection of the exact F03 retry.

The established builder retains its protected F01, corrected F02, accepted-pair
hashes and native 18-frame dissolves. Only its output root and F03 input change.
Importing this wrapper does not read, inspect, generate or encode media.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILDER = HERE.parent / "build_three_shot_review.py"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f03-sha", required=True,
                        help="Exact lowercase SHA256 of the inspected F03 retry source")
    parser.add_argument("--version", default="v1",
                        help="Exclusive new local preview version; default v1")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("mira_f03_retry_three_shot_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load established builder: {BUILDER}")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    # Do not recompute BRIDGE or replace any protected earlier source/constant.
    builder.HERE = HERE
    builder.F03 = HERE / "F03_source.mp4"
    result = builder.build(args.f03_sha, args.version)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
