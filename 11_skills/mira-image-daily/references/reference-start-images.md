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
model_profile_id,reference_image_path,status,notes
M01,02_brand/reference_models/M01_start.png,needed,Office model anchor
M02,02_brand/reference_models/M02_start.png,needed,Weekend model anchor
M03,02_brand/reference_models/M03_start.png,needed,Casual model anchor
```

Do not proceed with daily image generation for a model until its reference image exists and status is `approved`.

## Reference Image Requirements

Each reference start image must be:

- one person only
- front or slight three-quarter view
- neutral simple outfit, not trend-specific
- full body or at least head-to-shoe visible
- natural skin texture
- ordinary healthy body proportions
- no logos, no text, no watermark
- neutral background
- stable hairstyle and face
- age and body type matching `mira_model_roster.json`

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

