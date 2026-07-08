# Claude Design Prompt - Mira Template v2

Use this prompt to rebuild the Mira Canva template after the Scrolo-style reference discussion.

```text
Create a 3240 x 1350 px Instagram carousel master template for Mira, a high-fashion but fast-updating AI outfit magazine.

This is a 3-slide carousel master. It exports into three 1080 x 1350 px IG slides.

The key idea:
Do not design three separate Canva cards.
Design one cinematic editorial spread that becomes more interesting when the viewer swipes.

The carousel should feel like:
- a modern fashion magazine spread,
- a believable daily outfit moment,
- cinematic but wearable,
- quiet and image-led,
- premium without looking like runway or luxury-hotel advertising.

The carousel should not feel like:
- an infographic,
- a product catalog,
- a presentation,
- a weekly report,
- a virtual influencer profile,
- a generic Canva template.

Canvas:
- Master size: 3240 x 1350 px
- Slide 1: x 0-1080
- Slide 2: x 1080-2160
- Slide 3: x 2160-3240
- No visible gutters
- No final cut-line labels

Required editable Canva layer names:
- cover_image
- motion_crop
- detail_image
- slide2_line

Optional locked layers:
- scene_backplate
- boundary_insert
- film_crop
- brand_mark
- grain_overlay

Visual mechanics:
- Use full-bleed or near-full-bleed imagery.
- Let one large image or background continue across a slide boundary.
- Let one insert crop partially cross or touch a slide boundary.
- Use one close crop or film-still crop to create movement.
- Use negative space so the next slide feels like a reveal.
- Keep the layout editorial, not scrapbook-like.

Slide 1:
- Main visual hook.
- Use cover_image.
- Full-body or 3/4 body outfit frame.
- The outfit must be readable within one second.
- The image may extend 120-260 px past the Slide 1 / Slide 2 boundary.
- Do not crop the head, face, hands, or key garment details by accident.
- No headline in the first test version.

Slide 2:
- Swipe / transition frame.
- Use motion_crop.
- Use a cinematic crop: fabric, movement, hand, bag, shoes, street context, window light, or partial body.
- It should create a bridge between slide 1 and slide 3.
- The only weekly text is slide2_line.
- Place slide2_line over calm negative space.
- Text should feel like a whisper, not a caption box.

Slide 3:
- Closing editorial frame.
- Use detail_image.
- It may be a second lifestyle image, a full-body closing shot, or 2-3 horizontal film-still crops.
- If using film-still crops, keep the outfit clear and avoid crowding.
- Add a very small static "Mira" brand mark only if natural.
- No CTA wall.

Typography:
- slide2_line: Noto Serif TC Light or Regular, 30-42 pt at 1080 px slide width.
- Brand mark: Inter Medium, DM Mono, or a simple serif small-caps treatment.
- Maximum two typefaces.
- No decorative scripts, stickers, badges, arrows, product tags, or boxed captions.

Color and finish:
- Let the image decide the palette.
- Use subtle warm film grain if useful.
- Use a mild vignette only if it supports readability.
- Avoid heavy gradients, neon accents, obvious Canva shadows, and beige-only monotony.

Final export must not show:
- product lists,
- CTA text,
- "留言",
- "平價 / 質感 / 替代款",
- AI disclosure,
- placeholder instructions,
- template labels,
- icons,
- badges,
- arrows,
- tables.

Validation:
- The full outfit is clear.
- The carousel reads as one editorial spread.
- At least one image or crop creates a swipe reveal across a slide boundary.
- No accidental head crop.
- No AI artifacts are hidden by layout tricks.
- The final slices still work as individual IG slides.
```

If Claude Design makes it too plain:

```text
This still feels like three isolated slides. Redesign it as one continuous editorial spread. Add a boundary-crossing image crop, a full-bleed scene, and one insert crop that makes the viewer want to swipe.
```

If Claude Design adds too much text:

```text
Remove all text except {{slide2_line}} and a very small static Mira brand mark. This is an image-led fashion carousel, not a tips carousel.
```

If Claude Design looks too templated:

```text
Remove obvious Canva template elements: rounded caption boxes, stickers, icons, badges, framed cards, and decorative dividers. Use crop, scale, negative space, and image rhythm instead.
```
