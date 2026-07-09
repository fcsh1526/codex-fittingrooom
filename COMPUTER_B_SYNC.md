# Computer B Sync Handoff

Last synced locally: 2026-07-09

Purpose: let another computer continue the Mira workflow from GitHub without reading the old conversation.

Primary command center:

```text
COMMAND_CENTER.md
```

## Start On Computer B

Run from the repo folder:

```powershell
& 'C:\Users\Brandon_ChangChien\AppData\Local\Programs\Git\cmd\git.exe' pull origin main
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit
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
- Use Codex workspace image generation as the primary image path. Grok is not part of the active workflow.
- Zero reach is tracked as data, not a blocker.

## Current Top Item

```text
item = 2026-W27-001
type = carousel
model = M01
stage = needs_image_asset_selection
asset = n/a
next = Open codex_generation_handoff.md, generate M01 candidates, score review_sheet.csv, then run select_codex_assets.py.
```

Fresh test report:

```text
10_automation/PERPLEXITY_FRESH_PIPELINE_TEST_2026-07-09.md
```

## Files For Current Top Item

Open these when working on the carousel:

```text
10_automation/runs/2026-W27/canva_fill_guide.md
10_automation/runs/2026-W27/canva_asset_plan.md
10_automation/runs/2026-W27/daily_queue.csv
10_automation/runs/2026-W27/image_generation_briefs.md
10_automation/runs/2026-W27/image_review_template.csv
10_automation/runs/2026-W27/generated_images/2026-W27-001/codex_generation_handoff.md
10_automation/runs/2026-W27/generated_images/2026-W27-001/candidate_prompts.md
10_automation/runs/2026-W27/generated_images/2026-W27-001/review_sheet.csv
10_automation/runs/2026-W27/post_drafts.md
10_automation/runs/2026-W27/publish_checklist.md
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

Current command center audit:

```text
10_automation/INTEGRATION_AUDIT_2026-07-09.md
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
M01/M02/M03/M04/M05 are fixed internal model identities, not fixed outfit categories.
Any weekly trend can be styled for work, commute, weekend, date, travel, rainy day, or daily casual with any model when the content plan calls for it.
```

Do not publish model names in IG copy; they are only for consistent image generation.

Image generation note:

```text
W26-002 v2 assets and Canva copy `DAHO2rHNkZs` were invalidated after the user caught old model identity drift. Do not use A_v2/B_v2/C_v2 or the old Canva asset ids.

Next image set must be generated in Codex with:

02_brand/reference_models/M02_start_v3_face.png
02_brand/reference_models/M02_start_v3_full.png

2026-07-08 Canva automation trial note: A Contact Sheet duplicate `DAHOyDPZHeQ` was saved with old split Canva asset ids and failed again with missing person layers / blurred background-only street images. Do not export or publish that design. Future Canva autofill must use complete flat PNG/JPG assets only.
```

Installed skill:

```text
C:\Users\Brandon_ChangChien\.codex\skills\mira-image-daily
```

## Current Queue

```text
1. 2026-W27-001
   type = carousel
   model = M01
   stage = needs_image_asset_selection
   package = 10_automation/runs/2026-W27/generated_images/2026-W27-001/codex_generation_handoff.md
   action = generate Codex image candidates, score review_sheet.csv, then run select_codex_assets.py

2. 2026-W27-002
   type = carousel
   model = M02
   stage = needs_image_asset_selection

3. 2026-W27-003
   type = carousel
   model = M03
   stage = needs_image_asset_selection
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

Do not split Canva image uploads into background, person cutout, and object layers. Replace whole flat PNG/JPG images into the named frames. Do not use `image_to_design`, Magic Layers, or old Canva design asset ids unless the asset is verified as a complete flat image.

## Validation Status

Latest local checks:

```text
W27 baseline validation: pass
W27 require-assets validation: expected to fail until Codex image candidates are generated, scored, and selected
Smoke test: passed
```

## Reply Template

After working on Computer B, send Codex:

```text
今日回報：
item = 2026-W27-001
type = carousel
status =
Canva URL =
IG URL =
published at =
6h metrics = reach / likes / saves / comments / shares
24h metrics = reach / likes / saves / comments / shares
stuck =
```
