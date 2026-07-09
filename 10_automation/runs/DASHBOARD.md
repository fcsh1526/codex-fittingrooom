# Mira Weekly Dashboard

Runs directory: `10_automation\runs`
Run count: `2`

## Stage Counts

- `missing_weekly_packet_files`: `1`
- `quality_gate_not_passed`: `1`

## Runs

| Run | Stage | Quality | Cover Assets | Published | Metrics | Next Action |
|---|---|---|---:|---:|---:|---|
| `2026-W21-test` | `missing_weekly_packet_files` | `pass` | `2/2` | `True` | `2` | Run run_weekly_pipeline.py or build_weekly_packet.py to regenerate the weekly run folder. |
| `2026-W26` | `quality_gate_not_passed` | `fail` | `1/2` | `False` | `0` | Run validate_weekly_run.py and fix all errors before producing images or editing Canva. |
