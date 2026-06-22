# Computer B Sync Handoff

Last synced: 2026-06-22

Purpose: let another computer continue the Mika Lin workflow from GitHub without reading the old conversation.

## Start On Computer B

Run from the repo folder:

```powershell
& 'C:\Users\Brandon_ChangChien\AppData\Local\Programs\Git\cmd\git.exe' pull origin main
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-06-22
```

Then open:

```text
10_automation/DAILY_COCKPIT.html
```

If HTML is inconvenient, open:

```text
10_automation/DAILY_COCKPIT.md
10_automation/PUBLISH_QUEUE.md
10_automation/TODAY.md
```

## Current Strategy

Production-first.

```text
Keep producing polished carousel posts.
Zero reach is tracked as data, not a blocker.
Visibility tests are optional side checks.
No affiliate/product monetization until a channel has non-zero reach.
```

## Current Top Item

```text
item = 2026-W21-test-001
type = carousel
stage = ready_for_canva_and_publish
asset = IMG_1453.JPG
next = Use Canva handoff files to finish the carousel and publish it.
```

## Files For Current Top Item

Open these when working on the carousel:

```text
10_automation/runs/2026-W21-test/canva_fill_guide.md
10_automation/runs/2026-W21-test/canva_asset_plan.md
10_automation/runs/2026-W21-test/post_drafts.md
10_automation/runs/2026-W21-test/publish_checklist.md
```

## Current Queue

```text
1. 2026-W21-test-001
   type = carousel
   stage = ready_for_canva_and_publish
   action = finish Canva carousel and publish

2. 2026-W21-test-002-visibility-01
   type = visibility_test
   stage = ready_to_publish_visibility_test
   action = optional side test, not a blocker

3. 2026-W21-test-002
   type = carousel
   stage = visibility_recovery
   reach = 0
   action = keep production moving
```

## What To Send Back To Codex

After working on the top item, paste:

```text
今日回報：
item = 2026-W21-test-001
type = carousel
status =
Canva URL =
IG URL =
published at =
6h metrics = reach / likes / saves / comments / shares
24h metrics = reach / likes / saves / comments / shares
stuck =
```

## Git Rule Between Computers

Before switching computers:

```powershell
& 'C:\Users\Brandon_ChangChien\AppData\Local\Programs\Git\cmd\git.exe' status --short
& 'C:\Users\Brandon_ChangChien\AppData\Local\Programs\Git\cmd\git.exe' pull origin main
```

If there are local changes, commit and push them before moving to the other machine.

## Main Automation Commands

Create daily cockpit:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-06-22
```

Refresh queue only:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action queue
```

Run smoke test after setup or pull:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action smoke-test
```

Record post metrics:

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action metrics `
  -Week 2026-W21-test `
  -CarouselId 2026-W21-test-001 `
  -PostUrl "https://www.instagram.com/p/POST_ID/" `
  -PublishedAt "YYYY/MM/DD HH:mm" `
  -RecordMetrics `
  -MeasuredAt YYYY-MM-DD `
  -HoursAfterPublish 24 `
  -Reach 0 `
  -Likes 0 `
  -Saves 0 `
  -Comments 0 `
  -Shares 0
```
