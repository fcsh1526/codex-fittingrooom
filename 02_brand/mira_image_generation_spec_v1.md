# Mira Image Generation Spec v1

Purpose: make Mira's images feel like a fast-updating AI fashion magazine for Taiwan daily outfits, while keeping the workflow simple enough to repeat.

## Core Direction

Mira is not a single public virtual influencer. Mira is a magazine brand.

The public feed should feel like:

```text
Taiwan daily life + polished fashion magazine eye + approachable model + outfit clearly readable
```

The public feed should not feel like:

```text
virtual influencer roleplay, runway editorial, luxury hotel ad, brand campaign, selfie diary, product catalog
```

Internal model names must not appear on IG images, captions, Canva text, or public-facing copy.

## Internal Models

Use the roster in:

```text
02_brand/mira_model_roster.md
02_brand/mira_model_roster.json
```

Short production use:

```text
M01 = office / commute / meeting
M02 = weekend / date / cafe
M03 = casual / budget-friendly daily wear
```

The model profile controls visual consistency. It is not a character story.

## Image Requirements

Every generated image should satisfy these rules:

- Full outfit is readable in one second.
- Person looks like a stylish ordinary Taiwan woman, not a distant supermodel.
- Pose is natural: walking, standing, adjusting bag, checking phone, waiting near a window, holding coffee.
- Clothes are the hero; face is consistent but not over-glamorized.
- Scene feels local and daily: cafe window, shaded sidewalk, MRT-adjacent walkway, department store fitting area, bookstore street, covered sidewalk.
- Lighting is realistic: soft daylight, natural shadows, no plastic beauty render.
- No visible logos, no text, no watermark, no shopping CTA inside image.
- No Chinese words rendered inside the image.

## Rejection Rules

Reject images when any of these are obvious:

- AI plastic skin or wax-like face.
- Supermodel body proportions or luxury fashion campaign mood.
- Runway pose, hotel lobby glamour, resort background.
- Overly posed influencer shoot.
- Outfit is unclear, cropped off, hidden by pose, or hard to buy.
- Hands, legs, face, or clothing structure are visibly broken.
- Styling feels too expensive, too fantasy, too bridal, too childish, or too logo-driven.

## Carousel Asset Strategy

Each daily outfit starts with 2-3 candidate images.

Preferred minimum:

```text
1 strong full-body image
```

Canva usage:

- `cover_image`: best full-body lifestyle image.
- `texture_or_crop`: crop from the best image, such as fabric, skirt movement, bag, shoe, sleeve, or waist detail.
- `detail_image`: second usable image if available; otherwise reuse/crop the cover.

Do not force three unrelated photos. One excellent image plus smart cropping is better than three weak images.

## Candidate Set

For each daily outfit, create:

```text
candidate A = safest full-body lifestyle shot
candidate B = slightly closer fashion-magazine crop with outfit still readable
candidate C = alternate daily scene or movement shot
```

If candidate A is strong enough, stop and move to review. Do not over-generate just to fill slots.

## Prompt Template

Use English for image prompts, with clothing details kept precise.

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand in Taiwan.

Use internal model {model_profile_id} only as a private production profile. Do not render or include the model ID, name, text, watermark, logo, or caption in the image.

Model profile:
{visual_profile}

Outfit:
{clothing_item}. Palette: {color_palette}. Fabric: {fabric}. Fit: {fit}.

Styling:
{styling_rules}

Scene:
{scene}. Make it feel like a believable Taiwan daily-life moment, not a runway, not a luxury hotel ad, not a brand campaign.

Composition:
Vertical 4:5 image. Full outfit readable within one second. Natural posture. Soft daylight. Real skin texture. Clothes are clear. Face is natural, calm, and approachable.

Avoid:
supermodel proportions, runway pose, luxury resort, plastic skin, flawless beauty render, excessive filters, sexualized pose, childlike styling, celebrity likeness, visible logos, text, watermark.
```

## Review Scores

Use `image_review_template.csv`.

Score 1-5:

- `model_consistency`: does it match the internal model profile?
- `reader_relatability`: does she feel like a stylish ordinary person readers can project onto?
- `outfit_clarity`: can the outfit be understood quickly?
- `ai_realism`: does it avoid obvious AI texture, broken anatomy, and plastic skin?
- `commerce_value`: does the outfit make someone want to look for similar clothes?

Publishable rule:

```text
publishable = yes only if outfit_clarity >= 4 and ai_realism >= 4
```

If a picture is beautiful but too fake, too posed, or too far from daily life, mark `publishable = no`.

## First Test Direction

Start with:

```text
week = 2026-W26
carousel_id = 2026-W26-002
model_profile_id = M02
outfit = 波點洋裝
occasion = weekend / date / cafe
```

Goal: find the Mira image tone before scaling to M01 and M03.

