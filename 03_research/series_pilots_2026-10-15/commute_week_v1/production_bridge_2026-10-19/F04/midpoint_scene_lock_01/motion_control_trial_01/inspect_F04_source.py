"""Inspect only the new midpoint-controlled F04 source; no QA approval implied."""
import argparse
import json
import sys
from motion_control_context import inspect


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f04-sha", required=True, help="Exact new trial source SHA256; both failed sources are rejected")
    parser.add_argument("--version", default="v1", help="Exclusive source_inspection_v1/v2/... directory")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.f04_sha, args.version, __file__), ensure_ascii=False))
    except Exception as error:
        print(json.dumps({"status": "failed_no_approval_inferred", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
