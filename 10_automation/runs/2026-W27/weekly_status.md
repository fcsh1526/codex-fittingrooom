# Weekly Status

Run folder: `10_automation\runs\2026-W27`
Stage: `needs_image_asset_selection`

## Next Action

Fill the image review template after reviewing Codex outputs, then rerun select_codex_assets.py with that score sheet.

## Blocking Items

- `2026-W27-001`
- `2026-W27-002`
- `2026-W27-003`
- `2026-W27-004`
- `2026-W27-005`

## Suggested Commands

```powershell
open 10_automation\runs\2026-W27/image_generation_briefs.md
```

```powershell
python 10_automation/select_codex_assets.py --run-dir 10_automation\runs\2026-W27 --provider Codex --score-sheet 10_automation\runs\2026-W27/image_review_template.csv --drive-inventory path_to_image_inventory.csv
```

```powershell
python 10_automation/validate_weekly_run.py --run-dir 10_automation\runs\2026-W27 --min-rows 1 --require-assets
```

## Summary

- Packet rows: `5`
- Quality: `pass`
- Cover assets selected: `0` / `5`
- Published: `False`
- Metric checkpoints: `0`
