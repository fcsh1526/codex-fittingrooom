# 2026-W25 Work Order

Created: 2026-06-18

Purpose: restart the project with a more automated weekly carousel workflow.

## Current Priority

Produce a steady stream of polished Instagram carousel posts before monetization.

Do not prioritize affiliate links until reach is non-zero.

Because the first Instagram post stayed at zero reach for 10+ days, keep a visibility test running in parallel:

```text
continue carousel production -> optionally publish one simple single-image test -> record 6h/24h metrics when available
```

Do not wait for non-zero reach before producing the next polished carousel.

## Required Inputs From User

Paste these when ready:

```text
Perplexity weekly URL:
Google Drive folder for Grok images:
Canva panorama design URL:
Instagram account visibility status:
```

## If Perplexity URL Is Available

Codex should:

1. Extract 5 trends.
2. Pick 1-2 carousel candidates.
3. Run `10_automation/run_weekly_pipeline.py` if a CSV / markdown export is available.
4. Otherwise import selected rows into `04_prompts/item_prompt_database.csv`.
5. Use the generated `grok_prompts.md`, `canva_placeholder_values.csv`, `post_drafts.md`, and `publish_checklist.md`.

## If Grok Images Are Available

Codex should:

1. List the Drive folder.
2. Build an image inventory.
3. Review image quality.
4. Pick the cover and detail assets.
5. Update the weekly content packet.

## If Canva Design Is Available

Codex should:

1. Read placeholder fields.
2. Replace placeholder text.
3. Show preview.
4. Ask user before saving.
5. Record the final Canva URL.

## Current Automation Command

Start here after returning from a break:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit
```

Then open:

```text
10_automation/DAILY_COCKPIT.html
10_automation/TODAY.md
10_automation/PUBLISH_QUEUE.md
```

If today is a visibility recovery day, keep using the publish queue. The visibility package is optional side evidence:

```text
10_automation/runs/{week_id}/visibility_test_package.md
```

Full import + packet build example:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\run_weekly_pipeline.py `
  --week 2026-W25 `
  --perplexity-source path_or_url_to_perplexity_export `
  --limit 2
```

Packet-only example:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\build_weekly_packet.py `
  --week 2026-W21-test `
  --limit 2 `
  --output-dir 10_automation\runs\2026-W21-test
```

Generated files:

```text
weekly_content_packet.csv
grok_prompts.md
canva_placeholder_values.csv
post_drafts.md
publish_checklist.md
README.md
```

## If Instagram Still Has Zero Reach

Publish a simpler second test as a side check, but do not pause panorama carousel production.

Use:

```text
05_content/second_test_zero_reach_post.md
05_content/2026_06_18_reactivation_plan.md
09_sops/instagram_zero_reach_recovery.md
10_automation/runs/{week_id}/visibility_test_package.md
```

## Done Criteria For This Week

Minimum:

```text
1 polished carousel or simple second-test post published
metrics recorded after 24 hours
reach status known
```

Better:

```text
2 posts published
at least one post reaches 20+ people
one repeatable Canva template validated
```
