import argparse
import html
import json
from datetime import date
from pathlib import Path

from daily_brief import build_daily_brief


def clean(value):
    return " ".join(str(value or "").split()).strip()


def read_json(path):
    path = Path(path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def link_label(path):
    return Path(path).name


def normalize_path(path):
    return clean(path).replace("\\", "/")


def cockpit_href(path):
    path = normalize_path(path)
    prefix = "10_automation/"
    if path.startswith(prefix):
        return path[len(prefix) :]
    return path


def file_link(path):
    path = normalize_path(path)
    if not path:
        return ""
    return f'<a href="{html.escape(cockpit_href(path))}">{html.escape(link_label(path))}</a>'


def run_files(top_item):
    run_dir = clean(top_item.get("run_dir"))
    item_type = clean(top_item.get("item_type"))
    stage = clean(top_item.get("stage"))

    if item_type == "carousel" and stage in {"ready_for_canva_and_publish", "canva_committed_ready_to_publish"}:
        return [
            "10_automation/canva_template_registry.md",
            normalize_path(f"{run_dir}/canva_fill_guide.md"),
            normalize_path(f"{run_dir}/canva_asset_plan.md"),
            normalize_path(f"{run_dir}/post_drafts.md"),
            normalize_path(f"{run_dir}/publish_checklist.md"),
        ]
    if item_type == "carousel" and stage == "ready_for_canva_test":
        return [
            "10_automation/canva_template_registry.md",
            normalize_path(f"{run_dir}/canva_fill_guide.md"),
            normalize_path(f"{run_dir}/canva_asset_plan.md"),
            normalize_path(f"{run_dir}/canva_asset_slots.csv"),
            normalize_path(f"{run_dir}/canva_placeholder_map.json"),
            normalize_path(f"{run_dir}/generated_images/2026-W26-002"),
        ]
    if item_type == "carousel" and stage == "canva_blocked_waiting_for_flat_png_asset":
        return [
            "10_automation/canva_template_registry.md",
            normalize_path(f"{run_dir}/canva_automation_trial_log.md"),
            normalize_path(f"{run_dir}/canva_fill_guide.md"),
            normalize_path(f"{run_dir}/canva_asset_slots.csv"),
            normalize_path(f"{run_dir}/generated_images/2026-W26-002"),
        ]
    if item_type == "carousel" and stage == "needs_image_asset_selection":
        return [
            normalize_path(f"{run_dir}/generated_images/{clean(top_item.get('carousel_id'))}/codex_generation_handoff.md"),
            normalize_path(f"{run_dir}/generated_images/{clean(top_item.get('carousel_id'))}/candidate_prompts.md"),
            normalize_path(f"{run_dir}/generated_images/{clean(top_item.get('carousel_id'))}/review_sheet.csv"),
            normalize_path(f"{run_dir}/daily_queue.csv"),
            normalize_path(f"{run_dir}/image_generation_briefs.md"),
            normalize_path(f"{run_dir}/image_review_template.csv"),
            normalize_path(f"{run_dir}/generated_images"),
            normalize_path(f"{run_dir}/canva_asset_slots.csv"),
        ]
    if item_type == "carousel" and stage == "needs_visual_revision":
        return [
            "10_automation/canva_template_registry.md",
            normalize_path(f"{run_dir}/generated_images"),
            normalize_path(f"{run_dir}/image_review_template.csv"),
            normalize_path(f"{run_dir}/canva_asset_plan.md"),
            normalize_path(f"{run_dir}/canva_fill_guide.md"),
            normalize_path(f"{run_dir}/README.md"),
            "10_automation/mira_high_fashion_carousel_template_v2.md",
            "10_automation/claude_design_mira_template_v2_prompt.md",
        ]
    if item_type == "visibility_test":
        package = clean(top_item.get("package_path"))
        return [package] if package else []
    return [
        "10_automation/TODAY.md",
        "10_automation/PUBLISH_QUEUE.md",
    ]


def checklist_for(top_item):
    item_type = clean(top_item.get("item_type"))
    stage = clean(top_item.get("stage"))

    if item_type == "carousel" and stage == "ready_for_canva_and_publish":
        return [
            "Open the Canva panorama design.",
            "Use canva_fill_guide.md to fill the slide text.",
            "Place the recommended asset and detail image from canva_asset_plan.md.",
            "Export the 3 carousel slides or finish the Canva design.",
            "Publish or schedule the Instagram carousel.",
            "Send Codex the post URL, publish time, and any immediate notes.",
        ]
    if item_type == "carousel" and stage == "canva_committed_ready_to_publish":
        return [
            "Open the Canva panorama design and review the committed layout.",
            "Export the 3 carousel slides if the layout looks acceptable.",
            "Publish or schedule the Instagram carousel.",
            "Send Codex the post URL, publish time, and any immediate notes.",
        ]
    if item_type == "carousel" and stage == "ready_for_canva_test":
        return [
            "Do not publish this carousel yet.",
            "Test-fill the approved Mira Canva v2 template with A_v2, B_v2, and C_v2.",
            "Review Canva crops for headroom, feet, face clarity, and cross-slide motion crop.",
            "Commit Canva only if the preview is clean.",
            "If crop fails, adjust Canva placement before export.",
        ]
    if item_type == "carousel" and stage == "canva_blocked_waiting_for_flat_png_asset":
        return [
            "Do not export or publish the failed Canva draft.",
            "Resolve the selected complete PNG/JPG assets to verified Canva image asset ids.",
            "Confirm cover_image, motion_crop, and detail_image are whole flat image assets, not Magic Layers splits.",
            "Duplicate the recommended registered Canva master template again.",
            "Rerun the Canva fill only on the fresh duplicate.",
        ]
    if item_type == "carousel" and stage == "needs_image_asset_selection":
        return [
            "Open the Codex generation handoff for today's internal model and outfit.",
            "Generate image candidates inside the Codex workspace.",
            "Save candidates under generated_images.",
            "Review and score the candidates in image_review_template.csv.",
            "Run asset selection and validation.",
        ]
    if item_type == "carousel" and stage == "needs_visual_revision":
        return [
            "Do not publish this carousel yet.",
            "Verify the selected Mira Canva master has replaceable cover_image, motion_crop, detail_image, and slide2_line layers.",
            "Review the generated image candidates for face drift, ghosting, body artifacts, and outfit clarity.",
            "Regenerate better candidates before replacing Canva assets.",
            "Test-fill the Canva v2 template before export.",
        ]
    if item_type == "visibility_test":
        return [
            "Open visibility_test_package.md.",
            "Publish the single-image test only if it fits today's time.",
            "Share once to Story.",
            "Record 6h and 24h metrics when available.",
            "Keep carousel production moving even if reach is zero.",
        ]
    return [
        "Open PUBLISH_QUEUE.md.",
        "Work on the top item.",
        "Send Codex the missing input for that item.",
    ]


def reply_template(top_item):
    item_id = clean(top_item.get("carousel_id"))
    item_type = clean(top_item.get("item_type"))
    return "\n".join(
        [
            "今日回報：",
            f"item = {item_id}",
            f"type = {item_type}",
            "status = ",
            f"model = {clean(top_item.get('model_profile_id'))}",
            f"Canva URL = {clean(top_item.get('canva_design_url'))}",
            "IG URL = ",
            "published at = ",
            "6h metrics = reach / likes / saves / comments / shares",
            "24h metrics = reach / likes / saves / comments / shares",
            "stuck = ",
        ]
    )


def command_text(today):
    return f"powershell -ExecutionPolicy Bypass -File 10_automation\\mika_weekly.ps1 -Action cockpit -TodayDate {today}"


def html_card(title, body):
    return f'<section class="card"><h2>{html.escape(title)}</h2>{body}</section>'


def render_html(payload, cockpit_md):
    today = clean(payload.get("date")) or date.today().isoformat()
    queue = payload.get("publish_queue") or {}
    top = queue.get("top_item") or {}
    items = ((payload.get("dashboard") or {}).get("runs") or [])
    top_id = clean(top.get("carousel_id")) or "none"
    top_stage = clean(top.get("stage")) or "none"
    storage_key = f"mika-cockpit-{today}-{top_id}"
    files = run_files(top)
    checks = checklist_for(top)
    asset_url = clean(top.get("asset_url"))
    template_key = clean(top.get("canva_template_key")) or "n/a"
    template_name = clean(top.get("canva_template_name"))
    template_url = clean(top.get("canva_template_url"))
    design_url = clean(top.get("canva_design_url"))

    file_items = "".join(f"<li>{file_link(path)}</li>" for path in files if clean(path))
    check_items = "".join(
        f'<label class="check"><input type="checkbox" data-check="{idx}"><span>{html.escape(item)}</span></label>'
        for idx, item in enumerate(checks)
    )
    queue_json = read_json("10_automation/PUBLISH_QUEUE.json")
    queue_items = queue_json.get("items", [])
    queue_rows = "".join(
        "<tr>"
        f"<td>{html.escape(clean(row.get('item_type')))}</td>"
        f"<td>{html.escape(clean(row.get('carousel_id')))}</td>"
        f"<td>{html.escape(clean(row.get('model_profile_id')))}</td>"
        f"<td>{html.escape(clean((row.get('canva_template_key') or '') + ' ' + (row.get('canva_template_name') or '')))}</td>"
        f"<td>{html.escape(clean(row.get('stage')))}</td>"
        f"<td>{html.escape(clean(row.get('recommended_asset')))}</td>"
        f"<td>{html.escape(clean(row.get('next_action')))}</td>"
        "</tr>"
        for row in queue_items[:5]
    )
    mode = "Production-first: zero reach does not block carousel production."

    asset_block = ""
    if asset_url:
        asset_block = f'<p><a class="button" href="{html.escape(asset_url)}">Open Recommended Asset</a></p>'

    reply = reply_template(top)
    reply_escaped = html.escape(reply)
    command = command_text(today)

    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mira Daily Cockpit</title>
  <style>
    :root {{
      --bg: #f5f2ea;
      --paper: #fffdf8;
      --ink: #1e1d1a;
      --muted: #6f6a60;
      --line: #ddd4c5;
      --accent: #2f6f68;
      --accent2: #a45f3d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", "Noto Sans TC", Arial, sans-serif;
      color: var(--ink);
      background: var(--bg);
      line-height: 1.5;
    }}
    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 28px;
    }}
    header {{
      border-bottom: 2px solid var(--ink);
      padding-bottom: 18px;
      margin-bottom: 18px;
    }}
    h1 {{
      margin: 0;
      font-size: 34px;
      letter-spacing: 0;
    }}
    h2 {{
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }}
    p {{ margin: 8px 0; }}
    code, pre {{
      font-family: Consolas, "Courier New", monospace;
    }}
    pre {{
      white-space: pre-wrap;
      background: #f2eadf;
      border: 1px solid var(--line);
      padding: 12px;
      border-radius: 8px;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }}
    .pill {{
      border: 1px solid var(--line);
      background: var(--paper);
      border-radius: 999px;
      padding: 6px 10px;
      color: var(--muted);
      font-size: 13px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 16px;
      align-items: start;
    }}
    .card {{
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 16px;
    }}
    .hero {{
      border-color: var(--ink);
      border-width: 2px;
    }}
    .big {{
      font-size: 24px;
      font-weight: 700;
      margin: 4px 0;
    }}
    .muted {{ color: var(--muted); }}
    .button {{
      display: inline-block;
      background: var(--accent);
      color: white;
      text-decoration: none;
      border-radius: 6px;
      padding: 8px 12px;
      margin-right: 8px;
    }}
    .button.secondary {{
      background: var(--accent2);
    }}
    ul {{
      padding-left: 20px;
      margin: 0;
    }}
    li {{ margin: 6px 0; }}
    .check {{
      display: flex;
      gap: 10px;
      align-items: flex-start;
      padding: 10px 0;
      border-bottom: 1px solid var(--line);
    }}
    .check:last-child {{ border-bottom: 0; }}
    input[type="checkbox"] {{
      width: 20px;
      height: 20px;
      margin-top: 2px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      border-bottom: 1px solid var(--line);
      padding: 8px;
      text-align: left;
      vertical-align: top;
    }}
    th {{ color: var(--muted); font-weight: 600; }}
    @media (max-width: 760px) {{
      main {{ padding: 16px; }}
      .grid {{ grid-template-columns: 1fr; }}
      h1 {{ font-size: 28px; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Mira Daily Cockpit</h1>
      <div class="meta">
        <span class="pill">Date: {html.escape(today)}</span>
        <span class="pill">{html.escape(mode)}</span>
        <span class="pill">Top stage: {html.escape(top_stage)}</span>
      </div>
    </header>

    <section class="card hero">
      <h2>Today, Do This First</h2>
      <p class="big">{html.escape(top_id)}</p>
      <p><strong>Type:</strong> {html.escape(clean(top.get("item_type")))} / <strong>Model:</strong> {html.escape(clean(top.get("model_profile_id")) or "n/a")} / <strong>Stage:</strong> {html.escape(top_stage)}</p>
      <p><strong>Canva template:</strong> {html.escape(template_key)} {html.escape(template_name)}</p>
      <p><strong>Canva design URL:</strong> {f'<a href="{html.escape(design_url)}">{html.escape(design_url)}</a>' if design_url else 'n/a'}</p>
      <p><strong>Canva template URL:</strong> {f'<a href="{html.escape(template_url)}">{html.escape(template_url)}</a>' if template_url else 'n/a'}</p>
      <p><strong>Asset:</strong> {html.escape(clean(top.get("recommended_asset")) or "n/a")}</p>
      <p><strong>Next action:</strong> {html.escape(clean(top.get("next_action")))}</p>
      {asset_block}
    </section>

    <div class="grid">
      <div>
        {html_card("Checklist", check_items)}
        {html_card("Files To Open", f"<ul>{file_items}</ul>")}
        {html_card("Reply Template For Codex", f"<pre id='reply'>{reply_escaped}</pre><button class='button secondary' onclick='copyReply()'>Copy Reply Template</button>")}
      </div>
      <div>
        {html_card("Refresh Command", f"<pre>{html.escape(command)}</pre>")}
        {html_card("Queue Preview", f"<table><thead><tr><th>Type</th><th>ID</th><th>Model</th><th>Template</th><th>Stage</th><th>Asset</th><th>Next</th></tr></thead><tbody>{queue_rows}</tbody></table>")}
        {html_card("Reference", f"<p>{file_link(str(cockpit_md))}</p><p>{file_link('10_automation/TODAY.md')}</p><p>{file_link('10_automation/PUBLISH_QUEUE.md')}</p>")}
      </div>
    </div>
  </main>
  <script>
    const storageKey = {json.dumps(storage_key)};
    const boxes = Array.from(document.querySelectorAll('input[type="checkbox"][data-check]'));
    const saved = JSON.parse(localStorage.getItem(storageKey) || '{{}}');
    boxes.forEach(box => {{
      box.checked = !!saved[box.dataset.check];
      box.addEventListener('change', () => {{
        saved[box.dataset.check] = box.checked;
        localStorage.setItem(storageKey, JSON.stringify(saved));
      }});
    }});
    function copyReply() {{
      const text = document.getElementById('reply').innerText;
      navigator.clipboard.writeText(text);
    }}
  </script>
</body>
</html>
"""


def render_markdown(payload):
    top = (payload.get("publish_queue") or {}).get("top_item") or {}
    files = run_files(top)
    checks = checklist_for(top)
    lines = [
        "# Mira Daily Cockpit",
        "",
        f"Date: `{payload.get('date')}`",
        "",
        "## Today, Do This First",
        "",
        f"- Item: `{clean(top.get('carousel_id'))}`",
        f"- Type: `{clean(top.get('item_type'))}`",
        f"- Model: `{clean(top.get('model_profile_id')) or 'n/a'}`",
        f"- Canva template: `{clean(top.get('canva_template_key')) or 'n/a'}` {clean(top.get('canva_template_name'))}",
        f"- Canva template URL: {clean(top.get('canva_template_url')) or 'n/a'}",
        f"- Canva design URL: {clean(top.get('canva_design_url')) or 'n/a'}",
        f"- Stage: `{clean(top.get('stage'))}`",
        f"- Asset: `{clean(top.get('recommended_asset')) or 'n/a'}`",
        f"- Next action: {clean(top.get('next_action'))}",
        "",
        "## Checklist",
        "",
    ]
    for item in checks:
        lines.append(f"- [ ] {item}")
    lines.extend(["", "## Files To Open", ""])
    for path in files:
        lines.append(f"- `{path}`")
    lines.extend(["", "## Reply Template For Codex", "", "```text", reply_template(top), "```", ""])
    return "\n".join(lines)


def build_cockpit(
    runs_dir,
    today,
    today_md,
    today_json,
    queue_md,
    queue_json,
    queue_csv,
    output_html,
    output_md,
):
    payload = build_daily_brief(
        runs_dir,
        today_md,
        today_json,
        today,
        queue_csv=queue_csv,
        queue_md=queue_md,
        queue_json=queue_json,
    )
    output_html = Path(output_html)
    output_md = Path(output_md)
    output_html.write_text(render_html(payload, output_md), encoding="utf-8")
    output_md.write_text(render_markdown(payload), encoding="utf-8")
    return payload


def main():
    parser = argparse.ArgumentParser(description="Build a single daily cockpit page for the Mira workflow.")
    parser.add_argument("--runs-dir", default="10_automation/runs")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--today-md", default="10_automation/TODAY.md")
    parser.add_argument("--today-json", default="10_automation/TODAY.json")
    parser.add_argument("--queue-md", default="10_automation/PUBLISH_QUEUE.md")
    parser.add_argument("--queue-json", default="10_automation/PUBLISH_QUEUE.json")
    parser.add_argument("--queue-csv", default="10_automation/PUBLISH_QUEUE.csv")
    parser.add_argument("--output-html", default="10_automation/DAILY_COCKPIT.html")
    parser.add_argument("--output-md", default="10_automation/DAILY_COCKPIT.md")
    args = parser.parse_args()

    payload = build_cockpit(
        args.runs_dir,
        args.date,
        args.today_md,
        args.today_json,
        args.queue_md,
        args.queue_json,
        args.queue_csv,
        args.output_html,
        args.output_md,
    )
    top = (payload.get("publish_queue") or {}).get("top_item") or {}
    print(f"Cockpit top item: {clean(top.get('carousel_id')) or 'none'}")
    print(f"Wrote {args.output_html}")


if __name__ == "__main__":
    main()
