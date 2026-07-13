import argparse
import csv
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from mira_models import MODEL_IDS, validate_model_id


REQUIRED_FILES = [
    "weekly_content_packet.csv",
    "canva_placeholder_values.csv",
    "canva_fill_guide.md",
    "canva_placeholder_map.json",
    "canva_asset_slots.csv",
    "daily_queue.csv",
    "image_generation_briefs.md",
    "image_review_template.csv",
    "post_drafts.md",
    "publish_checklist.md",
    "README.md",
]


PACKET_REQUIRED_FIELDS = [
    "week_id",
    "carousel_id",
    "creator_name",
    "model_profile_id",
    "trend_name",
    "audience",
    "occasion",
    "prompt_id",
    "clothing_item",
    "color_palette",
    "fabric",
    "fit",
    "styling_rules",
    "scene",
]


CANVA_REQUIRED_FIELDS = [
    "carousel_id",
    "slide2_line",
    "caption_short",
    "hashtags",
]


CANVA_LENGTH_LIMITS = {
    "slide2_line": 28,
}


DISCLOSURE_TERMS = [
    "AI",
    "虛擬",
]


IMAGE_BRIEF_REQUIRED_TERMS = [
    "full outfit",
    "no visible logos",
    "no text",
    "no watermark",
    "sexualized pose",
    "childlike styling",
    "celebrity likeness",
]


BAD_ASSET_STATUSES = {
    "needed",
    "needs_review",
    "needs_scoring",
    "needs_regeneration",
    "rejected",
    "not_found",
    "missing",
}


ISO_WEEK_ID_PATTERN = re.compile(r"^(\d{4})-W(\d{2})(?:-test)?$")


def has_encoding_drift(value):
    text = str(value or "")
    if "\ufffd" in text:
        return True
    return any(0xE000 <= ord(char) <= 0xF8FF for char in text)


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_text(path):
    return Path(path).read_text(encoding="utf-8-sig")


def clean(value):
    return " ".join((value or "").split()).strip()


def add_issue(issues, severity, code, message):
    issues.append({"severity": severity, "code": code, "message": message})


def iso_week_start(week_id):
    match = ISO_WEEK_ID_PATTERN.fullmatch(clean(week_id))
    if not match:
        return None
    try:
        return date.fromisocalendar(int(match.group(1)), int(match.group(2)), 1)
    except ValueError:
        return None


def validate_required_files(run_dir, issues):
    for file_name in REQUIRED_FILES:
        path = run_dir / file_name
        if not path.exists():
            add_issue(issues, "error", "missing_file", f"Missing {file_name}.")
        elif path.stat().st_size == 0:
            add_issue(issues, "error", "empty_file", f"{file_name} is empty.")


def validate_packet_rows(run_dir, min_rows, issues):
    path = run_dir / "weekly_content_packet.csv"
    if not path.exists():
        return []

    rows = read_csv(path)
    if len(rows) < min_rows:
        add_issue(issues, "error", "packet_row_count", f"Expected at least {min_rows} packet row(s), got {len(rows)}.")

    seen_ids = set()
    seen_week_ids = set()
    for index, row in enumerate(rows, start=1):
        row_label = row.get("carousel_id") or f"row {index}"
        for field in PACKET_REQUIRED_FIELDS:
            if not clean(row.get(field)):
                add_issue(issues, "error", "packet_required_field", f"{row_label}: missing {field}.")
        carousel_id = clean(row.get("carousel_id"))
        if carousel_id in seen_ids:
            add_issue(issues, "error", "duplicate_carousel_id", f"Duplicate carousel_id: {carousel_id}.")
        seen_ids.add(carousel_id)
        week_id = clean(row.get("week_id"))
        if week_id:
            seen_week_ids.add(week_id)
            if not iso_week_start(week_id):
                add_issue(issues, "error", "iso_week_id", f"{row_label}: invalid ISO week id `{week_id}`.")
        if clean(row.get("creator_name")) != "Mira":
            add_issue(issues, "warning", "creator_name", f"{row_label}: creator_name should be Mira.")
        model_profile_id = clean(row.get("model_profile_id"))
        if not validate_model_id(model_profile_id):
            add_issue(issues, "error", "model_profile_id", f"{row_label}: model_profile_id must be one of {sorted(MODEL_IDS)}.")
    if len(seen_week_ids) > 1:
        add_issue(issues, "error", "mixed_week_ids", f"weekly_content_packet.csv contains multiple week ids: {sorted(seen_week_ids)}.")
    return rows


def validate_daily_queue(run_dir, packet_rows, issues):
    path = run_dir / "daily_queue.csv"
    if not path.exists():
        return []

    rows = read_csv(path)
    if len(rows) < 5:
        add_issue(issues, "error", "daily_queue_row_count", f"daily_queue.csv should contain at least 5 rows, got {len(rows)}.")

    packet_ids = {clean(row.get("carousel_id")) for row in packet_rows}
    packet_week_ids = {clean(row.get("week_id")) for row in packet_rows if clean(row.get("week_id"))}
    expected_week_id = next(iter(packet_week_ids)) if len(packet_week_ids) == 1 else ""
    expected_start = iso_week_start(expected_week_id) if expected_week_id else None
    required_fields = [
        "date",
        "daily_id",
        "week_id",
        "carousel_id",
        "model_profile_id",
        "trend_name",
        "clothing_item",
        "occasion",
        "image_status",
        "canva_status",
        "publish_status",
    ]
    seen_daily_ids = set()
    for index, row in enumerate(rows, start=1):
        row_label = clean(row.get("daily_id")) or f"daily queue row {index}"
        for field in required_fields:
            if not clean(row.get(field)):
                add_issue(issues, "error", "daily_queue_required_field", f"{row_label}: missing {field}.")
        daily_id = clean(row.get("daily_id"))
        if daily_id in seen_daily_ids:
            add_issue(issues, "error", "daily_queue_duplicate_id", f"Duplicate daily_id: {daily_id}.")
        seen_daily_ids.add(daily_id)
        if clean(row.get("carousel_id")) not in packet_ids:
            add_issue(issues, "error", "daily_queue_carousel_id", f"{row_label}: carousel_id is not in weekly_content_packet.csv.")
        row_week_id = clean(row.get("week_id"))
        if expected_week_id and row_week_id != expected_week_id:
            add_issue(issues, "error", "daily_queue_week_id", f"{row_label}: week_id `{row_week_id}` does not match `{expected_week_id}`.")
        if expected_start:
            expected_date = (expected_start + timedelta(days=index - 1)).isoformat()
            actual_date = clean(row.get("date"))
            if actual_date != expected_date:
                add_issue(
                    issues,
                    "error",
                    "daily_queue_iso_date",
                    f"{row_label}: date `{actual_date}` should be `{expected_date}` for ISO week `{expected_week_id}`.",
                )
        if not validate_model_id(row.get("model_profile_id")):
            add_issue(issues, "error", "daily_queue_model_profile_id", f"{row_label}: model_profile_id must be one of {sorted(MODEL_IDS)}.")
    return rows


def validate_image_generation_files(run_dir, packet_rows, issues):
    brief_path = run_dir / "image_generation_briefs.md"
    review_path = run_dir / "image_review_template.csv"
    if brief_path.exists():
        text = read_text(brief_path)
        text_lower = text.lower()
        for row in packet_rows:
            carousel_id = clean(row.get("carousel_id"))
            model_profile_id = clean(row.get("model_profile_id"))
            if carousel_id and carousel_id not in text:
                add_issue(issues, "error", "image_brief_missing_carousel", f"image_generation_briefs.md missing {carousel_id}.")
            if model_profile_id and model_profile_id not in text:
                add_issue(issues, "error", "image_brief_missing_model", f"image_generation_briefs.md missing {model_profile_id}.")
        for term in IMAGE_BRIEF_REQUIRED_TERMS:
            if term.lower() not in text_lower:
                add_issue(issues, "error", "image_brief_required_term", f"image_generation_briefs.md missing `{term}`.")
    if review_path.exists():
        rows = read_csv(review_path)
        review_ids = {clean(row.get("carousel_id")) for row in rows}
        packet_ids = {clean(row.get("carousel_id")) for row in packet_rows}
        for carousel_id in sorted(packet_ids - review_ids):
            add_issue(issues, "error", "image_review_missing_row", f"image_review_template.csv missing {carousel_id}.")


def validate_canva_rows(run_dir, packet_rows, issues):
    path = run_dir / "canva_placeholder_values.csv"
    if not path.exists():
        return []

    rows = read_csv(path)
    packet_ids = {clean(row.get("carousel_id")) for row in packet_rows}
    canva_ids = {clean(row.get("carousel_id")) for row in rows}
    missing_ids = packet_ids - canva_ids
    extra_ids = canva_ids - packet_ids

    for carousel_id in sorted(missing_ids):
        add_issue(issues, "error", "canva_missing_row", f"Missing Canva row for {carousel_id}.")
    for carousel_id in sorted(extra_ids):
        add_issue(issues, "warning", "canva_extra_row", f"Extra Canva row without packet row: {carousel_id}.")

    for index, row in enumerate(rows, start=1):
        row_label = row.get("carousel_id") or f"Canva row {index}"
        for field in CANVA_REQUIRED_FIELDS:
            if not clean(row.get(field)):
                add_issue(issues, "error", "canva_required_field", f"{row_label}: missing {field}.")
        for field, limit in CANVA_LENGTH_LIMITS.items():
            value = clean(row.get(field))
            if len(value) > limit:
                add_issue(issues, "warning", "canva_text_length", f"{row_label}: {field} is {len(value)} chars, limit {limit}.")
        for field in ["slide2_line", "caption_short", "hashtags"]:
            if has_encoding_drift(row.get(field)):
                add_issue(issues, "error", "canva_encoding_drift", f"{row_label}: {field} appears to contain mojibake or private-use replacement characters.")
        disclosure_text = clean(row.get("caption_short"))
        for term in DISCLOSURE_TERMS:
            if term not in disclosure_text:
                add_issue(issues, "error", "missing_disclosure", f"{row_label}: disclosure missing {term}.")
        hashtag_count = len(re.findall(r"#\S+", row.get("hashtags", "")))
        if hashtag_count < 6 or hashtag_count > 12:
            add_issue(issues, "warning", "hashtag_count", f"{row_label}: hashtag count is {hashtag_count}; target 6-12.")
    return rows


def validate_post_drafts(run_dir, packet_rows, issues):
    path = run_dir / "post_drafts.md"
    if not path.exists():
        return
    text = read_text(path)
    for row in packet_rows:
        carousel_id = clean(row.get("carousel_id"))
        if carousel_id and carousel_id not in text:
            add_issue(issues, "error", "post_draft_missing_carousel", f"post_drafts.md missing {carousel_id}.")
    for section in ["Instagram Caption", "Instagram First Comment", "Threads Copy", "Pinterest Pin"]:
        if section not in text:
            add_issue(issues, "error", "post_draft_missing_section", f"post_drafts.md missing {section}.")
    for term in DISCLOSURE_TERMS:
        if term not in text:
            add_issue(issues, "error", "post_draft_disclosure", f"post_drafts.md missing disclosure term {term}.")


def validate_canva_handoff(run_dir, packet_rows, issues, require_assets=False, required_asset_ids=None):
    packet_ids = {clean(row.get("carousel_id")) for row in packet_rows}
    packet_by_id = {clean(row.get("carousel_id")): row for row in packet_rows}
    required_asset_ids = set(required_asset_ids or packet_ids)
    mapping = {}

    map_path = run_dir / "canva_placeholder_map.json"
    if map_path.exists():
        try:
            mapping = json.loads(read_text(map_path))
        except json.JSONDecodeError as exc:
            add_issue(issues, "error", "canva_map_json", f"canva_placeholder_map.json is invalid JSON: {exc}.")
            mapping = {}

        map_ids = set(mapping.keys())
        for carousel_id in sorted(packet_ids - map_ids):
            add_issue(issues, "error", "canva_map_missing", f"canva_placeholder_map.json missing {carousel_id}.")
        for carousel_id in sorted(map_ids - packet_ids):
            add_issue(issues, "warning", "canva_map_extra", f"canva_placeholder_map.json has extra {carousel_id}.")
        for carousel_id, data in mapping.items():
            placeholders = data.get("placeholders", {})
            for token in ["{{slide2_line}}"]:
                if not clean(placeholders.get(token)):
                    add_issue(issues, "error", "canva_map_placeholder", f"{carousel_id}: missing {token} in placeholder map.")
                elif has_encoding_drift(placeholders.get(token)):
                    add_issue(issues, "error", "canva_map_encoding_drift", f"{carousel_id}: {token} appears to contain mojibake or private-use replacement characters.")
            for field in ["caption_short", "hashtags"]:
                if has_encoding_drift(data.get(field)):
                    add_issue(issues, "error", "canva_map_encoding_drift", f"{carousel_id}: {field} appears to contain mojibake or private-use replacement characters.")
            if not data.get("design_contract"):
                add_issue(issues, "warning", "canva_map_contract", f"{carousel_id}: missing design_contract.")

    slots_path = run_dir / "canva_asset_slots.csv"
    if slots_path.exists():
        rows = read_csv(slots_path)
        by_carousel = {}
        for row in rows:
            by_carousel.setdefault(clean(row.get("carousel_id")), []).append(row)
        for carousel_id in sorted(packet_ids):
            slots = by_carousel.get(carousel_id, [])
            slot_ids = {clean(row.get("slot_id")) for row in slots}
            require_carousel_assets = require_assets and carousel_id in required_asset_ids
            for slot_id in ["cover_image", "motion_crop", "detail_image"]:
                if slot_id not in slot_ids:
                    severity = "error" if require_carousel_assets else "warning"
                    add_issue(issues, severity, "canva_asset_slot", f"{carousel_id}: missing {slot_id} asset slot.")
            for row in slots:
                slot_id = clean(row.get("slot_id"))
                status = clean(row.get("status")).lower()
                if require_carousel_assets and status in BAD_ASSET_STATUSES:
                    add_issue(issues, "error", "canva_asset_slot_status", f"{carousel_id}: {slot_id} has non-publishable status `{status}`.")
            if require_carousel_assets:
                slot_file_by_id = {clean(row.get("slot_id")): clean(row.get("recommended_file")) for row in slots}
                for slot_id in ["cover_image", "motion_crop", "detail_image"]:
                    if not slot_file_by_id.get(slot_id):
                        add_issue(issues, "error", "canva_asset_required", f"{carousel_id}: {slot_id} has no recommended_file.")
                mapped_slots = mapping.get(carousel_id, {}).get("asset_slots", []) if mapping else []
                cover_file = slot_file_by_id.get("cover_image", "")
                mapped_cover = ""
                for mapped_slot in mapped_slots:
                    if clean(mapped_slot.get("slot_id")) == "cover_image":
                        mapped_cover = clean(mapped_slot.get("recommended_file"))
                        break
                if mapping and mapped_cover != cover_file:
                    add_issue(
                        issues,
                        "error",
                        "canva_map_asset_mismatch",
                        f"{carousel_id}: canva_placeholder_map.json cover_image `{mapped_cover}` does not match CSV `{cover_file}`.",
                    )

        if require_assets:
            active_selection = None
            for selection_name in ["codex_asset_selection.csv", "openai_asset_selection.csv", "grok_asset_selection.csv"]:
                selection_path = run_dir / selection_name
                if selection_path.exists():
                    active_selection = (selection_name, selection_path)
                    break
            if active_selection:
                selection_name, selection_path = active_selection
                for row in read_csv(selection_path):
                    carousel_id = clean(row.get("carousel_id"))
                    if carousel_id not in required_asset_ids:
                        continue
                    status = clean(row.get("selection_status")).lower()
                    if status and not status.startswith("selected"):
                        add_issue(issues, "error", "asset_selection_status", f"{carousel_id}: {selection_name} has selection_status `{status}`.")

        fill_guide = run_dir / "canva_fill_guide.md"
        if require_assets and fill_guide.exists():
            text = read_text(fill_guide)
            for carousel_id, packet in packet_by_id.items():
                if carousel_id not in required_asset_ids:
                    continue
                packet_status = clean(packet.get("status")).lower()
                if packet_status in {"ready_for_canva_test", "canva_blocked_waiting_for_flat_png_asset", "canva_committed", "canva_committed_ready_to_publish"} and "TBD" in text:
                    add_issue(issues, "error", "canva_verified_asset_tbd", f"{carousel_id}: canva_fill_guide.md still contains `TBD`; verified Canva flat image assets are incomplete.")


def write_reports(run_dir, issues):
    status = "pass" if not any(issue["severity"] == "error" for issue in issues) else "fail"
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")
    error_count = sum(1 for issue in issues if issue["severity"] == "error")
    report = {
        "status": status,
        "error_count": error_count,
        "warning_count": warning_count,
        "issues": issues,
    }

    (run_dir / "quality_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Weekly Run Quality Report",
        "",
        f"Status: `{status}`",
        f"Errors: `{error_count}`",
        f"Warnings: `{warning_count}`",
        "",
    ]
    if issues:
        lines.append("## Issues")
        lines.append("")
        for issue in issues:
            lines.append(f"- `{issue['severity']}` / `{issue['code']}`: {issue['message']}")
    else:
        lines.append("No issues found.")
    (run_dir / "quality_report.md").write_text("\n".join(lines), encoding="utf-8")

    return report


def validate_run(run_dir, min_rows=1, require_assets=False, carousel_id=""):
    run_dir = Path(run_dir)
    issues = []
    validate_required_files(run_dir, issues)
    packet_rows = validate_packet_rows(run_dir, min_rows=min_rows, issues=issues)
    validate_daily_queue(run_dir, packet_rows=packet_rows, issues=issues)
    validate_image_generation_files(run_dir, packet_rows=packet_rows, issues=issues)
    validate_canva_rows(run_dir, packet_rows=packet_rows, issues=issues)
    validate_post_drafts(run_dir, packet_rows=packet_rows, issues=issues)
    required_asset_ids = {clean(carousel_id)} if clean(carousel_id) else None
    if required_asset_ids and not required_asset_ids.issubset(
        {clean(row.get("carousel_id")) for row in packet_rows}
    ):
        add_issue(issues, "error", "unknown_carousel_id", f"Carousel id not found in packet: {clean(carousel_id)}.")
    validate_canva_handoff(
        run_dir,
        packet_rows=packet_rows,
        issues=issues,
        require_assets=require_assets,
        required_asset_ids=required_asset_ids,
    )
    return write_reports(run_dir, issues)


def main():
    parser = argparse.ArgumentParser(description="Validate a generated weekly Mira run folder.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--min-rows", type=int, default=1)
    parser.add_argument("--require-assets", action="store_true", help="Fail when required Canva image slots have no selected asset.")
    parser.add_argument("--carousel-id", default="", help="Limit strict asset checks to one carousel id.")
    parser.add_argument("--no-fail", action="store_true", help="Write reports but exit 0 even when errors exist.")
    args = parser.parse_args()

    report = validate_run(
        args.run_dir,
        min_rows=args.min_rows,
        require_assets=args.require_assets,
        carousel_id=args.carousel_id,
    )
    print(
        f"Validation {report['status']}: "
        f"{report['error_count']} error(s), {report['warning_count']} warning(s)."
    )
    if report["status"] != "pass" and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
