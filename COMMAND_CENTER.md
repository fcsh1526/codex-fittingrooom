# Mira Command Center

Last updated: 2026-07-16

Purpose: this file is the single command center for the Mira AI fashion magazine workflow. When other files disagree, use this file plus generated `DAILY_COCKPIT` / `PUBLISH_QUEUE` as the operational source of truth.

## Current Strategy

```text
Production-first:
keep producing polished, image-led Instagram carousel posts.
Target cadence is 5 carousel posts per week, one per day.
Each 5-post week uses M01-M05 exactly once in a reproducible shuffled order.
Zero reach is a distribution signal, not a reason to stop production.
```

Current workflow:

```text
Perplexity weekly trends -> 5-post weekly packet -> daily queue -> internal model M01-M05 rotation -> Hero-first photoreal image session -> image review -> asset selection -> Canva master duplicate -> publish -> metrics
```

Week numbering rule:

```text
Use ISO 8601 week dates everywhere.
Weeks start on Monday; W01 is the week containing the year's first Thursday.
The Perplexity week id, run folder, packet week_id, carousel id, and daily queue dates must agree.
Example: 2026-W27 = 2026-06-29 through 2026-07-05; 2026-W29 starts 2026-07-13.
An unfinished ISO-week batch remains in the production queue until its five carousel items are completed; the current calendar week does not archive it automatically.
```

## Canonical Files

Use these as the highest-priority files:

```text
COMMAND_CENTER.md
CURRENT_STATUS.md
COMPUTER_B_SYNC.md
10_automation/DAILY_COCKPIT.html
10_automation/PUBLISH_QUEUE.md
10_automation/TODAY.md
10_automation/runs/DASHBOARD.md
10_automation/INTEGRATION_AUDIT_2026-07-09.md
```

Model source of truth:

```text
02_brand/mira_model_roster.json
02_brand/mira_reference_images.csv
02_brand/reference_models/
```

Canva source of truth:

```text
10_automation/canva_template_registry.md
10_automation/canva_template_registry.json
```

Weekly run source of truth:

```text
10_automation/runs/{week_id}/weekly_content_packet.csv
10_automation/runs/{week_id}/daily_queue.csv
10_automation/runs/{week_id}/canva_placeholder_values.csv
10_automation/runs/{week_id}/canva_asset_slots.csv
10_automation/runs/{week_id}/codex_asset_selection.csv
```

## Daily Command

Run this first:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-07-09
```

Then open:

```text
10_automation/DAILY_COCKPIT.html
```

## Fresh Weekly Start From Perplexity

First check what the public Perplexity index currently exposes:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\resolve_perplexity_source.py `
  --index https://mika-lin-weekly.pplx.app/data/index.json `
  --json
```

If the returned week is the intended new week, run:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action pipeline `
  -UsePerplexityIndex `
  -Limit 2
```

The pipeline now creates the weekly packet, daily queue, Codex image job folders, `codex_generation_handoff.md`, Canva handoff files, and weekly status.

Current state as of 2026-07-16:

```text
Perplexity index latest imported run = 2026-W29
Active run folder = 10_automation/runs/2026-W29
W29 contains five carousel packets and assigns M01-M05 exactly once.
Old W29 v2 A/B/C selections are superseded for new production.
The Hero-first photoreal trial is complete for W29-001 through W29-005: five carousel sets, fifteen selected images, and strict validation at 0 errors / 0 warnings.
```

## Current Top Item

```text
items = 2026-W29-001 through 2026-W29-005
models = M01, M02, M04, M03, M05
stage = needs_visual_revision
selected assets = 15 / 15
blocking reason = default Canva center-cover crop cuts the hairstyle/head in most source images
next operation = create one near-square crop-safe A derivative pilot, replace it in W29-001, and validate the untouched Canva crop before scaling to the remaining designs
```

Current gate: visual revision before export. All 15 original PNGs and five committed Canva duplicates remain preserved, but they are not approved for publishing. Do not rely on Canva Smart Crop or manual focal adjustment as the automation path. Do not reuse old W29 v2 selections. Google Drive remains optional archive-only storage.

## Hero-First Photoreal Pilot

Active trial rule:

```text
A Hero = one coherent person-and-environment photograph using face/full-body anchors
optional A refinement = one lighting/camera-finish edit only
B Motion = edit derived from accepted A
C Detail = edit derived from accepted A
Canva = blocked until the three-asset session passes visual review
```

The accepted Hero must have plausible head/body proportions, real physical interaction, shared scene lighting, contact shadows, and no pasted-on appearance. B/C cannot independently reinterpret the wardrobe or scene.

Invalidated Canva flat image assets:

```text
cover_image Canva asset id = MAHOCYb2mPI
motion_crop Canva asset id = MAHOCUFmjRs
detail_image Canva asset id = MAHON_SkSjs
reason = generated before M02 v3 reference anchors; old model identity
```

Current Canva test copy:

```text
design_id = DAHO2rHNkZs
edit_url = https://www.canva.com/d/BADXM4PGvSs2Rlh
status = invalid, do not export or publish
```

Do not export or publish these failed Canva drafts:

```text
DAHOyDPZHeQ
DAHO2rHNkZs
```

## State Rules

A carousel can be `ready_for_canva_and_publish` only when all are true:

```text
image selection status = selected
cover_image = selected and has a file
motion_crop = selected and has a file
detail_image = selected and has a file
canva_frame_fit >= 4 for every selected asset
untouched center-cover crop preserves the full hairstyle, face, and required outfit focus
no slot has needs_review / needs_regeneration / rejected / missing
machine text files have no encoding drift
if Canva autofill is needed, all required flat Canva image asset ids are known
```

If any of those fail, the item must stay in one of these stages:

```text
needs_image_asset_selection
needs_visual_revision
canva_blocked_waiting_for_flat_png_asset
```

## Canva Rules

Use one registered master template:

```text
A Contact Sheet
B Symmetric
C Noir Evening
D Full-Bleed
E Weekend Air
```

Always duplicate the master before filling. Never overwrite the master.

Allowed image replacement:

```text
complete flat PNG/JPG image assets only
```

Disallowed for final fills:

```text
image_to_design
Magic Layers
background/person/object split assets
old Canva design asset ids unless verified as complete flat image assets
```

## Image Job Command

Prepare a strict image job:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action image-job `
  -Week 2026-W29 `
  -CarouselId 2026-W29-001 `
  -AssetProvider Codex
```

This writes:

```text
10_automation/runs/2026-W29/generated_images/2026-W29-001/image_job.md
10_automation/runs/2026-W29/generated_images/2026-W29-001/candidate_prompts.md
10_automation/runs/2026-W29/generated_images/2026-W29-001/review_sheet.csv
10_automation/runs/2026-W29/generated_images/2026-W29-001/codex_generation_handoff.md
```

## Validation Commands

Run these before treating the repo as synchronized:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action validate -Week 2026-W27 -Limit 5
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-07-09
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action smoke-test
```

Expected current result:

```text
W27 baseline validation should pass. W27 --require-assets validation should fail until generated images are scored and selected.
Smoke test should pass because generic automation entrypoints still work.
```

## Git Sync Rule

Before changing computers:

```powershell
& 'C:\Users\Brandon_ChangChien\AppData\Local\Programs\Git\cmd\git.exe' status --short
```

Do not push private user-upload source images unless explicitly approved.
