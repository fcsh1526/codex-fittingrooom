# Mira Weekly Dashboard

Runs directory: `10_automation\runs`
Run count: `3`

## Stage Counts

- `missing_weekly_packet_files`: `1`
- `archived`: `1`
- `canva_committed_ready_to_publish`: `1`

## Runs

| Run | Stage | Quality | Cover Assets | Published | Metrics | Next Action |
|---|---|---|---:|---:|---:|---|
| `2026-W21-test` | `missing_weekly_packet_files` | `pass` | `2/2` | `True` | `2` | Run run_weekly_pipeline.py or build_weekly_packet.py to regenerate the weekly run folder. |
| `2026-W26` | `archived` | `fail` | `1/2` | `False` | `0` | Archived by user decision. W26 is historical infrastructure work and must not return to the production queue. |
| `2026-W27` | `canva_committed_ready_to_publish` | `pass` | `5/5` | `True` | `0` | Open the committed Canva design, review/export the 3 carousel slices, then publish or schedule it. |
