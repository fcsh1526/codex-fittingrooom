import argparse
import csv
import subprocess
import sys
from pathlib import Path

from build_weekly_packet import main as build_main
from build_weekly_look_plan import build_look_plan
from check_weekly_status import check_status
from import_perplexity_export import import_rows
from resolve_perplexity_source import DEFAULT_INDEX_URL, resolve_source
from select_codex_assets import select_assets
from validate_weekly_run import validate_run
from prepare_reel_production import build as build_reel_production


def run_build_weekly_packet(week, limit, output_dir, source_database):
    original_argv = sys.argv[:]
    try:
        sys.argv = [
            "build_weekly_packet.py",
            "--source",
            source_database,
            "--week",
            week,
            "--limit",
            str(limit),
            "--output-dir",
            output_dir,
        ]
        build_main()
    finally:
        sys.argv = original_argv


def read_packets(run_dir):
    path = Path(run_dir) / "weekly_content_packet.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_look_plan(run_dir):
    path = Path(run_dir) / "weekly_look_plan.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def clean(value):
    return " ".join(str(value or "").split()).strip()


def prepare_codex_image_jobs(run_dir, provider):
    script = Path("11_skills") / "mira-image-daily" / "scripts" / "prepare_daily_image_job.py"
    if not script.exists():
        raise FileNotFoundError(f"Missing image job script: {script}")

    prepared = []
    looks = read_look_plan(run_dir)
    if looks:
        for look in looks:
            look_id = clean(look.get("look_id"))
            if not look_id:
                continue
            subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--project-root",
                    ".",
                    "--run-dir",
                    str(run_dir),
                    "--look-id",
                    look_id,
                    "--tool",
                    provider,
                    "--plan-only",
                ],
                check=True,
            )
            prepared.append(look_id)
        return prepared

    for packet in read_packets(run_dir):
        carousel_id = clean(packet.get("carousel_id"))
        if not carousel_id:
            continue
        subprocess.run(
            [
                sys.executable,
                str(script),
                "--project-root",
                ".",
                "--run-dir",
                str(run_dir),
                "--carousel-id",
                carousel_id,
                "--tool",
                provider,
                "--surface",
                "carousel",
            ],
            check=True,
        )
        prepared.append(carousel_id)
    return prepared


def main():
    parser = argparse.ArgumentParser(description="Run the weekly Mira automation pipeline.")
    parser.add_argument("--week", default="", help="Week id, e.g. 2026-W25. Optional with --use-perplexity-index; the latest index week will be used.")
    parser.add_argument("--perplexity-source", help="Optional CSV/Markdown file path or direct CSV URL.")
    parser.add_argument(
        "--editorial-source",
        help="Optional editor-approved CSV. Approved rows override raw Perplexity rows for packet selection.",
    )
    parser.add_argument(
        "--look-source",
        help="Optional editor-approved 2-3-look-per-theme CSV used to create weekly_look_plan.csv.",
    )
    parser.add_argument("--perplexity-index", default="", help="Optional Perplexity public index URL. Defaults to the saved Mira index when --use-perplexity-index is set.")
    parser.add_argument("--use-perplexity-index", action="store_true", help="Resolve the CSV URL from the Perplexity public index.")
    parser.add_argument("--database", default="04_prompts/item_prompt_database.csv")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--output-dir", help="Defaults to 10_automation/runs/{week}.")
    parser.add_argument("--dry-run-import", action="store_true")
    parser.add_argument("--skip-validation", action="store_true")
    parser.add_argument("--score-sheet", help="Optional scored Codex image CSV. If omitted, an empty review template is created.")
    parser.add_argument("--drive-inventory", help="Optional Drive image inventory CSV containing file_name and drive_url.")
    parser.add_argument("--asset-provider", default="Codex", help="Asset provider label for review templates and selection files.")
    parser.add_argument("--skip-asset-template", action="store_true", help="Do not create Codex asset review/selection files.")
    parser.add_argument("--skip-image-jobs", action="store_true", help="Do not prepare per-carousel Codex image job folders.")
    parser.add_argument("--skip-status", action="store_true", help="Do not write weekly_status.md/json.")
    args = parser.parse_args()

    source = args.perplexity_source
    if args.use_perplexity_index:
        resolved = resolve_source(index_source=args.perplexity_index or DEFAULT_INDEX_URL, week=args.week, latest=not bool(args.week))
        source = resolved["csv_url"]
        if not args.week:
            args.week = resolved["week"]
        print(f"Resolved Perplexity source: {source}")

    if not args.week:
        parser.error("--week is required unless --use-perplexity-index resolves a week.")

    imported_any = False
    if source:
        result = import_rows(
            source=source,
            database_path=args.database,
            week=args.week,
            dry_run=args.dry_run_import,
        )
        action = "Would import" if args.dry_run_import else "Imported"
        print(f"{action} {result['imported_rows']} row(s) for {args.week}.")
        imported_any = True

    if args.editorial_source:
        editorial_result = import_rows(
            source=args.editorial_source,
            database_path=args.database,
            week=args.week,
            dry_run=args.dry_run_import,
        )
        action = "Would import" if args.dry_run_import else "Imported"
        print(
            f"{action} {editorial_result['imported_rows']} editor-approved row(s) "
            f"for {args.week}."
        )
        imported_any = True

    if args.dry_run_import and imported_any:
        print("Dry run ended before packet build.")
        return

    output_dir = args.output_dir or str(Path("10_automation") / "runs" / args.week)
    run_build_weekly_packet(
        week=args.week,
        limit=args.limit,
        output_dir=output_dir,
        source_database=args.database,
    )
    if args.look_source:
        looks = build_look_plan(
            packet_path=Path(output_dir) / "weekly_content_packet.csv",
            source_path=args.look_source,
            output_path=Path(output_dir) / "weekly_look_plan.csv",
        )
        print(f"Prepared weekly look plan: {len(looks)} look(s).")
    if not args.skip_image_jobs:
        prepared = prepare_codex_image_jobs(output_dir, args.asset_provider)
        print(f"Prepared Codex image job(s): {len(prepared)}.")
    if not args.skip_validation:
        report = validate_run(output_dir, min_rows=args.limit)
        print(
            f"Validation {report['status']}: "
            f"{report['error_count']} error(s), {report['warning_count']} warning(s)."
        )
        if report["status"] != "pass":
            raise SystemExit(1)

    if not args.skip_asset_template:
        selections = select_assets(
            run_dir=output_dir,
            score_sheet=args.score_sheet,
            drive_inventory=args.drive_inventory,
            provider=args.asset_provider,
        )
        selected_count = sum(1 for row in selections if row["selection_status"] == "selected")
        print(f"Asset selection: {selected_count}/{len(selections)} carousel(s) selected.")

        if args.score_sheet and not args.skip_validation:
            report = validate_run(output_dir, min_rows=args.limit, require_assets=True)
            print(
                f"Asset validation {report['status']}: "
                f"{report['error_count']} error(s), {report['warning_count']} warning(s)."
            )
            if report["status"] != "pass":
                raise SystemExit(1)

    if (Path(output_dir) / "weekly_look_plan.csv").exists() and len(read_packets(output_dir)) == 5:
        build_reel_production(Path(__file__).resolve().parents[1], Path(output_dir))
        print("Prepared five two-look Reel production records (existing editorial fields preserved).")

    if not args.skip_status:
        status = check_status(output_dir)
        print(f"Stage: {status['stage']['stage']}")
        print(f"Next action: {status['stage']['next_action']}")
    print(f"Weekly pipeline complete: {output_dir}")


if __name__ == "__main__":
    main()
