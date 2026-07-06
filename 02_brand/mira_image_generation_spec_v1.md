# Mira Image Generation Spec v1

Purpose: make Mira's images feel like a fast-updating AI fashion magazine using global fashion trend research, while keeping the output wearable, daily, and repeatable.

This document is the readable project copy. The stricter operational version lives in the Codex skill:

```text
11_skills/mira-image-daily/
C:\Users\Brandon_ChangChien\.codex\skills\mira-image-daily\
```

## Core Direction

Mira is not a single public virtual influencer. Mira is a magazine brand.

The public feed should feel like:

```text
global trend signal + polished fashion magazine eye + approachable model + outfit clearly readable
```

The public feed should not feel like:

```text
virtual influencer roleplay, runway editorial, luxury hotel ad, brand campaign, selfie diary, product catalog
```

Internal model names must not appear on IG images, captions, Canva text, or public-facing copy.

Perplexity weekly research is global by default. Do not narrow trend discovery to Taiwan. The image task is to translate global signals into wearable daily outfits for Mira's audience.

## Internal Models

Use the roster in:

```text
02_brand/mira_model_roster.md
02_brand/mira_model_roster.json
```

Internal true-age metadata and prompt-safe visual age language:

```text
M01 true age 25 -> prompt visual age: early 20s
M02 true age 35 -> prompt visual age: late 20s, youthful
M03 true age 45 -> prompt visual age: mid 30s look, well-maintained
M04 true age 55 -> prompt visual age: early 40s look, elegant
```

True ages are roster metadata only. Image prompts must not include numeric true ages. Express age through styling and presence, not wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.

The model profile controls identity and visual consistency. It is not a character story and it is not tied to one clothing occasion.

Content buckets such as `office_capsule`, `date_outfit`, `weekend_daily`, `daily_style`, and `rainy_day` describe the outfit context. They do not decide the model by themselves. Any bucket can be styled for any age cohort when the content plan calls for it.

## Image Requirements

Every generated image should satisfy these rules:

- Full outfit is readable in one second.
- Person looks stylish and approachable, not like a distant supermodel.
- Pose is natural: walking, standing, adjusting bag, checking phone, waiting near a window, holding coffee.
- Clothes are the hero; face is consistent but not over-glamorized.
- Scene feels daily and believable: cafe window, shaded sidewalk, commute walkway, department store fitting area, bookstore street, covered sidewalk, quiet shopping street, simple studio with natural shadows.
- Lighting is realistic: soft daylight, natural shadows, no plastic beauty render.
- No visible logos, no text, no watermark, no shopping CTA inside image.
- No Chinese words rendered inside the image.

## Reference Start Image Requirement

Do not generate daily outfit images from text-only character descriptions.

Each model must first have approved face and full-body reference start images:

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

Approval is tracked in:

```text
02_brand/mira_reference_images.csv
```

Daily generation for a model is blocked until its row status is `approved` and both `reference_face_path` and `reference_full_path` exist.

Legacy draft pack folders are archived under run folders for audit. The only current truth source for approved anchors is:

```text
02_brand/mira_reference_images.csv
```

Old versions are never overwritten or deleted. Superseded paths stay in the manifest notes/audit trail. Candidate images and drafts must stay in run folders, not as canonical files under `02_brand/`.

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
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand using global fashion trend research.

Use internal model {model_profile_id} only as a private production profile. Do not render or include the model ID, name, text, watermark, logo, or caption in the image.

Model profile:
{visual_profile}

Prompt visual age language:
{prompt_age_language}

Age rendering:
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin is smooth and well-maintained.

Outfit:
{clothing_item}. Palette: {color_palette}. Fabric: {fabric}. Fit: {fit}.

Styling:
{styling_rules}

Scene:
{scene}. Make it feel like a believable daily-life fashion moment, not a runway, not a luxury hotel ad, not a brand campaign. Use the global trend signal, but translate it into wearable styling.

Composition:
Vertical 4:5 image. Full outfit readable within one second. Natural posture. Soft daylight. Real skin texture. Clothes are clear. Face is natural, calm, and approachable.

Avoid:
supermodel proportions, runway pose, luxury resort, plastic skin, flawless beauty render, excessive filters, sexualized pose, childlike styling, celebrity likeness, visible logos, text, watermark, wrinkle-based age cues, numeric true-age labels.
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

Goal: find the Mira image tone before scaling across M01/M02/M03/M04.
