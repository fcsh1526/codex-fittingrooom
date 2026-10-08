# Mira Canonical Production Workflow

Updated: 2026-10-08

This is the single source of truth for computer A, computer B, and every Codex task working on this repository. When another document conflicts with this file, follow this file and `10_automation/canva_template_registry.json`.

## Current Production Contract

```text
Perplexity public weekly CSV
-> ISO weekly run with five themes
-> M01-M05 used exactly once each week
-> one model is locked to each theme
-> expand each theme into exactly two editor-approved complete looks (ten looks total)
-> define one Reel-wide visual theme from the model's two weekly looks
-> storyboard connected shots: scene purpose, action start/end, framing, light and identity visibility
-> derive required starting images and styling-proof views from that storyboard
-> prepare both surface jobs for every look
-> Reel: native 9:16 full-person A plus a reviewed styling-proof view per look
-> Carousel: A full-person Hero + B scene application + C accessory detail
-> normalize Carousel A/B/C without stretching and review in the connected three-image Canva template
-> compile five theme/model Reels; each keeps one model, two looks, four usable full/proof views and one audience problem
-> user designs, edits, exports, and posts manually
-> link production records to post URL and 24h / 72h / 7d metric snapshots
```

Active rules:

- User decision 2026-10-05: preserve the five current W37 first-wave publishing videos delivered to Drive on 2026-10-02, their local originals, file IDs and paired caption links. New research cuts must use separate paths and, if uploaded, distinct filenames/file IDs in a separate research folder. Acceptance of a trial never authorizes replacing a first-wave file. Replacement requires a later explicit user instruction naming the intended replacement.
- User decision 2026-10-02: all subsequent shot/outfit switches default to a soft cross dissolve of approximately0.75 seconds, replacing the earlier direct-cut preference. Keep source character actions and speed unchanged. Plan overlapping handles, matched viewing positions and sufficient outfit-reading time in the storyboard. Validate the combined film; a transition must not conceal identity, wardrobe or background errors. Existing accepted exports remain historical versions; the pending M01 cut is revised under this rule.
- Editing QA clarification 2026-10-08: user accepts the exact M02 8.5s deep-to-light front-edge gesture research picture, explicitly valuing its dissolve overlap and softened viewing feeling. Brief cross-dissolve double outlines may be an accepted aesthetic effect. Evaluate normal-speed comfort, continuity and outfit readability; a historical no-visible-ghost diagnostic criterion is not automatic editorial rejection. Keep single-source face/clothing/hand/background integrity checks and existing failed diagnostics. This single-cut acceptance does not establish a mandatory shot format, full-outfit delivery or audience performance.
- Storyboard before Reel image generation: first define the entire film's visual theme, then design shots that connect, then generate their starting images. Every scene must serve the clothes, everyday situation or shot continuity. Do not assign decorative locations independently to each look and repair the sequence with transitions afterward.
- Plan each shot's action start/end, neighboring-shot connection, outfit evidence and identity information. A beautiful captured mid-action still is not automatically an animation-ready starting frame. Face visibility and selected identity references must support the planned motion; a frontal image alone does not guarantee dynamic identity stability. Side views remain possible when supported and tested.
- Creative direction: approachable daily-outfit editorial, with magazine composition and color. The former rapid two-look opening and fixed six-section edit are retired; use the current Reel SOP storyboard gate. Formal delivery remains one model and both looks.
- 2026-10-01 editorial clarification: the current two-shot cuts are individual examples, not a mandatory weekly template. Choose shot count, framing and movement from the clothing information each film needs to show. Technical QA, user acceptance of one cut, account-wide style adoption and audience performance are separate decisions; never infer the latter from the former. W37 comparison and M03's unvalidated material-detail trial are recorded in `reels/EDITORIAL_REVIEW_2026-10-01.md` and `reels/M03_storyboard_v1.md` under the weekly run.

- Use ISO 8601 week ids such as `2026-W29`.
- Produce five weekly themes with exactly two complete looks per theme: ten looks total.
- M01-M05 are private identity ids. Never render or publish them in Instagram content.
- Each of the five weekly themes keeps one model across all of its looks. Do not rotate identities inside a theme.
- Each theme contains two complete looks in `weekly_look_plan.csv`. Each changed outfit starts its own look-specific lock.
- Image work is created by `look_id`, not only by theme `carousel_id`. Every look must have both `reel/` and `carousel/` surface folders under `generated_images/{carousel_id}/looks/{look_id}/`.
- Reel requires one native 9:16 full-person A and one usable styling-proof view per look. Each of five weekly Reels keeps one model/theme and both looks. Reuse proof imagery only after vertical framing and clarity review; generate a missing proof view when necessary. Do not require all Carousel frames inside a Reel.
- Read `09_sops/mira_reel_production_sop.md` before video work. Current Reel rule (user decision 2026-09-29): deliver clean video and cover without baked-in text, subtitles, title cards or text overlays. Let shots show the styling point; put fuller explanation in the Instagram post caption. If a specific video truly needs on-screen words, notify the user with suggested wording, timing and placement so the user may add them manually in Instagram's editor; never render those words into the delivered file. Taiwan daily/commute audience, suitable music, about 15 seconds and 30–60 active production minutes remain test settings, not platform guarantees.
- W37 M02 reference/video pilot passed technical checks and the user's clean-visual approval on 2026-09-29. W37 may proceed one look at a time; newly generated stills remain candidates until individual user visual approval. Static approval, submitted generation, dynamic QA and final user approval are distinct states. A still-image approval never approves a video automatically.
- Carousel always requires three connected-template assets per look: A full-person Hero, B scene application, and C accessory detail. B/C follow accepted Carousel A and preserve the exact outfit and identity.
- Perplexity supplies global fashion trends. Codex localizes each selected outfit for wearable daily use.
- Mira uses `utility_with_immersion`: every daily story solves one concrete dressing decision through an immersive, high-quality lifestyle image or image sequence.
- Carousel and Reel are parallel delivery assets, not alternatives. Complete both surface packages for every look.
- Codex built-in image generation is the production still-image path. Grok may animate an accepted Reel A when needed, but it does not replace source-image generation or change the outfit design.
- Google Drive is optional archive storage, not a production dependency.
- User decision 2026-10-07: when saving Mira work to Drive, use `800.Codex IG/{YYYY}-W{WW}/` by the content's ISO week, not the generation/upload date. Root and verified week/subfolder IDs are in `10_automation/google_drive_archive_registry.json`. Reuse an existing verified week folder; create a missing one inside that root. W37 is now `800.Codex IG/2026-W37`, retaining its original folder ID and all media/document links. Research and cloud trials remain in the weekly research subtree. Reorganizing folders does not authorize replacing first-wave files or changing sharing permissions.
- GitHub is the cross-computer source of truth and the approved public image transport for Canva uploads.
- Instagram reach does not block production.
- Final Canva design, Reel assembly, export, and Instagram publishing are manual user steps.

## Source Of Truth Files

Read these after every `git pull`:

```text
10_automation/CANONICAL_WORKFLOW.md
CURRENT_STATUS.md
10_automation/DAILY_COCKPIT.html
10_automation/PUBLISH_QUEUE.md
10_automation/runs/DASHBOARD.md
```

Machine data:

```text
02_brand/mira_reference_images.csv
10_automation/canva_template_registry.json
10_automation/runs/{week_id}/weekly_content_packet.csv
10_automation/runs/{week_id}/weekly_look_plan.csv
10_automation/runs/{week_id}/daily_queue.csv
10_automation/runs/{week_id}/weekly_status.json
```

Research basis:

```text
03_research/instagram_daily_outfit_benchmark_2026-08-11.md
03_research/gpt_image_fashion_prompt_engineering_2026-08-12.md
```

## Computer Start Procedure

From the repository root:

```powershell
git pull origin main
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action dashboard
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action queue
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action cockpit
```

If `git` is not on `PATH` on computer A, use:

```powershell
& 'C:\Users\Brandon_ChangChien\AppData\Local\Programs\Git\cmd\git.exe' pull origin main
```

Do not start from an old chat summary. Start from the repository files above.

## Phase 1: Import The Perplexity Week

Public site and machine index:

```text
https://mika-lin-weekly.pplx.app
https://mika-lin-weekly.pplx.app/data/index.json
```

The report must be deployed. A file that exists only in the Perplexity workspace is not available to Codex.

Before building the production week, review the five Perplexity Editorial Conversion Cards. Perplexity is research input, not automatic publishing approval. If any topic is seasonally unsuitable, repetitive, inaccurate, or weak as a visual answer, create an editor-approved five-row CSV at:

```text
03_research/editorial_overrides/{week_id}.csv
```

Mark each approved row with `status=editorial_approved` and `editorial_status=approved` in `notes`. When approved rows exist for a week, packet selection must ignore the raw Perplexity rows. Store `audience_problem`, `editorial_answer`, `opening_hook`, `visual_proof`, and `practical_rule` as stable key-value pairs in `notes`.

After the five themes pass the editorial gate, create an editor-approved look source at `03_research/editorial_look_plans/{week_id}.csv`. Each theme must contain exactly two complete outfits. The production model is inherited from the theme packet and cannot be changed per look.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 `
  -Action pipeline `
  -Week 2026-WXX `
  -UsePerplexityIndex `
  -EditorialSource 03_research\editorial_overrides\2026-WXX.csv `
  -LookSource 03_research\editorial_look_plans\2026-WXX.csv `
  -Limit 5
```

Omit `-EditorialSource` only when the reviewed Perplexity rows are accepted without changes. Never create an override merely to reformat unchanged research.

Expected output:

```text
10_automation/runs/2026-WXX/weekly_content_packet.csv
10_automation/runs/2026-WXX/daily_queue.csv
10_automation/runs/2026-WXX/generated_images/{carousel_id}/
10_automation/runs/2026-WXX/quality_report.md
```

Acceptance checks:

- 20 Perplexity prompt rows are normally available.
- Exactly five carousel packets are selected.
- If an editorial override exists, all five packets come from `editorial_approved` rows and carry the five editorial fields into `weekly_content_packet.csv`.
- `weekly_look_plan.csv` contains exactly two looks for every theme, uses the same model as its parent theme, and gives every look a complete outfit, real scene, visible action, visual proof, and the fixed dual-surface plan.
- M01-M05 are assigned exactly once each.
- Dates follow the ISO week beginning Monday.
- `quality_report.md` has zero errors.

Never reuse an unfinished prior week as the new week. Keep historical files and create a new ISO run.

## Phase 2: Select The Canva Master Before Images

Each carousel uses one v3 master. The selected key is stored in `weekly_content_packet.csv` and resolved through `canva_template_registry.json`.

| Key | Use | A | B | C |
| --- | --- | --- | --- | --- |
| A | standard editorial | 1160x1190 | 980x430 | 1080x1080 |
| B | calm symmetric | 1240x1350 | 1140x560 | 1180x1350 |
| C | dark/evening | 1230x1350 | 1000x460 | 1180x1350 |
| D | full-bleed impact | 1240x1350 | 1140x1350 | 1180x1350 |
| E | airy weekend/linen | 1120x1050 | 1120x410 | 1060x1010 |

Do not generate a generic portrait set first. Frame ratio is part of generation.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 `
  -Action image-job `
  -Week 2026-WXX `
  -LookId 2026-WXX-001-L01 `
  -ImageSurface Reel `
  -AssetProvider Codex
```

Run both delivery-surface jobs for every look:

- Reel: run with `-ImageSurface Reel`, read `reel_frame_targets.json`, and generate one full-person A directly at 9:16 / 1080x1920. Do not use Canva ratios or the Carousel 15% crop rule.
- Carousel: run with `-ImageSurface Carousel`, read `canva_slot_targets.json`, and generate A full-person Hero, then B scene application and C accessory detail at the exact assigned Canva ratios.
- Keep identity, exact outfit, scene logic, and photographic treatment consistent, but create separate surface-specific compositions.
- Final Reel packaging uses five model/theme groups per week. Each group needs four usable views: full-person plus styling proof for each look. Full-person Reel A and Carousel compositions remain separate; no blanket reuse or required eight-still montage. Do not mix identities into one Reel.
- A look is not asset-complete until both surface folders pass review.

## Phase 3: Generate Hero A, Then Any Required Derivatives

Use `11_skills/mira-image-daily/SKILL.md`. The same skill is installed at `%USERPROFILE%\.codex\skills\mira-image-daily\SKILL.md`.

Identity inputs:

```text
02_brand/mira_reference_images.csv
02_brand/reference_models/{model}_*_face.png
02_brand/reference_models/{model}_*_full.png
```

Mandatory order after the surface is declared:

1. Confirm the packet's single `dressing_decision` and `visible_action` before writing any prompt.
2. Open `hero_A_prompt.md`; generate A Hero with both identity anchors and the exact A ratio.
3. Review identity, proportions, outfit, contact, scene lighting, expression, realism and frame safety using the review sheet.
4. If A has one correctable defect, make one targeted edit to the same image. Do not generate a competing A/B option.
5. Accept A as the session lock.
6. For Carousel, use `derivative_edit_prompt_templates.md` to derive required B Scene Application and C Accessory Detail from accepted Carousel A plus both anchors. These are sequence assets, not tests.
7. For Reel, save the accepted full-person A and the selected or generated styling-proof view with their separate review records. Keep a frontal diagnostic variant as a separate file; do not replace the approved original. For Carousel, save accepted A/B/C in the surface-specific job folder.

Photo rules:

- Full-frame mirrorless camera with a 50mm prime lens, chest-height camera, and level optical axis; no smartphone, computational portrait mode, or DSLR simulation unless explicitly overridden.
- Use the camera description for high-level look, viewpoint and composition. Do not put fixed aperture, shutter speed, ISO or white-balance numbers in GPT Image prompts.
- Hero prompts normally use 120-220 English words in this order: intended use and dressing decision -> input-image roles -> real scene and one visible action -> exact outfit -> photographic treatment -> composition -> short constraints.
- Use one final constraint line with no more than five essential exclusions. Do not append a long negative prompt.
- Describe observable realism: available natural light, believable ambient spill, realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness.
- Realistic adult proportions, not runway or nine-head anatomy.
- Scene light affects face, hair, clothes, hands, shoes, floor, props, and background consistently.
- Include believable contact and contact shadows.
- Keep exact body-part measurements, anatomy checks, contact-shadow checks, the 8% top margin, central 70% and crop tolerance in the review sheet rather than the base prompt.
- A shallow B frame requires a genuine wide composition, not a hard-cropped portrait.
- Preserve exact wardrobe construction and palette across A/B/C.

Reject: cropped head/hair; distorted proportions; pasted-on person or halo; mismatched lighting; wardrobe drift; frozen repeated poses; text/logo/watermark; celebrity likeness; or sexualized or childlike styling. For Reel, reject a source that is not composed directly as 9:16. For Carousel only, reject more than 15% required crop.

## Phase 4: Normalize To Exact Canva Pixels

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 `
  -Action canva-ready `
  -Week 2026-WXX `
  -CarouselId 2026-WXX-001 `
  -SourceA accepted_A.png `
  -SourceB accepted_B.png `
  -SourceC accepted_C.png
```

This phase is Carousel-only. `prepare_canva_ready_assets.py` must never stretch, must reject crop above 15%, and writes exact files plus `canva_ready_manifest.json` under `generated_images/{carousel_id}/canva_ready/`. Reel assets bypass this phase because they are generated directly for 9:16.

Inspect all three exact outputs. Keep status `needs_canva_frame_review` until the Canva preview passes.

## Phase 5: GitHub Asset Checkpoint

Commit and push exact-frame PNGs before Canva upload. This synchronizes computer B and creates stable GitHub raw URLs.

```powershell
git status --short
git add <exact intended files>
git commit -m "Add 2026-WXX-001 exact-frame image set"
git push origin main
```

Raw URL pattern:

```text
https://raw.githubusercontent.com/fcsh1526/codex-fittingrooom/main/10_automation/runs/{week_id}/generated_images/{carousel_id}/canva_ready/{file_name}.png
```

Only stage intended files. Do not add unrelated drafts or historical experiments. Do not add another public host or Drive dependency.

## Phase 6: Canva Draft Transaction

Use a duplicate of the assigned master. Never edit the v3 master for weekly content.

```text
canvas: 3240x1350
slice guides: x=1080 and x=2160
image slots: cover_image, motion_crop, detail_image
text slot: slide2_line
```

Connector sequence:

1. Upload the three exact PNGs from GitHub raw URLs.
2. Start a Canva transaction on the weekly duplicate.
3. Read every page image asset before replacement.
4. Replace only the registered A/B/C element ids.
5. Download the draft thumbnail into the look's `carousel/canva_ready/` folder and inspect the local PNG.
6. Show the preview in Codex with the local PNG's absolute filesystem path. Do not embed Canva's temporary signed thumbnail URL directly; it may not render in the desktop conversation and it expires.
7. Ask explicitly whether to save.
8. Commit only after `同意保存` or equivalent explicit approval.
9. Cancel if rejected.

Never use `image_to_design`, Magic Layers, split person/background assets, unverified old asset ids, manual Smart Crop as a substitute for composition, or a master design as the weekly target.

Canva acceptance:

- full hair and readable face where intended;
- outfit focus visible;
- no accidental crop at slide boundaries;
- coherent cross-slide panorama;
- full `Mira` mark inside its right-safe margin;
- no draft reported as saved until commit succeeds.

## Phase 7: Mark Ready For Manual Export

After Canva commit, update:

```text
generated_images/{carousel_id}/review_sheet.csv
generated_images/{carousel_id}/canva_ready/canva_ready_manifest.json
canva_asset_inventory.csv
canva_asset_slots.csv
codex_asset_selection.csv
daily_queue.csv
weekly_content_packet.csv
canva_autofill_status.md
CURRENT_STATUS.md
```

Approved states:

```text
review: canva_frame_approved
asset selection: exact_frame_approved
packet / queue: ready_for_manual_export
Canva: committed_exact_frame
```

Regenerate and validate:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action sync-canva-map -Week 2026-WXX
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action validate -Week 2026-WXX -RequireAssets
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action status -Week 2026-WXX
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action queue
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action cockpit
```

Required result: `Validation pass: 0 error(s), 0 warning(s).` Then commit and push all intended status files.

## Phase 8: Manual Export And Instagram

This is the intentional manual boundary:

1. Open the saved Canva duplicate.
2. Use the existing Canva slicing app.
3. Split `3240x1350` into three `1080x1350` images.
4. Export in left-to-right order.
5. Publish or schedule one Instagram Carousel.
6. Send Codex the Instagram URL and publish time.

Do not export the unsliced panorama as the post.

## Phase 9: Record Publish Result

For the current Reel contract, prepare `reels/production_manifest.json` using `prepare_reel_production.py`. Its five Reel records link both look IDs, four asset slots, storyboard, actual generation settings, clip selection, QA, timing and publication. Do not infer accepted files from names. Use `record_reel_metrics.py publish` to link an actual post to its explicit `reel_id`, then `snapshot` at 24h, 72h and 7d. Missing values remain empty; historical lifetime snapshots stay separate from fixed-age comparisons. See `07_metrics/REEL_METRICS.md`.

The command below remains for legacy Carousel records:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 `
  -Action metrics `
  -Week 2026-WXX `
  -CarouselId 2026-WXX-001 `
  -PostUrl "https://www.instagram.com/p/POST_ID/" `
  -PublishedAt "YYYY/MM/DD HH:mm"
```

Metrics are optional for production continuity. Zero reach never moves an unfinished carousel backward.

## State Machine

```text
needs_image_asset_selection
-> needs_canva_frame_review
-> canva_frame_approved
-> ready_for_manual_export
-> published_waiting_for_metrics
```

Failure states: `needs_visual_revision`, `canva_blocked_waiting_for_flat_png_asset`, `quality_gate_not_passed`.

`ready_for_manual_export` means Canva is already saved. Do not regenerate or refill unless the user reports a defect.

## End-Of-Session Git Procedure

```powershell
git status --short
git diff --check
git add <intended files>
git commit -m "Describe the completed production checkpoint"
git push origin main
```

The next computer starts with `git pull origin main`. Do not pass progress only through chat; every accepted asset, state change, Canva URL, and process change must be recorded in GitHub.

## W29 Verified Reference

```text
W29-001 M01 v3-B ready_for_manual_export
W29-002 M02 v3-E ready_for_manual_export
W29-003 M04 v3-B ready_for_manual_export
W29-004 M03 v3-B ready_for_manual_export
W29-005 M05 v3-E ready_for_manual_export
quality: 0 errors / 0 warnings
```

Use W29 as a structural example, never as future image sources.
