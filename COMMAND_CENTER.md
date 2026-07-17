# Mira Command Center

Updated: 2026-07-17

Detailed source of truth:

```text
10_automation/CANONICAL_WORKFLOW.md
```

Computer B handoff:

```text
COMPUTER_B_SYNC.md
```

## Current Strategy

```text
Production-first
5 Instagram carousels per ISO week
M01-M05 each used once
Perplexity global trend input
Codex exact-frame image generation
Canva v3 duplicate and approved transaction
manual three-slice export and Instagram publishing
```

Grok is inactive. Google Drive is optional archive storage. Zero reach does not stop production.

## Resume Work

```powershell
git pull origin main
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action dashboard
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action queue
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action cockpit
```

Open:

```text
10_automation/DAILY_COCKPIT.html
10_automation/PUBLISH_QUEUE.md
CURRENT_STATUS.md
```

Use the top queue item. Do not ask for a Day number.

## Stage Meaning

```text
needs_image_asset_selection = generate and review exact-ratio A/B/C
needs_canva_frame_review = prepare Canva draft and request approval
needs_visual_revision = reject and correct image or frame defect
ready_for_manual_export = Canva is already saved; only slice/export/post
published_waiting_for_metrics = post exists; metrics are optional follow-up
```

Never move a `ready_for_manual_export` item backward unless the user reports a visible defect.

## Current Verified State

```text
week = 2026-W29
quality = pass, 0 errors, 0 warnings
W29-001 M01 v3-B = ready_for_manual_export
W29-002 M02 v3-E = ready_for_manual_export
W29-003 M04 v3-B = ready_for_manual_export
W29-004 M03 v3-B = ready_for_manual_export
W29-005 M05 v3-E = ready_for_manual_export
```

W29 is a structural example only. Future weeks must use their own Perplexity rows and newly generated images.

## Canva Contract

```text
canvas = 3240x1350
slides = 3 x 1080x1350
guides = x 1080 and 2160
slots = cover_image, motion_crop, detail_image, slide2_line
```

Use a v3 master duplicate. Use complete flat PNGs. Preview the draft and save only after explicit user approval.

## End Work

```powershell
git status --short
git diff --check
git add <intended files>
git commit -m "Describe the completed checkpoint"
git push origin main
```

Every accepted asset, Canva URL, stage change, publish URL, and workflow change must be pushed to GitHub before switching computers.
