# Mira High-Fashion Carousel Template v2

Purpose: replace the plain 3-slot Canva layout with a high-fashion, image-led carousel system for Mira.

This brief is based on the user's Scrolo reference screenshots. Do not copy the exact night-city design, text, model, or imagery. Use the observed layout mechanics only: cinematic full-bleed imagery, cross-slide continuity, partial crops at slide boundaries, and very low text density.

## Core Direction

Mira should feel like:

```text
fast-updating AI fashion magazine -> believable outfit moment -> cinematic carousel swipe -> quiet caption -> profile-link commerce
```

Mira should not feel like:

```text
Canva placeholder sheet -> product catalog -> infographic -> virtual influencer roleplay -> AI render showcase
```

## What The Reference Teaches

The reference works because it uses carousel movement as part of the design:

- A large scene continues beyond one slide, so swiping feels like moving through one editorial spread.
- Important images sometimes sit across a slide boundary instead of staying inside one slide.
- Some crops are intentionally cut off by the slide edge, making the viewer want to swipe.
- Full-body, mid-shot, close-up, and environmental shots alternate like film frames.
- Text is sparse and secondary. The image creates the hook.
- Large type appears only when it is part of the mood, not to explain the content.
- The background scene has depth: foreground blur, midground subject, background lights or architecture.

## Canvas Contract

- Master canvas: `3240 x 1350 px`
- Export slices: `3 x 1080 x 1350 px`
- Cut lines: `x = 1080`, `x = 2160`
- Use one wide master design. Do not design three isolated cards.
- No visible gutters between slides.
- Do not add cut-line labels on the final export.

Required Canva names for automation compatibility:

```text
cover_image
motion_crop
detail_image
slide2_line
```

Optional Canva names for richer manual or connector editing:

```text
scene_backplate
boundary_insert
film_crop
brand_mark
grain_overlay
```

The optional layers can be locked after template creation. The required layers must remain editable.

## Slide Behavior

### Slide 1 - Hook Frame

Role: immediate outfit impact.

Layout:

- Use `cover_image` as the dominant visual.
- Full-bleed or near full-bleed image.
- Subject should be full-body or 3/4 body when the outfit needs to sell the look.
- The image may extend 120-260 px past the first cut line into Slide 2.
- A face or head must not sit on the cut line.
- Keep head clearance: at least 90 px from top edge if the head is visible.
- Text should usually be absent. If a headline is tested later, it must be mood-based, not explanatory.

Reject:

- Centered catalog pose.
- White studio background.
- Head cropped by the Canva frame.
- Slide 1 looking like a template cover with a big title.

### Slide 2 - Swipe / Transition Frame

Role: create the carousel movement.

Layout:

- Use `motion_crop` for a cinematic transition image.
- This can be a street/background crop, fabric detail, motion blur, bag/shoe crop, side profile, or partial body crop.
- At least one visual element should cross or touch a slide boundary.
- The crop can be deliberately incomplete, but it must look intentional.
- Use only one text line: `{{slide2_line}}`.
- Place the text over a calm area with enough contrast.
- Preferred text positions: lower-left, lower-center, or upper-left if the image has quiet space.

Text:

- One short mood sentence.
- No product list.
- No CTA.
- No AI disclosure.
- No "留言".
- No "平價 / 質感 / 替代款".

Reject:

- Text centered in a box.
- A normal single-image placeholder with a sentence pasted on it.
- Cropping that cuts the subject's head by accident.
- Any UI labels or template instructions visible in final export.

### Slide 3 - Closing Editorial Frame

Role: linger and make the outfit memorable.

Layout:

- Use `detail_image` as either:
  - a second lifestyle frame,
  - a full-body closing shot,
  - a horizontal film-strip crop stack,
  - or a detail frame of the same outfit.
- If there are enough assets, Slide 3 can use 2-3 horizontal strips like film stills.
- If only one strong asset exists, use a different crop, not a duplicated full view.
- Optional `Mira` brand mark should be small and quiet.

Reject:

- CTA wall.
- Product tags or prices.
- Collage that looks like a shopping board.
- Overcrowded crop stack where the outfit is unclear.

## Cross-Slide Composition Rules

Use at least two of these per carousel:

1. One hero image extends beyond a slide boundary.
2. One insert crop is partially cut by a slide edge.
3. One background image spans two slides or the full 3240 px master.
4. One frame uses negative space to make the next slide feel like a reveal.
5. One close-up crop contrasts with a full-body frame.

Do not use all effects at once if the post becomes busy. The result should feel editorial, not like a scrapbook.

## Image Asset Requirements

For each daily outfit, prepare at least three candidate image types:

```text
hero_outfit_frame
environment_or_motion_frame
detail_or_closeup_frame
```

Ideal image set:

- 1 clear outfit frame: full-body or 3/4 body, readable garment silhouette.
- 1 environmental frame: wider scene, subject can be smaller, daily-life context.
- 1 detail frame: fabric, shoes, bag, sleeve, waist, collar, hand movement, or walking crop.

If only two images pass QA:

- Use the stronger image as `cover_image`.
- Use a background or detail crop from the same image as `motion_crop`.
- Use the second image as `detail_image`.
- Do not force a three-frame collage if it exposes AI artifacts.

If only one image passes QA:

- Prefer single-image post or pause the day.
- Do not publish a weak carousel just to fill the template.

## Image Generation Guidance

Ask image generation for editorial continuity, not isolated product shots.

Prompt for:

- one believable daily-life location,
- the assigned Mira internal model,
- the trend clothing item,
- a clear outfit silhouette,
- natural movement or candid posture,
- cinematic depth,
- useful negative space,
- clean hands, face, and body edges,
- no duplicated person, no ghosting, no motion smear on the subject.

Avoid:

- runway,
- luxury hotel lobby,
- red carpet,
- high-glamour supermodel pose,
- plastic skin,
- distorted face,
- duplicated face,
- body afterimage,
- extra limbs,
- unreadable garment shape.

## Typography

Use text as a whisper.

- Main sentence: `Noto Serif TC Light` or `Noto Serif TC Regular`
- Brand mark: `Inter Medium`, `DM Mono`, or simple serif small caps
- Maximum two typefaces.
- Recommended `{{slide2_line}}` size: 30-42 pt on 1080 px slide width.
- Large headline is optional and should be avoided in the first Mira v2 test.
- Do not use script fonts, sticker labels, or boxed captions.

## Color And Finish

The palette should come from the image.

Allowed finishing:

- subtle warm film grain,
- mild vignette,
- soft black or cream text depending on image contrast,
- gentle editorial color grade.

Avoid:

- heavy gradient overlays,
- obvious Canva shadows,
- neon accents,
- template badges,
- dominant beige-only look across every post.

## Canva Validation Checklist

Before export:

- [ ] The carousel reads as one editorial spread, not three isolated cards.
- [ ] At least one image or crop creates a swipe reveal across a slide boundary.
- [ ] No subject head is accidentally cropped.
- [ ] The full outfit is understandable within one second.
- [ ] `slide2_line` is the only weekly text slot on the image.
- [ ] No CTA, product list, AI disclosure, comment bait, or template label appears on the image.
- [ ] `Mira` is small if present.
- [ ] The final slices still work one by one in IG preview.
- [ ] AI artifacts are hidden only if the image already passes QA; do not use layout to rescue a broken face or body.

## Claude Design / Canva Build Prompt

Use this when asking Claude Design to rebuild the template:

```text
Create a 3240 x 1350 px Instagram carousel master template for Mira, a high-fashion but fast-updating AI outfit magazine.

The design must export into three 1080 x 1350 px carousel slides. It should feel like one cinematic editorial spread being revealed through swiping, not three separate Canva cards.

Use these required editable Canva layer names:
- cover_image
- motion_crop
- detail_image
- slide2_line

Optional locked layers may be named:
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
- Keep text extremely low.
- The only weekly text placeholder is slide2_line.
- Add a very small static "Mira" brand mark only if it feels natural.

Mood:
Editorial, cinematic, intimate, wearable, modern fashion magazine.
Not infographic, not product catalog, not presentation, not obvious Canva template.

Final export must not show cut lines, template labels, placeholder instructions, product lists, CTA text, AI disclosure, icons, badges, arrows, tables, or decorative stickers.
```
