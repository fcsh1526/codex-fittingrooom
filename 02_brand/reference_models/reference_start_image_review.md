# Mira Reference Start Image Review

Generated: 2026-06-30

Status update: v1 faces were too similar. v2 candidates were generated with stronger separation in face shape, hairstyle, body proportion, and role energy. The user approved all three v2 files on 2026-06-30.

These are the approved identity anchors for the `$mira-image-daily` workflow.

## M01 Office

File:

```text
02_brand/reference_models/M01_start_v2.png
```

Review:

- Role fit: office / commute / meeting
- Strength: visibly more mature than M02/M03, short bob, sharper office presence, full-body clean reference
- Watch: strong professional mood; approve if M01 should be the most mature and structured model

## M02 Weekend

File:

```text
02_brand/reference_models/M02_start_v2.png
```

Review:

- Role fit: weekend / date / cafe
- Strength: rounder face, long wavy hair, softer smile, clearly different from M01 and M03
- Watch: still a bit polished; approve if this level of softness is right for weekend/date content

## M03 Casual

File:

```text
02_brand/reference_models/M03_start_v2.png
```

Review:

- Role fit: casual / budget-friendly daily wear
- Strength: short-hair casual identity, practical outfit, stronger ordinary-life relatability, distinct from long-haired M02
- Watch: face is still conventionally pretty; approve only if it feels ordinary enough for casual/small-budget content

## Previous v1 Files

Kept for comparison only:

```text
02_brand/reference_models/M01_start.png
02_brand/reference_models/M02_start.png
02_brand/reference_models/M03_start.png
```

## Approval Status

Approved manifest:

```text
02_brand/mira_reference_images.csv
```

All three v2 rows are now `approved`, so `$mira-image-daily` can prepare daily outfit image jobs for M01, M02, and M03.
