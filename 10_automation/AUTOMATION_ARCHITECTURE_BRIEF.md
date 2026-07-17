# Mira Automation Architecture Brief

Updated: 2026-07-17

Detailed operating instructions: `10_automation/CANONICAL_WORKFLOW.md`.

## 1. Objective

Produce five polished Instagram carousel packages per ISO week from global fashion trends, using M01-M05 exactly once each, while keeping only Canva slicing/export and Instagram posting manual.

## 2. System Flow

```text
Perplexity deployed index / CSV
-> import and weekly packet
-> five-item model rotation
-> Canva master selection
-> exact-frame Codex A/B/C generation
-> visual and machine validation
-> GitHub asset checkpoint
-> Canva draft transaction
-> user preview approval
-> committed Canva duplicate
-> manual slice/export/post
-> publish registry and optional metrics
```

## 3. System Layers

1. Trend: Perplexity public weekly report and machine CSV.
2. Planning: weekly packet, daily queue, prompt id, model assignment, template key.
3. Identity: M01-M05 face/full-body anchors.
4. Images: Hero-first A/B/C generation and exact-ratio normalization.
5. Canva: flat-image upload, transactional frame replacement, preview, approval, commit.
6. Control: weekly status, dashboard, publish queue, daily cockpit.
7. Distribution: manual export/publish, then URL and optional metrics recording.

## 4. Automation Boundary

Automated or Codex-operated:

- import latest deployed Perplexity week;
- select five rows and rotate M01-M05;
- select a Canva master before generation;
- prepare per-carousel prompt and exact slot contract;
- generate A Hero, derive B Motion and C Detail;
- validate identity, proportions, lighting, outfit continuity, and crop;
- normalize exact PNG dimensions without stretching;
- checkpoint assets and status to GitHub;
- upload flat PNGs to Canva;
- replace exact frames in a draft transaction;
- show preview and commit after explicit approval;
- regenerate status, queue, cockpit, and validation reports.

Intentional manual boundary:

- use Canva slicing app;
- export three 1080x1350 slides;
- publish/schedule Instagram;
- provide post URL and publish time.

Optional:

- Google Drive archive;
- 6h/24h metrics;
- visibility tests.

Inactive:

- Grok image generation;
- Google Drive as required image transport;
- five-slide Canva templates;
- Magic Layers or `image_to_design` final fills.

## 5. State Machine

```text
needs_image_asset_selection
-> needs_canva_frame_review
-> canva_frame_approved
-> ready_for_manual_export
-> published_waiting_for_metrics
```

Correction states:

```text
needs_visual_revision
canva_blocked_waiting_for_flat_png_asset
quality_gate_not_passed
```

`ready_for_manual_export` is terminal for automated production. It must not return to Canva unless the user reports a defect.

## 6. Data Contracts

Per week:

```text
weekly_content_packet.csv
daily_queue.csv
quality_report.md/json
weekly_status.md/json
```

Per carousel:

```text
image_job.md
candidate_prompts.md
canva_slot_targets.json
review_sheet.csv
canva_ready/*.png
canva_ready/canva_ready_manifest.json
```

Canva handoff:

```text
canva_asset_inventory.csv
canva_asset_slots.csv
canva_placeholder_map.json
codex_asset_selection.csv
canva_autofill_status.md
```

Control:

```text
runs/DASHBOARD.md
PUBLISH_QUEUE.md
TODAY.md
DAILY_COCKPIT.html
```

## 7. Canva Contract

```text
master canvas: 3240x1350
output: 3 x 1080x1350
guides: x=1080, x=2160
slots: cover_image, motion_crop, detail_image, slide2_line
```

One carousel uses one registered v3 master and three newly generated exact-frame images. Masters are duplicated, never edited directly.

## 8. Cross-Computer Contract

GitHub `main` is the source of truth. Every accepted image, Canva URL, transaction status, queue change, and workflow change is committed before switching computers.

Start:

```powershell
git pull origin main
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action cockpit
```

End:

```powershell
git status --short
git diff --check
git add <intended files>
git commit -m "Describe checkpoint"
git push origin main
```

## 9. Quality Gates

Image gate:

- fixed model identity and realistic proportions;
- shared person/environment lighting;
- exact outfit continuity;
- believable physical contact;
- full hair and outfit focus inside target frame;
- no more than 15% center crop;
- no stretch, border, text, logo, or watermark.

Canva gate:

- all page assets inspected before replacement;
- three complete flat images;
- correct registered element ids;
- draft thumbnail reviewed;
- explicit user save approval;
- successful commit;
- full `Mira` mark and clean slice boundaries.

Run gate:

```text
Validation pass: 0 error(s), 0 warning(s).
```

## 10. Verified Baseline

W29 completed the full exact-frame workflow:

```text
5 carousels
15 exact-frame images
5 committed Canva duplicates
all items ready_for_manual_export
0 validation errors
0 validation warnings
```

W29 is the regression reference for future weekly automation tests.
