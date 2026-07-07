# M02 v3 Full-Body Candidates From Direct Face Anchor

Generated: 2026-07-07

## Source

- Direct face anchor: `10_automation/runs/2026-W26/reference_anchor_candidates/direct_face_anchors_from_user_source/M02_start_v3_face_direct.png`
- Full-body candidate A: `10_automation/runs/2026-W26/reference_anchor_candidates/M02_v3_full_from_direct_face/M02_start_v3_full_candidate_A.png`
- Full-body candidate B: `10_automation/runs/2026-W26/reference_anchor_candidates/M02_v3_full_from_direct_face/M02_start_v3_full_candidate_B.png`
- Review contact sheet: `10_automation/runs/2026-W26/reference_anchor_candidates/M02_v3_full_from_direct_face/M02_start_v3_face_full_candidates_AB_contact_sheet.png`

## Method

The face anchor was not regenerated. It is a direct JPG-to-PNG conversion from the user-supplied `M02.JPG`.

The full-body candidates were generated as extension candidates using the direct face anchor as the identity reference. The intended rule is:

```text
face identity remains the same; body, neutral clothing, standing pose, and studio background are extended according to the Mira reference-start-image rules.
```

## Candidate Direction

Candidate A used the first strict identity-preservation prompt for M02, replacing the source-photo bare-shoulder/glamour styling with a neutral blouse, dark trousers, and flat shoes.

Candidate B used a stricter identity prompt focused on preserving the original warm smile, almond eyes, eyebrow spacing, oval face, cheek fullness, jaw balance, nose shape, and coral lip shape.

## Review Note

Candidate A was approved by the user on 2026-07-07 and copied to:

```text
02_brand/reference_models/M02_start_v3_full.png
```

The direct face anchor was copied to:

```text
02_brand/reference_models/M02_start_v3_face.png
```

Candidate B remains an unselected draft for comparison only.
