# Mira Reference Start Image Review

Generated: 2026-06-30

Phase A status update: 2026-07-06
Phase B M01 update: 2026-07-06
Phase B M01 v4 update: 2026-07-07
Phase B M02 v3 update: 2026-07-07
Phase B M03 v3 update: 2026-07-07
Phase B M04 v3 and M05 v1 split update: 2026-07-07
M01 v4 restoration and M06 face-only reserve update: 2026-08-04
M02 v3 restoration and M07 inactive reserve update: 2026-08-04
M03 v3 restoration and M08 inactive reserve update: 2026-08-04
M09 inactive reserve addition: 2026-08-04

Mira now uses five active fixed internal identities plus four inactive reserves, with true-age metadata and prompt-safe visual-age language:

```text
M01 true age 25 -> prompt visual age: early 20s
M02 true age 35 -> prompt visual age: late 20s, youthful
M03 true age 45 -> prompt visual age: mid 30s look, well-maintained
M04 true age 55 -> prompt visual age: early 40s look, elegant
M05 true age 20 -> prompt visual age: around 20, youthful adult
M06 true age 25 -> prompt visual age: early 20s (backup_face_only; not active)
M07 true age 35 -> prompt visual age: late 20s, youthful (backup_inactive; not active)
M08 true age 45 -> prompt visual age: mid 30s look, well-maintained (backup_inactive; not active)
M09 true age pending -> prompt visual age: adult; age calibration pending (backup_inactive; not active)
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
M04: 02_brand/reference_models/M04_start_v3_face.png
M04: 02_brand/reference_models/M04_start_v3_full.png
M05: 02_brand/reference_models/M05_start_v1_face.png
M05: 02_brand/reference_models/M05_start_v1_full.png
```

M01 was restored to its approved v4 anchors by user decision on 2026-08-04 after a direct v4/v5 comparison. These are the production-proven anchors already used in completed outfit-generation and Canva workflows. The rejected v5 files remain preserved for audit and are not the active M01 anchors.

M02 was restored to its approved v3 anchors by user decision on 2026-08-04 after a direct v3/v4 comparison. These are the production-proven anchors already used in completed outfit-generation and Canva workflows. The rejected v4 files remain preserved for audit and are not the active M02 anchors.

M03 was restored to its approved v3 anchors by user decision on 2026-08-04 after a direct v3/v4 comparison. These are the production-proven anchors already used in completed outfit-generation and Canva workflows. The rejected v4 files remain preserved for audit and are not the active M03 anchors.

M04 has completed the Phase B restart and now points to approved v3 anchors. The v3 face anchor is a direct PNG conversion from the user-supplied M04.JPG with no face regeneration. The v3 full-body anchor uses candidate B from the direct-face extension pass and was approved by the user on 2026-07-07.

M05 was created from the M04 candidate A split on 2026-07-07 after the user identified A and B as different people. M05 true age is 20, with prompt-safe visual age language `around 20, youthful adult`. The v1 face anchor is a deterministic crop from candidate A with no AI regeneration. The v1 full-body anchor is candidate A.

M06 was created as an inactive reserve on 2026-08-04 by copying the preserved M01 v5 face file byte-for-byte to `M06_start_v1_face.png`. M06 has no approved full-body anchor, has status `backup_face_only`, and must not enter production or weekly rotation unless the missing anchor is approved and the user explicitly activates the identity.

M07 was created as an inactive reserve on 2026-08-04 by copying the preserved M02 v4 face and full-body files byte-for-byte to `M07_start_v1_face.png` and `M07_start_v1_full.png`. M07 has status `backup_inactive` and must not enter production or weekly rotation unless the user explicitly activates the identity.

M08 was created as an inactive reserve on 2026-08-04 by copying the preserved M03 v4 face and full-body files byte-for-byte to `M08_start_v1_face.png` and `M08_start_v1_full.png`. M08 has status `backup_inactive` and must not enter production or weekly rotation unless the user explicitly activates the identity.

M09 was added as an inactive reserve on 2026-08-04 from the user-supplied `ChatGPT Image 2026年8月4日 上午11_48_29.png`. `M09_start_v1_full.png` is a byte-identical copy of the 864x1821 source. `M09_start_v1_face.png` is an unresized 384x512 deterministic crop from coordinates x=240, y=90 in the same source. No AI regeneration was used. M09 requires age calibration and explicit user activation before production or weekly rotation.

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
02_brand/reference_models/M04_start_v2_face.png
02_brand/reference_models/M04_start_v2_full.png
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
