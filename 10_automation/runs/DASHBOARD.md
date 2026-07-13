# Mira Weekly Dashboard

Runs directory: `10_automation\runs`
Run count: `3`

## Stage Counts

- `missing_weekly_packet_files`: `1`
- `archived`: `1`
- `canva_blocked_waiting_for_flat_png_asset`: `1`

## Runs

| Run | Stage | Quality | Cover Assets | Published | Metrics | Next Action |
|---|---|---|---:|---:|---:|---|
| `2026-W21-test` | `missing_weekly_packet_files` | `pass` | `2/2` | `True` | `2` | Run run_weekly_pipeline.py or build_weekly_packet.py to regenerate the weekly run folder. |
| `2026-W26` | `archived` | `fail` | `1/2` | `False` | `0` | Archived by user decision. W26 is historical infrastructure work and must not return to the production queue. |
| `2026-W27` | `canva_blocked_waiting_for_flat_png_asset` | `pass` | `5/5` | `True` | `0` | Resolve the selected complete PNG/JPG images to verified Canva image asset ids, then rerun the Canva fill on a fresh duplicate. Public URLs are optional; do not use image_to_design, Magic Layers, or old Canva design asset ids. Review quality_report.md for any additional strict validation blockers. |
