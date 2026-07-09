# Weekly Run Manifest - 2026-W26

Generated artifacts:

- `weekly_content_packet.csv`
- `daily_queue.csv`
- `image_generation_briefs.md`
- `image_review_template.csv`
- `grok_prompts.md`
- `canva_placeholder_values.csv`
- `canva_fill_guide.md`
- `canva_placeholder_map.json`
- `canva_asset_slots.csv`
- `post_drafts.md`
- `publish_checklist.md`

## Current Status

Do not publish any W26 Canva draft yet.

```text
2026-W26-001 = needs_image_asset_selection
2026-W26-002 = needs_image_asset_selection
```

## 2026-W26-001

Status: blocked on image selection.

Reason:

```text
motion_crop has non-publishable status needs_regeneration
codex_asset_selection.csv selection_status = needs_review
```

## 2026-W26-002

Status: blocked on image regeneration.

Reason:

```text
The A_v2/B_v2/C_v2 image assets were generated on 2026-07-02.
The approved M02 v3 reference anchors were created on 2026-07-07.
Therefore the committed Canva copy used the old model identity.
```

Invalid Canva drafts:

```text
DAHOyDPZHeQ = invalid, old asset / Magic Layers failure
DAHO2rHNkZs = invalid, old M02 identity; do not export or publish
```

Invalid old Canva asset ids:

```text
cover_image = MAHOCYb2mPI
motion_crop = MAHOCUFmjRs
detail_image = MAHON_SkSjs
```

Correct next action:

```text
Regenerate W26-002 with M02_start_v3_face.png and M02_start_v3_full.png.
Score the new images.
Rerun asset selection.
Only then duplicate Canva again.
```
