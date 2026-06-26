# Computer B Sync Handoff

Last synced locally: 2026-06-26

Purpose: let another computer continue the Mira workflow from GitHub without reading the old conversation.

## Start On Computer B

Run from the repo folder:

```powershell
& 'C:\Users\Brandon_ChangChien\AppData\Local\Programs\Git\cmd\git.exe' pull origin main
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-06-26
```

The PowerShell entrypoint is still named `mika_weekly.ps1` for compatibility. The public creator name is now `Mira`.

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

Production-first, image-led.

```text
Mira -> believable daily outfit images -> 3-slide low-text Canva carousel -> short caption -> profile link
```

Rules:

- Do not publish another old W21 Grok-similar carousel.
- Use the 3-slide minimal panorama template.
- Keep text off the carousel except `{{slide2_line}}`.
- Keep AI disclosure in the caption.
- Use OpenAI or Grok based on image quality and available credits.
- Zero reach is tracked as data, not a blocker.

## Current Top Item

```text
item = 2026-W26-002
type = carousel
stage = ready_for_canva_and_publish
asset = ChatGPT Image 2026年6月24日 下午03_30_10.png
next = Use Canva handoff files to finish the carousel and publish it.
```

## Files For Current Top Item

Open these when working on the carousel:

```text
10_automation/runs/2026-W26/canva_fill_guide.md
10_automation/runs/2026-W26/canva_asset_plan.md
10_automation/runs/2026-W26/post_drafts.md
10_automation/runs/2026-W26/publish_checklist.md
```

Current recommended template prompt:

```text
10_automation/claude_design_mira_template_v1_prompt.md
```

Current Mira identity file:

```text
02_brand/mira_identity_block.md
```

## Current Queue

```text
1. 2026-W26-002
   type = carousel
   stage = ready_for_canva_and_publish
   asset = ChatGPT Image 2026年6月24日 下午03_30_10.png
   action = finish the 3-slide Canva carousel and publish / schedule

2. 2026-W26-001
   type = carousel
   stage = ready_for_canva_and_publish
   asset = ChatGPT Image 2026年6月24日 下午03_30_22.png
   action = backup / second carousel candidate
```

## Canva Template Contract

Use:

```text
3240 x 1350 px master canvas
3 slides x 1080 x 1350 px
slice guides: x = 1080, 2160
```

Required Canva names:

```text
cover_image
texture_or_crop
detail_image
{{slide2_line}}
```

Do not use the old 5-slide / 10-slide report template for current IG production.

## Validation Status

Latest local checks:

```text
W26 validation: pass, 0 errors, 0 warnings
Smoke test: passed
```

## Reply Template

After working on Computer B, send Codex:

```text
今日回報：
item = 2026-W26-002
type = carousel
status =
Canva URL =
IG URL =
published at =
6h metrics = reach / likes / saves / comments / shares
24h metrics = reach / likes / saves / comments / shares
stuck =
```
