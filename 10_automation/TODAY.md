# Mira Daily Brief

Date: `2026-06-30`
Priority run: `2026-W26`
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

- `10_automation/runs/2026-W26/canva_fill_guide.md`
- `10_automation/runs/2026-W26/canva_asset_plan.md`
- `10_automation/runs/2026-W26/post_drafts.md`

## Generated Files

- `10_automation\PUBLISH_QUEUE.md`
- `10_automation\PUBLISH_QUEUE.json`
- `10_automation\PUBLISH_QUEUE.csv`

## Publish Queue Top Item

- Type: `carousel`
- ID: `2026-W26-002`
- Model: `M02`
- Stage: `ready_for_canva_and_publish`
- Asset: `2026-W26-002_M02_candidate_A.png`
- Next action: Use Canva handoff files to finish the carousel and publish it.

## Current Next Action

Use canva_fill_guide.md, canva_asset_plan.md, and post_drafts.md to finish Canva and publish the carousel.

## Fixed Flow

```text
Mira magazine -> weekly trend -> daily queue -> Codex image candidates -> Canva carousel -> publish -> metrics -> next decision
```

## Dashboard Summary

- Run count: `2`
- Stage counts: `{"missing_weekly_packet_files": 1, "ready_for_canva_and_publish": 1}`
