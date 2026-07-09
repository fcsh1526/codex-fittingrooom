# Integration Audit - 2026-07-09

Purpose: consolidate the current Mira automation state after multiple parallel infrastructure updates.

## Executive Summary

The system is not missing automation. It has several working automation layers, but the layers are not yet governed by one strict production state machine.

Current reliable facts:

- The active workflow is Mira magazine, not the old Mika/Mika Lin single virtual influencer workflow.
- Production-first remains the strategy: keep producing image-led Instagram carousel posts.
- Five internal models `M01` to `M05` are defined and approved in `02_brand/mira_reference_images.csv`.
- Five Canva master templates are registered in `10_automation/canva_template_registry.md/json`.
- The daily cockpit, publish queue, weekly dashboard, status checker, validation command, and smoke test all run.
- The current top item is `2026-W26-002` / `M02`.

Main reality check:

```text
Smoke test: pass
Existing validation: pass
Actual production readiness: blocked
```

The validation layer is too weak for the new Canva/template/reference workflow.

## Current Top Item

```text
item = 2026-W26-002
model = M02
stage = canva_blocked_waiting_for_flat_png_asset
recommended template = A Contact Sheet
asset set = A_v2 cover, B_v2 motion crop, C_v2 detail
```

Known Canva asset ids:

```text
cover_image = MAHOCYb2mPI
motion_crop = MAHOCUFmjRs
detail_image = TBD
```

Hard rule:

```text
Do not export or publish the failed Canva draft DAHOyDPZHeQ.
Do not use image_to_design, Magic Layers, split assets, or old Canva design asset ids for final fills.
```

## What Is Working

1. Weekly run folder exists:
   `10_automation/runs/2026-W26`

2. Five internal model anchors exist:
   `02_brand/mira_reference_images.csv`

3. Five Canva master templates exist:
   `10_automation/canva_template_registry.md`
   `10_automation/canva_template_registry.json`

4. Queue/cockpit generation works:
   `10_automation/PUBLISH_QUEUE.md`
   `10_automation/TODAY.md`
   `10_automation/DAILY_COCKPIT.html`

5. Smoke test passes:
   `powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action smoke-test`

## Current Integration Breaks

### 1. Validation Passes Despite Real Blockers

`validate --RequireAssets` currently passes, but it does not catch:

- `2026-W26-002` missing `detail_image` Canva image asset id.
- `2026-W26-001` having a `motion_crop` row with `status = needs_regeneration`.
- `codex_asset_selection.csv` saying `2026-W26-001` has `selection_status = needs_review`.
- `canva_placeholder_map.json` containing mojibake text while `canva_placeholder_values.csv` is clean.

Required fix: add strict production validation for Canva asset ids, asset slot status, asset selection status, and text encoding drift.

### 2. Queue Treats W26-001 As More Ready Than It Is

`PUBLISH_QUEUE.md` shows:

```text
2026-W26-001 = ready_for_canva_and_publish
```

But current data says:

```text
codex_asset_selection.csv = needs_review
canva_asset_slots.csv motion_crop = needs_regeneration
```

Required fix: publish queue should demote any carousel with `needs_review`, `needs_regeneration`, or missing selected asset slots.

### 3. Canva Placeholder Map Is Not The Source Of Truth

Clean text exists in:

```text
10_automation/runs/2026-W26/canva_placeholder_values.csv
10_automation/runs/2026-W26/canva_fill_guide.md
```

But `canva_placeholder_map.json` has mojibake for placeholder/caption text.

Required fix: regenerate `canva_placeholder_map.json` only from the clean CSV, then add a validation check that rejects mojibake-like replacement characters or obvious encoding drift.

### 4. Legacy Canva URL Still Exists In Weekly Packet

`weekly_content_packet.csv` still points to the legacy single Canva v2 template URL:

```text
https://www.canva.com/design/DAHOIZe_Qz0/YjBO1NIF7JQ0VsRyrVRaew/edit
```

The active template source is now the registry:

```text
10_automation/canva_template_registry.md/json
```

Required fix: either remove `canva_design_url` from weekly packets or make it hold the selected registry template URL after template selection.

### 5. Reference Pack Status Is Not Promoted To The Canonical Location

`CURRENT_STATUS.md` says `02_brand/mira_reference_packs.csv` exists, but it does not.

Draft pack data exists under:

```text
10_automation/runs/2026-W26/reference_model_drafts_phase_a/
```

Required fix: either promote the approved reference pack manifest into `02_brand/`, or remove the claim from current status and keep `mira_reference_images.csv` as the only canonical reference gate.

### 6. Image Skill Is Not Integrated Into The PowerShell Entrypoint

The repo has:

```text
11_skills/mira-image-daily/scripts/prepare_daily_image_job.py
```

But `10_automation/mika_weekly.ps1` has no `image-job` action that calls it.

Required fix: add a PowerShell action such as:

```text
-Action image-job -Week 2026-W26 -CarouselId 2026-W26-002
```

This should produce:

```text
generated_images/{carousel_id}/image_job.md
generated_images/{carousel_id}/candidate_prompts.md
generated_images/{carousel_id}/review_sheet.csv
```

### 7. GitHub Is Not Yet A Clean Sync Point

The working tree has many modified and untracked files. Computer B will not get this state from GitHub until the changes are intentionally grouped, committed, and pushed.

Required fix: create one cleanup commit only after the state machine and generated artifacts are made internally consistent.

## Recommended Repair Order

1. Fix state truth for W26:
   - Keep `2026-W26-002` blocked until `detail_image` Canva asset id is known.
   - Demote `2026-W26-001` from ready until motion crop and asset selection are truly publishable.

2. Regenerate machine files from clean sources:
   - `canva_placeholder_map.json`
   - `PUBLISH_QUEUE.*`
   - `TODAY.*`
   - `DAILY_COCKPIT.*`

3. Strengthen validation:
   - reject `needs_regeneration`
   - reject `needs_review` for publish-ready items
   - reject missing Canva flat asset ids when a run is in Canva fill stage
   - reject mojibake in machine text files

4. Integrate image job action:
   - add `mika_weekly.ps1 -Action image-job`
   - route it to `mira-image-daily/scripts/prepare_daily_image_job.py`

5. Update sync docs:
   - `CURRENT_STATUS.md`
   - `COMPUTER_B_SYNC.md`
   - cockpit command date should use current date or no fixed stale date.

6. Run checks:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action validate -Week 2026-W26 -Limit 2 -RequireAssets
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-07-09
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action smoke-test
```

7. Commit and push only after the generated files and source files agree.

## Immediate Production Decision

There are two valid next moves:

1. Continue `2026-W26-002`:
   - Get/resolve the complete flat Canva image asset id for `2026-W26-002_M02_candidate_C_v2.png`.
   - Rerun Canva fill on a fresh duplicate of Template A.

2. Temporarily skip `2026-W26-002` and produce a new carousel:
   - Do not use `2026-W26-001` until its motion crop and asset selection are fixed.
   - Use `mika-image-daily` to generate a clean new daily item from the approved M01-M05 references.
