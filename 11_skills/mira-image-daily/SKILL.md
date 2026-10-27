---
name: mira-image-daily
description: >-
  Use when working on the Mira AI fashion magazine image workflow in the 人物試衣間 project: turn global Perplexity weekly fashion rows into ten weekly looks, prepare both Reel and three-frame Carousel assets for every look, create concise Hero-first photoreal prompts with M01-M05 references, store outputs in weekly run folders, and review assets before Canva.
---

# Mira Image Daily

Use this skill for Mira image generation and Reel source planning, not for Canva layout. Mira is a fast-updating AI fashion magazine brand using global fashion trends, then translating them into wearable daily outfit images. Read `10_automation/CANONICAL_WORKFLOW.md`, `CURRENT_STATUS.md`, and the active week's `publishing_structure.md` before production; read `09_sops/mira_reel_production_sop.md` for video work.

## Required Project Context

Work inside the `人物試衣間` project root.

Canonical files:

```text
02_brand/mira_model_roster.json
02_brand/mira_reference_images.csv
10_automation/runs/{week_id}/weekly_content_packet.csv
10_automation/runs/{week_id}/weekly_look_plan.csv
10_automation/runs/{week_id}/daily_queue.csv
10_automation/runs/{week_id}/generated_images/{carousel_id}/looks/{look_id}/{surface}/review_sheet.csv
```

Before generating images, read:

```text
references/image-standard.md
references/reference-start-images.md
```

## Workflow

1. Identify the requested `look_id` in `weekly_look_plan.csv`. Its parent theme locks the model identity, while every look has its own complete outfit, scene and Hero lock. Use legacy `carousel_id` jobs only for weeks without a look plan.
2. Confirm the look's one `dressing_decision`, one `visible_action`, `visual_proof`, and `practical_rule`. Mira defaults to `utility_with_immersion`: solve one practical dressing question through an immersive lifestyle image.
3. Every approved look requires both delivery surfaces. Create separate `reel` and `carousel` jobs; never reuse one surface's crop rules for the other.
4. Load the model profile from `mira_model_roster.json`.
5. Confirm the required face and full-body reference start images exist through `mira_reference_images.csv`.
6. `--look-id ... --plan-only` may create a planning stub. Then run `scripts/prepare_daily_image_job.py --look-id ... --surface reel` and repeat with `--surface carousel` to create both strict surface-specific job folders.
7. For Reel, generate and approve one native 9:16 full-person A. For Carousel, generate and approve one full-person Hero A before any derivative.
8. If A has only one correctable defect, make one targeted edit to the same Hero. Do not create a competing A/B version. The accepted A becomes the session lock.
9. Carousel always requires B Scene Application and C Accessory Detail after A passes. B shows how the exact outfit works in its intended occasion through another corner, wider environmental view, or suitable setting. C focuses on the styling accessory while retaining enough garment context. Reel also needs one usable styling-proof view per look; review existing material for vertical composition and clarity before generating a missing view.
10. Save accepted outputs under the surface-specific job folder and fill the review sheet.
11. For `reel`, read `reel_frame_targets.json` and generate A directly at 9:16 for 1080x1920 delivery with the complete outfit readable. Record actual pixel dimensions separately. Final packaging creates five theme/model Reels; each keeps one model across two looks and uses four full/proof views. Do not require all Carousel frames in a Reel or compile different models together. Prepare linked records with `10_automation/prepare_reel_production.py`; static approval does not establish dynamic identity consistency.
12. For `carousel`, read `canva_slot_targets.json`, prepare all three accepted assets for the assigned Canva master, and run `prepare_canva_ready_assets.py` after A/B/C pass.
13. If the same scene is needed on both surfaces, keep identity, outfit, scene, and photographic treatment consistent but create a separate surface-specific composition.

For a reference/video diagnostic, preserve accepted originals and create separately named control variants. Change one factor at a time, use only actual UI-selected identity references, and record model/mode/duration/resolution, usable intervals, failures, retries, active minutes and waiting minutes. Inspect start/quarter/middle/three-quarter/end and motion/cut moments, then watch the entire selected clip. Never fabricate a pass for pending generation. Follow the active pilot gate before mass production.

Do not skip step 5. If either reference image is missing, stop and tell the user which reference image must be created or supplied first.

## Command

Use this from the project root:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  11_skills\mira-image-daily\scripts\prepare_daily_image_job.py `
  --project-root . `
  --run-dir 10_automation\runs\2026-W26 `
  --look-id 2026-W34-002-L01 `
  --surface carousel
```

For a Reel image session, use `--surface reel`. Look-specific files are written under `generated_images/{carousel_id}/looks/{look_id}/{surface}/`.

The script writes:

```text
10_automation/runs/{week_id}/generated_images/{carousel_id}/looks/{look_id}/look_plan.md
10_automation/runs/{week_id}/generated_images/{carousel_id}/looks/{look_id}/{surface}/image_job.md
10_automation/runs/{week_id}/generated_images/{carousel_id}/looks/{look_id}/{surface}/hero_A_prompt.md
10_automation/runs/{week_id}/generated_images/{carousel_id}/looks/{look_id}/{surface}/derivative_edit_prompt_templates.md
10_automation/runs/{week_id}/generated_images/{carousel_id}/looks/{look_id}/{surface}/review_sheet.csv
10_automation/runs/{week_id}/generated_images/{carousel_id}/looks/{look_id}/{surface}/canva_slot_targets.json|reel_frame_targets.json
```

When the selected Carousel master requires A/B/C and all three have visual approval, normalize them to the selected master:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  11_skills\mira-image-daily\scripts\prepare_canva_ready_assets.py `
  --project-root . `
  --run-dir 10_automation\runs\2026-W29 `
  --carousel-id 2026-W29-001 `
  --look-id 2026-W29-001-L01 `
  --source-a accepted_A.png `
  --source-b accepted_B.png `
  --source-c accepted_C.png
```

For current-contract weeks with `weekly_look_plan.csv`, always pass `--look-id`; exact assets and the manifest are written under that look's `carousel/canva_ready/`. Omit `--look-id` only for legacy weeks without a look plan.

## Generation Rules

- Use global trend input, but translate it into a wearable daily outfit image.
- One theme keeps one assigned model across exactly two looks. Each changed outfit starts a separate look-specific Hero; never treat another look's Hero as its session lock.
- Use the assigned internal model only: `M01`, `M02`, `M03`, `M04`, or `M05`.
- Use the model's approved face and full-body reference start images as identity anchors.
- Do not publish or render model IDs, names, labels, prompt notes, reference-image metadata, or numeric true ages.
- Generate and review each surface's A first. Do not queue Carousel B/C before Carousel A passes.
- A is one coherent lifestyle photograph with shared scene light, contact shadows, ambient spill, depth of field, and grain.
- A may receive at most one targeted single-defect edit while identity, outfit, scene and composition stay locked. This is correction, not A/B testing.
- Carousel B/C are required production assets. Accepted Carousel A anchors identity, exact outfit, styling placement, body build and photographic character. B is the scene-application frame and may use a different corner or setting for the same occasion; C is the accessory-detail frame and must avoid contrived hand poses.
- Treat face/full-body references as identity and proportion anchors only. Never copy their neutral expression, centered stance, hand position, studio background, or reference outfit.
- Carousel A/B should differ in environmental emphasis or camera angle while preserving identity, exact wardrobe, styling placement, body proportions and normal-lens photographic character. Do not design B as the next second of A's action. C may move closer to the accessory and supporting garment detail.
- Lock the delivery surface before generation. Reel uses direct 9:16 composition; Carousel uses the assigned Canva slot ratios. The Canva 15% crop limit never governs Reel generation.
- Lock the Mira camera body to a full-frame mirrorless camera for a premium magazine look. Use a 50mm prime lens near chest height with a level optical axis; never substitute a smartphone, computational portrait mode, DSLR look, low angle, or wide-angle perspective unless the user explicitly overrides the camera standard.
- Use camera language for the high-level look and composition. Do not put fixed aperture, shutter speed, ISO, or white-balance numbers in generation prompts; GPT Image interprets detailed camera settings loosely.
- Write Hero prompts in this order: intended use and dressing decision -> reference-image roles -> real scene and one visible action -> exact outfit -> photographic treatment -> composition -> short constraints.
- Aim for 120-220 English words in the Hero base prompt. Use positive, concrete visual language and one final constraint line with no more than five essential exclusions.
- Describe observable realism: available natural light, believable ambient spill, real skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. High-end magazine polish comes from framing, color and material detail, not beauty retouching or studio perfection.
- Include a real foreground or scene object with physically believable hand, foot, clothing, or bag interaction whenever suitable.
- Build one coherent three-role Carousel set: A full person, B scene application, C accessory detail. Do not create three unrelated full-body images.
- For Carousel, select the Canva master before generation and use the exact aspect ratios in `canva_slot_targets.json`; v3-D B is portrait while A/B/C motion frames in the other masters may be shallow horizontal strips.
- For Reel, generate one A directly as a 9:16 composition intended for 1080x1920 output. Do not use square or Carousel source geometry as an intermediate master.
- Treat the 8% top margin, central 70%, anatomy, contact shadows and crop safety as review requirements, not prose to overload the base generation prompt. Do not depend on Canva Smart Crop or manual focal-point adjustment.
- Carousel exact-pixel normalization may center-crop at most 15% and must never stretch the image. This limit is Carousel-only. Reel sources that are not composed directly as 9:16 must be regenerated.

Prompt age rule: use the model profile's prompt-age language only. Never include numeric true age. Preserve believable skin texture and normal human variation without age caricature, smoothing instructions or beauty retouching.

Reject images with supermodel distance, runway mood, luxury hotel advertising, plastic skin, obvious AI anatomy, hidden outfits, visible logos, image text, watermarks, celebrity likeness, or wrinkle-based age cues.

## Output Discipline

Store image outputs in the run folder:

```text
10_automation/runs/{week_id}/generated_images/{carousel_id}/looks/{look_id}/{surface}/
10_automation/runs/{week_id}/generated_images/{carousel_id}/looks/{look_id}/{surface}/canva_ready/
```

Use filenames like:

```text
{look_id}_{model_profile_id}_{surface}_candidate_A.png
{look_id}_{model_profile_id}_{surface}_candidate_B.png
{look_id}_{model_profile_id}_{surface}_candidate_C.png
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
