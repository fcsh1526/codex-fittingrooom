import argparse
import csv
import json
from datetime import date
from pathlib import Path


PUBLISH_FIELDS = [
    "record_date",
    "week_id",
    "carousel_id",
    "platform",
    "format",
    "post_url",
    "published_at",
    "content_bucket",
    "prompt_id",
    "run_dir",
    "drive_folder_url",
    "canva_design_url",
    "product_links_used",
    "cta",
    "status",
    "notes",
]


METRIC_FIELDS = [
    "record_date",
    "week_id",
    "carousel_id",
    "platform",
    "post_url",
    "measured_at",
    "hours_after_publish",
    "reach",
    "likes",
    "saves",
    "comments",
    "shares",
    "profile_visits",
    "new_followers",
    "cta_comments",
    "link_clicks",
    "decision",
    "interpretation",
    "next_action",
]


def clean(value):
    return " ".join((value or "").split()).strip()


def today():
    return date.today().isoformat()


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


def upsert(rows, row, key_fields):
    key = tuple(clean(row.get(field)) for field in key_fields)
    out = []
    replaced = False
    for existing in rows:
        existing_key = tuple(clean(existing.get(field)) for field in key_fields)
        if existing_key == key:
            merged = dict(existing)
            merged.update({k: v for k, v in row.items() if v != ""})
            out.append(merged)
            replaced = True
        else:
            out.append(existing)
    if not replaced:
        out.append(row)
    return out


def number(value):
    try:
        return int(clean(str(value)))
    except ValueError:
        return 0


def load_packet(run_dir, carousel_id):
    if not run_dir or not carousel_id:
        return {}
    path = Path(run_dir) / "weekly_content_packet.csv"
    for row in read_csv(path):
        if clean(row.get("carousel_id")) == carousel_id:
            return row
    return {}


def update_packet_post_url(run_dir, carousel_id, post_url):
    if not run_dir or not carousel_id or not post_url:
        return
    path = Path(run_dir) / "weekly_content_packet.csv"
    rows = read_csv(path)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    changed = False
    for row in rows:
        if clean(row.get("carousel_id")) == carousel_id:
            row["ig_post_url"] = post_url
            row["status"] = "published"
            row["next_action"] = "Record 6h and 24h metrics"
            changed = True
    if changed:
        write_csv(path, fieldnames, rows)


def decision_from_metrics(metrics):
    reach = number(metrics.get("reach"))
    saves = number(metrics.get("saves"))
    comments = number(metrics.get("comments"))
    shares = number(metrics.get("shares"))
    profile_visits = number(metrics.get("profile_visits"))
    link_clicks = number(metrics.get("link_clicks"))
    hours = number(metrics.get("hours_after_publish"))

    if reach == 0:
        return {
            "decision": "visibility_recovery",
            "interpretation": "Reach is zero, so this is a visibility or distribution signal, not a reason to stop carousel production.",
            "next_action": "Keep carousel production moving; optionally run a single-image visibility test and mirror to one backup channel.",
        }
    if reach < 20 and hours >= 24:
        return {
            "decision": "weak_distribution",
            "interpretation": "Reach is non-zero but still too low to judge the carousel concept.",
            "next_action": "Keep the post as a portfolio piece, test a clearer single-image hook, and mirror the asset to Threads or Pinterest.",
        }
    if reach < 20:
        return {
            "decision": "wait_for_24h",
            "interpretation": "Early reach is low but the checkpoint is not mature yet.",
            "next_action": "Wait until the 24h checkpoint, share once to Story, and avoid changing the concept too early.",
        }
    if saves > 0 or comments > 0 or shares > 0:
        return {
            "decision": "repeat_bucket",
            "interpretation": "The content generated an explicit value signal.",
            "next_action": "Create a second carousel in the same content bucket and prepare a simple product-list reply flow.",
        }
    if profile_visits > 0 or link_clicks > 0:
        return {
            "decision": "profile_interest",
            "interpretation": "The post created curiosity but not enough save/comment intent.",
            "next_action": "Improve the slide 1 hook and make the CTA more specific before testing commerce links.",
        }
    return {
        "decision": "hook_or_save_gap",
        "interpretation": "Reach exists, but there is no save/comment signal yet.",
        "next_action": "Revise the cover headline, make the outfit benefit more concrete, and test one more carousel in the same bucket.",
    }


def infer_week_from_run_dir(run_dir):
    if not run_dir:
        return ""
    return Path(run_dir).name


def publish_row(args, packet):
    carousel_id = clean(args.carousel_id)
    return {
        "record_date": args.record_date,
        "week_id": clean(args.week) or infer_week_from_run_dir(args.run_dir),
        "carousel_id": carousel_id,
        "platform": args.platform,
        "format": args.format,
        "post_url": clean(args.post_url),
        "published_at": clean(args.published_at),
        "content_bucket": clean(args.content_bucket) or clean(packet.get("content_bucket")),
        "prompt_id": clean(args.prompt_id) or clean(packet.get("prompt_id")),
        "run_dir": clean(args.run_dir),
        "drive_folder_url": clean(args.drive_folder_url),
        "canva_design_url": clean(args.canva_design_url),
        "product_links_used": args.product_links_used,
        "cta": clean(args.cta),
        "status": args.status,
        "notes": clean(args.notes),
    }


def metric_row(args, packet):
    base = {
        "record_date": args.record_date,
        "week_id": clean(args.week) or infer_week_from_run_dir(args.run_dir),
        "carousel_id": clean(args.carousel_id),
        "platform": args.platform,
        "post_url": clean(args.post_url),
        "measured_at": clean(args.measured_at),
        "hours_after_publish": str(args.hours_after_publish),
        "reach": str(args.reach),
        "likes": str(args.likes),
        "saves": str(args.saves),
        "comments": str(args.comments),
        "shares": str(args.shares),
        "profile_visits": str(args.profile_visits),
        "new_followers": str(args.new_followers),
        "cta_comments": str(args.cta_comments),
        "link_clicks": str(args.link_clicks),
        "decision": "",
        "interpretation": "",
        "next_action": "",
    }
    decision = decision_from_metrics(base)
    base.update(decision)
    return base


def write_run_reports(run_dir, publish_rows, metric_rows):
    if not run_dir:
        return
    run_dir = Path(run_dir)
    write_csv(run_dir / "publish_log.csv", PUBLISH_FIELDS, publish_rows)
    write_csv(run_dir / "metric_checkpoints.csv", METRIC_FIELDS, metric_rows)

    latest_publish = publish_rows[-1] if publish_rows else {}
    latest_metric = metric_rows[-1] if metric_rows else {}
    lines = [
        "# Publish Status",
        "",
        f"Post URL: {latest_publish.get('post_url') or latest_metric.get('post_url') or 'n/a'}",
        f"Platform: `{latest_publish.get('platform') or latest_metric.get('platform') or 'n/a'}`",
        f"Carousel ID: `{latest_publish.get('carousel_id') or latest_metric.get('carousel_id') or 'n/a'}`",
        "",
    ]
    if latest_metric:
        lines.extend(
            [
                "## Latest Metrics",
                "",
                f"- Measured at: `{latest_metric.get('measured_at')}`",
                f"- Hours after publish: `{latest_metric.get('hours_after_publish')}`",
                f"- Reach: `{latest_metric.get('reach')}`",
                f"- Likes: `{latest_metric.get('likes')}`",
                f"- Saves: `{latest_metric.get('saves')}`",
                f"- Comments: `{latest_metric.get('comments')}`",
                f"- Shares: `{latest_metric.get('shares')}`",
                "",
                "## Decision",
                "",
                f"- Decision: `{latest_metric.get('decision')}`",
                f"- Interpretation: {latest_metric.get('interpretation')}",
                f"- Next action: {latest_metric.get('next_action')}",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Next Checkpoints",
                "",
                "- Record 6h metrics.",
                "- Record 24h metrics.",
                "",
            ]
        )
    (run_dir / "publish_status.md").write_text("\n".join(lines), encoding="utf-8")

    status_json = {
        "latest_publish": latest_publish,
        "latest_metric": latest_metric,
    }
    (run_dir / "publish_status.json").write_text(
        json.dumps(status_json, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description="Record publish events and metrics for Mika Lin weekly carousel runs.")
    parser.add_argument("--run-dir")
    parser.add_argument("--week", default="")
    parser.add_argument("--carousel-id", default="")
    parser.add_argument("--platform", default="Instagram")
    parser.add_argument("--format", default="Carousel")
    parser.add_argument("--post-url", required=True)
    parser.add_argument("--published-at", default="")
    parser.add_argument("--record-date", default=today())
    parser.add_argument("--content-bucket", default="")
    parser.add_argument("--prompt-id", default="")
    parser.add_argument("--drive-folder-url", default="")
    parser.add_argument("--canva-design-url", default="")
    parser.add_argument("--product-links-used", default="no")
    parser.add_argument("--cta", default="")
    parser.add_argument("--status", default="published")
    parser.add_argument("--notes", default="")
    parser.add_argument("--global-dir", default="07_metrics")

    parser.add_argument("--record-metrics", action="store_true")
    parser.add_argument("--measured-at", default=today())
    parser.add_argument("--hours-after-publish", type=int, default=24)
    parser.add_argument("--reach", type=int, default=0)
    parser.add_argument("--likes", type=int, default=0)
    parser.add_argument("--saves", type=int, default=0)
    parser.add_argument("--comments", type=int, default=0)
    parser.add_argument("--shares", type=int, default=0)
    parser.add_argument("--profile-visits", type=int, default=0)
    parser.add_argument("--new-followers", type=int, default=0)
    parser.add_argument("--cta-comments", type=int, default=0)
    parser.add_argument("--link-clicks", type=int, default=0)
    args = parser.parse_args()

    packet = load_packet(args.run_dir, args.carousel_id)
    global_dir = Path(args.global_dir)

    publish = publish_row(args, packet)
    publish_path = global_dir / "publish_registry.csv"
    publish_rows = upsert(read_csv(publish_path), publish, ["platform", "post_url"])
    write_csv(publish_path, PUBLISH_FIELDS, publish_rows)

    run_publish_rows = []
    if args.run_dir:
        run_publish_rows = upsert(
            read_csv(Path(args.run_dir) / "publish_log.csv"),
            publish,
            ["platform", "post_url"],
        )

    metric_rows = []
    run_metric_rows = read_csv(Path(args.run_dir) / "metric_checkpoints.csv") if args.run_dir else []
    if args.record_metrics:
        metric = metric_row(args, packet)
        metrics_path = global_dir / "metric_checkpoints.csv"
        metric_rows = upsert(
            read_csv(metrics_path),
            metric,
            ["platform", "post_url", "measured_at", "hours_after_publish"],
        )
        write_csv(metrics_path, METRIC_FIELDS, metric_rows)
        if args.run_dir:
            run_metric_rows = upsert(
                read_csv(Path(args.run_dir) / "metric_checkpoints.csv"),
                metric,
                ["platform", "post_url", "measured_at", "hours_after_publish"],
            )

    if args.run_dir:
        write_run_reports(args.run_dir, run_publish_rows, run_metric_rows)
        update_packet_post_url(args.run_dir, args.carousel_id, args.post_url)

    print(f"Recorded publish event: {args.platform} {args.post_url}")
    if args.record_metrics:
        decision = decision_from_metrics(metric_row(args, packet))
        print(f"Decision: {decision['decision']}")
        print(f"Next action: {decision['next_action']}")


if __name__ == "__main__":
    main()
