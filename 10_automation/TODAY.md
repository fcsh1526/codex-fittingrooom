# Mira Daily Brief

Date: `2026-07-16`
Priority run: `2026-W29`
Stage: `needs_visual_revision`

## Decision

The current carousel should not be published until the generated assets pass the actual Canva frame-fit check.

## Today Only

1. Create a near-square crop-safe derivative from the accepted Hero while preserving face, outfit, body, scene, and lighting.
2. Replace the affected Canva frame on a pilot design without manual crop adjustment.
3. Confirm the full hairstyle, face, and outfit focus survive the untouched center-cover crop before scaling to the remaining designs.

## User Should Provide

- Visual approval of the first crop-safe pilot in Canva

## Codex Can Do Next

- Mark the run as blocked from publishing.
- Generate crop-safe derivatives from accepted assets.
- Enforce canva_frame_fit as a hard asset-selection gate.

## Useful Files

- `10_automation/runs/2026-W29/generated_images`
- `10_automation/runs/2026-W29/image_review_template.csv`
- `10_automation/runs/2026-W29/canva_asset_plan.md`

## Generated Files

- `10_automation/PUBLISH_QUEUE.md`
- `10_automation/PUBLISH_QUEUE.json`
- `10_automation/PUBLISH_QUEUE.csv`

## Publish Queue Top Item

- Type: `carousel`
- ID: `2026-W29-001`
- Model: `M01`
- Canva template: `B` Mira Template Master v3 - B Cross-Boundary Symmetric
- Canva template URL: https://www.canva.com/d/UoVSnPEpgguD3be
- Canva design URL: https://www.canva.com/d/oCPjHB_ErKCvfrX
- Stage: `needs_visual_revision`
- Asset: `2026-W29-001_M01_photoreal_pilot_candidate_A.png`
- Package: `n/a`
- Next action: Do not publish. Use the registered active Mira Canva master template, verify layer/frame compatibility, regenerate clean candidates, then test-fill before export.

## Current Next Action

Do not publish. Use the registered active Mira Canva master template, verify layer/frame compatibility, regenerate clean candidates, then test-fill before export.

## Fixed Flow

```text
Mira magazine -> weekly trend -> daily queue -> Codex Hero -> B/C derivatives -> Canva carousel -> publish -> metrics -> next decision
```

## Dashboard Summary

- Run count: `4`
- Stage counts: `{"missing_weekly_packet_files": 1, "archived": 2, "needs_visual_revision": 1}`
