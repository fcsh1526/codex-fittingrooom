import argparse
import sys
from pathlib import Path

from build_weekly_packet import main as build_main
from check_weekly_status import check_status
from import_perplexity_export import import_rows
from resolve_perplexity_source import DEFAULT_INDEX_URL, resolve_source
from select_codex_assets import select_assets
from validate_weekly_run import validate_run


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


def main():
    parser = argparse.ArgumentParser(description="Run the weekly Mira automation pipeline.")
    parser.add_argument("--week", required=True, help="Week id, e.g. 2026-W25.")
    parser.add_argument("--perplexity-source", help="Optional CSV/Markdown file path or direct CSV URL.")
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
    parser.add_argument("--skip-status", action="store_true", help="Do not write weekly_status.md/json.")
    args = parser.parse_args()

    source = args.perplexity_source
    if args.use_perplexity_index:
        resolved = resolve_source(index_source=args.perplexity_index or DEFAULT_INDEX_URL, week=args.week, latest=not bool(args.week))
        source = resolved["csv_url"]
        print(f"Resolved Perplexity source: {source}")

    if source:
        result = import_rows(
            source=source,
            database_path=args.database,
            week=args.week,
            dry_run=args.dry_run_import,
        )
        action = "Would import" if args.dry_run_import else "Imported"
        print(f"{action} {result['imported_rows']} row(s) for {args.week}.")
        if args.dry_run_import:
            print("Dry run ended before packet build.")
            return

    output_dir = args.output_dir or str(Path("10_automation") / "runs" / args.week)
    run_build_weekly_packet(
        week=args.week,
        limit=args.limit,
        output_dir=output_dir,
        source_database=args.database,
    )
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

    if not args.skip_status:
        status = check_status(output_dir)
        print(f"Stage: {status['stage']['stage']}")
        print(f"Next action: {status['stage']['next_action']}")
    print(f"Weekly pipeline complete: {output_dir}")


if __name__ == "__main__":
    main()
