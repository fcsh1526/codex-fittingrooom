# W30-004 Reel Storyboard v1

Status: layout approved; preview rendered; not published.

## Preview output

- Video: `W30-004_documentary_reel_preview_v1.mp4`
- Poster: `W30-004_documentary_reel_poster_v1.png`
- Codec: H.264 / AVC
- Dimensions: 1080 x 1920 px
- Measured duration: 6.019 seconds
- Audio: none
- Render method: project browser Canvas + MediaRecorder workflow

## Delivery

- Canvas: 1080 x 1920 px
- Aspect ratio: 9:16
- Total duration: 6.00 seconds
- Visual direction: unretouched documentary fashion-magazine sequence
- Motion rule: no artificial push-in, zoom, pan, shake, or generated pseudo-motion
- Transition rule: direct clean cuts only; no dissolve, flash, fade-in, or fade-out

## Source order and timing

| Time | Source | Purpose |
|---|---|---|
| 0.00-2.10 s | `2026-W30-004_M05_reel_accepted_A.png` | Establish the complete outfit and morning coffee setting immediately. |
| 2.10-4.05 s | `2026-W30-004_M05_reel_accepted_C.png` | Move closer to the rolled cuff, cotton texture, trouser waist, cup, and human gesture. |
| 4.05-6.00 s | `2026-W30-004_M05_reel_accepted_B.png` | End with the half-rising movement and bag strap, implying that she is leaving for work. |

Narrative order is A -> C -> B: setting -> tactile detail -> departure.

## Opening title

Exact text, split across two lines without adding punctuation:

```text
上班前的
咖啡時光
```

- Visible duration: 0.00-1.45 s
- Must already be fully visible on the first frame; no entrance animation
- Frame: accepted A only
- Alignment: left aligned
- Text box on 1080 x 1920 canvas:
  - x: 86 px
  - y: 250 px
  - maximum width: 360 px
  - maximum height: 170 px
- Placement: upper-left window area, fully clear of hair, face, shirt, coffee cup, and Reel right-side controls
- Preferred type: refined Traditional Chinese serif, medium weight
- Preferred size: approximately 56 px
- Line height: approximately 1.08
- Color: charcoal brown `#2B2926`
- Treatment: no background box, outline, glow, drop shadow, or decorative line
- Instagram-editor fallback: select the least decorative serif-like typeface, keep it small and left aligned, and visually match the position above

## Frame treatment

- Use each accepted image without reframing that changes the visible outfit or removes the existing environmental context.
- Do not apply automatic face tracking, Smart Crop, portrait cutout, or beauty enhancement.
- Do not animate the still images. The visual progression comes from the three different documentary moments and the two direct cuts.
- Keep A, C, and B at the same exposure and color treatment; do not apply separate filters.
- End directly on B at 6.00 seconds. Do not add an end card or call to action.

## Approval gate

Do not render or publish until the user approves:

1. A -> C -> B order
2. 2.10 / 1.95 / 1.95 second timing
3. two-line upper-left title placement
4. direct cuts with no artificial still-image movement
