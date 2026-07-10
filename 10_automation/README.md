# Automation Hub

Purpose: make the weekly Mira workflow repeatable with less discussion and fewer manual decisions.

Primary command center:

```text
../COMMAND_CENTER.md
```

The current priority is continuous production, not monetization. Mira is now treated as a fast-updating AI fashion magazine brand, not one public virtual influencer. The priority is:

```text
weekly fashion trend + 5-post daily outfit queue + M01-M05 weekly model rotation + Codex image brief + Canva carousel + basic reach test
```

Only after Instagram or another channel gets non-zero reach should affiliate links and product lists become the main work.

Production rule:

```text
zero reach does not stop carousel production
```

## Weekly Inputs

Each week needs these inputs:

1. Perplexity weekly trend URL or CSV.
2. Five selected trend / outfit directions for five daily carousels.
3. 2-4 Codex-generated or manually approved image candidates in the run folder.
4. One Canva panorama template or Canva brand template.
5. A final Instagram post URL and metrics after publishing.

## Weekly Outputs

Each week should produce:

1. `weekly_content_packet.csv`
2. Daily queue and image-generation briefs
3. Per-carousel Codex image job folders and generation handoffs
4. Canva placeholder values
5. Canva fill guide / placeholder map / asset slots
6. IG carousel caption and hashtags
7. Image review template and selected asset plan
8. Publish record
9. Metrics record

## Files In This Folder

- `mika_weekly.ps1`: Windows PowerShell entrypoint for the main weekly actions.
- `AUTOMATION_ARCHITECTURE_BRIEF.md`: slide-style briefing for the current automation architecture and boundaries.
- `smoke_test_weekly_pipeline.py`: end-to-end smoke test for weekly pipeline, asset selection, metrics decision, and PowerShell entrypoint.
- `weekly_carousel_pipeline.md`: the fixed weekly production workflow.
- `canva_connector_workflow.md`: how Codex should use the Canva connector for template edits and preview approval.
- `canva_template_registry.md` / `canva_template_registry.json`: active Mira Canva master template URLs, use cases, and automation slot contract.
- `instagram_visual_direction.md`: current low-text, image-led IG direction.
- `daily_cockpit.py`: creates the one-page daily HTML cockpit.
- `daily_brief.py`: creates `TODAY.md/json` from the dashboard so the next daily action is obvious.
- `publish_queue.py`: creates a per-carousel and visibility-test publish queue.
- `sync_canva_placeholder_map.py`: regenerates `canva_placeholder_map.json` from clean placeholder CSV and current asset slots.
- `../11_skills/mira-image-daily/scripts/prepare_daily_image_job.py`: prepares strict daily image jobs from approved M01-M05 reference anchors.
- `prepare_visibility_test.py`: creates a single-image Instagram visibility test package from a run folder.
- `weekly_content_packet_template.csv`: one-row template for a weekly carousel packet.
- `canva_placeholder_values_template.csv`: field values that Codex can paste into Canva.
- `weekly_handoff_checklist.md`: what the user should provide each week.
- `import_perplexity_export.py`: imports a Perplexity CSV or markdown CSV block into `04_prompts/item_prompt_database.csv`.
- `resolve_perplexity_source.py`: resolves the latest or requested weekly CSV from the Perplexity public index.
- `generate_canva_placeholders.py`: converts a weekly content packet CSV into Canva placeholder values.
- `generate_canva_handoff.py`: creates the Canva fill guide, placeholder JSON map, and asset slot CSV.
- `build_weekly_packet.py`: converts rows from `04_prompts/item_prompt_database.csv` into a weekly run folder.
- `generate_openai_images.py`: optional future API path for OpenAI image assets; not the current primary flow.
- `select_codex_assets.py`: selects cover/detail/crop assets from scored Codex review sheets and fills Canva asset slots.
- `select_grok_assets.py`: legacy compatibility module used internally by the Codex selector; do not use it as the active workflow entrypoint.
- `validate_weekly_run.py`: validates required files, missing fields, disclosure, prompt safety terms, hashtag count, and Canva text length.
- `record_post_metrics.py`: records publish URLs, 6h/24h metrics, and next-action decisions.
- `check_weekly_status.py`: reads a run folder and tells the current stage, blocking items, and next command.
- `weekly_dashboard.py`: scans all weekly run folders and writes a top-level dashboard.
- `run_weekly_pipeline.py`: optional one-command importer + weekly packet builder.

## Recommended Windows Entrypoint

Use `mika_weekly.ps1` for normal work.

If the overall system feels unclear, start with:

```text
10_automation/AUTOMATION_ARCHITECTURE_BRIEF.md
```

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

Create today's cockpit:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action cockpit `
  -TodayDate 2026-06-22
```

This writes:

```text
10_automation/DAILY_COCKPIT.html
10_automation/DAILY_COCKPIT.md
10_automation/TODAY.md
10_automation/PUBLISH_QUEUE.md
```

Prepare a daily image job:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action image-job `
  -Week 2026-W26 `
  -CarouselId 2026-W26-002 `
  -AssetProvider Codex
```

Regenerate Canva machine placeholder map from clean CSV:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action sync-canva-map `
  -Week 2026-W26
```

Create today's work brief and cockpit:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action today `
  -TodayDate 2026-06-22
```

This writes:

```text
10_automation/DAILY_COCKPIT.html
10_automation/DAILY_COCKPIT.md
10_automation/TODAY.md
10_automation/TODAY.json
```

Create the publish queue only:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action queue
```

This writes:

```text
10_automation/PUBLISH_QUEUE.md
10_automation/PUBLISH_QUEUE.json
10_automation/PUBLISH_QUEUE.csv
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

Use the saved Perplexity public weekly index instead of pasting a CSV URL:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action pipeline `
  -Week 2026-WXX `
  -UsePerplexityIndex `
  -Limit 2
```

Default index:

```text
https://mika-lin-weekly.pplx.app/data/index.json
```

Create a weekly run and select scored assets in the same command:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action pipeline `
  -Week 2026-W21-test `
  -ScoreSheet 07_metrics\w21_visual_review_scores.csv `
  -DriveInventory 07_metrics\w21_drive_image_inventory.csv `
  -Limit 2
```

Optional future path: plan OpenAI image generation without spending API credits:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action generate-images `
  -Week 2026-W25 `
  -ImageVariants 2 `
  -DryRunImages
```

Optional future path: generate OpenAI images after setting `OPENAI_API_KEY`:

```powershell
$env:OPENAI_API_KEY="YOUR_API_KEY"
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action generate-images `
  -Week 2026-W25 `
  -ImageVariants 2 `
  -ImageQuality medium
```

Current path: use `image_generation_briefs.md` to create candidates in `generated_images/`, score them in `image_review_template.csv`, then select Canva assets:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action assets `
  -Week 2026-W25 `
  -AssetProvider Codex `
  -ScoreSheet 10_automation\runs\2026-W25\image_review_template.csv
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
Wrote 2 carousel packet(s) and 5 daily item(s) to 10_automation\runs\2026-W21-test
```

Generated files:

- `weekly_content_packet.csv`
- `daily_queue.csv`
- `image_generation_briefs.md`
- `image_review_template.csv`
- `generated_images/`
- `grok_prompts.md` as a legacy backup prompt file
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

If Codex image scores are already available, include them:

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
daily_queue.csv
image_generation_briefs.md
image_review_template.csv
generated_images/{carousel_id}/codex_generation_handoff.md
generated_images/{carousel_id}/candidate_prompts.md
generated_images/{carousel_id}/review_sheet.csv
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

## Image Generation

The current primary flow is Codex workspace image generation plus semi-manual review:

1. Open `daily_queue.csv` to see today's outfit and `model_profile_id`.
2. Open `02_brand/mira_image_generation_spec_v1.md` for the shared image standard.
3. Open `image_generation_briefs.md` for the run-specific image brief.
4. For W26 M02 testing, open `10_automation/runs/2026-W26/m02_polka_image_test_brief.md`.
5. Generate or place candidate images in `generated_images/`.
6. Score candidates in `image_review_template.csv`.
7. Run asset selection with `--provider Codex`.

Reject images that feel like a runway, luxury hotel ad, over-posed influencer shoot, plastic skin, or distant supermodel styling. Keep the outfit clear, daily, Taiwan-relevant, and easy to imagine buying.

OpenAI remains an optional future API path when budget is available.

Dry run first:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\generate_openai_images.py `
  --run-dir 10_automation\runs\2026-W25 `
  --variants 2 `
  --dry-run
```

This writes:

```text
openai_prompts/
openai_image_inventory.csv
openai_asset_review_template.csv
```

When `OPENAI_API_KEY` is set, remove `--dry-run` to generate image files into:

```text
10_automation/runs/{week_id}/openai_images/
```

Keep all Chinese carousel text in Canva text layers. Do not ask the image model to render Chinese titles or CTAs inside the image.

## Asset Selection

After Codex images are reviewed and scored, select Canva-ready assets:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\select_codex_assets.py `
  --run-dir 10_automation\runs\2026-W21-test `
  --provider Codex `
  --score-sheet 10_automation\runs\2026-W21-test\image_review_template.csv
```

This writes:

```text
codex_asset_selection.csv
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

When a post stays at zero reach, create a simpler single-image test package as a side test. Continue producing carousels:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\prepare_visibility_test.py `
  --run-dir 10_automation\runs\2026-W21-test
```

The package includes:

- recommended image file and asset URL when available
- Instagram caption
- hashtags
- first comment
- Threads backup copy
- 6h / 24h metrics command template

## Publish Queue

The publish queue is the per-content source of truth. It includes both normal carousels and visibility tests:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\publish_queue.py `
  --runs-dir 10_automation\runs
```

Open:

```text
10_automation/PUBLISH_QUEUE.md
```

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
Perplexity -> daily queue -> Codex image candidates -> review -> Canva carousel -> IG post -> metrics -> decide next test
```

Codex workspace image generation is the primary image path. OpenAI API remains an optional future automation path; Grok is legacy historical data and is not part of the active workflow.
