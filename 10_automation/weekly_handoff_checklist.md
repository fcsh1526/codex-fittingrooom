# Weekly Handoff Checklist

When restarting work in Codex, paste this information:

```text
Week ID:
Perplexity weekly URL / CSV / markdown export:
Chosen trend / outfit:
Google Drive folder with Grok images:
Canva design URL:
Instagram account status:
Last post reach:
Anything stuck:
```

## Minimum Required To Continue

Codex can continue with only:

```text
Week ID
Perplexity weekly URL / CSV / markdown export
```

If the Perplexity export is ready, Codex should run:

```text
10_automation/run_weekly_pipeline.py
```

and produce the weekly Grok prompts, Canva placeholders, platform drafts, and publish checklist.

If visual review scores and Drive inventory are also ready, pass them into `run_weekly_pipeline.py` so it can select assets and write `weekly_status.md` in the same run.

When a run folder already exists, Codex should first run:

```text
10_automation/check_weekly_status.py
```

and follow `weekly_status.md`.

Before image production, confirm:

```text
quality_report.md status = pass
```

## If Canva Template Is Ready

Codex should use:

- `canva_fill_guide.md` for manual text replacement.
- `canva_placeholder_map.json` for plugin-based replacement later.
- `canva_asset_slots.csv` to decide which Grok image goes where.
- `canva_asset_plan.md` after Grok images have been scored and selected.

## If Grok Images Are Ready

Codex should ask for or produce:

- Drive image inventory
- visual review score sheet
- `grok_asset_selection.csv`
- updated `canva_asset_slots.csv`

Before Canva editing:

```text
validate_weekly_run.py --require-assets
```

## If Grok Images Are Not Ready

Codex should output:

- `grok_prompts.md`
- one recommended cover concept
- `canva_placeholder_values.csv`
- `post_drafts.md`
- `publish_checklist.md`

## If Canva Is Not Ready

Codex should output:

- 5-slide placeholder values
- layout notes for `5400 x 1350`
- short IG caption
- Canva asset slots

## If IG Reach Is Still Zero

Do not start affiliate links.

Run:

```text
09_sops/instagram_zero_reach_recovery.md
```

## If A Post Was Published

Paste:

```text
Week ID:
Carousel ID:
Post URL:
Published at:
6h metrics:
24h metrics:
```

Codex should run:

```text
10_automation/record_post_metrics.py
```

and check `publish_status.md` for the next action.
