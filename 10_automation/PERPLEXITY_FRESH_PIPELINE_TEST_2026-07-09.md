# Perplexity Fresh Pipeline Test - 2026-07-09

Purpose: verify a clean weekly run from the Perplexity public index into Codex image handoffs.

## Result

Status: `pass with external data caveat`

The automation now works from:

```text
Perplexity public index -> CSV import -> weekly packet -> daily queue -> Codex image job folders -> publish queue / cockpit
```

## External Data Caveat

The Perplexity public index currently resolves latest to:

```text
week = 2026-W26
csv = https://mika-lin-weekly.pplx.app/data/2026-W26.csv
```

As of 2026-07-09, there is no newer `2026-W28` row in the public index. A true new-week production run requires Perplexity to publish/update the weekly site first.

## Test Command

The clean-room test was run under `tmp/` so it did not overwrite the existing W26 run:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action pipeline `
  -UsePerplexityIndex `
  -Limit 2 `
  -RunDir tmp\fresh_perplexity_pipeline_v2\run `
  -Database tmp\fresh_perplexity_pipeline_v2\item_prompt_database.csv
```

## Verified Outputs

```text
weekly_content_packet.csv
daily_queue.csv
image_generation_briefs.md
image_review_template.csv
generated_images/2026-W26-001/codex_generation_handoff.md
generated_images/2026-W26-001/candidate_prompts.md
generated_images/2026-W26-001/review_sheet.csv
generated_images/2026-W26-002/codex_generation_handoff.md
generated_images/2026-W26-002/candidate_prompts.md
generated_images/2026-W26-002/review_sheet.csv
weekly_status.md
```

Fresh cockpit test also passed. The top item package pointed to:

```text
tmp\fresh_perplexity_pipeline_v2\run\generated_images\2026-W26-002\codex_generation_handoff.md
```

## Fix Applied

- `run_weekly_pipeline.py` can now omit `--week` when `--use-perplexity-index` is set.
- `mika_weekly.ps1 -Action pipeline -UsePerplexityIndex` no longer requires `-Week`.
- Weekly pipeline now prepares per-carousel Codex image job folders by default.
- `prepare_daily_image_job.py` now writes `codex_generation_handoff.md`.
- Smoke test now checks for the Codex generation handoff.

## Next Production Rule

Before running a real new week, check the latest Perplexity index:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\resolve_perplexity_source.py `
  --index https://mika-lin-weekly.pplx.app/data/index.json `
  --json
```

If the returned week is not the intended current week, update the Perplexity weekly site first.
