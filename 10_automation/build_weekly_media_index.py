import argparse
import csv
import hashlib
import json
import re
import struct
from datetime import date
from pathlib import Path
from urllib.parse import quote


APPROVED_STATUSES = {
    "accepted_reel_a",
    "accepted_session_lock",
    "approved",
    "canva_frame_approved",
    "exact_frame_approved",
    "user_approved",
}


def clean(value):
    return " ".join(str(value or "").split()).strip()


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def png_dimensions(path):
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"Expected PNG source: {path}")
    return struct.unpack(">II", header[16:24])


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_relative(path, project_root):
    return path.resolve().relative_to(project_root.resolve()).as_posix()


def github_urls(relative_path, repository, branch):
    encoded = quote(relative_path, safe="/")
    return {
        "raw_url": f"https://raw.githubusercontent.com/{repository}/{branch}/{encoded}",
        "github_url": f"https://github.com/{repository}/blob/{branch}/{encoded}",
    }


def approved_rows(review_path):
    rows = []
    for row in read_csv(review_path):
        status = clean(row.get("status")).lower()
        publishable = clean(row.get("publishable")).lower()
        if publishable == "yes" and status in APPROVED_STATUSES:
            rows.append(row)
    return rows


def reel_source(look_dir, project_root, repository, branch):
    review_path = look_dir / "reel" / "review_sheet.csv"
    rows = approved_rows(review_path)
    if len(rows) != 1:
        raise ValueError(f"Expected exactly one approved Reel source in {review_path}; found {len(rows)}")
    row = rows[0]
    path = review_path.parent / clean(row.get("candidate_file"))
    if not path.exists():
        raise FileNotFoundError(path)
    width, height = png_dimensions(path)
    ratio = width / height
    if abs(ratio - (9 / 16)) > 0.01:
        raise ValueError(f"Reel source is not native 9:16: {path} ({width}x{height})")
    relative = repo_relative(path, project_root)
    return {
        "status": "approved_native_9x16",
        "review_status": clean(row.get("status")),
        "source_path": relative,
        **github_urls(relative, repository, branch),
        "width": width,
        "height": height,
        "aspect_ratio": "9:16",
        "sha256": sha256(path),
    }


def carousel_sources(look_dir, project_root, repository, branch):
    review_path = look_dir / "carousel" / "review_sheet.csv"
    rows = approved_rows(review_path)
    by_role = {}
    for row in rows:
        filename = clean(row.get("candidate_file"))
        match = re.search(r"_carousel_candidate_([ABC])(?:_|\.)", filename)
        if not match:
            raise ValueError(f"Cannot determine Carousel role from {filename}")
        role = match.group(1)
        if role in by_role:
            raise ValueError(f"Multiple approved Carousel {role} rows in {review_path}")
        path = review_path.parent / filename
        if not path.exists():
            raise FileNotFoundError(path)
        relative = repo_relative(path, project_root)
        width, height = png_dimensions(path)
        by_role[role] = {
            "source_path": relative,
            **github_urls(relative, repository, branch),
            "width": width,
            "height": height,
            "review_status": clean(row.get("status")),
            "sha256": sha256(path),
        }
    missing = [role for role in "ABC" if role not in by_role]
    if missing:
        raise ValueError(f"Missing approved Carousel roles {missing} in {review_path}")
    return {"status": "approved_abc", "assets": by_role}


def canva_status(look_dir):
    record_path = look_dir / "carousel" / "canva_ready" / "canva_commit_record.json"
    if not record_path.exists():
        return {"status": "not_committed"}
    record = read_json(record_path)
    committed = clean(record.get("transaction_status")).lower() == "committed"
    return {
        "status": "committed_exact_frame" if committed else "not_committed",
        "design_id": clean(record.get("canva_design_id")),
        "title": clean(record.get("canva_title")),
        "display_copy": str(record.get("canva_display_copy") or ""),
        "edit_url": clean(record.get("canva_edit_url")),
        "view_url": clean(record.get("canva_view_url")),
        "transaction_id": clean(record.get("transaction_id")),
        "committed_at": clean(record.get("committed_at")),
    }


def build_indexes(run_dir, project_root, repository, branch, updated_at):
    look_plan_path = run_dir / "weekly_look_plan.csv"
    looks = read_csv(look_plan_path)
    if not looks:
        raise ValueError(f"No looks found in {look_plan_path}")
    week_ids = {clean(row.get("week_id")) for row in looks}
    if len(week_ids) != 1:
        raise ValueError(f"Expected one week id in {look_plan_path}: {sorted(week_ids)}")
    week_id = next(iter(week_ids))

    indexed_looks = []
    for row in sorted(looks, key=lambda item: (clean(item.get("carousel_id")), int(item.get("look_order") or 0))):
        carousel_id = clean(row.get("carousel_id"))
        look_id = clean(row.get("look_id"))
        look_order = int(row.get("look_order") or 0)
        look_dir = run_dir / "generated_images" / carousel_id / "looks" / look_id
        reel = reel_source(look_dir, project_root, repository, branch)
        carousel = carousel_sources(look_dir, project_root, repository, branch)
        canva = canva_status(look_dir)
        ready = (
            reel["status"] == "approved_native_9x16"
            and carousel["status"] == "approved_abc"
            and canva["status"] == "committed_exact_frame"
        )
        indexed_looks.append(
            {
                "look_id": look_id,
                "carousel_id": carousel_id,
                "theme_name": clean(row.get("theme_name")),
                "look_order": look_order,
                "look_name": clean(row.get("look_name")),
                "model_profile_id": clean(row.get("model_profile_id")),
                "dressing_decision": clean(row.get("dressing_decision")),
                "occasion": clean(row.get("occasion")),
                "scene": clean(row.get("scene")),
                "visible_action": clean(row.get("visible_action")),
                "status": "ready_for_manual_export" if ready else "incomplete",
                "reel_group": f"L{look_order:02d}",
                "reel": reel,
                "carousel": carousel,
                "canva": canva,
            }
        )

    theme_count = len({look["carousel_id"] for look in indexed_looks})
    ready_count = sum(look["status"] == "ready_for_manual_export" for look in indexed_looks)
    reels = []
    for look_order in (1, 2):
        sources = []
        group = [look for look in indexed_looks if look["look_order"] == look_order]
        for sequence, look in enumerate(group, start=1):
            reel = look["reel"]
            sources.append(
                {
                    "sequence": sequence,
                    "look_id": look["look_id"],
                    "carousel_id": look["carousel_id"],
                    "theme_name": look["theme_name"],
                    "look_name": look["look_name"],
                    "occasion": look["occasion"],
                    "scene": look["scene"],
                    "visible_action": look["visible_action"],
                    "source_path": reel["source_path"],
                    "raw_url": reel["raw_url"],
                    "github_url": reel["github_url"],
                    "width": reel["width"],
                    "height": reel["height"],
                    "aspect_ratio": reel["aspect_ratio"],
                    "sha256": reel["sha256"],
                }
            )
        reels.append(
            {
                "reel_id": f"{week_id}-REEL-{look_order:02d}",
                "group": f"L{look_order:02d}",
                "group_rule": f"look_order={look_order} across all five themes",
                "status": "ready_for_grok" if len(sources) == theme_count else "incomplete",
                "source_count": len(sources),
                "sources": sources,
            }
        )

    overall_ready = ready_count == len(indexed_looks) and all(reel["status"] == "ready_for_grok" for reel in reels)
    weekly = {
        "schema_version": "1.0",
        "week_id": week_id,
        "updated_at": updated_at,
        "repository": repository,
        "branch": branch,
        "status": "ready_for_reel_assembly_and_manual_export" if overall_ready else "incomplete",
        "progress": {
            "themes_total": theme_count,
            "looks_total": len(indexed_looks),
            "looks_ready_for_manual_export": ready_count,
            "reel_sources_approved": sum(look["reel"]["status"] == "approved_native_9x16" for look in indexed_looks),
            "carousel_sets_approved": sum(look["carousel"]["status"] == "approved_abc" for look in indexed_looks),
            "canva_designs_committed": sum(look["canva"]["status"] == "committed_exact_frame" for look in indexed_looks),
            "reels_ready_for_grok": sum(reel["status"] == "ready_for_grok" for reel in reels),
        },
        "source_of_truth": {
            "look_plan": repo_relative(look_plan_path, project_root),
            "reel_manifest": repo_relative(run_dir / "reel_asset_manifest.json", project_root),
            "rule": "Use the approved source_path or raw_url from reel_asset_manifest.json; never infer a Reel source from filenames.",
        },
        "looks": indexed_looks,
    }
    reel_manifest = {
        "schema_version": "1.0",
        "week_id": week_id,
        "updated_at": updated_at,
        "repository": repository,
        "branch": branch,
        "status": "ready_for_grok" if all(reel["status"] == "ready_for_grok" for reel in reels) else "incomplete",
        "usage": {
            "download": "Fetch raw_url at full resolution or clone the repository and read source_path.",
            "ordering": "Keep sources in ascending sequence order.",
            "motion_rule": "Use subtle believable movement based on visible_action. Preserve identity, outfit, body proportions, accessories, scene and camera perspective; do not redesign the still.",
            "do_not_use": "Do not use Carousel images, Canva-ready crops, Canva preview PNGs, rejected drafts, or unlisted Reel candidates.",
        },
        "reels": reels,
    }
    return weekly, reel_manifest


def write_json(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync_look_plan_status(path, weekly_index):
    rows = read_csv(path)
    by_look = {look["look_id"]: look for look in weekly_index["looks"]}
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            look = by_look.get(clean(row.get("look_id")))
            if look:
                row["status"] = look["status"]
                row["next_action"] = (
                    "Use reel_asset_manifest.json for Grok; open committed Canva design "
                    f"{look['canva'].get('design_id', '')} for manual slicing/export"
                )
            writer.writerow(row)


def weekly_markdown(index):
    progress = index["progress"]
    lines = [
        f"# {index['week_id']} Weekly Media Index",
        "",
        f"- Status: `{index['status']}`",
        f"- Progress: `{progress['looks_ready_for_manual_export']}/{progress['looks_total']}` looks ready",
        f"- Reel sources: `{progress['reel_sources_approved']}/{progress['looks_total']}` approved native 9:16",
        f"- Carousel sets: `{progress['carousel_sets_approved']}/{progress['looks_total']}` approved A/B/C",
        f"- Canva designs: `{progress['canva_designs_committed']}/{progress['looks_total']}` committed",
        f"- Reel packages: `{progress['reels_ready_for_grok']}/2` ready for Grok",
        "",
        "| Look | Theme | Reel | Carousel | Canva | Overall | Reel group |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for look in index["looks"]:
        lines.append(
            f"| `{look['look_id']}` | {look['theme_name']} | `{look['reel']['status']}` | "
            f"`{look['carousel']['status']}` | `{look['canva']['status']}` | `{look['status']}` | `{look['reel_group']}` |"
        )
    lines.extend(
        [
            "",
            "Machine consumers must use `reel_asset_manifest.json` for Reel source selection and ordering.",
            "",
        ]
    )
    return "\n".join(lines)


def reel_markdown(manifest):
    lines = [
        f"# {manifest['week_id']} Reel Asset Manifest",
        "",
        f"Status: `{manifest['status']}`",
        "",
        "Use only the files listed below, in sequence order. These are the approved native 9:16 Reel sources.",
        "",
    ]
    for reel in manifest["reels"]:
        lines.extend([f"## {reel['reel_id']} — {reel['group']}", ""])
        for source in reel["sources"]:
            lines.append(
                f"{source['sequence']}. `{source['look_id']}` — `{source['source_path']}` — "
                f"[raw]({source['raw_url']})"
            )
        lines.append("")
    lines.append("Do not substitute Carousel, Canva-ready, preview, rejected, or unlisted candidate files.")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Build look-level weekly media and Reel source indexes.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--repository", default="fcsh1526/codex-fittingrooom")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--updated-at", default=date.today().isoformat())
    parser.add_argument(
        "--sync-look-plan-status",
        action="store_true",
        help="Update weekly_look_plan.csv status and next_action from verified media evidence.",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    run_dir = Path(args.run_dir).resolve()
    weekly, reel_manifest = build_indexes(
        run_dir=run_dir,
        project_root=project_root,
        repository=args.repository,
        branch=args.branch,
        updated_at=args.updated_at,
    )
    write_json(run_dir / "weekly_media_index.json", weekly)
    write_json(run_dir / "reel_asset_manifest.json", reel_manifest)
    (run_dir / "weekly_media_index.md").write_text(weekly_markdown(weekly), encoding="utf-8")
    (run_dir / "reel_asset_manifest.md").write_text(reel_markdown(reel_manifest), encoding="utf-8")
    if args.sync_look_plan_status:
        sync_look_plan_status(run_dir / "weekly_look_plan.csv", weekly)
    print(run_dir / "weekly_media_index.json")
    print(run_dir / "reel_asset_manifest.json")


if __name__ == "__main__":
    main()
