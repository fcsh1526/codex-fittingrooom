# User-Provided Anchor Source Photos

Received: 2026-07-07

Purpose: restart Phase B anchor rebuild using user-provided source photos for M01-M04. These source photos are identity references only; approved production anchors are recorded in `02_brand/mira_reference_images.csv`.

M01 approval status: v4 face/full anchors approved on 2026-07-07. The M01 face anchor is a direct PNG conversion from `M01.JPG`; the M01 full-body anchor is candidate B from the direct-face extension pass.

M02 approval status: v3 face/full anchors approved on 2026-07-07. The M02 face anchor is a direct PNG conversion from `M02.JPG`; the M02 full-body anchor is candidate A from the direct-face extension pass.

M03 approval status: v3 face/full anchors approved on 2026-07-07. The M03 face anchor is a direct PNG conversion from `M03.JPG`; the M03 full-body anchor is candidate A from the direct-face extension pass.

M04 approval status: pending.

Source files:

```text
M01.JPG -> M01 identity source
M02.JPG -> M02 identity source
M03.JPG -> M03 identity source
M04.JPG -> M04 identity source
```

Version strategy:

```text
M01 already has approved v3 anchors, so this user-source rebuild will become v4 if approved.
M02, M03, and M04 do not yet have approved v3 anchors, so their approved user-source rebuilds will become v3.
```

Production conversion rules:

```text
Use each source photo for face identity and presence.
Do not preserve source-photo glamour styling, bare shoulders, glossy skin, or non-neutral background.
Generate neutral face/full anchor pairs with simple clothing, plain background, natural matte skin texture, and no logos/text/watermarks.
Keep true ages as metadata only; prompts use visual-age language.
```
