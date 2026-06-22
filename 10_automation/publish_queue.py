import argparse
import csv
import json
import re
from pathlib import Path


QUEUE_FIELDS = [
    "item_type",
    "week_id",
    "carousel_id",
    "prompt_id",
    "trend_name",
    "content_bucket",
    "stage",
    "platform",
    "recommended_asset",
    "asset_url",
    "post_url",
    "published_at",
    "latest_reach",
    "latest_decision",
    "next_action",
    "run_dir",
    "package_path",
]


def clean(value):
    return " ".join(str(value or "").split()).strip()


def read_csv(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def read_json(path):
    path = Path(path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def run_dirs_under(runs_dir):
    runs_dir = Path(runs_dir)
    if not runs_dir.exists():
        return []
    return sorted(
        path
        for path in runs_dir.iterdir()
        if path.is_dir()
        and (
            (path / "weekly_content_packet.csv").exists()
            or (path / "weekly_status.json").exists()
        )
    )


def extract_note_value(notes, key):
    pattern = rf"(?:^|;\s*){re.escape(key)}=([^;]+)"
    match = re.search(pattern, clean(notes))
    return clean(match.group(1)) if match else ""


def assets_by_carousel(run_dir):
    out = {}
    for row in read_csv(Path(run_dir) / "canva_asset_slots.csv"):
        carousel_id = clean(row.get("carousel_id"))
        slot_id = clean(row.get("slot_id"))
        if slot_id != "cover_image":
            continue
        out[carousel_id] = {
            "file": clean(row.get("recommended_file")),
            "url": extract_note_value(row.get("notes"), "drive_url"),
        }
    return out


def latest_by_carousel(rows, carousel_id):
    matches = [row for row in rows if clean(row.get("carousel_id")) == carousel_id]
    return matches[-1] if matches else {}


def stage_for_carousel(packet, asset, publish, metric):
    if metric:
        decision = clean(metric.get("decision"))
        return decision or "metrics_recorded_review_needed"
    if publish or clean(packet.get("status")) == "published":
        return "published_waiting_for_metrics"
    if not clean(asset.get("file")):
        return "needs_grok_asset_selection"
    return "ready_for_canva_and_publish"


def next_action_for_stage(stage):
    actions = {
        "visibility_recovery": "Keep carousel production moving; optionally publish or record the generated single-image visibility test in parallel.",
        "ready_to_publish_visibility_test": "Optional side test: publish the single-image visibility test, share once to Story, then record 6h / 24h metrics.",
        "published_waiting_for_metrics": "Record 6h / 24h metrics with record_post_metrics.py.",
        "needs_grok_asset_selection": "Generate or score Grok images, then run select_grok_assets.py.",
        "ready_for_canva_and_publish": "Use Canva handoff files to finish the carousel and publish it.",
        "weak_distribution": "Mirror the asset to Threads or Pinterest and test a clearer single-image hook.",
        "wait_for_24h": "Wait for the 24h checkpoint before changing the content direction.",
        "repeat_bucket": "Create a second carousel in the same content bucket.",
        "profile_interest": "Improve the cover hook and profile CTA before testing commerce links.",
        "hook_or_save_gap": "Revise the cover headline and make the outfit benefit clearer.",
    }
    return actions.get(stage, "Open weekly_status.md and follow the next action.")


def carousel_item(run_dir, packet, asset, publish_rows, metric_rows):
    carousel_id = clean(packet.get("carousel_id"))
    publish = latest_by_carousel(publish_rows, carousel_id)
    metric = latest_by_carousel(metric_rows, carousel_id)
    stage = stage_for_carousel(packet, asset, publish, metric)
    return {
        "item_type": "carousel",
        "week_id": clean(packet.get("week_id")) or Path(run_dir).name,
        "carousel_id": carousel_id,
        "prompt_id": clean(packet.get("prompt_id")),
        "trend_name": clean(packet.get("trend_name")),
        "content_bucket": clean(packet.get("content_bucket")),
        "stage": stage,
        "platform": clean(publish.get("platform")) or "Instagram",
        "recommended_asset": clean(asset.get("file")),
        "asset_url": clean(asset.get("url")),
        "post_url": clean(publish.get("post_url")) or clean(packet.get("ig_post_url")),
        "published_at": clean(publish.get("published_at")),
        "latest_reach": clean(metric.get("reach")),
        "latest_decision": clean(metric.get("decision")),
        "next_action": next_action_for_stage(stage),
        "run_dir": str(run_dir),
        "package_path": "",
    }


def visibility_item(run_dir, package, publish_rows, metric_rows):
    source_id = clean(package.get("source_carousel_id"))
    carousel_id = f"{source_id}-visibility-01"
    publish = latest_by_carousel(publish_rows, carousel_id)
    metric = latest_by_carousel(metric_rows, carousel_id)
    if metric:
        stage = clean(metric.get("decision")) or "metrics_recorded_review_needed"
    elif publish:
        stage = "published_waiting_for_metrics"
    else:
        stage = "ready_to_publish_visibility_test"

    asset = package.get("asset") or {}
    packet = package.get("source_packet") or {}
    return {
        "item_type": "visibility_test",
        "week_id": clean(packet.get("week_id")) or Path(run_dir).name,
        "carousel_id": carousel_id,
        "prompt_id": clean(packet.get("prompt_id")),
        "trend_name": clean(packet.get("trend_name")),
        "content_bucket": clean(packet.get("content_bucket")),
        "stage": stage,
        "platform": clean(publish.get("platform")) or "Instagram",
        "recommended_asset": clean(asset.get("file")),
        "asset_url": clean(asset.get("drive_url")),
        "post_url": clean(publish.get("post_url")),
        "published_at": clean(publish.get("published_at")),
        "latest_reach": clean(metric.get("reach")),
        "latest_decision": clean(metric.get("decision")),
        "next_action": next_action_for_stage(stage),
        "run_dir": str(run_dir),
        "package_path": str(Path(run_dir) / "visibility_test_package.md"),
    }


def item_priority(row):
    stage = clean(row.get("stage"))
    item_type = clean(row.get("item_type"))
    if item_type == "carousel" and stage == "ready_for_canva_and_publish":
        return 100
    if item_type == "carousel" and stage == "needs_grok_asset_selection":
        return 90
    priorities = {
        "published_waiting_for_metrics": 80,
        "ready_for_canva_and_publish": 75,
        "needs_grok_asset_selection": 70,
        "ready_to_publish_visibility_test": 45,
        "visibility_recovery": 40,
        "wait_for_24h": 50,
        "weak_distribution": 45,
        "hook_or_save_gap": 40,
        "profile_interest": 35,
        "repeat_bucket": 30,
    }
    return priorities.get(stage, 10)


def build_queue(runs_dir):
    rows = []
    for run_dir in run_dirs_under(runs_dir):
        packets = read_csv(run_dir / "weekly_content_packet.csv")
        publish_rows = read_csv(run_dir / "publish_log.csv")
        metric_rows = read_csv(run_dir / "metric_checkpoints.csv")
        assets = assets_by_carousel(run_dir)
        for packet in packets:
            carousel_id = clean(packet.get("carousel_id"))
            rows.append(carousel_item(run_dir, packet, assets.get(carousel_id, {}), publish_rows, metric_rows))

        visibility_package = read_json(run_dir / "visibility_test_package.json")
        if visibility_package:
            rows.append(visibility_item(run_dir, visibility_package, publish_rows, metric_rows))
    return sorted(rows, key=lambda row: (item_priority(row), clean(row.get("carousel_id"))), reverse=True)


def write_markdown(path, rows, runs_dir):
    lines = [
        "# Publish Queue",
        "",
        f"Runs directory: `{runs_dir}`",
        f"Queue items: `{len(rows)}`",
        "",
    ]
    if not rows:
        lines.extend(
            [
                "No publish queue items found.",
                "",
                "Create a weekly run with:",
                "",
                "```powershell",
                "powershell -ExecutionPolicy Bypass -File 10_automation\\mika_weekly.ps1 -Action pipeline -Week 2026-WXX -PerplexitySource path_or_url",
                "```",
                "",
            ]
        )
    else:
        top = rows[0]
        lines.extend(
            [
                "## Top Next Item",
                "",
                f"- Type: `{top['item_type']}`",
                f"- ID: `{top['carousel_id']}`",
                f"- Stage: `{top['stage']}`",
                f"- Asset: `{top['recommended_asset'] or 'n/a'}`",
                f"- Package: `{top['package_path'] or 'n/a'}`",
                f"- Next action: {top['next_action']}",
                "",
                "## Queue",
                "",
                "| Type | ID | Stage | Asset | Reach | Next Action |",
                "|---|---|---|---|---:|---|",
            ]
        )
        for row in rows:
            next_action = clean(row.get("next_action")).replace("|", "/")
            lines.append(
                f"| `{row['item_type']}` | `{row['carousel_id']}` | `{row['stage']}` | `{row['recommended_asset'] or 'n/a'}` | `{row['latest_reach'] or ''}` | {next_action} |"
            )
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_json(path, rows, runs_dir):
    payload = {
        "runs_dir": str(runs_dir),
        "item_count": len(rows),
        "top_item": rows[0] if rows else None,
        "items": rows,
    }
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def build_publish_queue(runs_dir, output_csv, output_md, output_json):
    rows = build_queue(runs_dir)
    write_csv(output_csv, QUEUE_FIELDS, rows)
    write_markdown(output_md, rows, runs_dir)
    payload = write_json(output_json, rows, runs_dir)
    return payload


def main():
    parser = argparse.ArgumentParser(description="Build a per-carousel publish queue across weekly Mika Lin run folders.")
    parser.add_argument("--runs-dir", default="10_automation/runs")
    parser.add_argument("--output-csv", default="10_automation/PUBLISH_QUEUE.csv")
    parser.add_argument("--output-md", default="10_automation/PUBLISH_QUEUE.md")
    parser.add_argument("--output-json", default="10_automation/PUBLISH_QUEUE.json")
    args = parser.parse_args()

    payload = build_publish_queue(args.runs_dir, args.output_csv, args.output_md, args.output_json)
    top = payload.get("top_item") or {}
    print(f"Queue items: {payload['item_count']}")
    print(f"Top stage: {top.get('stage', 'none')}")
    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()
