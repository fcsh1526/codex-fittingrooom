# Mira Canonical Production Workflow

Updated: 2026-07-17

This is the single source of truth for computer A, computer B, and every Codex task working on this repository. When another document conflicts with this file, follow this file and `10_automation/canva_template_registry.json`.

## Current Production Contract

```text
Perplexity public weekly CSV
-> ISO weekly run with five carousel packets
-> M01-M05 used exactly once each week
-> select one Canva v3 master for each carousel
-> generate exact-ratio A Hero, B Motion, C Detail in Codex
-> normalize without stretching and review
-> replace three flat images in a Canva duplicate
-> show draft preview and save only after user approval
-> user manually slices, exports, and posts to Instagram
-> record post URL and optional metrics
```

Active rules:

- Use ISO 8601 week ids such as `2026-W29`.
- Produce five Instagram carousels per week, normally one per weekday.
- M01-M05 are private identity ids. Never render or publish them in Instagram content.
- Perplexity supplies global fashion trends. Codex localizes each selected outfit for wearable daily use.
- Codex built-in image generation is the production image path. Grok is not part of the active workflow.
- Google Drive is optional archive storage, not a production dependency.
- GitHub is the cross-computer source of truth and the approved public image transport for Canva uploads.
- Instagram reach does not block production.
- The only required manual production step is Canva three-slice export and Instagram publishing.

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
10_automation/runs/{week_id}/daily_queue.csv
10_automation/runs/{week_id}/weekly_status.json
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

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 `
  -Action pipeline `
  -Week 2026-WXX `
  -UsePerplexityIndex `
  -Limit 5
```

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
  -CarouselId 2026-WXX-001 `
  -AssetProvider Codex
```

Read the generated `canva_slot_targets.json` before producing A/B/C.

## Phase 3: Generate A, B, And C In Codex

Use `11_skills/mira-image-daily/SKILL.md`. The same skill is installed at `%USERPROFILE%\.codex\skills\mira-image-daily\SKILL.md`.

Identity inputs:

```text
02_brand/mira_reference_images.csv
02_brand/reference_models/{model}_*_face.png
02_brand/reference_models/{model}_*_full.png
```

Mandatory order:

1. Generate A Hero with both identity anchors and the exact A ratio.
2. Review identity, proportions, outfit, contact, scene lighting, expression, and frame safety.
3. Accept A as the session lock. At most one targeted lighting/camera edit is allowed.
4. Derive B Motion from accepted A plus both anchors, at the exact B ratio.
5. Derive C Detail from accepted A plus both anchors, at the exact C ratio.
6. Save accepted files in the carousel job folder.

Photo rules:

- Normal 50mm full-frame-equivalent perspective, chest-height camera, level optical axis.
- Realistic adult proportions, not runway or nine-head anatomy.
- Scene light affects face, hair, clothes, hands, shoes, floor, props, and background consistently.
- Include believable contact and contact shadows.
- Keep the full hairstyle below an 8% top safe margin whenever the face appears.
- Keep face and outfit focus inside the central 70%.
- A shallow B frame requires a genuine wide composition, not a hard-cropped portrait.
- Preserve exact wardrobe construction and palette across A/B/C.

Reject: cropped head/hair; distorted proportions; pasted-on person or halo; mismatched lighting; wardrobe drift; frozen repeated poses; text/logo/watermark; celebrity likeness; sexualized or childlike styling; or more than 15% required crop.

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

`prepare_canva_ready_assets.py` must never stretch, must reject crop above 15%, and writes exact files plus `canva_ready_manifest.json` under `generated_images/{carousel_id}/canva_ready/`.

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
5. Download and inspect the draft thumbnail.
6. Show the preview to the user.
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
