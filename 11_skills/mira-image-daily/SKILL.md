---
name: mira-image-daily
description: Use when working on the Mira AI fashion magazine image workflow in the 人物試衣間 project: turning global Perplexity weekly fashion trend rows into daily image-generation jobs, enforcing M01/M02/M03/M04/M05 face/full reference-start-image consistency, creating candidate prompts, storing generated images in the project run folder, and preparing image review sheets before Canva.
---

# Mira Image Daily

Use this skill for Mira image generation, not for Canva layout. Mira is a fast-updating AI fashion magazine brand using global fashion trends, then translating them into wearable daily outfit images.

## Required Project Context

Work inside the `人物試衣間` project root.

Canonical files:

```text
02_brand/mira_model_roster.json
02_brand/mira_reference_images.csv
10_automation/runs/{week_id}/weekly_content_packet.csv
10_automation/runs/{week_id}/daily_queue.csv
10_automation/runs/{week_id}/generated_images/{carousel_id}/review_sheet.csv
```

Before generating images, read:

```text
references/image-standard.md
references/reference-start-images.md
```

## Workflow

1. Identify the daily item from `daily_queue.csv` or the requested `carousel_id`.
2. Load the model profile from `mira_model_roster.json`.
3. Confirm the required face and full-body reference start images exist through `mira_reference_images.csv`.
4. Run `scripts/prepare_daily_image_job.py` to create a strict job folder.
5. Use the generated candidate prompts with the available image-generation tool.
6. Save accepted outputs under the job folder and/or `generated_images/`.
7. Fill the job review sheet before asset selection or Canva.

Do not skip step 3. If either reference image is missing, stop and tell the user which reference image must be created or supplied first.

## Command

Use this from the project root:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  11_skills\mira-image-daily\scripts\prepare_daily_image_job.py `
  --project-root . `
  --run-dir 10_automation\runs\2026-W26 `
  --carousel-id 2026-W26-002
```

The script writes:

```text
10_automation/runs/{week_id}/generated_images/{carousel_id}/image_job.md
10_automation/runs/{week_id}/generated_images/{carousel_id}/candidate_prompts.md
10_automation/runs/{week_id}/generated_images/{carousel_id}/review_sheet.csv
```

## Generation Rules

- Use global trend input, but translate it into a wearable daily outfit image.
- Use the assigned internal model only: `M01`, `M02`, `M03`, `M04`, or `M05`.
- Use the model's approved face and full-body reference start images as identity anchors.
- Do not publish or render model IDs, names, labels, prompt notes, reference-image metadata, or numeric true ages.
- Generate 2-3 candidates first. Stop early if one is strong enough.
- Prefer one excellent full-body image plus smart crops over three weak unrelated images.

Prompt age rule:

```text
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin is smooth and well-maintained.
```

Reject images with supermodel distance, runway mood, luxury hotel advertising, plastic skin, obvious AI anatomy, hidden outfits, visible logos, image text, watermarks, celebrity likeness, or wrinkle-based age cues.

## Output Discipline

Store image outputs in the run folder:

```text
10_automation/runs/{week_id}/generated_images/{carousel_id}/
```

Use filenames like:

```text
{carousel_id}_{model_profile_id}_candidate_A.png
{carousel_id}_{model_profile_id}_candidate_B.png
{carousel_id}_{model_profile_id}_candidate_C.png
```

After generation, update the review sheet with:

```text
model_consistency
reader_relatability
outfit_clarity
ai_realism
commerce_value
publishable
status
notes
```

Only mark `publishable = yes` when `outfit_clarity >= 4` and `ai_realism >= 4`; user visual approval gates Canva readiness in the wider automation flow.
