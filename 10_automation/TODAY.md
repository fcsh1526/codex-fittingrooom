# Mira Daily Brief

Date: `2026-07-11`
Priority run: `2026-W27`
Stage: `ready_for_canva_and_publish`

## Decision

The run is ready for Canva assembly and publishing.

## Today Only

1. Open the Canva panorama template and fill text from canva_fill_guide.md.
2. Place images according to canva_asset_plan.md.
3. Publish or schedule the post, then send the post URL.

## User Should Provide

- Final Canva URL
- Instagram post URL
- Publish time

## Codex Can Do Next

- Check caption, CTA, hashtags, and AI disclosure.
- Record post URL and create 6h / 24h metrics commands.

## Useful Files

- `10_automation/runs/2026-W27/canva_fill_guide.md`
- `10_automation/runs/2026-W27/canva_asset_plan.md`
- `10_automation/runs/2026-W27/post_drafts.md`

## Generated Files

- `10_automation/PUBLISH_QUEUE.md`
- `10_automation/PUBLISH_QUEUE.json`
- `10_automation/PUBLISH_QUEUE.csv`

## Publish Queue Top Item

- Type: `carousel`
- ID: `2026-W27-001`
- Model: `M01`
- Canva template: `B` Mira Template Master - B Symmetric
- Canva template URL: https://www.canva.com/design/DAHOxwp1cZ8/cIfSmcVa-DAJJrT-21PJoA/edit
- Canva design URL: n/a
- Stage: `ready_for_canva_and_publish`
- Asset: `2026-W27-001_M01_candidate_A.png`
- Package: `n/a`
- Next action: Use Canva handoff files to finish the carousel and publish it.

## Current Next Action

Use Canva handoff files to finish the carousel and publish it.

## Fixed Flow

```text
Mira magazine -> weekly trend -> daily queue -> Codex image candidates -> Canva carousel -> publish -> metrics -> next decision
```

## Dashboard Summary

- Run count: `3`
- Stage counts: `{"missing_weekly_packet_files": 1, "quality_gate_not_passed": 1, "needs_image_asset_selection": 1}`
