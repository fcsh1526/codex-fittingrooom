# Mira Daily Brief

Date: `2026-07-13`
Priority run: `2026-W27`
Stage: `ready_for_canva_test`

## Decision

The v2 image candidates are selected and the next step is Canva test-fill, not publishing.

## Today Only

1. Open the approved Mira Canva v2 template.
2. Duplicate a registered Mira Canva master, then fill cover_image with A_v2, motion_crop with B_v2, and detail_image with C_v2.
3. Replace slide2_line with the approved short line.
4. Review the Canva preview for head crop, feet crop, face clarity, and cross-slide composition before committing.

## User Should Provide

- Canva test-fill preview
- Decision to commit or adjust crops

## Codex Can Do Next

- Use Canva connector autofill labels or manual fill guide.
- Show the Canva preview before any commit.
- Keep publish_status as not_published until the user approves the layout.

## Useful Files

- `10_automation/runs/2026-W27/canva_fill_guide.md`
- `10_automation/runs/2026-W27/canva_asset_plan.md`
- `10_automation/runs/2026-W27/canva_asset_slots.csv`

## Generated Files

- `10_automation\PUBLISH_QUEUE.md`
- `10_automation\PUBLISH_QUEUE.json`
- `10_automation\PUBLISH_QUEUE.csv`

## Publish Queue Top Item

- Type: `carousel`
- ID: `2026-W27-003`
- Model: `M03`
- Canva template: `A` Mira Template Master - A Contact Sheet
- Canva template URL: https://www.canva.com/design/DAHOx6hb1Ug/A1sysuKRtad0lCYR8jqBQg/edit
- Canva design URL: n/a
- Stage: `ready_for_canva_test`
- Asset: `2026-W27-003_M03_v2_candidate_A.png`
- Package: `n/a`
- Next action: Do not publish yet. Test-fill the approved Mira Canva v2 template with selected v2 assets, review crops, then decide whether to commit.

## Current Next Action

Do not publish yet. Test-fill the approved Mira Canva v2 template with selected v2 assets, review crops, then decide whether to commit.

## Fixed Flow

```text
Mira magazine -> weekly trend -> daily queue -> Codex image candidates -> Canva carousel -> publish -> metrics -> next decision
```

## Dashboard Summary

- Run count: `3`
- Stage counts: `{"missing_weekly_packet_files": 1, "archived": 1, "ready_for_canva_test": 1}`
