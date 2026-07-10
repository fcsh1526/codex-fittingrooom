import argparse
import csv
import json
from pathlib import Path


ASSET_SLOT_FIELDS = [
    "carousel_id",
    "slot_id",
    "slide_range",
    "asset_type",
    "purpose",
    "recommended_file",
    "status",
    "notes",
]


SELECTION_FIELDS = [
    "carousel_id",
    "prompt_id",
    "cover_asset",
    "cover_url",
    "detail_asset",
    "detail_url",
    "texture_asset",
    "texture_url",
    "selection_status",
    "notes",
]


SCORE_FIELDS = [
    "prompt_id",
    "file_name",
    "tool",
    "identity_consistency",
    "outfit_clarity",
    "body_integrity",
    "platform_fit",
    "shopping_value",
    "publishable",
    "best_platform",
    "status",
    "notes",
]


def clean(value):
    return " ".join((value or "").split()).strip()


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_with_fields(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def number(value):
    try:
        return int(clean(value))
    except ValueError:
        return 0


def score_row(row):
    codex_fields = [
        "model_consistency",
        "reader_relatability",
        "outfit_clarity",
        "ai_realism",
        "commerce_value",
    ]
    legacy_fields = [
        "identity_consistency",
        "outfit_clarity",
        "body_integrity",
        "platform_fit",
        "shopping_value",
    ]
    fields = codex_fields if any(clean(row.get(field)) for field in codex_fields) else legacy_fields
    return sum(number(row.get(field)) for field in fields)


def status_rank(row):
    status = clean(row.get("status")).lower()
    platform = clean(row.get("best_platform")).lower()
    publishable = clean(row.get("publishable")).lower()
    rank = 0
    if publishable in {"yes", "true", "1"}:
        rank += 20
    if status == "selected":
        rank += 20
    elif status == "backup":
        rank += 10
    if "instagram carousel" in platform:
        rank += 8
    elif "instagram" in platform:
        rank += 5
    elif "pinterest" in platform:
        rank += 2
    return rank


def ranked_assets(rows):
    return sorted(
        rows,
        key=lambda row: (
            status_rank(row),
            score_row(row),
            asset_file_name(row),
        ),
        reverse=True,
    )


def asset_file_name(row):
    return clean(row.get("file_name")) or clean(row.get("candidate_file"))


def candidate_label(row):
    stem = Path(asset_file_name(row)).stem.lower()
    for label in ["a", "b", "c"]:
        if stem.endswith(f"_candidate_{label}") or stem.endswith(f"-candidate-{label}"):
            return label.upper()
    return ""


def drive_lookup(rows):
    lookup = {}
    for row in rows:
        file_name = asset_file_name(row)
        if file_name:
            lookup[file_name] = {
                "drive_url": clean(row.get("drive_url")),
                "file_id": clean(row.get("file_id")),
                "mime_type": clean(row.get("mime_type")),
                "file_path": clean(row.get("file_path")),
            }
    return lookup


def build_selection(packet, score_rows, drive_rows):
    prompt_id = clean(packet.get("prompt_id"))
    carousel_id = clean(packet.get("carousel_id"))
    candidates = ranked_assets(
        row
        for row in score_rows
        if (clean(row.get("prompt_id")) == prompt_id or clean(row.get("carousel_id")) == carousel_id)
        and clean(row.get("publishable")).lower() in {"yes", "true", "1"}
    )

    if not candidates:
        return {
            "carousel_id": carousel_id,
            "prompt_id": prompt_id,
            "cover_asset": "",
            "cover_url": "",
            "detail_asset": "",
            "detail_url": "",
            "texture_asset": "",
            "texture_url": "",
            "selection_status": "needs_review",
            "notes": "No publishable scored assets found for this prompt.",
        }

    def file_name(row):
        return asset_file_name(row) if row else ""

    def url_for(row):
        if not row:
            return ""
        asset = drive_rows.get(file_name(row), {})
        return asset.get("drive_url") or asset.get("file_path") or ""

    labeled = {}
    for row in candidates:
        label = candidate_label(row)
        if label and label not in labeled:
            labeled[label] = row

    if labeled:
        missing = [label for label in ["A", "B", "C"] if label not in labeled]
        if missing:
            return {
                "carousel_id": carousel_id,
                "prompt_id": prompt_id,
                "cover_asset": "",
                "cover_url": "",
                "detail_asset": "",
                "detail_url": "",
                "texture_asset": "",
                "texture_url": "",
                "selection_status": "needs_review",
                "notes": f"Three publishable A/B/C assets required; missing {', '.join(missing)}.",
            }

        cover = labeled["A"]
        texture = labeled["B"]
        detail = labeled["C"]
        notes = [
            f"cover=A score={score_row(cover)}",
            f"motion_crop=B score={score_row(texture)}",
            f"detail=C score={score_row(detail)}",
        ]
        return {
            "carousel_id": carousel_id,
            "prompt_id": prompt_id,
            "cover_asset": file_name(cover),
            "cover_url": url_for(cover),
            "detail_asset": file_name(detail),
            "detail_url": url_for(detail),
            "texture_asset": file_name(texture),
            "texture_url": url_for(texture),
            "selection_status": "selected",
            "notes": "; ".join(notes),
        }

    cover = candidates[0]
    detail = candidates[1] if len(candidates) > 1 else None
    texture = detail or cover

    notes = []
    notes.append(f"cover_score={score_row(cover)}")
    if detail:
        notes.append(f"detail_score={score_row(detail)}")
    else:
        notes.append("detail_reuses_cover")

    return {
        "carousel_id": carousel_id,
        "prompt_id": prompt_id,
        "cover_asset": file_name(cover),
        "cover_url": url_for(cover),
        "detail_asset": file_name(detail),
        "detail_url": url_for(detail),
        "texture_asset": file_name(texture),
        "texture_url": url_for(texture),
        "selection_status": "selected",
        "notes": "; ".join(notes),
    }


def slot_note(base_note, file_name, url):
    existing_parts = [
        clean(part)
        for part in clean(base_note).split(";")
        if clean(part)
        and not clean(part).startswith("selected_file=")
        and not clean(part).startswith("drive_url=")
    ]
    parts = existing_parts
    if file_name:
        parts.append(f"selected_file={file_name}")
    if url:
        parts.append(f"drive_url={url}")
    return "; ".join(part for part in parts if part)


def update_asset_slots(slot_rows, selections):
    selection_by_carousel = {row["carousel_id"]: row for row in selections}
    updated = []
    for row in slot_rows:
        out = dict(row)
        carousel_id = clean(row.get("carousel_id"))
        slot_id = clean(row.get("slot_id"))
        selection = selection_by_carousel.get(carousel_id)
        if not selection or selection.get("selection_status") != "selected":
            updated.append(out)
            continue

        if slot_id == "cover_image":
            out["recommended_file"] = selection["cover_asset"]
            out["status"] = "selected" if selection["cover_asset"] else "needed"
            out["notes"] = slot_note(row.get("notes"), selection["cover_asset"], selection["cover_url"])
        elif slot_id == "detail_image":
            out["recommended_file"] = selection["detail_asset"] or selection["cover_asset"]
            out["status"] = "selected" if out["recommended_file"] else "optional"
            out["notes"] = slot_note(row.get("notes"), out["recommended_file"], selection["detail_url"] or selection["cover_url"])
        elif slot_id in {"motion_crop", "texture_or_crop"}:
            out["slot_id"] = "motion_crop"
            out["recommended_file"] = selection["texture_asset"]
            out["status"] = "selected_from_crop" if selection["texture_asset"] else "optional"
            out["notes"] = slot_note(row.get("notes"), selection["texture_asset"], selection["texture_url"])
        updated.append(out)
    return updated


def update_placeholder_map(run_dir, slot_rows):
    path = Path(run_dir) / "canva_placeholder_map.json"
    if not path.exists():
        return
    mapping = json.loads(path.read_text(encoding="utf-8"))
    by_carousel = {}
    for row in slot_rows:
        by_carousel.setdefault(clean(row.get("carousel_id")), []).append(row)

    for carousel_id, slots in by_carousel.items():
        if carousel_id in mapping:
            mapping[carousel_id]["asset_slots"] = slots

    path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")


def update_daily_queue(run_dir, selections):
    path = Path(run_dir) / "daily_queue.csv"
    if not path.exists():
        return
    rows, fieldnames = read_csv_with_fields(path)
    if not fieldnames:
        return

    selected_ids = {
        clean(row.get("carousel_id"))
        for row in selections
        if clean(row.get("selection_status")) == "selected"
    }
    if not selected_ids:
        return

    updated = []
    for row in rows:
        out = dict(row)
        if clean(row.get("carousel_id")) in selected_ids:
            out["image_status"] = "asset_selected"
            if clean(out.get("canva_status")) in {"", "not_started"}:
                out["canva_status"] = "ready_for_canva"
            note = clean(out.get("notes"))
            marker = "Asset selected; ready for Canva."
            if marker not in note:
                out["notes"] = "; ".join(part for part in [note, marker] if part)
        updated.append(out)

    write_csv(path, fieldnames, updated)


def write_asset_plan(path, selections, provider="Codex"):
    lines = [
        f"# {provider.title()} Asset Selection Plan",
        "",
        f"Use this after {provider} images are generated, uploaded if needed, and reviewed.",
        "",
    ]
    for row in selections:
        lines.extend(
            [
                f"## {row['carousel_id']} / {row['prompt_id']}",
                "",
                f"- Status: `{row['selection_status']}`",
                f"- Cover: `{row['cover_asset'] or 'needed'}`",
                f"- Cover URL: {row['cover_url'] or 'n/a'}",
                f"- Detail: `{row['detail_asset'] or row['cover_asset'] or 'needed'}`",
                f"- Detail URL: {row['detail_url'] or row['cover_url'] or 'n/a'}",
                f"- Texture / crop: `{row['texture_asset'] or 'optional'}`",
                f"- Notes: {row['notes']}",
                "",
            ]
        )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_review_template(path, packets, provider="Codex"):
    rows = []
    for packet in packets:
        prompt_id = clean(packet.get("prompt_id"))
        for index in range(1, 6):
            row = {field: "" for field in SCORE_FIELDS}
            row["prompt_id"] = prompt_id
            row["tool"] = provider
            row["file_name"] = f"{prompt_id}_{provider.lower()}_variant_{index}.jpg"
            row["publishable"] = "pending"
            row["status"] = "review"
            rows.append(row)
    write_csv(path, SCORE_FIELDS, rows)


def select_assets(run_dir, score_sheet=None, drive_inventory=None, provider="Codex"):
    run_dir = Path(run_dir)
    packets = read_csv(run_dir / "weekly_content_packet.csv")
    slot_rows = read_csv(run_dir / "canva_asset_slots.csv")
    score_rows = read_csv(score_sheet) if score_sheet else []
    drive_rows = drive_lookup(read_csv(drive_inventory)) if drive_inventory else {}
    provider_slug = clean(provider).lower() or "codex"

    if not score_rows:
        write_review_template(run_dir / f"{provider_slug}_asset_review_template.csv", packets, provider=provider)
        selections = [
            {
                "carousel_id": clean(packet.get("carousel_id")),
                "prompt_id": clean(packet.get("prompt_id")),
                "cover_asset": "",
                "cover_url": "",
                "detail_asset": "",
                "detail_url": "",
                "texture_asset": "",
                "texture_url": "",
                "selection_status": "needs_scoring",
                "notes": f"Fill {provider_slug}_asset_review_template.csv after reviewing {provider} outputs.",
            }
            for packet in packets
        ]
    else:
        selections = [build_selection(packet, score_rows, drive_rows) for packet in packets]

    write_csv(run_dir / f"{provider_slug}_asset_selection.csv", SELECTION_FIELDS, selections)
    write_asset_plan(run_dir / "canva_asset_plan.md", selections, provider=provider)
    updated_slots = update_asset_slots(slot_rows, selections)
    write_csv(run_dir / "canva_asset_slots.csv", ASSET_SLOT_FIELDS, updated_slots)
    update_placeholder_map(run_dir, updated_slots)
    update_daily_queue(run_dir, selections)
    return selections


def main():
    parser = argparse.ArgumentParser(description="Select image assets for a generated weekly Canva handoff.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--score-sheet", help="CSV with scored image assets.")
    parser.add_argument("--drive-inventory", help="Optional inventory CSV containing file_name and drive_url or file_path.")
    parser.add_argument("--provider", default="Codex", help="Asset provider label, e.g. Codex or OpenAI.")
    args = parser.parse_args()

    selections = select_assets(
        run_dir=args.run_dir,
        score_sheet=args.score_sheet,
        drive_inventory=args.drive_inventory,
        provider=args.provider,
    )
    selected_count = sum(1 for row in selections if row["selection_status"] == "selected")
    print(f"Wrote asset selections for {len(selections)} carousel(s); selected {selected_count}.")


if __name__ == "__main__":
    main()
