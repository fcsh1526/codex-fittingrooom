"""Append operator-reviewed new midpoint-controlled F04 to the exact accepted prefix.

18-frame/0.75s dissolve, native24fps720x1280, full raster, no text/audio/retime.
No earlier join is recomposed. Both prior failed F04 source hashes are rejected.
"""
import argparse
import json
import sys
from motion_control_context import build


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f04-sha", required=True, help="Exact newly inspected trial source SHA256")
    parser.add_argument("--version", default="v1", help="Exclusive four_shot_review_v1/v2/... directory")
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.f04_sha, args.version, __file__), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
