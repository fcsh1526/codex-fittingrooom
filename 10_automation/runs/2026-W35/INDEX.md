# W35 Production Index

Use these files in this order:

1. `weekly_media_index.json` — machine-readable progress for all ten looks, including separate Reel, Carousel and Canva states.
2. `reel_asset_manifest.json` — the only approved source list and sequence for the two Grok Reel jobs.
3. `weekly_media_index.md` and `reel_asset_manifest.md` — human-readable mirrors.
4. `weekly_look_plan.csv` — editorial metadata and the synchronized completion status for every look.

Current result:

```text
10/10 looks ready_for_manual_export
10/10 Reel A sources approved_native_9x16
10/10 Carousel A/B/C sets approved
10/10 Canva designs committed_exact_frame
2/2 Reel packages ready_for_grok
```

`weekly_status.json` is the legacy five-theme automation status and does not represent the look-level media completion gate. Media robots must use `weekly_media_index.json` instead.

Never infer the source image from a folder scan. Use only each `source_path` or `raw_url` listed in `reel_asset_manifest.json`.
