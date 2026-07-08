# Computer B Sync Handoff

Last synced locally: 2026-07-08

Purpose: let another computer continue the Mira workflow from GitHub without reading the old conversation.

## Start On Computer B

Run from the repo folder:

```powershell
& 'C:\Users\Brandon_ChangChien\AppData\Local\Programs\Git\cmd\git.exe' pull origin main
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-06-29
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
Mira magazine -> global weekly trend -> daily outfit queue -> internal model profile -> approved reference start image -> believable outfit images -> 3-slide low-text Canva carousel -> short caption -> profile link
```

Rules:

- Do not publish another old W21 Grok-similar carousel.
- Use the 3-slide Mira high-fashion carousel v2 template direction.
- Keep text off the carousel except `{{slide2_line}}`.
- Keep AI disclosure in the caption.
- Use the `$mira-image-daily` skill for image jobs.
- Do not generate daily outfit images for a model until its reference start image is approved.
- Keep OpenAI API / Grok as optional backup paths only.
- Zero reach is tracked as data, not a blocker.

## Current Top Item

```text
item = 2026-W26-002
type = carousel
model = M02
stage = needs_visual_revision
asset = ChatGPT Image 2026年6月24日 下午03_30_10.png
next = Do not publish. Canva v2 template is built and autofill labels are saved; regenerate cleaner image candidates, then test-fill the template.
```

## Files For Current Top Item

Open these when working on the carousel:

```text
10_automation/runs/2026-W26/canva_fill_guide.md
10_automation/runs/2026-W26/canva_asset_plan.md
10_automation/runs/2026-W26/daily_queue.csv
10_automation/runs/2026-W26/image_generation_briefs.md
10_automation/runs/2026-W26/image_review_template.csv
10_automation/runs/2026-W26/m02_polka_image_test_brief.md
10_automation/runs/2026-W26/post_drafts.md
10_automation/runs/2026-W26/publish_checklist.md
10_automation/mira_high_fashion_carousel_template_v2.md
10_automation/claude_design_mira_template_v2_prompt.md
02_brand/mira_reference_images.csv
02_brand/reference_models/REFERENCE_IMAGE_REQUIREMENTS.md
11_skills/mira-image-daily/SKILL.md
```

Current recommended template prompt:

```text
10_automation/claude_design_mira_template_v2_prompt.md
```

Current Canva template:

```text
10_automation/canva_template_registry.md
10_automation/canva_template_registry.json
```

Canva automation status:

```text
Five Canva master templates were registered on 2026-07-08.

Master templates:
A Contact Sheet = https://www.canva.com/design/DAHOx6hb1Ug/A1sysuKRtad0lCYR8jqBQg/edit
B Symmetric = https://www.canva.com/design/DAHOxwp1cZ8/cIfSmcVa-DAJJrT-21PJoA/edit
C Noir Evening = https://www.canva.com/design/DAHOyEHkFvg/DBpyigPr05vQqxuuqV7wKA/edit
D Full-Bleed = https://www.canva.com/design/DAHOyNz_Dh4/SCdZqafV5zkpK5TVIB6kMw/edit
E Weekend Air = https://www.canva.com/design/DAHOyEiLL24/yTWykrCQdrFjncOa46cq9g/edit

Required slots:
cover_image
motion_crop
detail_image
slide2_line
```

Current Mira identity file:

```text
02_brand/mira_identity_block.md
02_brand/mira_model_roster.md
02_brand/mira_image_generation_spec_v1.md
02_brand/mira_reference_images.csv
```

Internal model rule:

```text
M01 = office / commute
M02 = weekend / date / cafe
M03 = casual / budget-friendly daily wear
```

Do not publish model names in IG copy; they are only for consistent image generation.

Image generation note:

```text
W26-002 should not be published from the old Canva fill. The user rejected it on 2026-07-01 because the generated images had face drift / ghosting and Slide 2 cropped the head. The new Canva v2 template is built; regenerate candidates through $mira-image-daily, then test-fill the v2 template.
```

Installed skill:

```text
C:\Users\Brandon_ChangChien\.codex\skills\mira-image-daily
```

## Current Queue

```text
1. 2026-W26-002
   type = carousel
   model = M02
   stage = ready_for_canva_and_publish
   asset = ChatGPT Image 2026年6月24日 下午03_30_10.png
   action = finish the 3-slide Canva carousel and publish / schedule

2. 2026-W26-001
   type = carousel
   model = M01
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
motion_crop
detail_image
slide2_line
```

Do not use the old 5-slide / 10-slide report template for current IG production.

Do not return to a plain 3-slot placeholder layout. Use one registered Mira master template, duplicate it, then replace the named slots in the duplicate. The carousel should read as one editorial spread with intentional cross-slide crops, low text, and no accidental head crop.

Do not split Canva image uploads into background, person cutout, and object layers. Replace whole flat images into the named frames.

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
