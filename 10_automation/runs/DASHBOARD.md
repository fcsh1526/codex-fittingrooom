# Mira Weekly Dashboard

Runs directory: `10_automation\runs`
Run count: `4`

## Stage Counts

- `archived`: `2`
- `missing_weekly_packet_files`: `1`
- `ready_for_manual_export`: `1`

## Runs

| Run | Stage | Quality | Cover Assets | Published | Metrics | Next Action |
|---|---|---|---:|---:|---:|---|
| `2026-W21-test` | `missing_weekly_packet_files` | `pass` | `2/2` | `True` | `2` | Run run_weekly_pipeline.py or build_weekly_packet.py to regenerate the weekly run folder. |
| `2026-W26` | `archived` | `fail` | `1/2` | `False` | `0` | Archived by user decision. W26 is historical infrastructure work and must not return to the production queue. |
| `2026-W27` | `archived` | `pass` | `5/5` | `True` | `0` | Preserved but removed from the active queue on 2026-07-15 when the user activated the W29 Hero-first photoreal pilot. Existing W27 Canva drafts remain available and must not override the new trial workflow. |
| `2026-W29` | `ready_for_manual_export` | `pass` | `5/5` | `False` | `0` | Open the saved Canva panoramas, split each 3240x1350 design into three 1080x1350 slides, then export and publish or schedule them. |
