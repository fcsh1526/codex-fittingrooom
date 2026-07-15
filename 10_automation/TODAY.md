# Mira Daily Brief

Date: `2026-07-15`
Priority run: `2026-W29`
Stage: `needs_image_asset_selection`

## Decision

The next bottleneck is a Hero-first Codex image session, review, and asset selection.

## Today Only

1. Open daily_queue.csv and image_generation_briefs.md.
2. Generate and review one integrated-scene Hero for the assigned internal model.
3. After Hero approval, derive B Motion and C Detail from that accepted Hero and score the session.

## User Should Provide

- Optional candidate image notes if manual review is needed.

## Codex Can Do Next

- Create or update image review inventory.
- Select cover/detail assets and update canva_asset_slots.csv.
- Validate with --require-assets before Canva work.

## Useful Files

- `10_automation/runs/2026-W29/daily_queue.csv`
- `10_automation/runs/2026-W29/image_generation_briefs.md`
- `10_automation/runs/2026-W29/image_review_template.csv`
- `10_automation/select_codex_assets.py`

## Generated Files

- `10_automation\PUBLISH_QUEUE.md`
- `10_automation\PUBLISH_QUEUE.json`
- `10_automation\PUBLISH_QUEUE.csv`

## Publish Queue Top Item

- Type: `carousel`
- ID: `2026-W29-002`
- Model: `M02`
- Canva template: `E` Mira Template Master v3 - E Cross-Boundary Weekend Air
- Canva template URL: https://www.canva.com/d/djICquyAb4kcGwW
- Canva design URL: n/a
- Stage: `needs_image_asset_selection`
- Asset: `n/a`
- Package: `10_automation\runs\2026-W29\generated_images\2026-W29-002\codex_generation_handoff.md`
- Next action: Generate, regenerate, or score publishable image assets, then rerun asset selection before Canva.

## Current Next Action

Generate, regenerate, or score publishable image assets, then rerun asset selection before Canva.

## Fixed Flow

```text
Mira magazine -> weekly trend -> daily queue -> Codex Hero -> B/C derivatives -> Canva carousel -> publish -> metrics -> next decision
```

## Dashboard Summary

- Run count: `4`
- Stage counts: `{"missing_weekly_packet_files": 1, "archived": 2, "needs_image_asset_selection": 1}`
