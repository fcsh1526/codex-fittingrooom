# Mira Reference Start Image Review

Generated: 2026-06-30

These are candidate identity anchors for the `$mira-image-daily` workflow. Do not mark them `approved` until the user accepts the face, hairstyle, body proportions, and overall role fit.

## M01 Office

File:

```text
02_brand/reference_models/M01_start.png
```

Review:

- Role fit: office / commute / meeting
- Strength: full body, clean background, practical office outfit
- Watch: face may read slightly younger than late 20s to early 30s; approve only if acceptable

## M02 Weekend

File:

```text
02_brand/reference_models/M02_start.png
```

Review:

- Role fit: weekend / date / cafe
- Strength: soft styling, long hair, approachable expression
- Watch: slightly more polished than ordinary daily; approve only if this is the desired weekend baseline

## M03 Casual

File:

```text
02_brand/reference_models/M03_start.png
```

Review:

- Role fit: casual / budget-friendly daily wear
- Strength: full body, simple casual outfit, strong everyday relatability
- Watch: currently has tied-back hair; approve only if this should become the stable M03 hairstyle identity

## Approval Step

If accepted, update:

```text
02_brand/mira_reference_images.csv
```

from:

```text
candidate_review
```

to:

```text
approved
```

Only then should `$mira-image-daily` prepare daily outfit image jobs for that model.

