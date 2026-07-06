# Mira Reference Start Image Review

Generated: 2026-06-30

Phase A status update: 2026-07-06

Mira now uses four fixed internal identities with true-age metadata and prompt-safe visual-age language:

```text
M01 true age 25 -> prompt visual age: early 20s
M02 true age 35 -> prompt visual age: late 20s, youthful
M03 true age 45 -> prompt visual age: mid 30s look, well-maintained
M04 true age 55 -> prompt visual age: early 40s look, elegant
```

The old single-image start files are retained for audit. Previous reference-pack draft folders were moved to the run archive. They are not the current source of truth.

## Current Source Of Truth

Use:

```text
02_brand/mira_reference_images.csv
```

Current approved transitional anchors:

```text
M01: 02_brand/reference_models/M01_start_v2_face.png
M01: 02_brand/reference_models/M01_start_v2_full.png
M02: 02_brand/reference_models/M02_start_v2_face.png
M02: 02_brand/reference_models/M02_start_v2_full.png
M03: 02_brand/reference_models/M03_start_v2_face.png
M03: 02_brand/reference_models/M03_start_v2_full.png
M04: 02_brand/reference_models/M04_start_v2_face.png
M04: 02_brand/reference_models/M04_start_v2_full.png
```

These v2 anchors are only a Phase A remap so the factory has consistent numbering before Phase B. Phase B will replace them one model at a time with v3 face/full anchors after user approval.

## Legacy Files

Kept for comparison only:

```text
02_brand/reference_models/M01_start.png
02_brand/reference_models/M01_start_v2.png
02_brand/reference_models/M02_start.png
02_brand/reference_models/M02_start_v2.png
02_brand/reference_models/M03_start.png
02_brand/reference_models/M03_start_v2.png
02_brand/reference_models/M04_start.png
02_brand/reference_models/M04_start_v1.png
10_automation/runs/2026-W26/reference_model_drafts_phase_a/*_pack_v1/
```

Do not use these legacy paths directly for new daily outfit image jobs unless `mira_reference_images.csv` points to them.

## Prompt Rule

When generating any new anchor candidate or daily outfit image:

```text
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin is smooth and well-maintained.
```
