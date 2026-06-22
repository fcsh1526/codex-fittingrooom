# Weekly Carousel Pipeline

This is the fixed workflow for producing polished Instagram carousel content.

For normal Windows use, prefer:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit
```

After pulling changes or switching computers, run:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action smoke-test
```

## Stage 1 - Trend Input

User provides either:

```text
Perplexity weekly page URL
```

or

```text
Perplexity CSV / markdown report
```

Codex imports with:

```text
10_automation/import_perplexity_export.py
```

Then Codex extracts:

- week id
- trend name
- audience
- occasion
- clothing item
- color palette
- fabric
- fit
- styling rules
- shopping keywords

Output:

```text
10_automation/runs/{week_id}/weekly_content_packet.csv
```

filled for the current week.

## Stage 2 - Prompt Selection

Pick one primary outfit direction per carousel.

Selection rules:

- prioritize clear full-body outfits
- prioritize Taiwan-relevant daily usage
- avoid purely editorial looks until there is reach
- avoid hard-to-buy product concepts
- keep the outfit explainable in one sentence

## Stage 3 - Grok Prompting

Use:

```text
10_automation/runs/{week_id}/grok_prompts.md
```

with the Mika Lin identity block and generate 3-5 image variants.

Prompt must include:

- fictional AI virtual creator
- same identity
- full outfit visible
- no logos
- practical Taiwan setting
- no sexualized pose
- no celebrity likeness

Preferred scenes while reach is low:

- office lobby
- MRT-adjacent walkway
- cafe street
- department store fitting area
- simple studio wall

Avoid for now:

- European resort background
- runway stage
- luxury logo setting
- abstract editorial scene

## Stage 4 - Image Review

Score each image:

```text
identity_consistency
outfit_clarity
body_integrity
platform_fit
shopping_value
```

Pick:

- 1 cover image
- 1 detail / full-body backup
- 1 optional alternate

If a score sheet exists, select assets automatically:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\select_grok_assets.py `
  --run-dir 10_automation\runs\{week_id} `
  --score-sheet path_to_visual_review_scores.csv `
  --drive-inventory path_to_drive_image_inventory.csv
```

Output:

- `grok_asset_selection.csv`
- `canva_asset_plan.md`
- updated `canva_asset_slots.csv`

## Stage 5 - Canva Carousel

Use a Canva panorama design:

```text
5400 x 1350
```

Export target:

```text
5 slides, each 1080 x 1350
```

Required placeholder fields:

```text
slide1_title
slide1_subtitle
slide1_disclosure
slide2_kicker
slide2_title
slide2_body
slide3_kicker
slide3_title
slide3_body
slide4_kicker
slide4_title
slide4_body
slide5_title
slide5_cta
slide5_note
slide5_disclosure
```

Weekly Canva handoff files:

```text
10_automation/runs/{week_id}/canva_fill_guide.md
10_automation/runs/{week_id}/canva_placeholder_map.json
10_automation/runs/{week_id}/canva_asset_slots.csv
```

Use `canva_fill_guide.md` for manual copy/paste today. Use `canva_placeholder_map.json` as the future Canva plugin automation input.

## Stage 6 - Instagram Publish

Use:

```text
10_automation/runs/{week_id}/post_drafts.md
10_automation/runs/{week_id}/publish_checklist.md
```

While the account has little or zero reach, prefer:

- one clear outfit concept
- short caption
- direct comment CTA
- 8-12 hashtags
- first comment added immediately
- one Story share after publishing

Do not add affiliate links until there is non-zero reach.

## Stage 7 - Metrics

Record after 6 hours and 24 hours:

```text
reach
likes
saves
comments
shares
profile_visits
new_followers
cta_comments
```

Use:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\record_post_metrics.py `
  --run-dir 10_automation\runs\{week_id} `
  --week {week_id} `
  --carousel-id {carousel_id} `
  --platform Instagram `
  --format Carousel `
  --post-url "https://www.instagram.com/p/POST_ID/" `
  --published-at "YYYY/MM/DD HH:mm" `
  --record-metrics `
  --measured-at YYYY-MM-DD `
  --hours-after-publish 24 `
  --reach 0 `
  --likes 0 `
  --saves 0 `
  --comments 0 `
  --shares 0
```

Decision rule:

- `reach = 0`: record zero-reach recovery as a side test, but keep carousel production moving
- `reach > 0 but saves = 0`: adjust hook / visual clarity
- `saves > 0`: make a second carousel in same bucket
- `comments > 0`: prepare product list / reply flow

## One-Command Weekly Pipeline

If the Perplexity export is ready, run the full pipeline:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\run_weekly_pipeline.py `
  --week 2026-W25 `
  --perplexity-source path_or_url_to_perplexity_export `
  --limit 2
```

If scored Grok images are already available, add:

```text
--score-sheet path_to_visual_review_scores.csv
--drive-inventory path_to_drive_image_inventory.csv
```

The pipeline will then select cover/detail assets, validate with `--require-assets`, and write `weekly_status.md`.

If the weekly rows are already imported into `04_prompts/item_prompt_database.csv`, generate only the weekly run folder:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\build_weekly_packet.py `
  --week 2026-W21-test `
  --limit 2 `
  --output-dir 10_automation\runs\2026-W21-test
```

This creates:

- `weekly_content_packet.csv`
- `grok_prompts.md`
- `canva_placeholder_values.csv`
- `canva_fill_guide.md`
- `canva_placeholder_map.json`
- `canva_asset_slots.csv`
- `post_drafts.md`
- `publish_checklist.md`
- `quality_report.md`
- `quality_report.json`
- `README.md`

The quality report must pass before producing Grok images or editing Canva.

After Grok assets are selected, run validation with:

```text
--require-assets
```

## Resume Rule

Whenever work resumes after a break, create the daily brief first:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit
```

Then open:

```text
10_automation/DAILY_COCKPIT.html
10_automation/TODAY.md
10_automation/PUBLISH_QUEUE.md
```

Use `PUBLISH_QUEUE.md` to decide the exact next content item. It tracks normal carousels and single-image visibility tests separately.

If you need the raw all-run dashboard, run:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\weekly_dashboard.py `
  --runs-dir 10_automation\runs
```

If the dashboard shows `visibility_recovery`, keep carousel production moving. Use the visibility package only as a side test:

```text
05_content/2026_06_18_reactivation_plan.md
```

Generate or refresh the single-image test package when useful:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action visibility-test -Week {week_id}
```

Use:

```text
10_automation/runs/{week_id}/visibility_test_package.md
```

For a specific run, check the current stage with:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\check_weekly_status.py `
  --run-dir 10_automation\runs\{week_id}
```

Then follow `weekly_status.md`.
