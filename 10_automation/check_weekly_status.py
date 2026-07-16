import argparse
import csv
import json
from pathlib import Path


REQUIRED_RUN_FILES = [
    "weekly_content_packet.csv",
    "canva_placeholder_values.csv",
    "canva_fill_guide.md",
    "canva_asset_slots.csv",
    "daily_queue.csv",
    "image_generation_briefs.md",
    "image_review_template.csv",
    "post_drafts.md",
    "publish_checklist.md",
    "quality_report.md",
]


def clean(value):
    return " ".join((value or "").split()).strip()


def read_csv(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_json(path):
    path = Path(path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def file_state(run_dir):
    states = {}
    for file_name in REQUIRED_RUN_FILES:
        path = run_dir / file_name
        states[file_name] = {
            "exists": path.exists(),
            "size": path.stat().st_size if path.exists() else 0,
        }
    return states


def quality_status(run_dir):
    report = read_json(run_dir / "quality_report.json")
    if not report:
        return {
            "status": "missing",
            "error_count": None,
            "warning_count": None,
        }
    return {
        "status": report.get("status", "unknown"),
        "error_count": report.get("error_count"),
        "warning_count": report.get("warning_count"),
    }


def asset_status(run_dir):
    slots = read_csv(run_dir / "canva_asset_slots.csv")
    selections = []
    for selection_name in ["codex_asset_selection.csv", "openai_asset_selection.csv", "grok_asset_selection.csv"]:
        selection_path = run_dir / selection_name
        if selection_path.exists():
            selections = read_csv(selection_path)
            break
    carousel_ids = sorted({clean(row.get("carousel_id")) for row in slots if clean(row.get("carousel_id"))})
    missing_cover = []
    missing_detail = []
    selected_count = 0
    selected_carousel_ids = []

    for carousel_id in carousel_ids:
        rows = [row for row in slots if clean(row.get("carousel_id")) == carousel_id]
        cover = next((row for row in rows if clean(row.get("slot_id")) == "cover_image"), {})
        detail = next((row for row in rows if clean(row.get("slot_id")) == "detail_image"), {})
        if not clean(cover.get("recommended_file")):
            missing_cover.append(carousel_id)
        else:
            selected_count += 1
            selected_carousel_ids.append(carousel_id)
        if not clean(detail.get("recommended_file")):
            missing_detail.append(carousel_id)

    template_exists = any(
        (run_dir / name).exists()
        for name in ["image_review_template.csv", "codex_asset_review_template.csv", "openai_asset_review_template.csv", "grok_asset_review_template.csv"]
    )
    selection_exists = any(
        (run_dir / name).exists()
        for name in ["codex_asset_selection.csv", "openai_asset_selection.csv", "grok_asset_selection.csv"]
    )

    return {
        "carousel_count": len(carousel_ids),
        "selection_exists": selection_exists,
        "review_template_exists": template_exists,
        "selected_cover_count": selected_count,
        "selected_carousel_ids": selected_carousel_ids,
        "missing_cover": missing_cover,
        "missing_detail": missing_detail,
        "selection_rows": len(selections),
    }


def publish_status(run_dir):
    publish_rows = read_csv(run_dir / "publish_log.csv")
    metric_rows = read_csv(run_dir / "metric_checkpoints.csv")
    latest_publish = publish_rows[-1] if publish_rows else {}
    latest_metric = metric_rows[-1] if metric_rows else {}
    published_carousel_ids = sorted(
        {clean(row.get("carousel_id")) for row in publish_rows if clean(row.get("carousel_id"))}
    )
    return {
        "published": bool(latest_publish),
        "metric_count": len(metric_rows),
        "latest_publish": latest_publish,
        "latest_metric": latest_metric,
        "latest_decision": clean(latest_metric.get("decision")),
        "latest_next_action": clean(latest_metric.get("next_action")),
        "published_carousel_ids": published_carousel_ids,
    }


def packet_status(run_dir):
    rows = read_csv(run_dir / "weekly_content_packet.csv")
    published_count = sum(1 for row in rows if clean(row.get("status")) == "published")
    ready_for_canva_test = [
        clean(row.get("carousel_id"))
        for row in rows
        if clean(row.get("status")).lower() == "ready_for_canva_test"
    ]
    canva_committed_ready_to_publish = [
        clean(row.get("carousel_id"))
        for row in rows
        if clean(row.get("status")).lower()
        in {"canva_committed", "canva_committed_ready_to_publish"}
    ]
    canva_blocked_waiting_for_flat_png_asset = [
        clean(row.get("carousel_id"))
        for row in rows
        if clean(row.get("status")).lower() == "canva_blocked_waiting_for_flat_png_asset"
    ]
    needs_visual_revision = [
        clean(row.get("carousel_id"))
        for row in rows
        if clean(row.get("status")).lower() == "needs_visual_revision"
    ]
    inactive_statuses = {"paused", "archived", "do_not_publish", "skip"}
    inactive_count = sum(1 for row in rows if clean(row.get("status")).lower() in inactive_statuses)
    return {
        "row_count": len(rows),
        "published_count": published_count,
        "ready_for_canva_test": ready_for_canva_test,
        "canva_committed_ready_to_publish": canva_committed_ready_to_publish,
        "canva_blocked_waiting_for_flat_png_asset": canva_blocked_waiting_for_flat_png_asset,
        "needs_visual_revision": needs_visual_revision,
        "inactive_count": inactive_count,
        "all_inactive": bool(rows) and inactive_count == len(rows),
        "carousel_ids": [clean(row.get("carousel_id")) for row in rows if clean(row.get("carousel_id"))],
    }


def determine_stage(files, quality, assets, publishing, packet=None):
    packet = packet or {}
    missing_files = [name for name, state in files.items() if not state["exists"]]
    if missing_files:
        return {
            "stage": "missing_weekly_packet_files",
            "next_action": "Run run_weekly_pipeline.py or build_weekly_packet.py to regenerate the weekly run folder.",
            "blocking_items": missing_files,
        }

    if packet.get("all_inactive"):
        return {
            "stage": "paused",
            "next_action": "This run is paused or archived. Create a new OpenAI-first run before publishing more content.",
            "blocking_items": [],
        }

    if quality["status"] != "pass":
        return {
            "stage": "quality_gate_not_passed",
            "next_action": "Run validate_weekly_run.py and fix all errors before producing images or editing Canva.",
            "blocking_items": [f"quality_status={quality['status']}"],
        }

    # Keep the weekly production line moving until every carousel has image
    # assets. One earlier carousel waiting for Canva must not hide later image
    # jobs that are still incomplete.
    if assets["missing_cover"]:
        if assets["review_template_exists"] and assets["selection_rows"]:
            next_action = "Continue generating and scoring the remaining Codex image jobs, then rerun select_codex_assets.py. Canva work for already selected carousels can proceed in parallel."
        elif assets["selection_exists"]:
            next_action = "Review the remaining image jobs, score publishable A/B/C sets, then rerun select_codex_assets.py."
        else:
            next_action = "Use the Codex generation handoff to generate workspace images, score them in image_review_template.csv, then run select_codex_assets.py."
        return {
            "stage": "needs_image_asset_selection",
            "next_action": next_action,
            "blocking_items": assets["missing_cover"],
        }

    if packet.get("needs_visual_revision"):
        return {
            "stage": "needs_visual_revision",
            "next_action": "Read canva_slot_targets.json, create A/B/C for the assigned master frame ratios, normalize them without stretching, and do not publish until the untouched Canva fill and canva_frame_fit pass.",
            "blocking_items": packet.get("needs_visual_revision"),
        }

    if packet.get("canva_blocked_waiting_for_flat_png_asset"):
        return {
            "stage": "canva_blocked_waiting_for_flat_png_asset",
            "next_action": "Resolve the selected complete PNG/JPG images to verified Canva image asset ids, then rerun the Canva fill on a fresh duplicate. Public URLs are optional; do not use image_to_design, Magic Layers, or old Canva design asset ids. Review quality_report.md for any additional strict validation blockers.",
            "blocking_items": packet.get("canva_blocked_waiting_for_flat_png_asset"),
        }

    if packet.get("ready_for_canva_test"):
        return {
            "stage": "ready_for_canva_test",
            "next_action": "Test-fill the registered active Mira Canva master template, review the crop preview, then commit only after user approval.",
            "blocking_items": packet.get("ready_for_canva_test"),
        }

    if packet.get("canva_committed_ready_to_publish"):
        return {
            "stage": "canva_committed_ready_to_publish",
            "next_action": "Open the committed Canva design, review/export the 3 carousel slices, then publish or schedule it.",
            "blocking_items": packet.get("canva_committed_ready_to_publish"),
        }

    ready_for_canva = sorted(
        set(assets.get("selected_carousel_ids", []))
        - set(publishing.get("published_carousel_ids", []))
    )
    if ready_for_canva:
        return {
            "stage": "ready_for_canva_and_publish",
            "next_action": "Use the selected image assets and Canva handoff to fill the next carousel, then export and publish it.",
            "blocking_items": ready_for_canva,
        }

    if not publishing["published"]:
        return {
            "stage": "ready_for_canva_and_publish",
            "next_action": "Use canva_fill_guide.md, canva_asset_plan.md, and post_drafts.md to finish Canva and publish the carousel.",
            "blocking_items": [],
        }

    if publishing["published"] and publishing["metric_count"] == 0:
        return {
            "stage": "published_waiting_for_metrics",
            "next_action": "Run record_post_metrics.py at the 6h and 24h checkpoints.",
            "blocking_items": [],
        }

    if publishing["latest_decision"]:
        return {
            "stage": publishing["latest_decision"],
            "next_action": publishing["latest_next_action"],
            "blocking_items": [],
        }

    return {
        "stage": "metrics_recorded_review_needed",
        "next_action": "Open publish_status.md and decide whether to repeat, revise, or run recovery.",
        "blocking_items": [],
    }


def command_suggestions(run_dir, stage):
    run_dir_str = str(run_dir)
    suggestions = []
    if stage == "quality_gate_not_passed":
        suggestions.append(
            f"python 10_automation/validate_weekly_run.py --run-dir {run_dir_str} --min-rows 1"
        )
    elif stage == "needs_image_asset_selection":
        suggestions.append(
            f"open {run_dir_str}/image_generation_briefs.md"
        )
        suggestions.append(
            f"python 10_automation/select_codex_assets.py --run-dir {run_dir_str} --provider Codex --score-sheet {run_dir_str}/image_review_template.csv --drive-inventory path_to_image_inventory.csv"
        )
        suggestions.append(
            f"python 10_automation/validate_weekly_run.py --run-dir {run_dir_str} --min-rows 1 --require-assets"
        )
    elif stage == "ready_for_canva_test":
        suggestions.append(f"open {run_dir_str}/canva_fill_guide.md")
        suggestions.append(f"open {run_dir_str}/canva_asset_plan.md")
        suggestions.append("Open the registered active Mira Canva master template and test-fill selected assets.")
    elif stage == "needs_visual_revision":
        suggestions.append(f"open {run_dir_str}/generated_images")
        suggestions.append(f"open {run_dir_str}/canva_asset_plan.md")
        suggestions.append("Use canva_slot_targets.json and prepare_canva_ready_assets.py before revising the Canva design.")
    elif stage == "canva_blocked_waiting_for_flat_png_asset":
        visual_review = run_dir / "W29_v2_VISUAL_REVIEW.html"
        if visual_review.exists():
            suggestions.append(f"open {visual_review}")
        suggestions.append(f"open {run_dir_str}/canva_asset_plan.md")
        suggestions.append(f"open {run_dir_str}/generated_images")
    elif stage == "ready_for_canva_and_publish":
        suggestions.append(f"open {run_dir_str}/canva_fill_guide.md")
        suggestions.append(f"open {run_dir_str}/canva_asset_plan.md")
        suggestions.append(f"open {run_dir_str}/post_drafts.md")
    elif stage == "canva_committed_ready_to_publish":
        suggestions.append("open 10_automation/canva_template_registry.md")
        suggestions.append(f"open {run_dir_str}/post_drafts.md")
        suggestions.append(f"open {run_dir_str}/publish_checklist.md")
    elif stage == "published_waiting_for_metrics":
        suggestions.append(
            f"python 10_automation/record_post_metrics.py --run-dir {run_dir_str} --record-metrics --hours-after-publish 24 --reach 0 --likes 0 --saves 0 --comments 0 --shares 0 --post-url POST_URL"
        )
    elif stage == "visibility_recovery":
        suggestions.append("open 05_content/2026_06_18_reactivation_plan.md")
        suggestions.append("open 10_automation/PUBLISH_QUEUE.md")
        suggestions.append("open 09_sops/instagram_zero_reach_recovery.md")
    return suggestions


def write_status_reports(run_dir, status):
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "weekly_status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Weekly Status",
        "",
        f"Run folder: `{run_dir}`",
        f"Stage: `{status['stage']['stage']}`",
        "",
        "## Next Action",
        "",
        status["stage"]["next_action"],
        "",
    ]
    if status["stage"]["blocking_items"]:
        lines.extend(["## Blocking Items", ""])
        for item in status["stage"]["blocking_items"]:
            lines.append(f"- `{item}`")
        lines.append("")

    if status["commands"]:
        lines.extend(["## Suggested Commands", ""])
        for command in status["commands"]:
            lines.extend(["```powershell", command, "```", ""])

    lines.extend(
        [
            "## Summary",
            "",
            f"- Packet rows: `{status['packet']['row_count']}`",
            f"- Quality: `{status['quality']['status']}`",
            f"- Cover assets selected: `{status['assets']['selected_cover_count']}` / `{status['assets']['carousel_count']}`",
            f"- Published: `{status['publish']['published']}`",
            f"- Metric checkpoints: `{status['publish']['metric_count']}`",
            "",
        ]
    )
    (run_dir / "weekly_status.md").write_text("\n".join(lines), encoding="utf-8")


def check_status(run_dir):
    run_dir = Path(run_dir)
    run_state = read_json(run_dir / "run_state.json")
    files = file_state(run_dir)
    quality = quality_status(run_dir)
    assets = asset_status(run_dir)
    publishing = publish_status(run_dir)
    packet = packet_status(run_dir)
    if clean(run_state.get("status")).lower() == "archived":
        stage = {
            "stage": "archived",
            "next_action": clean(run_state.get("reason")) or "This historical run is archived and excluded from production queues.",
            "blocking_items": [],
        }
    else:
        stage = determine_stage(files, quality, assets, publishing, packet=packet)
    commands = command_suggestions(run_dir, stage["stage"])
    status = {
        "run_dir": str(run_dir),
        "run_state": run_state,
        "stage": stage,
        "packet": packet,
        "files": files,
        "quality": quality,
        "assets": assets,
        "publish": publishing,
        "commands": commands,
    }
    write_status_reports(run_dir, status)
    return status


def main():
    parser = argparse.ArgumentParser(description="Check the current stage and next action for a weekly Mira run folder.")
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    status = check_status(args.run_dir)
    print(f"Stage: {status['stage']['stage']}")
    print(f"Next action: {status['stage']['next_action']}")
    print(f"Wrote {Path(args.run_dir) / 'weekly_status.md'}")


if __name__ == "__main__":
    main()
