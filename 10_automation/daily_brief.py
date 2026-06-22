import argparse
import json
from datetime import date
from pathlib import Path

from prepare_visibility_test import build_visibility_test
from publish_queue import build_publish_queue
from weekly_dashboard import build_dashboard


STAGE_PRIORITY = {
    "visibility_recovery": 100,
    "published_waiting_for_metrics": 90,
    "quality_gate_not_passed": 80,
    "missing_weekly_packet_files": 75,
    "needs_grok_asset_selection": 70,
    "ready_for_canva_and_publish": 60,
    "weak_distribution": 50,
    "wait_for_24h": 45,
    "hook_or_save_gap": 40,
    "profile_interest": 35,
    "repeat_bucket": 30,
    "metrics_recorded_review_needed": 20,
}


def clean(value):
    return " ".join(str(value or "").split()).strip()


def pick_priority_run(dashboard):
    runs = dashboard.get("runs", [])
    if not runs:
        return None
    return sorted(
        runs,
        key=lambda row: (
            STAGE_PRIORITY.get(clean(row.get("stage")), 10),
            clean(row.get("run_dir")),
        ),
        reverse=True,
    )[0]


def stage_brief(stage):
    briefs = {
        "visibility_recovery": {
            "decision": "Today is an Instagram visibility recovery day, not a carousel production day.",
            "tasks": [
                "Check Instagram: public account, Account Status, profile grid visibility, and whether the post opens from another account.",
                "Publish one simple single-image test with direct comment CTA, then share it once to Story.",
                "Send the post to 3-5 trusted people and record 6h / 24h metrics.",
            ],
            "user_inputs": [
                "IG audit result",
                "Second-test post URL and publish time",
                "6h and 24h metrics",
            ],
            "codex_actions": [
                "Record the new post and metrics with record_post_metrics.py.",
                "Update the weekly dashboard and decide whether Instagram remains a growth channel.",
                "Prepare Threads / Pinterest fallback copy if the second test is still zero reach.",
            ],
            "files": [
                "10_automation/runs/{run}/visibility_test_package.md",
                "05_content/2026_06_18_reactivation_plan.md",
                "09_sops/instagram_zero_reach_recovery.md",
            ],
        },
        "published_waiting_for_metrics": {
            "decision": "A post is live; metrics are the only useful next input.",
            "tasks": [
                "Open Instagram insights for the post.",
                "Record reach, likes, saves, comments, shares, profile visits, and follows.",
                "Send the numbers back before changing the content direction.",
            ],
            "user_inputs": ["Post URL", "6h / 24h metrics"],
            "codex_actions": [
                "Record metrics and update publish_status.md.",
                "Decide repeat, revise, or visibility recovery based on the metrics.",
            ],
            "files": ["10_automation/record_post_metrics.py"],
        },
        "quality_gate_not_passed": {
            "decision": "Fix the content packet before image production.",
            "tasks": [
                "Do not generate Grok images yet.",
                "Run validation and fix missing fields, disclosure, prompt safety terms, or Canva text length.",
                "Regenerate handoff files after validation passes.",
            ],
            "user_inputs": ["No user input needed unless source trend data is wrong."],
            "codex_actions": [
                "Run validate_weekly_run.py.",
                "Patch the packet or generator, then rerun validation.",
            ],
            "files": ["10_automation/validate_weekly_run.py"],
        },
        "missing_weekly_packet_files": {
            "decision": "Regenerate the weekly run folder.",
            "tasks": [
                "Confirm the week ID and Perplexity export source.",
                "Run the weekly pipeline.",
                "Check quality_report.md before image production.",
            ],
            "user_inputs": ["Week ID", "Perplexity weekly URL / CSV / markdown export"],
            "codex_actions": [
                "Run run_weekly_pipeline.py.",
                "Create Grok prompts, Canva placeholders, post drafts, and checklist.",
            ],
            "files": ["10_automation/run_weekly_pipeline.py"],
        },
        "needs_grok_asset_selection": {
            "decision": "The next bottleneck is Grok image review and asset selection.",
            "tasks": [
                "Use grok_prompts.md to generate 30-50 Grok images or enough variants for the selected carousel.",
                "Put the images in Google Drive with clear numbering.",
                "Share the Drive folder or score sheet for selection.",
            ],
            "user_inputs": ["Google Drive Grok output folder", "Optional visual score sheet"],
            "codex_actions": [
                "Create or update image inventory.",
                "Select cover/detail assets and update canva_asset_slots.csv.",
                "Validate with --require-assets before Canva work.",
            ],
            "files": [
                "10_automation/runs/{run}/grok_prompts.md",
                "10_automation/select_grok_assets.py",
            ],
        },
        "ready_for_canva_and_publish": {
            "decision": "The run is ready for Canva assembly and publishing.",
            "tasks": [
                "Open the Canva panorama template and fill text from canva_fill_guide.md.",
                "Place images according to canva_asset_plan.md.",
                "Publish or schedule the post, then send the post URL.",
            ],
            "user_inputs": ["Final Canva URL", "Instagram post URL", "Publish time"],
            "codex_actions": [
                "Check caption, CTA, hashtags, and AI disclosure.",
                "Record post URL and create 6h / 24h metrics commands.",
            ],
            "files": [
                "10_automation/runs/{run}/canva_fill_guide.md",
                "10_automation/runs/{run}/canva_asset_plan.md",
                "10_automation/runs/{run}/post_drafts.md",
            ],
        },
        "repeat_bucket": {
            "decision": "There is a signal; repeat the same content bucket before changing strategy.",
            "tasks": [
                "Pick one adjacent outfit angle from the same trend bucket.",
                "Create the next carousel using the same structure.",
                "Prepare a simple product-list reply flow only after repeat signal holds.",
            ],
            "user_inputs": ["Preferred follow-up trend or Perplexity export"],
            "codex_actions": [
                "Build the next weekly packet.",
                "Draft carousel copy and CTA for the same bucket.",
            ],
            "files": ["10_automation/run_weekly_pipeline.py"],
        },
    }
    return briefs.get(
        stage,
        {
            "decision": "Review the weekly status before producing more content.",
            "tasks": [
                "Open weekly_status.md for the priority run.",
                "Follow the next action shown there.",
                "Record any publish or metrics event before starting a new carousel.",
            ],
            "user_inputs": ["Current blocker or latest metrics"],
            "codex_actions": [
                "Update dashboard and route the run to the next production step.",
            ],
            "files": ["10_automation/runs/DASHBOARD.md"],
        },
    )


def no_run_brief():
    return {
        "decision": "No weekly run exists yet; start from Perplexity trend input.",
        "tasks": [
            "Provide the current Perplexity weekly URL, CSV, or markdown export.",
            "Confirm the week ID.",
            "Let Codex run the weekly pipeline to create prompts, Canva placeholders, drafts, and checklist.",
        ],
        "user_inputs": ["Week ID", "Perplexity weekly URL / CSV / markdown export"],
        "codex_actions": [
            "Run run_weekly_pipeline.py.",
            "Generate grok_prompts.md, canva_fill_guide.md, post_drafts.md, and publish_checklist.md.",
        ],
        "files": ["10_automation/run_weekly_pipeline.py"],
    }


def render_markdown(today, dashboard, priority_run, brief, generated_files=None, publish_queue=None):
    generated_files = generated_files or []
    publish_queue = publish_queue or {}
    run_name = Path(priority_run["run_dir"]).name if priority_run else "none"
    stage = clean(priority_run.get("stage")) if priority_run else "needs_weekly_input"
    next_action = clean(priority_run.get("next_action")) if priority_run else brief["decision"]

    lines = [
        "# Mika Lin Daily Brief",
        "",
        f"Date: `{today}`",
        f"Priority run: `{run_name}`",
        f"Stage: `{stage}`",
        "",
        "## Decision",
        "",
        brief["decision"],
        "",
        "## Today Only",
        "",
    ]
    for index, task in enumerate(brief["tasks"], start=1):
        lines.append(f"{index}. {task}")
    lines.extend(["", "## User Should Provide", ""])
    for item in brief["user_inputs"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Codex Can Do Next", ""])
    for item in brief["codex_actions"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Useful Files", ""])
    for file_name in brief["files"]:
        lines.append(f"- `{file_name.replace('{run}', run_name)}`")
    if generated_files:
        lines.extend(["", "## Generated Files", ""])
        for file_name in generated_files:
            lines.append(f"- `{file_name}`")
    top_item = publish_queue.get("top_item") or {}
    if top_item:
        lines.extend(
            [
                "",
                "## Publish Queue Top Item",
                "",
                f"- Type: `{top_item.get('item_type')}`",
                f"- ID: `{top_item.get('carousel_id')}`",
                f"- Stage: `{top_item.get('stage')}`",
                f"- Asset: `{top_item.get('recommended_asset') or 'n/a'}`",
                f"- Next action: {top_item.get('next_action')}",
            ]
        )
    lines.extend(
        [
            "",
            "## Current Next Action",
            "",
            next_action,
            "",
            "## Fixed Flow",
            "",
            "```text",
            "person identity -> weekly trend -> prompt packet -> Grok images -> Canva carousel -> publish -> metrics -> next decision",
            "```",
            "",
            "## Dashboard Summary",
            "",
            f"- Run count: `{dashboard.get('run_count', 0)}`",
            f"- Stage counts: `{json.dumps(dashboard.get('stage_counts', {}), ensure_ascii=False)}`",
            "",
        ]
    )
    return "\n".join(lines)


def build_daily_brief(
    runs_dir,
    output_md,
    output_json,
    today=None,
    queue_csv="10_automation/PUBLISH_QUEUE.csv",
    queue_md="10_automation/PUBLISH_QUEUE.md",
    queue_json="10_automation/PUBLISH_QUEUE.json",
):
    today = today or date.today().isoformat()
    dashboard = build_dashboard(runs_dir)
    priority_run = pick_priority_run(dashboard)
    brief = stage_brief(clean(priority_run.get("stage"))) if priority_run else no_run_brief()
    generated_files = []

    if priority_run and clean(priority_run.get("stage")) == "visibility_recovery":
        _, visibility_md, visibility_json = build_visibility_test(priority_run["run_dir"])
        generated_files.extend([str(visibility_md), str(visibility_json)])

    queue = build_publish_queue(runs_dir, queue_csv, queue_md, queue_json)
    generated_files.extend([queue_md, queue_json, queue_csv])

    payload = {
        "date": today,
        "priority_run": priority_run,
        "decision": brief["decision"],
        "tasks": brief["tasks"],
        "user_inputs": brief["user_inputs"],
        "codex_actions": brief["codex_actions"],
        "useful_files": brief["files"],
        "generated_files": generated_files,
        "publish_queue": {
            "item_count": queue["item_count"],
            "top_item": queue["top_item"],
        },
        "dashboard": dashboard,
    }

    output_md = Path(output_md)
    output_json = Path(output_json)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(
        render_markdown(today, dashboard, priority_run, brief, generated_files, queue),
        encoding="utf-8",
    )
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def main():
    parser = argparse.ArgumentParser(description="Create today's Mika Lin work brief from the weekly dashboard.")
    parser.add_argument("--runs-dir", default="10_automation/runs")
    parser.add_argument("--output-md", default="10_automation/TODAY.md")
    parser.add_argument("--output-json", default="10_automation/TODAY.json")
    parser.add_argument("--queue-csv", default="10_automation/PUBLISH_QUEUE.csv")
    parser.add_argument("--queue-md", default="10_automation/PUBLISH_QUEUE.md")
    parser.add_argument("--queue-json", default="10_automation/PUBLISH_QUEUE.json")
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()

    payload = build_daily_brief(
        args.runs_dir,
        args.output_md,
        args.output_json,
        args.date,
        queue_csv=args.queue_csv,
        queue_md=args.queue_md,
        queue_json=args.queue_json,
    )
    priority = payload["priority_run"] or {}
    print(f"Stage: {priority.get('stage', 'needs_weekly_input')}")
    print(f"Decision: {payload['decision']}")
    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()
