import argparse
import json
from collections import Counter
from pathlib import Path

from check_weekly_status import check_status


def run_dirs_under(runs_dir):
    runs_dir = Path(runs_dir)
    if not runs_dir.exists():
        return []
    return sorted(
        path
        for path in runs_dir.iterdir()
        if path.is_dir()
        and (
            (path / "weekly_content_packet.csv").exists()
            or (path / "weekly_status.json").exists()
        )
    )


def summarize_status(status):
    stage = status["stage"]["stage"]
    packet = status["packet"]
    assets = status["assets"]
    publish = status["publish"]
    return {
        "run_dir": status["run_dir"],
        "stage": stage,
        "next_action": status["stage"]["next_action"],
        "packet_rows": packet["row_count"],
        "quality": status["quality"]["status"],
        "cover_assets": f"{assets['selected_cover_count']}/{assets['carousel_count']}",
        "published": publish["published"],
        "metric_checkpoints": publish["metric_count"],
        "latest_decision": publish.get("latest_decision", ""),
    }


def write_dashboard(runs_dir, summaries):
    runs_dir = Path(runs_dir)
    runs_dir.mkdir(parents=True, exist_ok=True)
    dashboard_json = {
        "runs_dir": str(runs_dir),
        "run_count": len(summaries),
        "stage_counts": dict(Counter(row["stage"] for row in summaries)),
        "runs": summaries,
    }
    (runs_dir / "DASHBOARD.json").write_text(
        json.dumps(dashboard_json, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Mika Lin Weekly Dashboard",
        "",
        f"Runs directory: `{runs_dir}`",
        f"Run count: `{len(summaries)}`",
        "",
    ]

    if not summaries:
        lines.extend(
            [
                "No weekly run folders found.",
                "",
                "Create one with:",
                "",
                "```powershell",
                "powershell -ExecutionPolicy Bypass -File 10_automation\\mika_weekly.ps1 -Action pipeline -Week 2026-WXX -PerplexitySource path_or_url_to_perplexity_export",
                "```",
                "",
            ]
        )
    else:
        lines.extend(["## Stage Counts", ""])
        for stage, count in Counter(row["stage"] for row in summaries).most_common():
            lines.append(f"- `{stage}`: `{count}`")
        lines.extend(["", "## Runs", ""])
        lines.append("| Run | Stage | Quality | Cover Assets | Published | Metrics | Next Action |")
        lines.append("|---|---|---|---:|---:|---:|---|")
        for row in summaries:
            run_name = Path(row["run_dir"]).name
            next_action = row["next_action"].replace("|", "/")
            lines.append(
                f"| `{run_name}` | `{row['stage']}` | `{row['quality']}` | `{row['cover_assets']}` | `{row['published']}` | `{row['metric_checkpoints']}` | {next_action} |"
            )
        lines.append("")

    (runs_dir / "DASHBOARD.md").write_text("\n".join(lines), encoding="utf-8")
    return dashboard_json


def build_dashboard(runs_dir):
    statuses = []
    for run_dir in run_dirs_under(runs_dir):
        statuses.append(check_status(run_dir))
    summaries = [summarize_status(status) for status in statuses]
    return write_dashboard(runs_dir, summaries)


def main():
    parser = argparse.ArgumentParser(description="Build a dashboard for all weekly Mika Lin run folders.")
    parser.add_argument("--runs-dir", default="10_automation/runs")
    args = parser.parse_args()

    dashboard = build_dashboard(args.runs_dir)
    print(f"Dashboard runs: {dashboard['run_count']}")
    print(f"Wrote {Path(args.runs_dir) / 'DASHBOARD.md'}")


if __name__ == "__main__":
    main()
