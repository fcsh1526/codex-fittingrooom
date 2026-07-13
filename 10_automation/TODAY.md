# Mira Daily Brief

Date: `2026-07-13`
Priority run: `2026-W27`
Stage: `canva_blocked_waiting_for_flat_png_asset`

## Decision

The Canva draft is blocked because the previous fill reused split Canva assets. Do not export or publish it.

## Today Only

1. Resolve the selected A_v2, B_v2, and C_v2 PNGs to verified Canva image asset ids.
2. Duplicate one registered Mira master again after the image assets are safe.
3. Fill only `cover_image`, `motion_crop`, and `detail_image` with verified complete flat assets, then review before saving.

## User Should Provide

- Canva image asset ids for the three complete PNGs
- Approval after the new preview is visible

## Codex Can Do Next

- Use only verified flat image assets for Canva replacement.
- Stop if only local PNG paths are available and no verified Canva image asset ids exist.
- Keep failed Canva drafts out of the publish queue.

## Useful Files

- `10_automation/runs/2026-W27/canva_automation_trial_log.md`
- `10_automation/runs/2026-W27/canva_fill_guide.md`
- `10_automation/runs/2026-W27/generated_images/2026-W26-002`

## Generated Files

- `10_automation\PUBLISH_QUEUE.md`
- `10_automation\PUBLISH_QUEUE.json`
- `10_automation\PUBLISH_QUEUE.csv`

## Publish Queue Top Item

- Type: `carousel`
- ID: `2026-W27-002`
- Model: `M02`
- Canva template: `B` Mira Template Master - B Symmetric
- Canva template URL: https://www.canva.com/design/DAHOxwp1cZ8/cIfSmcVa-DAJJrT-21PJoA/edit
- Canva design URL: n/a
- Stage: `canva_blocked_waiting_for_flat_png_asset`
- Asset: `2026-W27-002_M02_v2_candidate_A.png`
- Package: `n/a`
- Next action: Do not export failed Canva drafts. Resolve the selected PNGs to verified Canva image asset ids, then rerun fill on a fresh duplicate.

## Current Next Action

Do not export failed Canva drafts. Resolve the selected PNGs to verified Canva image asset ids, then rerun fill on a fresh duplicate.

## Fixed Flow

```text
Mira magazine -> weekly trend -> daily queue -> Codex image candidates -> Canva carousel -> publish -> metrics -> next decision
```

## Dashboard Summary

- Run count: `3`
- Stage counts: `{"missing_weekly_packet_files": 1, "archived": 1, "canva_blocked_waiting_for_flat_png_asset": 1}`
