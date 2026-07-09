# Current Status - Mira AI Fashion Creator

Last updated: 2026-07-09

## Project Goal

Build a repeatable AI fashion magazine workflow: global fashion trend research, localized Traditional Chinese publishing, and daily outfit images with consistent internal models.

Current priority:

```text
global weekly trend -> daily outfit queue -> internal model profile -> approved reference start image -> Codex image job -> minimal Canva carousel -> Instagram post -> metrics
```

Latest automation test:

```text
2026-07-09 fresh Perplexity pipeline test passed in tmp/fresh_perplexity_pipeline_v2.
Perplexity public index currently resolves latest to 2026-W26, so a true new-week run is blocked until Perplexity publishes a newer weekly row.
```

Monetization is intentionally delayed until there is non-zero reach.

Today's priority:

```text
use approved M01-M05 reference anchors -> generate daily outfit images -> choose one registered Canva master template -> duplicate/fill/export
```

## Current Stage

Mira AI outfit daily system v2, now controlled from `COMMAND_CENTER.md`.

Mira is no longer treated as one public virtual person. The brand is a fast-updating AI fashion magazine with 5 fixed internal models: M01, M02, M03, M04, and M05. Model names stay internal; IG should feel like a polished magazine with familiar recurring people, not a virtual influencer roleplay account.

Production rule:

```text
Zero reach does not block the next carousel.
```

Current image source rule:

```text
Use the installed $mira-image-daily skill first. Daily outfit generation is blocked until the assigned model has an approved reference start image. Codex workspace image generation is the primary path. Grok is not part of the active workflow.
```

Current validation rule:

```text
Smoke test verifies automation entrypoints.
Strict W26 validation verifies production readiness.
It is expected to fail until current W26 blockers are fixed.
```

## Key Links

- GitHub repo: https://github.com/fcsh1526/codex-fittingrooom
- Perplexity weekly site: https://mika-lin-weekly.pplx.app/
- W21 test page: https://mika-lin-weekly.pplx.app/weeks/2026-W21-test.html
- W21 CSV: https://mika-lin-weekly.pplx.app/data/2026-W21-test.csv
- Canva panorama carousel design: https://www.canva.com/d/jJOq1Yimawt9wfU
- Legacy Mira Canva v2 single template: https://www.canva.com/design/DAHOIZe_Qz0/YjBO1NIF7JQ0VsRyrVRaew/edit
- Mira Canva template registry: `10_automation/canva_template_registry.md`
- Mira Template Master - A Contact Sheet: https://www.canva.com/design/DAHOx6hb1Ug/A1sysuKRtad0lCYR8jqBQg/edit
- Mira Template Master - B Symmetric: https://www.canva.com/design/DAHOxwp1cZ8/cIfSmcVa-DAJJrT-21PJoA/edit
- Mira Template Master - C Noir Evening: https://www.canva.com/design/DAHOyEHkFvg/DBpyigPr05vQqxuuqV7wKA/edit
- Mira Template Master - D Full-Bleed: https://www.canva.com/design/DAHOyNz_Dh4/SCdZqafV5zkpK5TVIB6kMw/edit
- Mira Template Master - E Weekend Air: https://www.canva.com/design/DAHOyEiLL24/yTWykrCQdrFjncOa46cq9g/edit
- Published IG carousel: https://www.instagram.com/p/DZCTbtWGuhx/?igsh=aG9kcjl3OWIybm01
- Published asset Drive folder: https://drive.google.com/drive/folders/1tRiBkj2JbAiuv6Ol88Jx6-FpF2a6nKml

## Completed

- Perplexity W21 test report was validated.
- 20 W21 prompt rows were imported into `04_prompts/item_prompt_database.csv`.
- Day 3 Grok prompt set was created.
- W21 Grok images were reviewed.
- Canva plugin was enabled in Codex.
- Old Canva panorama carousel template was tested at `5400 x 1350`.
- New Canva direction is `3240 x 1350`, exported as 3 image-led slides.
- First Instagram carousel was published.
- 24-hour and 10+ day zero-reach status were recorded.
- Instagram zero-reach recovery SOP was created.
- A second simple test post was drafted.
- Automation hub was created in `10_automation/`.
- Weekly packet builder was tested and generated `10_automation/runs/2026-W21-test/`.
- Weekly run folder now includes daily queue, image briefs, legacy Grok prompts, Canva placeholders, platform post drafts, and publish checklist.
- Perplexity import automation now supports CSV files, direct CSV URLs, and markdown reports with fenced CSV blocks.
- One-command weekly pipeline was tested with `10_automation/examples/perplexity_export_example.md`.
- Weekly run quality validation now checks required files, required fields, model profile ids, AI disclosure, prompt safety terms, hashtag count, and Canva text length.
- Canva handoff automation now generates `canva_fill_guide.md`, `canva_placeholder_map.json`, and `canva_asset_slots.csv`.
- Asset selection automation now fills cover/detail/crop asset slots from visual review scores and optional Drive inventory.
- Publish and metrics automation now records post URLs, 6h/24h metrics, and next-action decisions.
- Weekly status automation now writes `weekly_status.md/json` and tells the next action for each run folder.
- Weekly dashboard automation now scans all run folders and writes `10_automation/runs/DASHBOARD.md/json`.
- Daily brief automation now writes `10_automation/TODAY.md/json` and translates dashboard status into today's 1-3 tasks.
- Daily cockpit automation now writes `10_automation/DAILY_COCKPIT.html/md` as the main daily-use artifact.
- Publish queue automation now writes `10_automation/PUBLISH_QUEUE.md/json/csv` and tracks each carousel / visibility test separately.
- Visibility test automation now writes `visibility_test_package.md/json` for single-image Instagram recovery tests.
- Main weekly pipeline now creates daily queue, image review, and status files by default and can select scored assets when score sheets are provided.
- Windows shortcut `10_automation/mika_weekly.ps1` now wraps pipeline, status, dashboard, queue, today, visibility-test, assets, metrics, and validate actions.
- Smoke test automation now verifies weekly pipeline, asset selection, metrics decisions, dashboard output, daily brief output, publish queue output, visibility test package output, and PowerShell entrypoint.
- Daily heartbeat was updated from old Day X companionship to queue-based automation status checking.
- Automation architecture brief was added to explain the current state machine and manual boundaries.
- Cross-computer handoff was added in `COMPUTER_B_SYNC.md` so Computer B can continue from GitHub without reading the old conversation.
- OpenAI image-generation automation exists as an optional future API path.
- Asset selection now supports provider labels such as Codex and OpenAI; old Grok files are legacy historical data only.
- Perplexity public index resolution was added, so Codex can use the saved weekly site instead of requiring a pasted CSV URL every time.
- Instagram creative direction changed to 3-slide, image-led, low-text carousel posts with simple captions and profile-link shopping direction.
- Canva connector workflow and template spec were simplified to one text placeholder: `{{slide2_line}}`.
- Mira was renamed from Mika and repositioned as an AI fashion magazine brand.
- Internal model roster v6 now uses 5 fixed model identities: `M01`, `M02`, `M03`, `M04`, and `M05`, with true ages kept as internal metadata and prompt-safe visual-age language used for image generation.
- Mira image generation was changed from Taiwan-only wording to global trend research with wearable daily styling.
- `$mira-image-daily` skill was created and installed to `C:\Users\Brandon_ChangChien\.codex\skills\mira-image-daily`.
- Reference start image manifest was added at `02_brand/mira_reference_images.csv`; M01/M02/M03/M04/M05 are approved for reference-start checks.
- Reference pack manifest was added at `02_brand/mira_reference_packs.csv`; all 20 pack entries are approved across full-body, half-body, face-front, 3/4 face, and side-profile.
- Weekly packets now include `model_profile_id`.
- Content buckets no longer map permanently to models; weekly packet builds rotate across `M01`, `M02`, `M03`, `M04`, and `M05`, unless a row explicitly sets `model_profile_id`.
- Weekly run folders now generate `daily_queue.csv`, `image_generation_briefs.md`, `image_review_template.csv`, and `generated_images/`.
- Daily cockpit and publish queue now show the internal model profile for each top item.
- Daily cockpit and publish queue now show the selected Canva master template key, name, and URL.
- `COMMAND_CENTER.md` is the primary operational entrypoint for this repo.
- Mira high-fashion carousel template v2 was added after reviewing the Scrolo-style reference screenshots. The new direction keeps the 3240 x 1350 / 3-slide automation contract, but requires cross-slide editorial movement, boundary crops, low text, and stricter head-crop validation.
- Five Claude Design Mira template variants were pushed to Canva as master templates: A Contact Sheet, B Symmetric, C Noir Evening, D Full-Bleed, and E Weekend Air.
- The active Canva master registry is `10_automation/canva_template_registry.md` and `10_automation/canva_template_registry.json`.
- Current Canva automation slot contract is `cover_image`, `motion_crop`, `detail_image`, and `slide2_line`.
- Daily Canva use should duplicate one master template before replacing assets. Do not write daily content directly into master templates.
- Canva image replacement must use whole flat PNG/JPG images in named frames. Do not use `image_to_design`, Magic Layers, split background/person/object assets, or old Canva design asset ids unless the asset is verified as a complete flat image.
- First automation trial on 2026-07-08 duplicated `A Contact Sheet` to `DAHOyDPZHeQ`, but the saved result is a failed test because it reused split Canva assets and lost the person layer. Do not export or publish that design.
- The failed W26-002 Canva copy `DAHO2rHNkZs` and old Canva image asset ids were invalidated because they used the old model identity. W26-002 is back at `needs_image_asset_selection` and must be regenerated with M02 v3 reference anchors through Codex.
- User decided to abandon old W26 production progress and use a clean new-week test path instead. The W26 folder remains historical; do not use it as the proof of current automation health.
- Fresh Perplexity pipeline test report was added at `10_automation/PERPLEXITY_FRESH_PIPELINE_TEST_2026-07-09.md`.

## Latest Published Post

- Instagram URL: https://www.instagram.com/p/DZCTbtWGuhx/?igsh=aG9kcjl3OWIybm01
- Confirmed publish time: 2026/06/01 16:08
- Format: Carousel
- Theme / prompt id: Sumer Looks!
- Product links: none
- CTA: 想看同風格清單？留言「沙色套裝」我整理平價 / 質感 / 替代款

## Current Metrics

First metrics check on 2026-06-02:

```text
reach = 0
likes = 0
saves = 0
comments = 0
shares = 0
profile_visits = 0
new_followers = 0
cta_comments = 0
```

10+ day visibility check on 2026-06-12:

```text
10+ days with no exposure / reach.
```

Interpretation:

```text
Treat this as an account visibility, distribution, or channel setup issue. Do not treat it as content failure.
```

## Automation Files

Start here:

```text
COMMAND_CENTER.md
COMPUTER_B_SYNC.md
10_automation/AUTOMATION_ARCHITECTURE_BRIEF.md
10_automation/DAILY_COCKPIT.html
10_automation/README.md
10_automation/2026_W25_work_order.md
10_automation/weekly_carousel_pipeline.md
10_automation/weekly_handoff_checklist.md
10_automation/TODAY.md
10_automation/PUBLISH_QUEUE.md
10_automation/runs/DASHBOARD.md
10_automation/runs/2026-W21-test/visibility_test_package.md
```

Core templates:

```text
10_automation/weekly_content_packet_template.csv
10_automation/canva_placeholder_values_template.csv
02_brand/mira_identity_block.md
02_brand/mira_model_roster.md
02_brand/mira_model_roster.json
02_brand/mira_image_generation_spec_v1.md
02_brand/mira_reference_images.csv
02_brand/reference_models/REFERENCE_IMAGE_REQUIREMENTS.md
02_brand/reference_models/reference_start_image_review.md
11_skills/mira-image-daily/SKILL.md
10_automation/runs/2026-W26/m02_polka_image_test_brief.md
10_automation/mira_high_fashion_carousel_template_v2.md
10_automation/claude_design_mira_template_v2_prompt.md
10_automation/canva_template_registry.md
10_automation/canva_template_registry.json
```

Recovery files:

```text
09_sops/instagram_zero_reach_recovery.md
05_content/second_test_zero_reach_post.md
```

## What The User Should Provide Next

For the next weekly carousel run:

```text
Perplexity weekly URL or use saved public index:
Canva panorama design URL:
Instagram account visibility status:
```

If Instagram is still at zero reach:

```text
Use PUBLISH_QUEUE.md first. Use 05_content/2026_06_18_reactivation_plan.md only as a side visibility check.
```

1. Do not publish another old Grok-similar carousel.
2. Use approved reference packs in `02_brand/mira_reference_packs.csv` before daily outfit generation.
3. Keep hairstyle flexible in daily outfit images only when the face structure, age cohort, and skin realism stay close to the approved face references.
4. Use `$mira-image-daily` to prepare daily image jobs from `daily_queue.csv`.
5. Score candidates in `image_review_template.csv` or the generated job review sheet.
6. Use the Canva template registry to select one Mira master template, duplicate it, then test-fill the duplicate.
7. Record metrics after publishing.

Current image-generation discussion should start from:

```text
02_brand/mira_image_generation_spec_v1.md
02_brand/mira_reference_images.csv
11_skills/mira-image-daily/SKILL.md
10_automation/runs/2026-W26/generated_images/2026-W26-002/codex_generation_handoff.md
```

## Next Codex Work

When the user provides the next Perplexity URL or Drive folder, Codex should:

1. Run `10_automation/daily_brief.py` first to create `TODAY.md`.
2. Open `10_automation/PUBLISH_QUEUE.md` to see the exact next content item.
3. If the top item is a visibility test, treat it as optional side evidence; do not let it block the next carousel.
4. Run `10_automation/weekly_dashboard.py` if the raw all-run table is needed.
5. Run `10_automation/check_weekly_status.py` if a specific run folder already exists.
6. Run `10_automation/run_weekly_pipeline.py --use-perplexity-index` if using the saved Perplexity public site, or pass `--perplexity-source` if a direct export is available.
7. Otherwise import weekly prompt rows into `04_prompts/item_prompt_database.csv`, then run `10_automation/build_weekly_packet.py`.
8. Confirm `quality_report.md` status is `pass`.
9. Open `daily_queue.csv` to confirm today's model profile and outfit.
10. Open `image_generation_briefs.md` and generate / place candidate images in `generated_images/`.
11. Score `image_review_template.csv`.
12. Run `10_automation/select_codex_assets.py --provider Codex` after images are scored.
13. Confirm `validate_weekly_run.py --require-assets` passes.
14. Use generated Canva handoff files or Canva connector edits to duplicate and fill one registered Mira Canva master template. Canva autofill must stop unless the selected images have verified Canva image asset ids for complete flat PNG/JPG assets.
15. Use generated IG / Threads / Pinterest drafts.
16. Run `10_automation/record_post_metrics.py` after publishing and at 6h/24h checkpoints.

On Windows, prefer the shortcut:

```text
10_automation/mika_weekly.ps1
```

First command after returning from a break:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit
```

Then open:

```text
COMPUTER_B_SYNC.md
10_automation/DAILY_COCKPIT.html
10_automation/TODAY.md
10_automation/PUBLISH_QUEUE.md
```

Only after reach becomes non-zero should Codex create affiliate/product links.
