---
name: mira-image-daily
description: Use when working on the Mira AI fashion magazine image workflow in the 人物試衣間 project: turn global Perplexity weekly fashion rows into daily Hero-first photoreal image sessions, enforce M01-M05 face and body references, derive B Motion and C Detail from an accepted Hero, store outputs in weekly run folders, and review assets before Canva.
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
5. Generate one integrated-scene Hero A with both model references. Review it before any other generation.
6. If A has correct identity, proportions, outfit, physical contact, and scene lighting, optionally run one lighting/camera-finish edit. This accepted A becomes the session lock.
7. Create B Motion and C Detail as edits derived from accepted A, with the two model references attached. Do not independently regenerate the outfit or scene.
8. Save accepted outputs under the job folder and fill the review sheet before asset selection or Canva.
9. Read `canva_slot_targets.json`. Prepare A/B/C for the exact frame dimensions of the already assigned master; do not generate one generic portrait set before template selection.
10. Run `scripts/prepare_canva_ready_assets.py` to normalize approved, crop-safe sources to exact frame pixels without stretching. The script rejects source/frame mismatches that need more than 15% center crop.
11. Verify the untouched result in the assigned Canva master. If the full hairstyle, face, or outfit focus is cropped, reject the asset or create a better-composed derivative before Canva commit.

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
10_automation/runs/{week_id}/generated_images/{carousel_id}/canva_slot_targets.json
```

After A/B/C visual approval, normalize them to the selected master:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  11_skills\mira-image-daily\scripts\prepare_canva_ready_assets.py `
  --project-root . `
  --run-dir 10_automation\runs\2026-W29 `
  --carousel-id 2026-W29-001 `
  --source-a accepted_A.png `
  --source-b accepted_B.png `
  --source-c accepted_C.png
```

## Generation Rules

- Use global trend input, but translate it into a wearable daily outfit image.
- Use the assigned internal model only: `M01`, `M02`, `M03`, `M04`, or `M05`.
- Use the model's approved face and full-body reference start images as identity anchors.
- Do not publish or render model IDs, names, labels, prompt notes, reference-image metadata, or numeric true ages.
- Generate and review A first. Do not queue B/C before A passes.
- A is one coherent lifestyle photograph with shared scene light, contact shadows, ambient spill, depth of field, and grain.
- A may receive at most one targeted lighting/camera-finish edit while identity, outfit, anatomy, pose, scene, and composition stay locked.
- B/C must be edits derived from accepted A and preserve its exact outfit, scene, lighting logic, body build, and photographic treatment. Independent B/C generation is not allowed.
- Treat face/full-body references as identity and proportion anchors only. Never copy their neutral expression, centered stance, hand position, studio background, or reference outfit.
- A/B should differ in body angle, gaze, hand interaction, and expression while preserving identity, wardrobe, body proportions, normal-lens perspective, and scene continuity. C may use a closer outfit-detail crop.
- Use a normal 50mm full-frame-equivalent perspective near chest height with a level optical axis. Never use a low angle or wide-angle perspective for full-body images.
- Include a real foreground or scene object with physically believable hand, foot, clothing, or bag interaction whenever suitable.
- Prefer one excellent integrated Hero plus two controlled derivatives over three unrelated full-body images.
- Select the Canva master before generation. A/B/C must use the exact aspect ratios in `canva_slot_targets.json`; v3-D B is portrait while A/B/C motion frames in the other masters may be shallow horizontal strips.
- Keep the full hairstyle below an 8% top safe margin, preserve scene space above the hair, and keep face/outfit focus in the central 70%. Do not depend on Canva Smart Crop or manual focal-point adjustment.
- Exact pixel normalization may center-crop at most 15% and must never stretch the image. A larger required crop means the source composition is wrong and must be regenerated.

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
10_automation/runs/{week_id}/generated_images/{carousel_id}/canva_ready/
```

Use filenames like:

```text
{carousel_id}_{model_profile_id}_candidate_A.png
{carousel_id}_{model_profile_id}_candidate_B.png
{carousel_id}_{model_profile_id}_candidate_C.png
```

For the active pilot, a refined accepted A may use:

```text
{carousel_id}_{model_profile_id}_candidate_A_refined_v2.png
```

After generation, update the review sheet with:

```text
model_consistency
body_proportion_consistency
reader_relatability
outfit_clarity
ai_realism
commerce_value
scene_lighting_integration
outfit_continuity
expression_liveliness
pose_variation
canva_frame_fit
publishable
status
notes
```

Only mark `publishable = yes` when `body_proportion_consistency >= 4`, `outfit_clarity >= 4`, `ai_realism >= 4`, `scene_lighting_integration >= 4`, `outfit_continuity >= 4`, `expression_liveliness >= 4`, `pose_variation >= 4`, and `canva_frame_fit >= 4`. Any body-to-leg ratio drift, fashion-elongated anatomy, pasted-on lighting, missing contact shadow, white border, A/B/C wardrobe drift, frozen expression, repeated centered pose, or default Canva crop that cuts hair/face/outfit focus is an automatic rejection. User visual approval gates Canva readiness in the wider automation flow.
