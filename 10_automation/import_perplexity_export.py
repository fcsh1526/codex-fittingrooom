import argparse
import csv
import io
import re
import sys
import urllib.request
from pathlib import Path


DATABASE_FIELDS = [
    "id",
    "week",
    "trend_name",
    "audience",
    "occasion",
    "clothing_item",
    "color_palette",
    "fabric",
    "fit",
    "styling_rules",
    "model_identity",
    "pose",
    "background",
    "camera_style",
    "negative_prompt",
    "shopping_keywords",
    "affiliate_links",
    "status",
    "notes",
]


EXTRA_NOTE_FIELDS = [
    "trend_origin",
    "platform_priority",
    "cta",
    "global_context",
    "why_now",
    "taiwan_localization",
    "content_angle",
    "content_angles",
    "score",
]


DEFAULT_NEGATIVE_PROMPT = (
    "AI virtual outfit only; no real person; no celebrity; "
    "no childlike appearance; no nudity; no logo."
)


def clean(value):
    return " ".join((value or "").replace("\ufeff", "").split()).strip()


def read_source(source):
    if re.match(r"^https?://", source):
        request = urllib.request.Request(source, headers={"User-Agent": "MikaLinPipeline/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
        return raw.decode("utf-8-sig", errors="replace")
    return Path(source).read_text(encoding="utf-8-sig")


def extract_csv_text(text):
    stripped = text.strip()
    if stripped.startswith("id,") or stripped.startswith("week,"):
        return stripped

    fence_pattern = re.compile(r"```(?:csv|text)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)
    for match in fence_pattern.finditer(text):
        candidate = match.group(1).strip()
        first_line = candidate.splitlines()[0].strip() if candidate.splitlines() else ""
        if first_line.startswith("id,") or first_line.startswith("week,"):
            return candidate

    lines = text.splitlines()
    for index, line in enumerate(lines):
        normalized = line.strip()
        if normalized.startswith("id,") and "clothing_item" in normalized:
            collected = []
            for item in lines[index:]:
                if item.strip().startswith("```"):
                    break
                if item.strip():
                    collected.append(item)
            if collected:
                return "\n".join(collected).strip()

    raise ValueError("No CSV export found. Expected a CSV file or a markdown fenced CSV block.")


def read_csv_rows(csv_text):
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = []
    for row in reader:
        if any(clean(value) for value in row.values()):
            rows.append({clean(key): clean(value) for key, value in row.items() if key})
    return rows


def load_database(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_database(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=DATABASE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def note_value(row):
    existing = clean(row.get("notes"))
    extras = []
    if existing:
        extras.append(existing)
    for key in EXTRA_NOTE_FIELDS:
        value = clean(row.get(key))
        if value:
            extras.append(f"{key}={value}")
    return "; ".join(extras)


def normalize_row(row, week, index):
    row_week = clean(row.get("week")) or week
    row_id = clean(row.get("id")) or f"{row_week}-P{index:03d}"
    return {
        "id": row_id,
        "week": row_week,
        "trend_name": clean(row.get("trend_name")),
        "audience": clean(row.get("audience")),
        "occasion": clean(row.get("occasion")),
        "clothing_item": clean(row.get("clothing_item")),
        "color_palette": clean(row.get("color_palette")),
        "fabric": clean(row.get("fabric")),
        "fit": clean(row.get("fit")),
        "styling_rules": clean(row.get("styling_rules")),
        "model_identity": clean(row.get("model_identity")) or "Mika Lin",
        "pose": clean(row.get("pose")),
        "background": clean(row.get("background")),
        "camera_style": clean(row.get("camera_style")),
        "negative_prompt": clean(row.get("negative_prompt")) or DEFAULT_NEGATIVE_PROMPT,
        "shopping_keywords": clean(row.get("shopping_keywords")),
        "affiliate_links": clean(row.get("affiliate_links")),
        "status": clean(row.get("status")) or "draft",
        "notes": note_value(row),
    }


def import_rows(source, database_path, week, dry_run=False):
    text = read_source(source)
    csv_text = extract_csv_text(text)
    source_rows = read_csv_rows(csv_text)
    normalized = [
        normalize_row(row, week=week, index=index)
        for index, row in enumerate(source_rows, start=1)
        if clean(row.get("trend_name")) and clean(row.get("clothing_item"))
    ]
    if not normalized:
        raise ValueError("CSV was found, but no usable prompt rows had trend_name and clothing_item.")

    existing = load_database(database_path)
    replacement_keys = {(row["week"], row["id"]) for row in normalized}
    kept = [row for row in existing if (clean(row.get("week")), clean(row.get("id"))) not in replacement_keys]
    merged = kept + normalized

    if not dry_run:
        write_database(database_path, merged)

    return {
        "source_rows": len(source_rows),
        "imported_rows": len(normalized),
        "kept_rows": len(kept),
        "total_rows": len(merged),
        "week": week,
    }


def main():
    parser = argparse.ArgumentParser(description="Import Perplexity weekly CSV export into item_prompt_database.csv.")
    parser.add_argument("--source", required=True, help="CSV/Markdown file path or direct CSV URL.")
    parser.add_argument("--week", required=True, help="Week id, e.g. 2026-W25.")
    parser.add_argument("--database", default="04_prompts/item_prompt_database.csv")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        result = import_rows(
            source=args.source,
            database_path=args.database,
            week=args.week,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"Import failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    action = "Would import" if args.dry_run else "Imported"
    print(
        f"{action} {result['imported_rows']} row(s) for {result['week']} "
        f"from {result['source_rows']} source row(s). Database total: {result['total_rows']}."
    )


if __name__ == "__main__":
    main()
