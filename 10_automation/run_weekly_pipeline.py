import argparse
import sys
from pathlib import Path

from build_weekly_packet import main as build_main
from import_perplexity_export import import_rows


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
    parser = argparse.ArgumentParser(description="Run the weekly Mika Lin automation pipeline.")
    parser.add_argument("--week", required=True, help="Week id, e.g. 2026-W25.")
    parser.add_argument("--perplexity-source", help="Optional CSV/Markdown file path or direct CSV URL.")
    parser.add_argument("--database", default="04_prompts/item_prompt_database.csv")
    parser.add_argument("--limit", type=int, default=2)
    parser.add_argument("--output-dir", help="Defaults to 10_automation/runs/{week}.")
    parser.add_argument("--dry-run-import", action="store_true")
    args = parser.parse_args()

    if args.perplexity_source:
        result = import_rows(
            source=args.perplexity_source,
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
    print(f"Weekly pipeline complete: {output_dir}")


if __name__ == "__main__":
    main()
