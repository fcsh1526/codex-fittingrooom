# Reference Start Images

Mira requires strict reference start images before daily generation.

Purpose:

```text
same internal model face + same body proportions + controlled variation only in outfit, pose, scene, and styling
```

## Canonical Manifest

Use:

```text
02_brand/mira_reference_images.csv
```

Required rows:

```text
model_profile_id,true_age,visual_age_prompt,reference_version,reference_face_path,reference_full_path,status,superseded_paths,notes
M01,25,early 20s,v3,02_brand/reference_models/M01_start_v3_face.png,02_brand/reference_models/M01_start_v3_full.png,needed,,Prompt uses visual age only
M02,35,"late 20s, youthful",v3,02_brand/reference_models/M02_start_v3_face.png,02_brand/reference_models/M02_start_v3_full.png,needed,,Prompt uses visual age only
M03,45,"mid 30s look, well-maintained",v3,02_brand/reference_models/M03_start_v3_face.png,02_brand/reference_models/M03_start_v3_full.png,needed,,Prompt uses visual age only
M04,55,"early 40s look, elegant",v3,02_brand/reference_models/M04_start_v3_face.png,02_brand/reference_models/M04_start_v3_full.png,needed,,Prompt uses visual age only
M05,20,"around 20, youthful adult",v1,02_brand/reference_models/M05_start_v1_face.png,02_brand/reference_models/M05_start_v1_full.png,needed,,Prompt uses visual age only
```

Do not proceed with daily image generation for a model until both reference images exist and status is `approved`.

## Reference Image Requirements

Each reference start pair must include:

- one person only
- one face anchor: front or slight three-quarter portrait
- one full-body anchor: head-to-shoe visible
- neutral simple outfit, not trend-specific
- natural skin texture
- ordinary healthy body proportions
- no logos, no text, no watermark
- neutral background
- stable hairstyle and face
- age and body type matching `mira_model_roster.json`
- prompt visual age language, not numeric true age, when generating anchors

## What Can Change Later

Allowed to vary:

- outfit
- shoes and bag
- pose
- scene
- crop
- lighting direction within realism
- accessories within the outfit plan

Not allowed to drift:

- face structure
- apparent age range
- body proportions
- core hairstyle identity
- ethnicity or overall look
- model role, such as making M02 look like M01

## Missing Reference Handling

If a reference image is missing:

1. Stop generation.
2. Tell the user exactly which file is missing.
3. Offer to create the reference-start-image brief first.
4. Do not create daily outfit candidates yet.
