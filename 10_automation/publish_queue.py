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
    "model_profile_id",
    "canva_template_key",
    "canva_template_name",
    "canva_template_url",
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

TEMPLATE_REGISTRY_PATH = Path(__file__).with_name("canva_template_registry.json")


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


def load_template_registry(path=TEMPLATE_REGISTRY_PATH):
    registry = read_json(path)
    templates = {}
    for template in registry.get("templates", []):
        key = clean(template.get("key")).upper()
        if key:
            templates[key] = template
    return templates


def choose_template(packet, templates):
    if not templates:
        return {}

    explicit = clean(packet.get("canva_template_key") or packet.get("template_key")).upper()
    if explicit in templates:
        return templates[explicit]

    blob = " ".join(
        clean(packet.get(field))
        for field in [
            "trend_name",
            "content_bucket",
            "audience",
            "occasion",
            "clothing_item",
            "color_palette",
            "fabric",
            "fit",
            "styling_rules",
            "scene",
        ]
    ).lower()

    keyword_rules = [
        ("C", ["noir", "evening", "night", "autumn", "winter", "晚宴", "夜", "夜晚", "秋冬", "秋", "冬", "低光"]),
        ("B", ["office", "commute", "formal", "tailored", "blazer", "通勤", "上班", "正式", "剪裁", "西外", "西裝"]),
        ("E", ["weekend", "linen", "cafe", "airy", "週末", "假日", "亞麻", "咖啡", "留白"]),
        ("D", ["full-bleed", "hero image", "image-led", "strong visual", "大片", "強視覺", "滿版"]),
    ]
    for key, keywords in keyword_rules:
        if key in templates and any(keyword in blob for keyword in keywords):
            return templates[key]
    return templates.get("A") or next(iter(templates.values()))


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
        if not carousel_id or not slot_id:
            continue
        out.setdefault(
            carousel_id,
            {
                "file": "",
                "url": "",
                "slots": {},
                "invalid_slots": [],
                "missing_slots": [],
                "selection_status": "",
            },
        )
        file_name = clean(row.get("recommended_file"))
        status = clean(row.get("status")).lower()
        out[carousel_id]["slots"][slot_id] = {
            "file": file_name,
            "status": status,
            "url": extract_note_value(row.get("notes"), "drive_url"),
        }
        if slot_id == "cover_image":
            out[carousel_id]["file"] = file_name
            out[carousel_id]["url"] = extract_note_value(row.get("notes"), "drive_url")
        if status in {"needed", "needs_review", "needs_scoring", "needs_regeneration", "rejected", "not_found", "missing"}:
            out[carousel_id]["invalid_slots"].append(f"{slot_id}:{status}")

    for asset in out.values():
        for slot_id in ["cover_image", "motion_crop", "detail_image"]:
            slot = asset["slots"].get(slot_id, {})
            if not clean(slot.get("file")):
                asset["missing_slots"].append(slot_id)
    return out


def asset_selection_statuses(run_dir):
    out = {}
    for file_name in ["codex_asset_selection.csv", "openai_asset_selection.csv", "grok_asset_selection.csv"]:
        path = Path(run_dir) / file_name
        if not path.exists():
            continue
        for row in read_csv(path):
            carousel_id = clean(row.get("carousel_id"))
            if carousel_id and carousel_id not in out:
                out[carousel_id] = clean(row.get("selection_status")).lower()
    return out


def latest_by_carousel(rows, carousel_id):
    matches = [row for row in rows if clean(row.get("carousel_id")) == carousel_id]
    return matches[-1] if matches else {}


def stage_for_carousel(packet, asset, publish, metric):
    packet_status = clean(packet.get("status")).lower()
    if packet_status == "ready_for_canva_test":
        return "ready_for_canva_test"
    if packet_status == "needs_visual_revision":
        return "needs_visual_revision"
    if packet_status == "canva_blocked_waiting_for_flat_png_asset":
        return "canva_blocked_waiting_for_flat_png_asset"
    if packet_status in {"paused", "archived", "do_not_publish", "skip"}:
        return packet_status
    if metric:
        decision = clean(metric.get("decision"))
        return decision or "metrics_recorded_review_needed"
    if publish or packet_status == "published":
        return "published_waiting_for_metrics"
    if clean(asset.get("selection_status")).lower() in {"needs_review", "needs_scoring", "needs_regeneration", "rejected"}:
        return "needs_image_asset_selection"
    if asset.get("invalid_slots") or asset.get("missing_slots"):
        return "needs_image_asset_selection"
    if not clean(asset.get("file")):
        return "needs_image_asset_selection"
    if packet_status in {"canva_committed", "canva_committed_ready_to_publish"}:
        return "canva_committed_ready_to_publish"
    return "ready_for_canva_and_publish"


def next_action_for_stage(stage):
    actions = {
        "visibility_recovery": "Keep carousel production moving; optionally publish or record the generated single-image visibility test in parallel.",
        "ready_to_publish_visibility_test": "Optional side test: publish the single-image visibility test, share once to Story, then record 6h / 24h metrics.",
        "published_waiting_for_metrics": "Record 6h / 24h metrics with record_post_metrics.py.",
        "needs_image_asset_selection": "Generate, regenerate, or score publishable image assets, then rerun asset selection before Canva.",
        "needs_grok_asset_selection": "Generate or score images, then run select_grok_assets.py.",
        "needs_visual_revision": "Do not publish. Use the approved Mira Canva v2 template, verify layer/frame compatibility, regenerate clean candidates, then test-fill before export.",
        "ready_for_canva_test": "Do not publish yet. Test-fill the approved Mira Canva v2 template with selected v2 assets, review crops, then decide whether to commit.",
        "canva_blocked_waiting_for_flat_png_asset": "Do not export failed Canva drafts. Resolve the selected PNGs to verified Canva image asset ids, then rerun fill on a fresh duplicate.",
        "paused": "Paused by user; do not publish unless reactivated.",
        "archived": "Archived; do not publish.",
        "do_not_publish": "Do not publish this item.",
        "skip": "Skipped; choose another content item.",
        "ready_for_canva_and_publish": "Use Canva handoff files to finish the carousel and publish it.",
        "canva_committed_ready_to_publish": "Open the Canva design, review the committed layout, export the 3 carousel slides, then publish or schedule it.",
        "weak_distribution": "Mirror the asset to Threads or Pinterest and test a clearer single-image hook.",
        "wait_for_24h": "Wait for the 24h checkpoint before changing the content direction.",
        "repeat_bucket": "Create a second carousel in the same content bucket.",
        "profile_interest": "Improve the cover hook and profile CTA before testing commerce links.",
        "hook_or_save_gap": "Revise the cover headline and make the outfit benefit clearer.",
    }
    return actions.get(stage, "Open weekly_status.md and follow the next action.")


def carousel_item(run_dir, packet, asset, publish_rows, metric_rows, template=None):
    carousel_id = clean(packet.get("carousel_id"))
    publish = latest_by_carousel(publish_rows, carousel_id)
    metric = latest_by_carousel(metric_rows, carousel_id)
    stage = stage_for_carousel(packet, asset, publish, metric)
    template = template or {}
    return {
        "item_type": "carousel",
        "week_id": clean(packet.get("week_id")) or Path(run_dir).name,
        "carousel_id": carousel_id,
        "prompt_id": clean(packet.get("prompt_id")),
        "model_profile_id": clean(packet.get("model_profile_id")),
        "canva_template_key": clean(template.get("key")),
        "canva_template_name": clean(template.get("name")),
        "canva_template_url": clean(template.get("url")),
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
        "model_profile_id": clean(packet.get("model_profile_id")),
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
    if stage in {"paused", "archived", "do_not_publish", "skip"}:
        return -10
    if item_type == "carousel" and stage == "needs_visual_revision":
        return 115
    if item_type == "carousel" and stage == "canva_blocked_waiting_for_flat_png_asset":
        return 114
    if item_type == "carousel" and stage == "ready_for_canva_test":
        return 112
    if item_type == "carousel" and stage == "canva_committed_ready_to_publish":
        return 110
    if item_type == "carousel" and stage == "ready_for_canva_and_publish":
        return 100
    if item_type == "carousel" and stage in {"needs_image_asset_selection", "needs_grok_asset_selection"}:
        return 90
    priorities = {
        "published_waiting_for_metrics": 80,
        "needs_visual_revision": 95,
        "canva_blocked_waiting_for_flat_png_asset": 94,
        "ready_for_canva_test": 92,
        "canva_committed_ready_to_publish": 90,
        "ready_for_canva_and_publish": 75,
        "needs_image_asset_selection": 70,
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
    templates = load_template_registry()
    for run_dir in run_dirs_under(runs_dir):
        packets = read_csv(run_dir / "weekly_content_packet.csv")
        paused_ids = {
            clean(packet.get("carousel_id"))
            for packet in packets
            if clean(packet.get("status")).lower() in {"paused", "archived", "do_not_publish", "skip"}
        }
        publish_rows = read_csv(run_dir / "publish_log.csv")
        metric_rows = read_csv(run_dir / "metric_checkpoints.csv")
        assets = assets_by_carousel(run_dir)
        selection_statuses = asset_selection_statuses(run_dir)
        for packet in packets:
            carousel_id = clean(packet.get("carousel_id"))
            template = choose_template(packet, templates)
            asset = assets.get(carousel_id, {})
            asset["selection_status"] = selection_statuses.get(carousel_id, clean(asset.get("selection_status")))
            rows.append(carousel_item(run_dir, packet, asset, publish_rows, metric_rows, template))

        visibility_package = read_json(run_dir / "visibility_test_package.json")
        package_status = clean(visibility_package.get("status")).lower()
        if (
            visibility_package
            and package_status not in {"paused", "archived", "do_not_publish", "skip"}
            and clean(visibility_package.get("source_carousel_id")) not in paused_ids
        ):
            rows.append(visibility_item(run_dir, visibility_package, publish_rows, metric_rows))
    active_rows = [row for row in rows if item_priority(row) >= 0]
    return sorted(active_rows, key=lambda row: (item_priority(row), clean(row.get("carousel_id"))), reverse=True)


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
                f"- Model: `{top.get('model_profile_id') or 'n/a'}`",
                f"- Canva template: `{top.get('canva_template_key') or 'n/a'}` {top.get('canva_template_name') or ''}",
                f"- Canva template URL: {top.get('canva_template_url') or 'n/a'}",
                f"- Stage: `{top['stage']}`",
                f"- Asset: `{top['recommended_asset'] or 'n/a'}`",
                f"- Package: `{top['package_path'] or 'n/a'}`",
                f"- Next action: {top['next_action']}",
                "",
                "## Queue",
                "",
                "| Type | ID | Model | Template | Stage | Asset | Reach | Next Action |",
                "|---|---|---|---|---|---|---:|---|",
            ]
        )
        for row in rows:
            next_action = clean(row.get("next_action")).replace("|", "/")
            template_label = clean(f"{row.get('canva_template_key')} {row.get('canva_template_name')}")
            lines.append(
                f"| `{row['item_type']}` | `{row['carousel_id']}` | `{row.get('model_profile_id') or 'n/a'}` | `{template_label or 'n/a'}` | `{row['stage']}` | `{row['recommended_asset'] or 'n/a'}` | `{row['latest_reach'] or ''}` | {next_action} |"
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
    parser = argparse.ArgumentParser(description="Build a per-carousel publish queue across weekly Mira run folders.")
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
