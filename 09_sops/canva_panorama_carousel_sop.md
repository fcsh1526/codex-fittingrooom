# Canva Panorama Carousel SOP

Updated: 2026-07-17

This is the active Mira v3 three-slide carousel. The old five-slide `5400x1350` layout is retired.

## Canvas Contract

```text
master: 3240x1350 px
slice 1: x=0..1079
slice 2: x=1080..2159
slice 3: x=2160..3239
export: 3 images at 1080x1350 px
```

Required fields: `cover_image`, `motion_crop`, `detail_image`, `slide2_line`.

Use a registered v3 master from `10_automation/canva_template_registry.json`. Duplicate it; never edit the master.

## Image Preparation

1. Select the master before generation.
2. Read exact A/B/C sizes from `canva_slot_targets.json`.
3. Generate A Hero at the A ratio.
4. Derive B Motion and C Detail from accepted A at their own ratios.
5. Keep complete hair and face inside the target frame.
6. Normalize without stretching.
7. Reject required center crop above 15%.

Do not insert one narrow portrait into all three frames.

## Connector Procedure

1. Upload three complete flat PNG images.
2. Start a transaction on the weekly duplicate.
3. Inspect all page image assets.
4. Replace only A/B/C frame element ids.
5. Inspect and show the draft thumbnail.
6. Commit only after explicit save approval.
7. Cancel or revise if rejected.

Never use Magic Layers, `image_to_design`, split person/background assets, or unverified old asset ids for final fills.

## Visual Acceptance

- The three slides read as one editorial panorama.
- Cross-slide overlaps are intentional.
- No face, hair, or key outfit detail is accidentally cut.
- Slide 2 has one short editorial line.
- The bottom-right `Mira` mark is fully visible.
- Person and environment share believable lighting and depth.
- A/B/C preserve identity and wardrobe.

## Manual Export

After commit and `ready_for_manual_export`:

1. Open the saved weekly Canva design.
2. Use the existing Canva slicing app.
3. Slice at x=1080 and x=2160.
4. Export three `1080x1350` images left to right.
5. Publish one Instagram Carousel.
6. Send Codex the Instagram URL and publish time.

The slicing/export step is intentionally manual. Zero reach does not move the item backward.

Complete process: `10_automation/CANONICAL_WORKFLOW.md`.
