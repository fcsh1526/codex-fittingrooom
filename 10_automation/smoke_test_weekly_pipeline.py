import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TMP_ROOT = ROOT / "tmp" / "smoke_weekly_pipeline"


def rel(path):
    return str(Path(path))


def ensure_tmp_path(path):
    resolved = Path(path).resolve()
    tmp_resolved = (ROOT / "tmp").resolve()
    try:
        resolved.relative_to(tmp_resolved)
    except ValueError as exc:
        raise RuntimeError(f"Refusing to touch non-tmp path: {resolved}") from exc


def clean_tmp():
    ensure_tmp_path(TMP_ROOT)
    if TMP_ROOT.exists():
        shutil.rmtree(TMP_ROOT)
    TMP_ROOT.mkdir(parents=True, exist_ok=True)


def run_command(args):
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print("$ " + " ".join(str(arg) for arg in args))
    print(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {args}")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def assert_exists(path, label):
    if not Path(path).exists():
        raise AssertionError(f"{label} missing: {path}")


def test_new_week_without_assets():
    run_dir = TMP_ROOT / "run-w25"
    database = TMP_ROOT / "database-w25.csv"
    run_command(
        [
            sys.executable,
            "10_automation/run_weekly_pipeline.py",
            "--week",
            "2026-W25",
            "--perplexity-source",
            "10_automation/examples/perplexity_export_example.md",
            "--database",
            rel(database),
            "--limit",
            "2",
            "--output-dir",
            rel(run_dir),
        ]
    )

    status = read_json(run_dir / "weekly_status.json")
    assert_equal(status["stage"]["stage"], "needs_grok_asset_selection", "new week stage")
    assert_exists(run_dir / "grok_asset_review_template.csv", "Grok review template")
    assert_exists(run_dir / "weekly_status.md", "weekly status")


def test_week_with_scored_assets():
    run_dir = TMP_ROOT / "run-w21"
    run_command(
        [
            sys.executable,
            "10_automation/run_weekly_pipeline.py",
            "--week",
            "2026-W21-test",
            "--database",
            "04_prompts/item_prompt_database.csv",
            "--limit",
            "2",
            "--output-dir",
            rel(run_dir),
            "--score-sheet",
            "07_metrics/w21_visual_review_scores.csv",
            "--drive-inventory",
            "07_metrics/w21_drive_image_inventory.csv",
        ]
    )

    status = read_json(run_dir / "weekly_status.json")
    assert_equal(status["stage"]["stage"], "ready_for_canva_and_publish", "scored week stage")
    assert_equal(status["assets"]["selected_cover_count"], 2, "selected cover count")
    assert_exists(run_dir / "canva_asset_plan.md", "Canva asset plan")


def test_zero_reach_decision():
    run_dir = TMP_ROOT / "run-w25"
    metrics_dir = TMP_ROOT / "metrics"
    run_command(
        [
            sys.executable,
            "10_automation/record_post_metrics.py",
            "--run-dir",
            rel(run_dir),
            "--global-dir",
            rel(metrics_dir),
            "--week",
            "2026-W25",
            "--carousel-id",
            "2026-W25-001",
            "--platform",
            "Instagram",
            "--format",
            "Carousel",
            "--post-url",
            "https://www.instagram.com/p/DZCTbtWGuhx/",
            "--published-at",
            "2026/06/01 16:08",
            "--record-date",
            "2026-06-02",
            "--record-metrics",
            "--measured-at",
            "2026-06-02",
            "--hours-after-publish",
            "24",
            "--reach",
            "0",
            "--likes",
            "0",
            "--saves",
            "0",
            "--comments",
            "0",
            "--shares",
            "0",
        ]
    )
    run_command([sys.executable, "10_automation/check_weekly_status.py", "--run-dir", rel(run_dir)])
    status = read_json(run_dir / "weekly_status.json")
    assert_equal(status["stage"]["stage"], "visibility_recovery", "zero reach stage")
    assert_exists(run_dir / "publish_status.md", "publish status")


def test_powershell_entrypoint_if_available():
    powershell = shutil.which("powershell")
    if not powershell:
        print("Skipping PowerShell entrypoint smoke test: powershell not found.")
        return
    run_dir = TMP_ROOT / "run-w21"
    run_command(
        [
            powershell,
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            "10_automation/mika_weekly.ps1",
            "-Action",
            "status",
            "-RunDir",
            rel(run_dir),
        ]
    )
    run_command(
        [
            powershell,
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            "10_automation/mika_weekly.ps1",
            "-Action",
            "today",
            "-RunsDir",
            rel(TMP_ROOT),
            "-TodayOutput",
            rel(TMP_ROOT / "PS_TODAY.md"),
            "-TodayJson",
            rel(TMP_ROOT / "PS_TODAY.json"),
            "-QueueOutput",
            rel(TMP_ROOT / "PS_QUEUE.md"),
            "-QueueJson",
            rel(TMP_ROOT / "PS_QUEUE.json"),
            "-QueueCsv",
            rel(TMP_ROOT / "PS_QUEUE.csv"),
            "-CockpitHtml",
            rel(TMP_ROOT / "PS_COCKPIT.html"),
            "-CockpitMd",
            rel(TMP_ROOT / "PS_COCKPIT.md"),
        ]
    )
    assert_exists(TMP_ROOT / "PS_TODAY.md", "PowerShell daily brief")
    assert_exists(TMP_ROOT / "PS_COCKPIT.html", "PowerShell daily cockpit")
    run_command(
        [
            powershell,
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            "10_automation/mika_weekly.ps1",
            "-Action",
            "visibility-test",
            "-RunDir",
            rel(run_dir),
            "-VisibilityOutput",
            rel(TMP_ROOT / "PS_VISIBILITY.md"),
            "-VisibilityJson",
            rel(TMP_ROOT / "PS_VISIBILITY.json"),
        ]
    )
    assert_exists(TMP_ROOT / "PS_VISIBILITY.md", "PowerShell visibility test package")


def test_weekly_dashboard():
    run_command([sys.executable, "10_automation/weekly_dashboard.py", "--runs-dir", rel(TMP_ROOT)])
    dashboard = read_json(TMP_ROOT / "DASHBOARD.json")
    assert_equal(dashboard["run_count"], 2, "dashboard run count")
    assert_exists(TMP_ROOT / "DASHBOARD.md", "weekly dashboard")


def test_daily_brief():
    run_command(
        [
            sys.executable,
            "10_automation/daily_brief.py",
            "--runs-dir",
            rel(TMP_ROOT),
            "--output-md",
            rel(TMP_ROOT / "TODAY.md"),
            "--output-json",
            rel(TMP_ROOT / "TODAY.json"),
            "--queue-md",
            rel(TMP_ROOT / "PUBLISH_QUEUE.md"),
            "--queue-json",
            rel(TMP_ROOT / "PUBLISH_QUEUE.json"),
            "--queue-csv",
            rel(TMP_ROOT / "PUBLISH_QUEUE.csv"),
            "--date",
            "2026-06-18",
        ]
    )
    brief = read_json(TMP_ROOT / "TODAY.json")
    assert_equal(brief["priority_run"]["stage"], "ready_for_canva_and_publish", "daily brief priority stage")
    assert_exists(TMP_ROOT / "TODAY.md", "daily brief")
    assert_equal(brief["publish_queue"]["top_item"]["stage"], "ready_for_canva_and_publish", "daily brief queue top stage")


def test_daily_cockpit():
    run_command(
        [
            sys.executable,
            "10_automation/daily_cockpit.py",
            "--runs-dir",
            rel(TMP_ROOT),
            "--today-md",
            rel(TMP_ROOT / "COCKPIT_TODAY.md"),
            "--today-json",
            rel(TMP_ROOT / "COCKPIT_TODAY.json"),
            "--queue-md",
            rel(TMP_ROOT / "COCKPIT_QUEUE.md"),
            "--queue-json",
            rel(TMP_ROOT / "COCKPIT_QUEUE.json"),
            "--queue-csv",
            rel(TMP_ROOT / "COCKPIT_QUEUE.csv"),
            "--output-html",
            rel(TMP_ROOT / "COCKPIT_ONLY.html"),
            "--output-md",
            rel(TMP_ROOT / "COCKPIT_ONLY.md"),
            "--date",
            "2026-06-18",
        ]
    )
    assert_exists(TMP_ROOT / "COCKPIT_ONLY.html", "daily cockpit html")
    assert_exists(TMP_ROOT / "COCKPIT_ONLY.md", "daily cockpit markdown")


def test_publish_queue():
    run_command(
        [
            sys.executable,
            "10_automation/publish_queue.py",
            "--runs-dir",
            rel(TMP_ROOT),
            "--output-md",
            rel(TMP_ROOT / "QUEUE_ONLY.md"),
            "--output-json",
            rel(TMP_ROOT / "QUEUE_ONLY.json"),
            "--output-csv",
            rel(TMP_ROOT / "QUEUE_ONLY.csv"),
        ]
    )
    queue = read_json(TMP_ROOT / "QUEUE_ONLY.json")
    assert_equal(queue["top_item"]["stage"], "ready_for_canva_and_publish", "publish queue top stage")
    assert_exists(TMP_ROOT / "QUEUE_ONLY.md", "publish queue")


def test_visibility_test_package():
    run_dir = TMP_ROOT / "run-w21"
    run_command(
        [
            sys.executable,
            "10_automation/prepare_visibility_test.py",
            "--run-dir",
            rel(run_dir),
            "--output-md",
            rel(TMP_ROOT / "visibility_test_package.md"),
            "--output-json",
            rel(TMP_ROOT / "visibility_test_package.json"),
        ]
    )
    package = read_json(TMP_ROOT / "visibility_test_package.json")
    assert_equal(package["source_carousel_id"], "2026-W21-test-001", "visibility package source carousel")
    assert_exists(TMP_ROOT / "visibility_test_package.md", "visibility test package")


def main():
    clean_tmp()
    test_new_week_without_assets()
    test_week_with_scored_assets()
    test_zero_reach_decision()
    test_powershell_entrypoint_if_available()
    test_weekly_dashboard()
    test_daily_brief()
    test_daily_cockpit()
    test_publish_queue()
    test_visibility_test_package()
    print("Smoke test passed.")


if __name__ == "__main__":
    main()
