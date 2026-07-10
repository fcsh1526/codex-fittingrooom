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

If no weekly CSV URL is pasted, use the saved public index:

```text
https://mika-lin-weekly.pplx.app/data/index.json
```

Codex imports with:

```text
10_automation/import_perplexity_export.py
```

or resolves the CSV from the saved index with:

```text
10_automation/resolve_perplexity_source.py
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
- model_profile_id

Output:

```text
10_automation/runs/{week_id}/weekly_content_packet.csv
10_automation/runs/{week_id}/daily_queue.csv
```

filled for the current week.

## Stage 2 - Daily Queue And Model Selection

Pick 5-7 outfit directions for the week, then prepare one daily outfit at a time.

Selection rules:

- prioritize clear full-body outfits
- prioritize Taiwan-relevant daily usage
- avoid purely editorial looks until there is reach
- avoid hard-to-buy product concepts
- keep the outfit explainable in one sentence
- keep the outfit context independent from the internal model profile

Internal model age cohorts:

```text
M01 true age 25 -> prompt visual age: early 20s
M02 true age 35 -> prompt visual age: late 20s, youthful
M03 true age 45 -> prompt visual age: mid 30s look, well-maintained
M04 true age 55 -> prompt visual age: early 40s look, elegant
M05 true age 20 -> prompt visual age: around 20, youthful adult
```

True ages stay in roster metadata only. Image prompts must express age through styling and presence, not wrinkles, and must use the prompt visual-age language rather than numeric true ages.

Content buckets still describe outfit context, such as `office_capsule`, `date_outfit`, `weekend_daily`, `daily_style`, and `rainy_day`, but they no longer decide the model. The packet builder assigns all five internal models exactly once per 5-post week using a reproducible shuffled order. Perplexity rows provide outfit topics and styling inputs only; source `model_profile_id` values are ignored to protect weekly model coverage.

Do not publish model names. They are internal controls for visual consistency only.

## Stage 3 - Image Generation Briefs

The current primary path is Codex workspace image generation plus semi-manual review. Start from:

```text
10_automation/runs/{week_id}/daily_queue.csv
10_automation/runs/{week_id}/image_generation_briefs.md
```

For each daily outfit, generate or place image candidates into:

```text
10_automation/runs/{week_id}/generated_images/
```

Each brief combines:

- `model_profile_id`
- trend / clothing item
- occasion
- Taiwan-relevant daily setting
- outfit clarity requirements
- visual rejection rules

OpenAI API remains an optional future path when budget is available. Dry run first, which costs nothing:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action generate-images `
  -Week {week_id} `
  -ImageVariants 2 `
  -DryRunImages
```

After setting `OPENAI_API_KEY`, generate the image files:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action generate-images `
  -Week {week_id} `
  -ImageVariants 2 `
  -ImageQuality medium
```

Outputs:

- `openai_prompts/`
- `openai_images/`
- `openai_image_inventory.csv`
- `openai_asset_review_template.csv`

Keep Chinese titles, CTAs, and AI disclosure in Canva text layers. Do not render them into the image.

No product list, comment CTA, AI disclosure, or template instruction text should appear inside the image.

Codex prompts must include:

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
model_consistency
reader_relatability
outfit_clarity
ai_realism
commerce_value
```

Pick:

- 1 cover image
- 1 detail / full-body backup
- 1 optional alternate

If a score sheet exists, select assets automatically:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\select_codex_assets.py `
  --run-dir 10_automation\runs\{week_id} `
  --provider Codex `
  --score-sheet 10_automation\runs\{week_id}\image_review_template.csv
```

Output:

- `{provider}_asset_selection.csv`
- `canva_asset_plan.md`
- updated `canva_asset_slots.csv`

## Stage 5 - Canva Carousel

Use a Canva panorama design:

```text
3240 x 1350
```

Export target:

```text
3 slides, each 1080 x 1350
```

Required placeholder fields:

```text
slide2_line
```

Slide roles:

- Slide 1: image-led hook, no required text.
- Slide 2: one short transition sentence.
- Slide 3: image-led ending, no CTA wall.

Keep AI disclosure in the caption, not on the image.

Weekly Canva handoff files:

```text
10_automation/runs/{week_id}/canva_fill_guide.md
10_automation/runs/{week_id}/canva_placeholder_map.json
10_automation/runs/{week_id}/canva_asset_slots.csv
```

Use `canva_fill_guide.md` for manual copy/paste if needed. The Canva connector can also replace text and image fills from `canva_placeholder_map.json` and `canva_asset_plan.md`, then show thumbnails for approval before saving.

Final Canva export must remove template labels, cut-line text, product list text, comment CTA, and AI disclosure from the image. Only imagery, `{{slide2_line}}`, and small `Mira` brand text should remain.

## Stage 6 - Instagram Publish

Use:

```text
10_automation/runs/{week_id}/post_drafts.md
10_automation/runs/{week_id}/publish_checklist.md
```

While the account has little or zero reach, prefer:

- one clear outfit concept
- short caption
- profile-link shopping direction
- 8-12 hashtags
- one Story share after publishing

Do not make the carousel itself look like a shopping catalog until reach and click behavior are clearer.

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

If scored images are already available, add:

```text
--asset-provider Codex
--score-sheet path_to_visual_review_scores.csv
--drive-inventory path_to_image_inventory.csv
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
- `daily_queue.csv`
- `image_generation_briefs.md`
- `image_review_template.csv`
- `generated_images/{carousel_id}/codex_generation_handoff.md`
- `generated_images/{carousel_id}/candidate_prompts.md`
- `generated_images/{carousel_id}/review_sheet.csv`
- `grok_prompts.md` legacy backup prompt file
- `canva_placeholder_values.csv`
- `canva_fill_guide.md`
- `canva_placeholder_map.json`
- `canva_asset_slots.csv`
- `post_drafts.md`
- `publish_checklist.md`
- `quality_report.md`
- `quality_report.json`
- `README.md`

The quality report must pass before image generation or editing Canva.

After image assets are selected, run validation with:

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
