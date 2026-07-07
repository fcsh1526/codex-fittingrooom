# M01 v4 Full-Body Candidate From Direct Face Anchor

Generated: 2026-07-07

## Source

- Direct face anchor: `10_automation/runs/2026-W26/reference_anchor_candidates/direct_face_anchors_from_user_source/M01_start_v4_face_direct.png`
- Full-body candidate A: `10_automation/runs/2026-W26/reference_anchor_candidates/M01_v4_full_from_direct_face/M01_start_v4_full_candidate_A.png`
- Full-body candidate B: `10_automation/runs/2026-W26/reference_anchor_candidates/M01_v4_full_from_direct_face/M01_start_v4_full_candidate_B.png`
- Review contact sheets:
  - `10_automation/runs/2026-W26/reference_anchor_candidates/M01_v4_full_from_direct_face/M01_start_v4_face_full_candidate_A_contact_sheet.png`
  - `10_automation/runs/2026-W26/reference_anchor_candidates/M01_v4_full_from_direct_face/M01_start_v4_face_full_candidates_AB_contact_sheet.png`

## Method

The face anchor was not regenerated. It is a direct JPG-to-PNG conversion from the user-supplied `M01.JPG`.

The full-body image was generated as an extension candidate using the direct face anchor as the identity reference. The intended rule is:

```text
face identity remains the same; body, neutral clothing, standing pose, and studio background are extended according to the Mira reference-start-image rules.
```

## Full-Body Generation Brief

```text
Edit/extend the currently visible M01 face anchor image into a full-body production anchor.
Identity preservation is highest priority.
Preserve the same large calm eyes, eyelid shape, eyebrow shape, delicate nose, soft lips, cheek shape, jaw softness, skin tone, and quiet youthful East Asian presence.

Create a vertical full-body head-to-shoes studio reference image.
The model should read as a clearly adult early-20s East Asian woman with ordinary healthy petite-to-medium proportions.
Use a simple white cotton blouse or minimal white shirt, dark charcoal straight-leg trousers, and simple black flats or minimal loafers.
Plain neutral light-gray studio wall and floor, soft natural studio lighting, natural skin texture, no plastic skin.
No necklace, no earrings, no visible jewelry, no logos, no text, no watermark, no fantasy snow/sparkle effects.

Avoid changing the face, eye shape, nose, lips, jaw, ethnicity, or apparent age.
Avoid mature executive styling, runway pose, luxury advertising, childlike styling, distorted hands, hidden feet, cropped body, or excessive retouching.
```

## Review Note

Candidate B was approved by the user on 2026-07-07 and copied to:

```text
02_brand/reference_models/M01_start_v4_full.png
```

The direct face anchor was copied to:

```text
02_brand/reference_models/M01_start_v4_face.png
```

Candidate A remains a rejected draft. Candidate B used a stricter identity-preservation prompt after candidate A showed mild face drift in the eyes, nose, mouth, and apparent maturity.
