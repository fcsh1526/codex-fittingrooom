# Automation Hub

Purpose: make the weekly Mika Lin workflow repeatable with less discussion and fewer manual decisions.

The current priority is not monetization. The priority is:

```text
stable character + weekly fashion trend + Grok image prompts + polished Instagram carousel + basic reach test
```

Only after Instagram or another channel gets non-zero reach should affiliate links and product lists become the main work.

## Weekly Inputs

Each week needs these inputs:

1. Perplexity weekly trend URL or CSV.
2. One selected trend / outfit direction.
3. 3-5 Grok output images in Google Drive.
4. One Canva panorama template copy.
5. A final Instagram post URL and metrics after publishing.

## Weekly Outputs

Each week should produce:

1. `weekly_content_packet.csv`
2. 3-5 Grok prompts
3. Canva placeholder values
4. Canva fill guide / placeholder map / asset slots
5. IG carousel caption and hashtags
6. Drive asset inventory
7. Publish record
8. Metrics record

## Files In This Folder

- `mika_weekly.ps1`: Windows PowerShell entrypoint for the main weekly actions.
- `smoke_test_weekly_pipeline.py`: end-to-end smoke test for weekly pipeline, asset selection, metrics decision, and PowerShell entrypoint.
- `weekly_carousel_pipeline.md`: the fixed weekly production workflow.
- `daily_brief.py`: creates `TODAY.md/json` from the dashboard so the next daily action is obvious.
- `prepare_visibility_test.py`: creates a single-image Instagram visibility test package from a run folder.
- `weekly_content_packet_template.csv`: one-row template for a weekly carousel packet.
- `canva_placeholder_values_template.csv`: field values that Codex can paste into Canva.
- `weekly_handoff_checklist.md`: what the user should provide each week.
- `import_perplexity_export.py`: imports a Perplexity CSV or markdown CSV block into `04_prompts/item_prompt_database.csv`.
- `generate_canva_placeholders.py`: converts a weekly content packet CSV into Canva placeholder values.
- `generate_canva_handoff.py`: creates the Canva fill guide, placeholder JSON map, and asset slot CSV.
- `build_weekly_packet.py`: converts rows from `04_prompts/item_prompt_database.csv` into a weekly run folder.
- `select_grok_assets.py`: selects cover/detail/crop assets from Grok review scores and fills Canva asset slots.
- `validate_weekly_run.py`: validates required files, missing fields, disclosure, prompt safety terms, hashtag count, and Canva text length.
- `record_post_metrics.py`: records publish URLs, 6h/24h metrics, and next-action decisions.
- `check_weekly_status.py`: reads a run folder and tells the current stage, blocking items, and next command.
- `weekly_dashboard.py`: scans all weekly run folders and writes a top-level dashboard.
- `run_weekly_pipeline.py`: optional one-command importer + weekly packet builder.

## Recommended Windows Entrypoint

Use `mika_weekly.ps1` for normal work.

Check an existing run:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action status `
  -Week 2026-W21-test
```

Check all runs first when returning after a break:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action dashboard
```

Create today's work brief:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action today
```

This writes:

```text
10_automation/TODAY.md
10_automation/TODAY.json
```

Create a single-image visibility test package:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action visibility-test `
  -Week 2026-W21-test
```

This writes:

```text
10_automation/runs/{week_id}/visibility_test_package.md
10_automation/runs/{week_id}/visibility_test_package.json
```

The dashboard action writes:

```text
10_automation/runs/DASHBOARD.md
10_automation/runs/DASHBOARD.json
```

Create a weekly run from Perplexity:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action pipeline `
  -Week 2026-W25 `
  -PerplexitySource path_or_url_to_perplexity_export `
  -Limit 2
```

Create a weekly run and select Grok assets in the same command:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action pipeline `
  -Week 2026-W21-test `
  -ScoreSheet 07_metrics\w21_visual_review_scores.csv `
  -DriveInventory 07_metrics\w21_drive_image_inventory.csv `
  -Limit 2
```

Record post metrics:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action metrics `
  -Week 2026-W25 `
  -CarouselId 2026-W25-001 `
  -PostUrl "https://www.instagram.com/p/POST_ID/" `
  -PublishedAt "2026/06/18 16:08" `
  -RecordMetrics `
  -MeasuredAt 2026-06-19 `
  -HoursAfterPublish 24 `
  -Reach 0
```

Run a workflow smoke test after pulling changes or moving to another computer:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action smoke-test
```

The smoke test writes only to `tmp/smoke_weekly_pipeline/`.

## Placeholder Generator

Example:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\generate_canva_placeholders.py `
  --input 10_automation\examples\weekly_content_packet_example.csv `
  --output tmp\generated_canva_placeholder_test.csv
```

Expected result:

```text
Wrote 1 row(s) to tmp\generated_canva_placeholder_test.csv
```

## Weekly Packet Builder

Use this when the weekly Perplexity prompts have already been imported into `04_prompts/item_prompt_database.csv`.

Example:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\build_weekly_packet.py `
  --week 2026-W21-test `
  --limit 2 `
  --output-dir 10_automation\runs\2026-W21-test
```

Expected result:

```text
Wrote 2 carousel packet(s) to 10_automation\runs\2026-W21-test
```

Generated files:

- `weekly_content_packet.csv`
- `grok_prompts.md`
- `canva_placeholder_values.csv`
- `canva_fill_guide.md`
- `canva_placeholder_map.json`
- `canva_asset_slots.csv`
- `post_drafts.md`
- `publish_checklist.md`
- `README.md`

## Perplexity Importer

Use this when Perplexity provides a direct CSV export, a downloaded CSV, or a markdown report that contains a fenced CSV block.

Dry run:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\import_perplexity_export.py `
  --source 10_automation\examples\perplexity_export_example.md `
  --week 2026-W25 `
  --dry-run
```

Import:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\import_perplexity_export.py `
  --source path_or_url_to_perplexity_export `
  --week 2026-W25
```

The importer upserts rows by `(week, id)` so re-running the same week replaces that week's matching prompt rows instead of duplicating them.

## One-Command Weekly Pipeline

Use this when a Perplexity export is ready and you want the full weekly packet in one run:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\run_weekly_pipeline.py `
  --week 2026-W25 `
  --perplexity-source path_or_url_to_perplexity_export `
  --limit 2
```

If Grok image scores are already available, include them:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\run_weekly_pipeline.py `
  --week 2026-W21-test `
  --limit 2 `
  --score-sheet 07_metrics\w21_visual_review_scores.csv `
  --drive-inventory 07_metrics\w21_drive_image_inventory.csv
```

Output:

```text
10_automation/runs/2026-W25/
```

The one-command pipeline runs quality validation by default and writes:

```text
quality_report.md
quality_report.json
grok_asset_review_template.csv
grok_asset_selection.csv
canva_asset_plan.md
weekly_status.md
weekly_status.json
```

To validate an existing run folder:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\validate_weekly_run.py `
  --run-dir 10_automation\runs\2026-W21-test `
  --min-rows 2
```

## Grok Asset Selection

After Grok images are reviewed and scored, select Canva-ready assets:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\select_grok_assets.py `
  --run-dir 10_automation\runs\2026-W21-test `
  --score-sheet 07_metrics\w21_visual_review_scores.csv `
  --drive-inventory 07_metrics\w21_drive_image_inventory.csv
```

This writes:

```text
grok_asset_selection.csv
canva_asset_plan.md
```

and updates:

```text
canva_asset_slots.csv
```

Before editing Canva with final image assets, run:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\validate_weekly_run.py `
  --run-dir 10_automation\runs\2026-W21-test `
  --min-rows 2 `
  --require-assets
```

## Publish And Metrics

After publishing, record the post URL:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\record_post_metrics.py `
  --run-dir 10_automation\runs\2026-W25 `
  --week 2026-W25 `
  --carousel-id 2026-W25-001 `
  --platform Instagram `
  --format Carousel `
  --post-url "https://www.instagram.com/p/POST_ID/" `
  --published-at "2026/06/18 16:08"
```

At 6h and 24h, record metrics:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\record_post_metrics.py `
  --run-dir 10_automation\runs\2026-W25 `
  --week 2026-W25 `
  --carousel-id 2026-W25-001 `
  --platform Instagram `
  --format Carousel `
  --post-url "https://www.instagram.com/p/POST_ID/" `
  --published-at "2026/06/18 16:08" `
  --record-metrics `
  --measured-at 2026-06-19 `
  --hours-after-publish 24 `
  --reach 0 `
  --likes 0 `
  --saves 0 `
  --comments 0 `
  --shares 0
```

This writes:

```text
07_metrics/publish_registry.csv
07_metrics/metric_checkpoints.csv
10_automation/runs/{week_id}/publish_status.md
10_automation/runs/{week_id}/publish_status.json
```

## Visibility Test Package

When a post stays at zero reach, create a simpler single-image test package before making another carousel:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\prepare_visibility_test.py `
  --run-dir 10_automation\runs\2026-W21-test
```

The package includes:

- recommended Grok image file and Drive URL
- Instagram caption
- hashtags
- first comment
- Threads backup copy
- 6h / 24h metrics command template

## Weekly Status Check

When returning to the project after a break, start with the all-run dashboard:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\weekly_dashboard.py `
  --runs-dir 10_automation\runs
```

Then open:

```text
10_automation/runs/DASHBOARD.md
```

For the fastest daily workflow, run:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\daily_brief.py `
  --runs-dir 10_automation\runs
```

Then open:

```text
10_automation/TODAY.md
```

When returning to a specific run folder, use:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\check_weekly_status.py `
  --run-dir 10_automation\runs\2026-W21-test
```

This writes:

```text
weekly_status.md
weekly_status.json
```

Use `weekly_status.md` as the current source of truth for the next action.

## Operating Rule

Do not rebuild the workflow every week.

Every week should follow:

```text
Perplexity -> prompt packet -> Grok images -> Canva carousel -> IG post -> metrics -> decide next test
```
