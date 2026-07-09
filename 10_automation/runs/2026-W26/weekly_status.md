# Weekly Status

Run folder: `10_automation\runs\2026-W26`
Stage: `quality_gate_not_passed`

## Next Action

Run validate_weekly_run.py and fix all errors before producing images or editing Canva.

## Blocking Items

- `quality_status=fail`

## Suggested Commands

```powershell
python 10_automation/validate_weekly_run.py --run-dir 10_automation\runs\2026-W26 --min-rows 1
```

## Summary

- Packet rows: `2`
- Quality: `fail`
- Cover assets selected: `1` / `2`
- Published: `False`
- Metric checkpoints: `0`
