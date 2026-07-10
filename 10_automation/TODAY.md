# Mira Daily Brief

Date: `2026-07-11`
Priority run: `2026-W27`
Stage: `needs_image_asset_selection`

## Decision

The next bottleneck is Codex workspace image generation, review, and asset selection.

## Today Only

1. Open daily_queue.csv and image_generation_briefs.md.
2. Generate image candidates inside the Codex workspace for the assigned internal model.
3. Review and score the generated image candidates in image_review_template.csv.

## User Should Provide

- Optional candidate image notes if manual review is needed.

## Codex Can Do Next

- Create or update image review inventory.
- Select cover/detail assets and update canva_asset_slots.csv.
- Validate with --require-assets before Canva work.

## Useful Files

- `10_automation/runs/2026-W27/daily_queue.csv`
- `10_automation/runs/2026-W27/image_generation_briefs.md`
- `10_automation/runs/2026-W27/image_review_template.csv`
- `10_automation/select_codex_assets.py`

## Generated Files

- `10_automation/PUBLISH_QUEUE.md`
- `10_automation/PUBLISH_QUEUE.json`
- `10_automation/PUBLISH_QUEUE.csv`

## Publish Queue Top Item

- Type: `carousel`
- ID: `2026-W27-002`
- Model: `M02`
- Canva template: `B` Mira Template Master - B Symmetric
- Canva template URL: https://www.canva.com/design/DAHOxwp1cZ8/cIfSmcVa-DAJJrT-21PJoA/edit
- Canva design URL: n/a
- Stage: `needs_image_asset_selection`
- Asset: `n/a`
- Package: `10_automation\runs\2026-W27\generated_images\2026-W27-002\codex_generation_handoff.md`
- Next action: Generate, regenerate, or score publishable image assets, then rerun asset selection before Canva.

## Current Next Action

Generate, regenerate, or score publishable image assets, then rerun asset selection before Canva.

## Fixed Flow

```text
Mira magazine -> weekly trend -> daily queue -> Codex image candidates -> Canva carousel -> publish -> metrics -> next decision
```

## Dashboard Summary

- Run count: `3`
- Stage counts: `{"missing_weekly_packet_files": 1, "quality_gate_not_passed": 1, "published_waiting_for_metrics": 1}`
