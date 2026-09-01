# Weekly Status

Run folder: `10_automation\runs\2026-W36`
Stage: `needs_image_asset_selection`

## Next Action

Continue generating and scoring the remaining Codex image jobs, then rerun select_codex_assets.py. Canva work for already selected carousels can proceed in parallel.

## Blocking Items

- `2026-W36-001`
- `2026-W36-002`
- `2026-W36-003`
- `2026-W36-004`
- `2026-W36-005`

## Suggested Commands

```powershell
open 10_automation\runs\2026-W36/image_generation_briefs.md
```

```powershell
python 10_automation/select_codex_assets.py --run-dir 10_automation\runs\2026-W36 --provider Codex --score-sheet 10_automation\runs\2026-W36/image_review_template.csv --drive-inventory path_to_image_inventory.csv
```

```powershell
python 10_automation/validate_weekly_run.py --run-dir 10_automation\runs\2026-W36 --min-rows 1 --require-assets
```

## Summary

- Packet rows: `5`
- Quality: `pass`
- Cover assets selected: `0` / `5`
- Published: `False`
- Metric checkpoints: `0`
