# Mira Reference Image Requirements

The daily image workflow must not start from a loose text-only character prompt. Each internal model needs one approved reference start image.

Expected files:

```text
02_brand/reference_models/M01_start.png
02_brand/reference_models/M02_start.png
02_brand/reference_models/M03_start.png
```

Approval manifest:

```text
02_brand/mira_reference_images.csv
```

Set `status` to `approved` only after the image matches the model roster and can be used as a stable identity anchor.

Reference start image rules:

- one person only
- full body, head to shoes visible
- neutral simple outfit
- neutral background
- natural face and skin texture
- no logos, no text, no watermark
- consistent with `02_brand/mira_model_roster.json`

