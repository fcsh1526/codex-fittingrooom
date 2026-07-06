# Mira Reference Image Requirements

The daily image workflow must not start from a loose text-only character prompt. Each internal model needs one approved face anchor and one approved full-body anchor.

Expected files:

```text
02_brand/reference_models/M01_start_v{version}_face.png
02_brand/reference_models/M01_start_v{version}_full.png
02_brand/reference_models/M02_start_v{version}_face.png
02_brand/reference_models/M02_start_v{version}_full.png
02_brand/reference_models/M03_start_v{version}_face.png
02_brand/reference_models/M03_start_v{version}_full.png
02_brand/reference_models/M04_start_v{version}_face.png
02_brand/reference_models/M04_start_v{version}_full.png
```

Approval manifest:

```text
02_brand/mira_reference_images.csv
```

Set `status` to `approved` only after both anchor files match the model roster and can be used as stable identity anchors.

Reference start image rules:

- one person only
- face anchor: clean face-front or slight 3/4 portrait
- full anchor: full body, head to shoes visible
- neutral simple outfit
- neutral background
- natural face and skin texture
- no logos, no text, no watermark
- consistent with `02_brand/mira_model_roster.json`

Old versions are never overwritten or deleted. The manifest points to the current approved face/full pair; superseded paths stay in the row notes/audit fields.
