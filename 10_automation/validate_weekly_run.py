import argparse
import csv
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "weekly_content_packet.csv",
    "grok_prompts.md",
    "canva_placeholder_values.csv",
    "canva_fill_guide.md",
    "canva_placeholder_map.json",
    "canva_asset_slots.csv",
    "post_drafts.md",
    "publish_checklist.md",
    "README.md",
]


PACKET_REQUIRED_FIELDS = [
    "week_id",
    "carousel_id",
    "creator_name",
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
    "slide1_title",
    "slide1_subtitle",
    "slide1_disclosure",
    "slide2_title",
    "slide2_body",
    "slide3_title",
    "slide3_body",
    "slide4_title",
    "slide4_body",
    "slide5_title",
    "slide5_cta",
    "slide5_note",
    "slide5_disclosure",
    "caption_short",
    "hashtags",
]


CANVA_LENGTH_LIMITS = {
    "slide1_title": 18,
    "slide1_subtitle": 24,
    "slide2_title": 28,
    "slide2_body": 42,
    "slide3_title": 26,
    "slide3_body": 46,
    "slide4_title": 18,
    "slide4_body": 48,
    "slide5_title": 18,
    "slide5_cta": 22,
    "slide5_note": 32,
}


DISCLOSURE_TERMS = [
    "AI",
    "虛擬穿搭",
    "非真人試穿",
]


GROK_REQUIRED_TERMS = [
    "fictional",
    "same fictional identity",
    "full outfit",
    "no real person",
    "no celebrity",
    "no childlike",
    "no nudity",
    "no visible brand logos",
]


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def clean(value):
    return " ".join((value or "").split()).strip()


def add_issue(issues, severity, code, message):
    issues.append({"severity": severity, "code": code, "message": message})


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
    for index, row in enumerate(rows, start=1):
        row_label = row.get("carousel_id") or f"row {index}"
        for field in PACKET_REQUIRED_FIELDS:
            if not clean(row.get(field)):
                add_issue(issues, "error", "packet_required_field", f"{row_label}: missing {field}.")
        carousel_id = clean(row.get("carousel_id"))
        if carousel_id in seen_ids:
            add_issue(issues, "error", "duplicate_carousel_id", f"Duplicate carousel_id: {carousel_id}.")
        seen_ids.add(carousel_id)
        if clean(row.get("creator_name")) != "Mika Lin":
            add_issue(issues, "warning", "creator_name", f"{row_label}: creator_name should be Mika Lin.")
    return rows


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
        disclosure_text = " ".join(
            clean(row.get(field))
            for field in ["slide1_disclosure", "slide5_disclosure", "caption_short"]
        )
        for term in DISCLOSURE_TERMS:
            if term not in disclosure_text:
                add_issue(issues, "error", "missing_disclosure", f"{row_label}: disclosure missing {term}.")
        hashtag_count = len(re.findall(r"#\S+", row.get("hashtags", "")))
        if hashtag_count < 6 or hashtag_count > 12:
            add_issue(issues, "warning", "hashtag_count", f"{row_label}: hashtag count is {hashtag_count}; target 6-12.")
    return rows


def validate_grok_prompt(run_dir, issues):
    path = run_dir / "grok_prompts.md"
    if not path.exists():
        return
    text = read_text(path).lower()
    for term in GROK_REQUIRED_TERMS:
        if term.lower() not in text:
            add_issue(issues, "error", "grok_required_term", f"grok_prompts.md missing `{term}`.")


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


def validate_canva_handoff(run_dir, packet_rows, issues):
    packet_ids = {clean(row.get("carousel_id")) for row in packet_rows}

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
            for token in ["{{slide1_title}}", "{{slide1_disclosure}}", "{{slide5_cta}}", "{{slide5_disclosure}}"]:
                if not clean(placeholders.get(token)):
                    add_issue(issues, "error", "canva_map_placeholder", f"{carousel_id}: missing {token} in placeholder map.")
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
            for slot_id in ["cover_image", "detail_image", "texture_or_crop"]:
                if slot_id not in slot_ids:
                    add_issue(issues, "warning", "canva_asset_slot", f"{carousel_id}: missing {slot_id} asset slot.")


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


def validate_run(run_dir, min_rows=1):
    run_dir = Path(run_dir)
    issues = []
    validate_required_files(run_dir, issues)
    packet_rows = validate_packet_rows(run_dir, min_rows=min_rows, issues=issues)
    validate_canva_rows(run_dir, packet_rows=packet_rows, issues=issues)
    validate_grok_prompt(run_dir, issues)
    validate_post_drafts(run_dir, packet_rows=packet_rows, issues=issues)
    validate_canva_handoff(run_dir, packet_rows=packet_rows, issues=issues)
    return write_reports(run_dir, issues)


def main():
    parser = argparse.ArgumentParser(description="Validate a generated weekly Mika Lin run folder.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--min-rows", type=int, default=1)
    parser.add_argument("--no-fail", action="store_true", help="Write reports but exit 0 even when errors exist.")
    args = parser.parse_args()

    report = validate_run(args.run_dir, min_rows=args.min_rows)
    print(
        f"Validation {report['status']}: "
        f"{report['error_count']} error(s), {report['warning_count']} warning(s)."
    )
    if report["status"] != "pass" and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
