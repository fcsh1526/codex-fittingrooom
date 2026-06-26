# Claude Design Prompt - Mira Template v1

Use this prompt in Claude Design to generate the first reusable Canva template.

```text
Design a 3-slide Instagram carousel template for an AI virtual fashion account called "Mira".

CONCEPT
This is not a tips carousel, not an infographic, and not a weekly report.
It is a lifestyle fashion carousel: image-led, cinematic, quiet, and intimate.
The entire carousel should feel like three frames from the same relaxed afternoon:
a person getting dressed, stepping out, and moving through the city.

Visual language:
Editorial Minimal x Cinematic Film.
Think Kinfolk magazine meets a warm film photographer's street archive.
Not a Vogue runway editorial.
Not a product lookbook.
Not an AI render showcase.

CANVAS SPEC
- Master canvas: 3240 x 1350 px, horizontal
- Split into 3 equal vertical slides
- Each slide: 1080 x 1350 px, 4:5 portrait
- Cut lines at x = 1080 and x = 2160
- Design must work as a reusable Canva template
- Every week, only three image frames and one short text line change

IMPORTANT PLACEHOLDER NAMES
Use these exact Canva frame / layer names:
- cover_image
- texture_or_crop
- detail_image
- {{slide2_line}}

Do not use {{slide1_image}}, {{slide2_image}}, {{slide3_image}}, or {{week_label}}.
Do not add extra editable text placeholders.

TARGET AUDIENCE
Asian / Taiwanese women, age 20-35.
Daily outfit ideas, commute outfits, cafe dates, casual errands.
They appreciate affordable style with real aesthetic taste.
They scroll quickly, so the outfit must be understandable within one second.

SLIDE 1 - VISUAL HOOK
Purpose: stop the scroll and show the outfit.
Layout:
- Full-bleed or near full-bleed portrait photo, 85-95% of slide area
- One image frame named cover_image
- Use a full-body or 3/4 lifestyle outfit image
- Suggested scenes: cafe window, side street, indoor natural light, commute station
- Avoid runway, luxury hotel lobby, showroom, white studio, or symmetrical posed ad shots
- No large headline
- No trend name in big type
- No icons, decorative frames, stickers, arrows, badges, or text boxes
- Text density should be near zero

SLIDE 2 - MOOD / TRANSITION
Purpose: breathing space with one quiet sentence.
Layout:
- Full-bleed or near full-bleed image frame named texture_or_crop
- Use a cinematic crop of the same outfit: fabric, waist-down detail, hand holding coffee, bag, shoes, window light, or street context
- One text placeholder only: {{slide2_line}}
- The text is a short mood sentence, not a caption, not a product description
- Place the text lower-left or lower-center with generous whitespace
- Font: Noto Serif TC Regular or Light, 32-38 pt equivalent at 1080 px width
- Color: #F0EDE6 over image, or #1C1C1C on light background
- No additional labels, tags, secondary text, tips, CTA, table, product list, or score badges

SLIDE 3 - CLOSING IMAGE
Purpose: linger and let the outfit breathe one more time.
Layout:
- Full-bleed or near full-bleed image frame named detail_image
- Use a second lifestyle pose, detail crop, back view, mid-distance candid-feel image, shoes, bag, collar, or fabric texture
- Optional static brand identifier: "Mira", bottom-right, very small, 16-18 pt
- The brand text is static, not a weekly placeholder
- No CTA wall
- No "save this post"
- No product names, links, affiliate labels, or shopping copy

COLOR SYSTEM
- Warm white background when needed: #F8F5F0
- Off-white secondary surface: #FAFAF8
- Primary text on light background: #1C1C1C
- Text on image: #F0EDE6
- Accent, use once at most: #C4673A
- Optional secondary tone: #9B8FA0
- Maximum 3 colors per slide
- No gradients, neon, or high-saturation backgrounds

TYPOGRAPHY
- Chinese short sentence: Noto Serif TC Regular or Light
- Small brand label: Inter Medium or DM Mono
- Maximum 2 typefaces across the carousel
- No decorative scripts or handwritten fonts
- Minimum readable size on mobile: 24 pt at 1080 px canvas width
- Keep Chinese letter spacing natural

IMAGE TREATMENT
- Add subtle warm film grain at 10-15% opacity if available
- Use a gentle warm color grade
- Avoid heavy dark transparent overlays
- The image should still feel clean, daily, and approachable
- The treatment should reduce AI smoothness without making the carousel look gritty

WHAT THIS IS NOT
Do not make this look like:
- A Canva infographic template
- A business presentation
- A weekly trend report with scores and tables
- A fashion lookbook with product tags and prices
- An AI showcase with perfect-skin renders
- A Korean beauty brand with excessive pink tones
- A carousel with checklist icons, arrows, or numbered tips

OUTPUT
Generate the 3-slide carousel as a visual mockup.
Show realistic image placeholder zones using warm cream rectangles or neutral photo placeholders.
Use the exact placeholder names listed above.
Make the design export-ready for Canva, or provide an annotated design specification that can be rebuilt in Canva.
```

## Follow-Up Prompts

If it looks too much like a presentation:

```text
This looks too much like a presentation slide. Remove all text elements except {{slide2_line}} on Slide 2 and the small static "Mira" label on Slide 3. The images should carry the visual weight. Text is a whisper, not a headline.
```

If it has too many decorative elements:

```text
Strip all decorative elements: icons, arrows, borders, frames, divider lines, stickers, and badges. The only allowed elements are image frames, one short text line on Slide 2, and a small brand label on Slide 3.
```

If it looks too much like a Canva template:

```text
This feels too templated. Remove rounded text boxes, icon rows, colored badges, and obvious social media template elements. The hierarchy should be image first, one quiet line second, and brand name last.
```

If it feels too AI-polished:

```text
Apply subtle warm film grain at 10-15% opacity, a gentle warm color grade, and a very light vignette. The result should feel like warm afternoon film photography, not a rendered AI image.
```
