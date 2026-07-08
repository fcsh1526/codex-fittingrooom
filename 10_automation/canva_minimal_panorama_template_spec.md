# Canva Minimal Panorama Template Spec

Purpose: create one reusable Canva template for Mira's image-led Instagram carousels.

Current production direction:

```text
Use 10_automation/mira_high_fashion_carousel_template_v2.md as the primary visual brief.
This file remains the automation contract for required Canva layer names and export size.
```

Current Canva v2 template:

```text
See 10_automation/canva_template_registry.md for the five active Canva master templates.
```

Automation status:

```text
2026-07-08: Five Canva master templates were registered. Required slots are cover_image, motion_crop, detail_image, and slide2_line.
```

## Template Identity

```text
Mira Template v2
Style: High-Fashion Editorial x Cinematic Swipe
Role: lifestyle fashion carousel, not a weekly report
```

The post should feel like:

```text
believable virtual lifestyle outfit -> instant visual attraction -> short caption -> profile link
```

It should not feel like:

```text
text-heavy carousel -> comment bait -> product list -> hard sell
```

## Canvas

- Master size: `3240 x 1350 px`
- Export slices: `3 x 1080 x 1350 px`
- Vertical guide lines: `x = 1080`, `x = 2160`
- Safe margin for small text: `90 px`
- Recommended Canva setup: one wide master design, then export and slice into three carousel images.

## Canva Element Names

Use these exact frame / layer names so Codex automation can match the template:

```text
cover_image
motion_crop
detail_image
slide2_line
```

Do not introduce weekly text placeholders such as `{{week_label}}` unless automation is updated later.

Canva autofill labels:

```text
cover_image
motion_crop
detail_image
slide2_line
```

## Slide Layout

### Slide 1 - Visual Hook

- Slot: `cover_image`
- Main role: stop the scroll and show the outfit.
- Use the strongest full-body or near-full-body lifestyle image.
- Image should cover 85-95% of the slide.
- The image may extend slightly past the Slide 1 / Slide 2 cut line if the face and head remain safely inside the frame.
- No large headline, trend name, CTA, icon, sticker, or text block.
- Outfit shape must be clear within one second.

### Slide 2 - Mood / Transition

- Slot: `motion_crop`
- Main role: quiet pause with one short sentence.
- Use a cinematic crop, outfit detail, blurred background crop, or simple lifestyle context image.
- At least one crop, insert, or background element should create a swipe reveal across a slide boundary.
- Only text placeholder:

```text
{{slide2_line}}
```

- Text should be one short sentence, placed lower-left or lower-center with generous whitespace.
- Avoid labels, bullets, CTA, disclosure, product names, or explanatory copy.

### Slide 3 - Closing Image

- Slot: `detail_image`
- Main role: let the outfit breathe one more time.
- Use a second lifestyle image if available.
- If only one image exists, reuse it with a different crop.
- If enough strong assets exist, this slide can use 2-3 horizontal film-still crops, but only when the outfit remains readable and the result does not feel crowded.
- Optional static brand name: `Mira`, bottom-right, very small.
- No CTA wall.

## Style Rules

- Keep the carousel image-led.
- Use at most one main sentence across the whole carousel.
- Images should occupy 85-95% of each slide.
- Treat the 3240 px canvas as one editorial spread, not three isolated cards.
- Use boundary crops intentionally, but never crop a head, face, hand, or key garment detail by accident.
- Add subtle warm film grain or warm tone overlay when useful to reduce AI smoothness.
- Do not put AI disclosure on the image; keep it in the Instagram caption.
- Do not use "留言...", "平價 / 質感 / 替代款", product-list copy, or shopping CTA on the image.
- Do not add large decorative cards, boxed text areas, gradients, icons, arrows, badges, or tables.

## Color System

```text
Warm white: #F8F5F0
Off-white: #FAFAF8
Charcoal: #1C1C1C
Cream on image: #F0EDE6
Terracotta accent: #C4673A
Dusty mauve optional: #9B8FA0
```

Use a maximum of 3 colors per slide. Use the accent color sparingly.

## Typography

- Chinese sentence: `Noto Serif TC` or `Noto Sans TC`
- Small brand / label: `Inter Medium` or `DM Mono`
- Maximum 2 typefaces across the carousel.
- Minimum readable size on mobile: `24 pt` on a 1080 px wide slide.
- No decorative scripts or handwritten fonts for this version.

## W26 Test Fill

Recommended first test item:

```text
2026-W26-002
```

Image:

```text
10_automation/runs/2026-W26/openai_images/ChatGPT Image 2026年6月24日 下午03_30_10.png
```

Slide 2 text:

```text
波點洋裝，讓約會多一點記憶點。
```

Caption direction:

```text
短內文 + 相似單品放在個人頁連結 + AI 生成虛擬造型影像。
```
