"""Manual Reel publication links and append-only metric observations.

No Instagram requests, production-state changes, or legacy CSV migrations.
Unknown values stay empty; a correction adds a revision instead of erasing history.
"""

import argparse
import csv
import hashlib
import json
import re
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse


CHECKPOINTS = ("24h", "72h", "7d", "lifetime_snapshot")
SCOPES = ("instagram", "instagram_facebook_combined", "instagram_public_grid")
COUNTS = ("views", "reach", "likes", "comments", "saves", "shares", "sends", "follows", "profile_visits")
MEASURES = ("non_follower_views_percent", "total_watch_seconds", "average_watch_seconds", "skip_rate_percent")
RATIOS = {f"{metric}_per_reach": metric for metric in ("likes", "saves", "shares", "sends", "follows")}
KEY_FIELDS = ("post_id", "checkpoint", "observed_at", "source", "scope")
METRIC_FIELDS = ["snapshot_id", "revision", "recorded_at", *KEY_FIELDS, *COUNTS, *MEASURES, *RATIOS, "notes"]
PUBLISH_FIELDS = [
    "post_id", "post_url", "published_at", "reel_id", "production_manifest", "duration_seconds",
    "format_variant", "opening_hook", "production_minutes", "generation_attempts", "cost_amount",
    "cost_currency", "source", "observed_at", "notes",
]


def read_csv(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def timestamp(value, field):
    value = str(value).strip()
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            date.fromisoformat(value)
        else:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                raise ValueError("datetime needs an explicit UTC offset; use date only if time is unknown")
    except ValueError as error:
        raise ValueError(f"Invalid {field}: {value}. {error}") from error
    return value


def number(value, field, integer=False, percent=False):
    if value is None or str(value).strip() == "":
        return ""
    try:
        parsed = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError(f"{field} must be a nonnegative number or empty") from error
    if not parsed.is_finite() or parsed < 0 or (integer and parsed != parsed.to_integral_value()):
        raise ValueError(f"Invalid {field}: {value}")
    if percent and parsed > 100:
        raise ValueError(f"{field} must be between 0 and 100")
    return str(int(parsed)) if integer else format(parsed.normalize(), "f")


def post_identity(post_url):
    parsed = urlparse(post_url)
    match = re.fullmatch(r"/(?:reel|p)/([A-Za-z0-9_-]+)/?", parsed.path)
    if parsed.scheme != "https" or parsed.netloc not in ("www.instagram.com", "instagram.com") or not match:
        raise ValueError("Use the HTTPS Instagram permalink for this Reel")
    return match.group(1), f"https://www.instagram.com/reel/{match.group(1)}/"


def manifest_reel_ids(value):
    """Match explicit ids only; never infer a week/model from filenames."""
    if not isinstance(value, dict):
        return set()
    found = {str(value["reel_id"])} if value.get("reel_id") else set()
    for collection in ("reels", "groups"):
        entries = value.get(collection, [])
        if isinstance(entries, list):
            for entry in entries:
                if isinstance(entry, dict) and entry.get("reel_id"):
                    found.add(str(entry["reel_id"]))
    return found


def record_publication(project_root, data):
    project_root = Path(project_root)
    unexpected = set(data) - set(PUBLISH_FIELDS)
    if unexpected:
        raise ValueError(f"Unknown publication fields: {sorted(unexpected)}")
    post_id, post_url = post_identity(data["post_url"])
    path = project_root / "07_metrics/reel_publish_registry.csv"
    rows = read_csv(path)
    existing = next((row for row in rows if row["post_id"] == post_id), {})
    row = {field: existing.get(field, "") for field in PUBLISH_FIELDS}
    row.update({key: "" if value is None else str(value).strip() for key, value in data.items()})
    row.update(post_id=post_id, post_url=post_url)
    for field in ("observed_at", "source"):
        if not row[field]:
            raise ValueError(f"{field} is required")
    for field in ("observed_at", "published_at"):
        if row[field]:
            row[field] = timestamp(row[field], field)
    for field in ("duration_seconds", "production_minutes", "cost_amount", "generation_attempts"):
        row[field] = number(row[field], field, integer=field == "generation_attempts")
    if row["cost_amount"] and not re.fullmatch(r"[A-Z]{3}", row["cost_currency"]):
        raise ValueError("A recorded cost requires an explicit three-letter currency, e.g. TWD")
    if row["production_manifest"]:
        if not row["reel_id"]:
            raise ValueError("production_manifest requires an explicit reel_id")
        manifest_path = Path(row["production_manifest"])
        if not manifest_path.is_absolute():
            manifest_path = project_root / manifest_path
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        if row["reel_id"] not in manifest_reel_ids(manifest):
            raise ValueError("reel_id is not present in the supplied production manifest")
        try:
            row["production_manifest"] = manifest_path.resolve().relative_to(project_root.resolve()).as_posix()
        except ValueError:
            row["production_manifest"] = str(manifest_path.resolve())
    if row != existing:
        rows = [row if item["post_id"] == post_id else item for item in rows] if existing else rows + [row]
        write_csv(path, PUBLISH_FIELDS, rows)
    return row


def latest_snapshots(rows):
    latest = {}
    for row in rows:
        key = row["snapshot_id"]
        if key not in latest or int(row["revision"]) > int(latest[key]["revision"]):
            latest[key] = row
    return list(latest.values())


def record_snapshot(project_root, data):
    project_root = Path(project_root)
    allowed = set(KEY_FIELDS + COUNTS + MEASURES + ("notes",))
    unexpected = set(data) - allowed
    if unexpected:
        raise ValueError(f"Unknown metric fields: {sorted(unexpected)}")
    for field in KEY_FIELDS:
        if not str(data.get(field, "")).strip():
            raise ValueError(f"{field} is required")
    if data["checkpoint"] not in CHECKPOINTS or data["scope"] not in SCOPES:
        raise ValueError("Invalid checkpoint or scope")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", data["post_id"]):
        raise ValueError("Invalid Instagram post id")
    data = dict(data)
    data["observed_at"] = timestamp(data["observed_at"], "observed_at")
    data["source"] = str(data["source"]).strip()
    for field in COUNTS + MEASURES:
        if field in data:
            data[field] = number(data[field], field, integer=field in COUNTS, percent=field.endswith("percent"))
    if not any(row["post_id"] == data["post_id"] for row in read_csv(project_root / "07_metrics/reel_publish_registry.csv")):
        raise ValueError("Register this post with the publish command before recording metrics")
    path = project_root / "07_metrics/reel_metric_snapshots.csv"
    rows = read_csv(path)
    snapshot_id = hashlib.sha256(json.dumps([data[field] for field in KEY_FIELDS]).encode()).hexdigest()[:20]
    previous = next((row for row in reversed(rows) if row["snapshot_id"] == snapshot_id), {})
    row = {field: previous.get(field, "") for field in METRIC_FIELDS}
    row.update({key: "" if value is None else str(value) for key, value in data.items()})
    row["snapshot_id"] = snapshot_id
    for derived, numerator in RATIOS.items():
        row[derived] = ""
        if row["reach"] and Decimal(row["reach"]) > 0 and row[numerator] != "":
            row[derived] = format(Decimal(row[numerator]) / Decimal(row["reach"]), ".8f")
    content_fields = [field for field in METRIC_FIELDS if field not in ("recorded_at", "revision")]
    if previous and all(row[field] == previous[field] for field in content_fields):
        return previous
    row["revision"] = str(int(previous.get("revision", 0)) + 1)
    row["recorded_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=METRIC_FIELDS)
        if not rows:
            writer.writeheader()
        writer.writerow(row)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    commands = parser.add_subparsers(dest="command", required=True)
    publish = commands.add_parser("publish", help="Register an existing Instagram Reel, optionally link a known production reel_id")
    for field in PUBLISH_FIELDS:
        if field != "post_id":
            publish.add_argument("--" + field.replace("_", "-"), required=field in ("post_url", "source", "observed_at"), default=argparse.SUPPRESS)
    snapshot = commands.add_parser("snapshot", help="Record or revise a dated observation; unspecified values remain unknown")
    snapshot.add_argument("--post-url", required=True)
    snapshot.add_argument("--checkpoint", choices=CHECKPOINTS, required=True)
    snapshot.add_argument("--observed-at", required=True)
    snapshot.add_argument("--source", required=True)
    snapshot.add_argument("--scope", choices=SCOPES, required=True)
    for field in COUNTS + MEASURES + ("notes",):
        snapshot.add_argument("--" + field.replace("_", "-"), default=argparse.SUPPRESS)
    latest = commands.add_parser("latest", help="Read only the latest revision of each observation, without collapsing observation dates")
    latest.add_argument("--post-url")
    args = vars(parser.parse_args())
    project_root, command = args.pop("project_root"), args.pop("command")
    try:
        if command == "publish":
            result = record_publication(project_root, args)
        elif command == "snapshot":
            args["post_id"] = post_identity(args.pop("post_url"))[0]
            result = record_snapshot(project_root, args)
        else:
            result = latest_snapshots(read_csv(project_root / "07_metrics/reel_metric_snapshots.csv"))
            if args.get("post_url"):
                post_id = post_identity(args["post_url"])[0]
                result = [row for row in result if row["post_id"] == post_id]
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
