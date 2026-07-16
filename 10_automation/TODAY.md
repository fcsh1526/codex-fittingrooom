# Mira Daily Brief

Date: `2026-07-16`
Priority run: `2026-W29`
Stage: `needs_visual_revision`

## Decision

The current carousel should not be published until the generated assets pass the actual Canva frame-fit check.

## Today Only

1. Read canva_slot_targets.json and create each remaining A/B/C derivative for its exact assigned frame ratio.
2. Run prepare_canva_ready_assets.py to normalize approved sources without stretching or more than 15% center crop.
3. Replace the complete A/B/C set and confirm the full hairstyle, face, and outfit focus survive the untouched Canva fill.

## User Should Provide

- Visual approval of the first crop-safe pilot in Canva

## Codex Can Do Next

- Mark the run as blocked from publishing.
- Generate assigned-frame-ratio derivatives from accepted assets.
- Enforce canva_frame_fit as a hard asset-selection gate.

## Useful Files

- `10_automation/runs/2026-W29/generated_images`
- `10_automation/runs/2026-W29/image_review_template.csv`
- `10_automation/runs/2026-W29/canva_asset_plan.md`

## Generated Files

- `10_automation\PUBLISH_QUEUE.md`
- `10_automation\PUBLISH_QUEUE.json`
- `10_automation\PUBLISH_QUEUE.csv`

## Publish Queue Top Item

- Type: `carousel`
- ID: `2026-W29-005`
- Model: `M05`
- Canva template: `E` Mira Template Master v3 - E Cross-Boundary Weekend Air
- Canva template URL: https://www.canva.com/d/djICquyAb4kcGwW
- Canva design URL: https://www.canva.com/d/gDyY0MlyrDQlQNI
- Stage: `needs_visual_revision`
- Asset: `2026-W29-005_M05_photoreal_pilot_candidate_A.png`
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
