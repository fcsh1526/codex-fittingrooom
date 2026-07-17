# Current Status - Mira AI Fashion Creator

Last updated: 2026-07-17

## Project Goal

Canonical cross-computer workflow: `10_automation/CANONICAL_WORKFLOW.md`. Computer B handoff: `COMPUTER_B_SYNC.md`.

Build a repeatable AI fashion magazine workflow: global fashion trend research, localized Traditional Chinese publishing, and daily outfit images with consistent internal models.

Current priority:

```text
global weekly trend -> daily outfit queue -> internal model profile -> approved reference start image -> Codex image job -> minimal Canva carousel -> Instagram post -> metrics
```

Latest automation test:

```text
2026-07-09 W27 Perplexity pipeline passed from https://mika-lin-weekly.pplx.app/data/index.json.
Active run folder: 10_automation/runs/2026-W27.
Current top item: 2026-W27-002; W27-001 is published.

2026-07-14 W29 was verified live in the public index and imported automatically from https://mika-lin-weekly.pplx.app/data/2026-W29.csv.
The W29 run contains 20 imported rows and 5 carousel packets, with one distinct trend per carousel and each of M01-M05 assigned exactly once. Validation passes with 0 errors and 0 warnings.
Perplexity has proposed a Monday auto-publish task because weekly files were repeatedly left in its workspace without deploy/publish. The recommended guarded schedule is documented in 10_automation/perplexity_autopublish_schedule.md and awaits user confirmation in Perplexity.

2026-07-15 W29 old v2 A/B/C production was superseded after the user identified synthetic body proportions and weak person/environment integration.
M01 passed a new Codex Hero-first photoreal pilot: one integrated scene was generated from the approved face/full-body anchors and received one targeted lighting/camera-finish refinement.
The refined Hero has plausible body proportions, physical hand/stone and shoe/floor contact, and materially improved shared scene lighting. It is accepted as the trial session lock, while its remaining catalog-like stiffness is recorded as a known pilot limitation.
W29-001 through W29-005 now each have an approved A Hero, B Motion, and C Detail set selected by the automation. The complete week contains 15 selected photoreal images across M01, M02, M04, M03, and M05.
The five W29 v3 Canva duplicates were initially filled on 2026-07-16, but visual review found that generic narrow portrait sources were center-cover cropped by Canva's exact frames. W29-001 through W29-005 have now completed the corrected path: each A/B/C set was purpose-built for its assigned master, visually reviewed in Canva, approved by the user, and saved. All five are `ready_for_manual_export`. Old W29 v2 selections must not be used for new Canva work.

The v3-E `MIRA` brand mark geometry was corrected and saved on 2026-07-16 in the master and in W29-002 / W29-005. Its text box now ends at x=3200 on the 3240px canvas, leaving a 40px right-safe margin.

All five v3 masters were audited on 2026-07-16 and their exact A/B/C frame geometry is now stored in `canva_template_registry.json`. New weekly packets choose one master before image-job generation. Each job writes `canva_slot_targets.json`, and its A/B/C prompts use the assigned frame ratios instead of one generic portrait ratio. `prepare_canva_ready_assets.py` normalizes approved sources to exact frame pixels without stretching and rejects center crops above 15%.

W29-001, W29-003 and W29-004 correctly resolve to v3-B: A `1240x1350`, B `1140x560`, C `1180x1350`. W29-002 and W29-005 resolve to v3-E: A `1120x1050`, B `1120x410`, C `1060x1010`. All five saved designs preserve complete hair and faces, keep the outfit focus visible, and show the full `MIRA` mark. W29 image and Canva production is complete; the remaining step is manual three-slice export and Instagram publishing.

On 2026-07-17 the complete current workflow was consolidated into `10_automation/CANONICAL_WORKFLOW.md` for computer A, computer B, and future Codex tasks. `README.md`, `COMMAND_CENTER.md`, `COMPUTER_B_SYNC.md`, the Canva panorama SOP, the connector workflow, and the architecture brief now point to that canonical contract. The retired five-slide Canva instructions and stale W27 computer-B handoff were removed.

Week ids use ISO 8601 exclusively: Monday is day 1, and W01 is the week containing the year's first Thursday. ISO calendar position and production completion are separate states; unfinished items remain active after their source week ends.
```

W27 image-production checkpoint:

```text
W27-001 is published. The original W27-002 through W27-005 images were rejected on 2026-07-13 for subject/background lighting mismatch; M04-B also failed wardrobe continuity and M03-A had letterboxing.
W27-002 through W27-005 now have non-destructive v2 A/B/C candidates. B/C use candidate A as an explicit wardrobe lock.
Image review now includes hard gates for scene_lighting_integration and outfit_continuity. Pasted-on lighting, missing contact shadows, letterboxing, or any wardrobe drift automatically rejects a candidate.
Google Drive is optional archive-only storage and is no longer a Canva pipeline dependency.
W27 is preserved as historical output but archived from the active queue on 2026-07-15 so its Canva drafts cannot override the W29 Hero-first photoreal trial.
```

Current Canva ingestion rule:

```text
Primary path: local generated PNG -> GitHub sync -> public raw GitHub URL -> Canva asset id.
Google Drive is not required. Do not request or change Drive sharing merely to satisfy Canva ingestion.
If images must stay private, use manual Canva Uploads because the current Canva connector has no local-file byte upload tool.
Do not use image_to_design or Magic Layers.
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
canva_frame_fit >= 4 is required for modern Codex image assets.
A default Canva center-cover crop that cuts hair, face, or outfit focus is an automatic rejection.
```

## Key Links

- GitHub repo: https://github.com/fcsh1526/codex-fittingrooom
- Perplexity weekly site: https://mika-lin-weekly.pplx.app/
- W21 test page: https://mika-lin-weekly.pplx.app/weeks/2026-W21-test.html
- W21 CSV: https://mika-lin-weekly.pplx.app/data/2026-W21-test.csv
- Canva panorama carousel design: https://www.canva.com/d/jJOq1Yimawt9wfU
- Legacy Mira Canva v2 single template: https://www.canva.com/design/DAHOIZe_Qz0/YjBO1NIF7JQ0VsRyrVRaew/edit
- Mira Canva template registry: `10_automation/canva_template_registry.md`
- Mira v3 A Cross-Boundary Contact Sheet: https://www.canva.com/d/c-IyIaIsCawzyCI
- Mira v3 B Cross-Boundary Symmetric: https://www.canva.com/d/UoVSnPEpgguD3be
- Mira v3 C Cross-Boundary Noir: https://www.canva.com/d/C9QGHZ6OH7HtYux
- Mira v3 D Cross-Boundary Full-Bleed: https://www.canva.com/d/Kh_uu5y-twQzbF-
- Mira v3 E Cross-Boundary Weekend Air: https://www.canva.com/d/djICquyAb4kcGwW
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
- Content buckets no longer map permanently to models. Weekly packet builds now assign `M01`, `M02`, `M03`, `M04`, and `M05` exactly once per 5-post week using a reproducible shuffled order; Perplexity controls outfit topics, not model identity.
- Weekly run folders now generate `daily_queue.csv`, `image_generation_briefs.md`, `image_review_template.csv`, and `generated_images/`.
- Daily cockpit and publish queue now show the internal model profile for each top item.
- Daily cockpit and publish queue now show the selected Canva master template key, name, and URL.
- `COMMAND_CENTER.md` is the primary operational entrypoint for this repo.
- Mira high-fashion carousel template v2 was added after reviewing the Scrolo-style reference screenshots. The new direction keeps the 3240 x 1350 / 3-slide automation contract, but requires cross-slide editorial movement, boundary crops, low text, and stricter head-crop validation.
- Five Claude Design Mira template variants were pushed to Canva as master templates: A Contact Sheet, B Symmetric, C Noir Evening, D Full-Bleed, and E Weekend Air.
- Five cross-boundary v3 copies were approved and committed in Canva on 2026-07-14. The active registry now points to v3; v2 remains archived.
- v3-E master and W29-002 / W29-005 were corrected on 2026-07-16 so the bottom-right `MIRA` mark stays inside a 40px right-safe margin.
- The image pipeline now requires assigned-frame-ratio crop-safe output and a `canva_frame_fit` score before a carousel can be marked publishable.
- All five v3 master frame geometries are machine-readable; template selection now occurs before A/B/C prompt generation.
- `prepare_canva_ready_assets.py` creates exact frame-sized PNGs without stretching and blocks source/frame mismatches requiring more than 15% crop.
- The active Canva master registry is `10_automation/canva_template_registry.md` and `10_automation/canva_template_registry.json`.
- Current Canva automation slot contract is `cover_image`, `motion_crop`, `detail_image`, and `slide2_line`.
- Daily Canva use should duplicate one master template before replacing assets. Do not write daily content directly into master templates.
- Canva image replacement must use whole flat PNG/JPG images in named frames. Do not use `image_to_design`, Magic Layers, split background/person/object assets, or old Canva design asset ids unless the asset is verified as a complete flat image.
- First automation trial on 2026-07-08 duplicated `A Contact Sheet` to `DAHOyDPZHeQ`, but the saved result is a failed test because it reused split Canva assets and lost the person layer. Do not export or publish that design.
- The failed W26-002 Canva copy `DAHO2rHNkZs` and old Canva image asset ids were invalidated because they used the old model identity. W26-002 is back at `needs_image_asset_selection` and must be regenerated with M02 v3 reference anchors through Codex.
- User decided to abandon old W26 production progress and use a clean new-week test path instead. The W26 folder remains historical; do not use it as the proof of current automation health.
- Fresh Perplexity pipeline test report was added at `10_automation/PERPLEXITY_FRESH_PIPELINE_TEST_2026-07-09.md`.
- W27 was generated from the Perplexity public index into `10_automation/runs/2026-W27` with 5 carousel packets and 5 Codex generation handoffs.
- W29 was verified in the public index and imported into `10_automation/runs/2026-W29`; row selection now prioritizes one outfit from each distinct trend before filling remaining slots.
- Perplexity auto-publish requirements were documented so a weekly report is not considered complete until the HTML, CSV, and public index are all live and verified.

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
10_automation/runs/2026-W27/generated_images/2026-W27-001/codex_generation_handoff.md
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
10_automation/runs/2026-W27/generated_images/2026-W27-001/codex_generation_handoff.md
```

## Next Codex Work

The daily Production Worker should:

1. Run `10_automation/daily_brief.py` first to create `TODAY.md`.
2. Open `10_automation/PUBLISH_QUEUE.md` to see the exact next content item.
3. If the top item is a visibility test, treat it as optional side evidence; do not let it block the next carousel.
4. Run `10_automation/weekly_dashboard.py` if the raw all-run table is needed.
5. Run `10_automation/check_weekly_status.py` if a specific run folder already exists.
6. Run `10_automation/run_weekly_pipeline.py --use-perplexity-index` if using the saved Perplexity public site, or pass `--perplexity-source` if a direct export is available.
7. Otherwise import weekly prompt rows into `04_prompts/item_prompt_database.csv`, then run `10_automation/build_weekly_packet.py`.
8. Confirm `quality_report.md` status is `pass`.
9. Open `daily_queue.csv` to confirm today's model profile and outfit.
10. Open the top item's generated handoff and use built-in imagegen to generate A/B/C candidates with approved face/full references.
11. Score the carousel-local `generated_images/{carousel_id}/review_sheet.csv`.
12. Run `10_automation/select_codex_assets.py --provider Codex`; it automatically discovers carousel-local review sheets when `--score-sheet` is omitted.
13. Confirm strict assets validation passes for the top carousel with `validate -Week YYYY-WXX -CarouselId YYYY-WXX-NNN -RequireAssets`; run whole-week strict validation only after all five are produced.
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
