import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path


def clean(value):
    return " ".join(str(value or "").split()).strip()


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


def extract_note_value(notes, key):
    pattern = rf"(?:^|;\s*){re.escape(key)}=([^;]+)"
    match = re.search(pattern, clean(notes))
    return clean(match.group(1)) if match else ""


def latest_carousel_id(run_dir):
    publish_status = read_json(Path(run_dir) / "publish_status.json")
    latest_publish = publish_status.get("latest_publish") or {}
    if clean(latest_publish.get("carousel_id")):
        return clean(latest_publish.get("carousel_id"))

    packets = read_csv(Path(run_dir) / "weekly_content_packet.csv")
    for row in packets:
        if clean(row.get("status")) == "published":
            return clean(row.get("carousel_id"))
    return clean(packets[0].get("carousel_id")) if packets else ""


def packet_for(run_dir, carousel_id):
    for row in read_csv(Path(run_dir) / "weekly_content_packet.csv"):
        if clean(row.get("carousel_id")) == carousel_id:
            return row
    return {}


def assets_for(run_dir, carousel_id):
    rows = [
        row
        for row in read_csv(Path(run_dir) / "canva_asset_slots.csv")
        if clean(row.get("carousel_id")) == carousel_id
    ]
    by_slot = {clean(row.get("slot_id")): row for row in rows}

    def asset(slot_id):
        row = by_slot.get(slot_id, {})
        return {
            "slot_id": slot_id,
            "file": clean(row.get("recommended_file")),
            "drive_url": extract_note_value(row.get("notes"), "drive_url"),
            "notes": clean(row.get("notes")),
        }

    cover = asset("cover_image")
    detail = asset("detail_image")
    return {
        "recommended": cover if cover["file"] else detail,
        "cover": cover,
        "detail": detail,
    }


def outfit_label(packet):
    item = clean(packet.get("clothing_item")).lower()
    palette = clean(packet.get("color_palette")).lower()
    fit = clean(packet.get("fit")).lower()

    if "blazer" in item or "blazer" in fit:
        if "cream" in palette or "off-white" in palette:
            return "奶油白西裝套裝"
        if "beige" in palette or "sand" in palette:
            return "沙色西裝套裝"
        return "淺色西裝套裝"
    if "vest" in item:
        return "針織背心穿搭"
    if "trouser" in item or "pants" in item:
        return "寬褲穿搭"
    return "這套通勤穿搭"


def audience_line(packet):
    audience = clean(packet.get("audience"))
    occasion = clean(packet.get("occasion")) or "日常"
    bucket = clean(packet.get("content_bucket"))
    if "通勤" in audience or "通勤" in occasion or "office" in bucket:
        return "我想測試「輕正式通勤」方向：有整理過，但不會像面試套裝。"
    return f"我想測試「{occasion}」方向：看起來有整理過，但不會太用力。"


def caption(packet):
    label = outfit_label(packet)
    return "\n".join(
        [
            f"上班不想太正式，{label}可以嗎？",
            "",
            f"這套是 AI 虛擬穿搭示意，{audience_line(packet)}",
            "",
            f"你會穿這種{label}出門嗎？",
            "留言 1 = 會",
            "留言 2 = 不會",
            "",
            "AI 虛擬穿搭示意，非真人試穿。",
        ]
    )


def first_comment():
    return "\n".join(
        [
            "想看同風格清單可以留言「通勤套裝」，我會整理平價 / 質感 / 替代款。",
            "AI 虛擬穿搭示意，非真人試穿。",
        ]
    )


def hashtags():
    return "#通勤穿搭 #上班穿搭 #女生穿搭 #西裝外套 #寬褲穿搭 #小資穿搭 #AI穿搭 #虛擬穿搭 #穿搭靈感 #每日穿搭"


def threads_copy(packet):
    label = outfit_label(packet)
    return "\n".join(
        [
            f"上班不想太正式，{label}可以嗎？",
            "",
            "我在測 AI 虛擬穿搭帳號的通勤風格方向。你會穿這種搭配出門嗎？留言 1=會，2=不會。",
            "",
            "AI 虛擬穿搭示意，非真人試穿。",
        ]
    )


def metrics_command(run_dir, week_id, carousel_id):
    return "\n".join(
        [
            "powershell -ExecutionPolicy Bypass -File 10_automation\\mika_weekly.ps1 `",
            "  -Action metrics `",
            f"  -RunDir {run_dir} `",
            f"  -Week {week_id} `",
            f"  -CarouselId {carousel_id}-visibility-01 `",
            "  -PostUrl \"POST_URL\" `",
            "  -PublishedAt \"YYYY/MM/DD HH:mm\" `",
            "  -RecordMetrics `",
            "  -MeasuredAt YYYY-MM-DD `",
            "  -HoursAfterPublish 24 `",
            "  -Reach 0 `",
            "  -Likes 0 `",
            "  -Saves 0 `",
            "  -Comments 0 `",
            "  -Shares 0",
        ]
    )


def render_markdown(package):
    asset = package["asset"]
    packet = package["source_packet"]
    lines = [
        "# Visibility Test Package",
        "",
        f"Created: `{package['created_at']}`",
        f"Run folder: `{package['run_dir']}`",
        f"Source carousel: `{package['source_carousel_id']}`",
        f"Prompt ID: `{packet.get('prompt_id', '')}`",
        "",
        "## Purpose",
        "",
        "Use one simple post to test whether Instagram can distribute this account at all. Do not use a panorama carousel for this test.",
        "",
        "## Image",
        "",
        f"- Recommended file: `{asset.get('file') or 'needed'}`",
        f"- Drive URL: {asset.get('drive_url') or 'n/a'}",
        "",
        "## Instagram Caption",
        "",
        "```text",
        package["instagram_caption"],
        "```",
        "",
        "## Hashtags",
        "",
        "```text",
        package["hashtags"],
        "```",
        "",
        "## First Comment",
        "",
        "```text",
        package["first_comment"],
        "```",
        "",
        "## Threads Backup",
        "",
        "```text",
        package["threads_copy"],
        "```",
        "",
        "## Publish Checklist",
        "",
        "1. Confirm Instagram account is public and Account Status has no restriction.",
        "2. Publish this as one single-image post.",
        "3. Add the first comment immediately.",
        "4. Share once to Story.",
        "5. Send to 3-5 trusted people for a clean visibility check.",
        "6. Record metrics after 6 hours and 24 hours.",
        "",
        "## Metrics Command Template",
        "",
        "Replace `POST_URL`, `YYYY/MM/DD HH:mm`, `YYYY-MM-DD`, and metric numbers.",
        "",
        "```powershell",
        package["metrics_command"],
        "```",
        "",
        "## Pass / Fail",
        "",
        "- Pass: `reach >= 20`",
        "- Strong pass: `reach >= 100`, `saves >= 1`, or `comments >= 1`",
        "- Fail: `reach = 0` after account audit, Story share, and trusted-person seed traffic",
        "",
    ]
    return "\n".join(lines)


def build_visibility_test(run_dir, output_md=None, output_json=None, carousel_id=None):
    run_dir = Path(run_dir)
    carousel_id = carousel_id or latest_carousel_id(run_dir)
    packet = packet_for(run_dir, carousel_id)
    assets = assets_for(run_dir, carousel_id)
    asset = assets["recommended"]
    week_id = clean(packet.get("week_id")) or run_dir.name

    package = {
        "created_at": date.today().isoformat(),
        "run_dir": str(run_dir),
        "source_carousel_id": carousel_id,
        "source_packet": packet,
        "asset": asset,
        "fallback_asset": assets["detail"],
        "instagram_caption": caption(packet),
        "hashtags": hashtags(),
        "first_comment": first_comment(),
        "threads_copy": threads_copy(packet),
        "metrics_command": metrics_command(str(run_dir), week_id, carousel_id),
    }

    output_md = Path(output_md) if output_md else run_dir / "visibility_test_package.md"
    output_json = Path(output_json) if output_json else run_dir / "visibility_test_package.json"
    output_md.write_text(render_markdown(package), encoding="utf-8")
    output_json.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
    return package, output_md, output_json


def main():
    parser = argparse.ArgumentParser(description="Create a simple single-image visibility test package from a weekly run folder.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--carousel-id", default="")
    parser.add_argument("--output-md", default="")
    parser.add_argument("--output-json", default="")
    args = parser.parse_args()

    package, output_md, output_json = build_visibility_test(
        run_dir=args.run_dir,
        output_md=args.output_md or None,
        output_json=args.output_json or None,
        carousel_id=args.carousel_id or None,
    )
    print(f"Visibility test source: {package['source_carousel_id']}")
    print(f"Recommended asset: {package['asset'].get('file') or 'needed'}")
    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")


if __name__ == "__main__":
    main()
