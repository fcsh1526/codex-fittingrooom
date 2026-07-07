# M04 v3 Full-Body Candidates From Direct Face Anchor

Generated: 2026-07-07

## Source

- Direct face anchor: `10_automation/runs/2026-W26/reference_anchor_candidates/direct_face_anchors_from_user_source/M04_start_v3_face_direct.png`
- Full-body candidate A: `10_automation/runs/2026-W26/reference_anchor_candidates/M04_v3_full_from_direct_face/M04_start_v3_full_candidate_A.png`
- Full-body candidate B: `10_automation/runs/2026-W26/reference_anchor_candidates/M04_v3_full_from_direct_face/M04_start_v3_full_candidate_B.png`
- Review contact sheet: `10_automation/runs/2026-W26/reference_anchor_candidates/M04_v3_full_from_direct_face/M04_start_v3_face_full_candidates_AB_contact_sheet.png`

## Method

The face anchor was not regenerated. It is a direct JPG-to-PNG conversion from the user-supplied `M04.JPG`.

The full-body candidates were generated as extension candidates using the direct face anchor as the identity reference. The intended rule is:

```text
face identity remains the same; body, neutral clothing, standing pose, and studio background are extended according to the Mira reference-start-image rules.
```

## Candidate Direction

Candidate A used a safe neutral full-body anchor prompt for M04: crisp ivory/white shirt, dark charcoal straight-leg trousers, black loafers or low heels, and controlled dark side-part hair.

Candidate B used a stricter identity prompt focused on preserving the original long narrow face, strong eyebrows, eye shape, straight nose, soft neutral lips, calm expression, and dark side-swept hair identity.

## Review Note

The user judged candidate A and candidate B to be different people.

Candidate B was approved as M04 on 2026-07-07 and copied to:

```text
02_brand/reference_models/M04_start_v3_full.png
```

The direct M04 face anchor was copied to:

```text
02_brand/reference_models/M04_start_v3_face.png
```

Candidate A was not rejected. It was split into a new M05 identity with true age metadata set to 20 and prompt-safe visual age language `around 20, youthful adult`.

Candidate A was copied to:

```text
02_brand/reference_models/M05_start_v1_full.png
```

The M05 face anchor was created as a deterministic crop from candidate A, with no AI regeneration, and copied to:

```text
02_brand/reference_models/M05_start_v1_face.png
```

Split review sheet:

```text
10_automation/runs/2026-W26/reference_anchor_candidates/M04_v3_full_from_direct_face/M04_M05_split_approval_contact_sheet.png
```
