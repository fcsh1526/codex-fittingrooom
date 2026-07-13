import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TMP_ROOT = ROOT / "tmp" / "smoke_weekly_pipeline"
sys.path.insert(0, str(ROOT / "10_automation"))

from mira_models import MODEL_ROTATION, model_for_index
from build_weekly_packet import week_start_date


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


def read_csv(path):
    import csv

    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


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
    assert_equal(status["stage"]["stage"], "needs_image_asset_selection", "new week stage")
    assert_exists(run_dir / "codex_asset_review_template.csv", "Codex review template")
    assert_exists(run_dir / "weekly_status.md", "weekly status")
    assert_exists(run_dir / "daily_queue.csv", "daily queue")
    assert_exists(run_dir / "image_generation_briefs.md", "image generation briefs")
    assert_exists(run_dir / "image_review_template.csv", "image review template")
    assert_exists(
        run_dir / "generated_images" / "2026-W25-001" / "codex_generation_handoff.md",
        "Codex generation handoff",
    )
    queue = read_csv(run_dir / "daily_queue.csv")
    packets = read_csv(run_dir / "weekly_content_packet.csv")
    assert_equal(len(queue), 5, "daily queue row count")
    if not all(row.get("model_profile_id") in {"M01", "M02", "M03", "M04", "M05"} for row in packets):
        raise AssertionError("weekly packet model_profile_id must be M01/M02/M03/M04/M05")


def test_weekly_model_rotation_uses_all_five():
    w28_models = [model_for_index(index, week_id="2026-W28") for index in range(1, 6)]
    assert_equal(sorted(w28_models), MODEL_ROTATION, "weekly model roster coverage")
    assert_equal(len(set(w28_models)), 5, "weekly model roster uniqueness")

    w27_models = [model_for_index(index, week_id="2026-W27") for index in range(1, 6)]
    assert_equal(w27_models, MODEL_ROTATION, "W27 locked model order")


def test_iso_week_dates():
    assert_equal(str(week_start_date("2026-W27")), "2026-06-29", "ISO W27 Monday")
    assert_equal(str(week_start_date("2026-W28")), "2026-07-06", "ISO W28 Monday")
    assert_equal(str(week_start_date("2026-W29")), "2026-07-13", "ISO W29 Monday")


def test_perplexity_index_resolver():
    run_command(
        [
            sys.executable,
            "10_automation/resolve_perplexity_source.py",
            "--index",
            "10_automation/examples/perplexity_index_example.json",
            "--week",
            "2026-W25",
        ]
    )


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
    assert_equal(
        status["stage"]["stage"],
        "canva_blocked_waiting_for_flat_png_asset",
        "scored week without Canva asset ids",
    )
    assert_equal(status["assets"]["selected_cover_count"], 2, "selected cover count")
    assert_exists(run_dir / "canva_asset_plan.md", "Canva asset plan")
    assert_exists(run_dir / "daily_queue.csv", "scored week daily queue")


def test_openai_image_dry_run():
    run_dir = TMP_ROOT / "run-w25"
    run_command(
        [
            sys.executable,
            "10_automation/generate_openai_images.py",
            "--run-dir",
            rel(run_dir),
            "--variants",
            "2",
            "--dry-run",
        ]
    )
    inventory = run_dir / "openai_image_inventory.csv"
    assert_exists(inventory, "OpenAI image inventory")
    assert_exists(run_dir / "openai_asset_review_template.csv", "OpenAI asset review template")
    assert_exists(run_dir / "openai_prompts", "OpenAI prompt folder")


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
    assert_equal(status["stage"]["stage"], "needs_image_asset_selection", "production continues after zero reach")
    assert_equal(status["publish"]["latest_decision"], "visibility_recovery", "zero reach side decision")
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
    assert_equal(
        brief["priority_run"]["stage"],
        "canva_blocked_waiting_for_flat_png_asset",
        "daily brief run-level blocker",
    )
    assert_exists(TMP_ROOT / "TODAY.md", "daily brief")
    assert_equal(
        brief["publish_queue"]["top_item"]["stage"],
        "needs_image_asset_selection",
        "daily brief keeps production moving",
    )
    if not brief["publish_queue"]["top_item"].get("model_profile_id"):
        raise AssertionError("daily brief top item should include model_profile_id")


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
    assert_equal(queue["top_item"]["stage"], "needs_image_asset_selection", "publish queue production-first top stage")
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


def test_canva_inventory_powershell_route():
    powershell = shutil.which("powershell")
    if not powershell:
        print("Skipping Canva inventory PowerShell route test: powershell not found.")
        return

    import csv

    run_dir = TMP_ROOT / "run-w21"
    inventory_path = run_dir / "canva_asset_inventory.csv"
    slot_rows = read_csv(run_dir / "canva_asset_slots.csv")
    with inventory_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file_name", "canva_asset_id"])
        writer.writeheader()
        for index, row in enumerate(slot_rows, start=1):
            file_name = (row.get("recommended_file") or "").strip()
            if file_name:
                writer.writerow({"file_name": file_name, "canva_asset_id": f"TEST_ASSET_{index:02d}"})

    command = [
        powershell,
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        "10_automation/mika_weekly.ps1",
        "-Action",
        "assets",
        "-RunDir",
        rel(run_dir),
        "-ScoreSheet",
        "07_metrics/w21_visual_review_scores.csv",
        "-DriveInventory",
        "07_metrics/w21_drive_image_inventory.csv",
        "-CanvaInventory",
        rel(inventory_path),
        "-AssetProvider",
        "Codex",
    ]
    run_command(command)
    run_command(command)
    run_command([sys.executable, "10_automation/check_weekly_status.py", "--run-dir", rel(run_dir)])

    status = read_json(run_dir / "weekly_status.json")
    assert_equal(status["stage"]["stage"], "ready_for_canva_test", "Canva inventory routed through PowerShell")
    for row in read_csv(run_dir / "canva_asset_slots.csv"):
        notes = row.get("notes") or ""
        assert_equal(notes.count("canva_asset_id="), 1, "idempotent Canva asset note")


def main():
    clean_tmp()
    test_iso_week_dates()
    test_weekly_model_rotation_uses_all_five()
    test_perplexity_index_resolver()
    test_new_week_without_assets()
    test_week_with_scored_assets()
    test_openai_image_dry_run()
    test_zero_reach_decision()
    test_powershell_entrypoint_if_available()
    test_weekly_dashboard()
    test_daily_brief()
    test_daily_cockpit()
    test_publish_queue()
    test_visibility_test_package()
    test_canva_inventory_powershell_route()
    print("Smoke test passed.")


if __name__ == "__main__":
    main()
