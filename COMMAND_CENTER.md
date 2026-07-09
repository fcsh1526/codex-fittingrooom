# Mira Command Center

Last updated: 2026-07-09

Purpose: this file is the single command center for the Mira AI fashion magazine workflow. When other files disagree, use this file plus generated `DAILY_COCKPIT` / `PUBLISH_QUEUE` as the operational source of truth.

## Current Strategy

```text
Production-first:
keep producing polished, image-led Instagram carousel posts.
Zero reach is a distribution signal, not a reason to stop production.
```

Current workflow:

```text
Perplexity trend -> weekly packet -> daily queue -> internal model M01-M05 -> reference-start image job -> image review -> asset selection -> Canva master duplicate -> publish -> metrics
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

## Current Top Item

```text
item = 2026-W26-002
model = M02
stage = ready_for_canva_test
template = A Contact Sheet
```

Verified Canva flat image assets:

```text
cover_image Canva asset id = MAHOCYb2mPI
motion_crop Canva asset id = MAHOCUFmjRs
detail_image Canva asset id = MAHON_SkSjs
```

Current Canva test copy:

```text
design_id = DAHO2rHNkZs
edit_url = https://www.canva.com/d/FAQqtC4Lubay7GY
status = copied, not filled or committed yet
```

Do not export or publish the failed Canva draft:

```text
DAHOyDPZHeQ
```

## State Rules

A carousel can be `ready_for_canva_and_publish` only when all are true:

```text
image selection status = selected
cover_image = selected and has a file
motion_crop = selected and has a file
detail_image = selected and has a file
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
  -Week 2026-W26 `
  -CarouselId 2026-W26-002 `
  -AssetProvider Codex
```

This writes:

```text
10_automation/runs/2026-W26/generated_images/2026-W26-002/image_job.md
10_automation/runs/2026-W26/generated_images/2026-W26-002/candidate_prompts.md
10_automation/runs/2026-W26/generated_images/2026-W26-002/review_sheet.csv
```

## Validation Commands

Run these before treating the repo as synchronized:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action validate -Week 2026-W26 -Limit 2 -RequireAssets
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-07-09
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action smoke-test
```

Expected current result:

```text
W26 strict validation should fail until the Canva detail_image asset id and W26-001 image selection issues are resolved.
Smoke test should pass because generic automation entrypoints still work.
```

## Git Sync Rule

Before changing computers:

```powershell
& 'C:\Users\Brandon_ChangChien\AppData\Local\Programs\Git\cmd\git.exe' status --short
```

Do not push private user-upload source images unless explicitly approved.
