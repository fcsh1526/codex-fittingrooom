# Mira Reference Start Image Review

Generated: 2026-06-30

Phase A status update: 2026-07-06
Phase B M01 update: 2026-07-06
Phase B M01 v4 update: 2026-07-07
Phase B M02 v3 update: 2026-07-07
Phase B M03 v3 update: 2026-07-07

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

Current approved anchors:

```text
M01: 02_brand/reference_models/M01_start_v4_face.png
M01: 02_brand/reference_models/M01_start_v4_full.png
M02: 02_brand/reference_models/M02_start_v3_face.png
M02: 02_brand/reference_models/M02_start_v3_full.png
M03: 02_brand/reference_models/M03_start_v3_face.png
M03: 02_brand/reference_models/M03_start_v3_full.png
M04: 02_brand/reference_models/M04_start_v2_face.png
M04: 02_brand/reference_models/M04_start_v2_full.png
```

M01 has completed the Phase B restart and now points to approved v4 anchors. The v4 face anchor is a direct PNG conversion from the user-supplied M01.JPG with no face regeneration. The v4 full-body anchor uses candidate B from the direct-face extension pass and was approved by the user on 2026-07-07.

M02 has completed the Phase B restart and now points to approved v3 anchors. The v3 face anchor is a direct PNG conversion from the user-supplied M02.JPG with no face regeneration. The v3 full-body anchor uses candidate A from the direct-face extension pass and was approved by the user on 2026-07-07.

M03 has completed the Phase B restart and now points to approved v3 anchors. The v3 face anchor is a direct PNG conversion from the user-supplied M03.JPG with no face regeneration. The v3 full-body anchor uses candidate A from the direct-face extension pass and was approved by the user on 2026-07-07.

M04 still uses transitional v2 anchors until its own Phase B rebuild is approved.

## Legacy Files

Kept for comparison only:

```text
02_brand/reference_models/M01_start.png
02_brand/reference_models/M01_start_v2.png
02_brand/reference_models/M01_start_v3_face.png
02_brand/reference_models/M01_start_v3_full.png
02_brand/reference_models/M02_start.png
02_brand/reference_models/M02_start_v2.png
02_brand/reference_models/M02_start_v2_face.png
02_brand/reference_models/M02_start_v2_full.png
02_brand/reference_models/M03_start.png
02_brand/reference_models/M03_start_v2.png
02_brand/reference_models/M03_start_v2_face.png
02_brand/reference_models/M03_start_v2_full.png
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
