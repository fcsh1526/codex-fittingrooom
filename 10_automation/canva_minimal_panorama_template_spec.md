# Canva Minimal Panorama Template Spec

Purpose: define the shared automation contract for Mira's registered Canva master templates.

Current production direction:

```text
Use 10_automation/mira_high_fashion_carousel_template_v2.md as the primary visual brief.
Use 10_automation/canva_template_registry.md as the source of truth for the five active Canva master templates.
This file remains the shared automation contract for required Canva layer names and export size.
```

Current Canva template version:

```text
See 10_automation/canva_template_registry.md for the five active Canva master templates.
```

Automation status:

```text
2026-07-14: Five cross-boundary v3 Canva master templates were committed and registered. Required slots are cover_image, motion_crop, detail_image, and slide2_line.
```

## Template Identity

```text
Mira Template v3
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
- Cross-boundary requirement: at least two image frames must extend 100-200 px across `x = 1080` or `x = 2160`; merely touching a cut line does not count.

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
- Production target: `cover_image` crosses `x = 1080` by 120-200 px.
- No large headline, trend name, CTA, icon, sticker, or text block.
- Outfit shape must be clear within one second.

### Slide 2 - Mood / Transition

- Slot: `motion_crop`
- Main role: quiet pause with one short sentence.
- Use a cinematic crop, outfit detail, blurred background crop, or simple lifestyle context image.
- At least one crop, insert, or background element should create a swipe reveal across a slide boundary.
- Production target: `motion_crop` either begins before `x = 1080` or crosses `x = 2160` by at least 100 px.
- Only text placeholder:

```text
{{slide2_line}}
```

- Text should be one short sentence, placed lower-left or lower-center with generous whitespace.
- Weekly text is concise English editorial mood copy with an intentional line break supplied by automation; do not rely on Canva auto-wrap.
- Text must occupy a face-free safe zone and remain at least 90 px from both cut lines.
- Avoid labels, bullets, CTA, disclosure, product names, or explanatory copy.

### Slide 3 - Closing Image

- Slot: `detail_image`
- Main role: let the outfit breathe one more time.
- Use a second lifestyle image if available.
- If only one image exists, reuse it with a different crop.
- If enough strong assets exist, this slide can use 2-3 horizontal film-still crops, but only when the outfit remains readable and the result does not feel crowded.
- Optional static brand name: `Mira`, bottom-right, very small.
- Production target: `detail_image` begins 80-140 px before `x = 2160` to create a reveal into slide 3.
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

- English mood sentence: `Cormorant Garamond`, `Libre Baskerville`, or another restrained editorial serif available in the template
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
