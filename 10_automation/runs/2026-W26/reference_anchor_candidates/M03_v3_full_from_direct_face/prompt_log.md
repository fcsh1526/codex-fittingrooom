# M03 v3 Full-Body Candidates From Direct Face Anchor

Generated: 2026-07-07

## Source

- Direct face anchor: `10_automation/runs/2026-W26/reference_anchor_candidates/direct_face_anchors_from_user_source/M03_start_v3_face_direct.png`
- Full-body candidate A: `10_automation/runs/2026-W26/reference_anchor_candidates/M03_v3_full_from_direct_face/M03_start_v3_full_candidate_A.png`
- Full-body candidate B: `10_automation/runs/2026-W26/reference_anchor_candidates/M03_v3_full_from_direct_face/M03_start_v3_full_candidate_B.png`
- Review contact sheet: `10_automation/runs/2026-W26/reference_anchor_candidates/M03_v3_full_from_direct_face/M03_start_v3_face_full_candidates_AB_contact_sheet.png`

## Method

The face anchor was not regenerated. It is a direct JPG-to-PNG conversion from the user-supplied `M03.JPG`.

The full-body candidates were generated as extension candidates using the direct face anchor as the identity reference. The intended rule is:

```text
face identity remains the same; body, neutral clothing, standing pose, and studio background are extended according to the Mira reference-start-image rules.
```

## Candidate Direction

Candidate A used a safe neutral full-body anchor prompt for M03: soft white/ivory blouse or fine-knit top, dark charcoal straight-leg trousers, simple black flats or loafers, and long dark-brown polished waves.

Candidate B used a stricter identity prompt focused on preserving the original warm smile, almond eyes, eyebrow spacing, oval face, cheek fullness, jaw balance, nose shape, coral lip shape, and long wavy hair identity.

## Review Note

Candidate A was approved by the user on 2026-07-07 and copied to:

```text
02_brand/reference_models/M03_start_v3_full.png
```

The direct face anchor was copied to:

```text
02_brand/reference_models/M03_start_v3_face.png
```

Candidate B remains an unselected draft for comparison only.
