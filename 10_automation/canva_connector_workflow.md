# Canva Connector Workflow

Purpose: make Canva assembly semi-automatic while keeping the carousel image-led and low-text.

## What Canva Connector Can Automate

Codex can use the Canva connector to:

1. Open or duplicate a Canva brand template.
2. Replace the single text placeholder.
3. Replace or insert image fills.
4. Resize or reposition image crops.
5. Generate page thumbnails for review.
6. Commit changes only after user approval.

## Current Best Workflow

```text
weekly_content_packet.csv
-> OpenAI / Grok images
-> image inventory + review scores
-> canva_asset_plan.md
-> canva_placeholder_map.json
-> Canva connector edits the 3-slide template
-> user reviews thumbnails
-> commit Canva changes
-> export / publish
```

## Canva Template Requirement

Use a 3-slide panorama master canvas:

```text
3240 x 1350 px
slice guides: x = 1080, 2160
export: 3 images, each 1080 x 1350 px
```

Text placeholders:

```text
{{slide2_line}}
```

Image placeholders:

```text
cover_image
texture_or_crop
detail_image
```

Slide roles:

1. Image-led hook. No required text.
2. One short transition sentence only.
3. Image-led ending. No CTA wall.

Keep AI disclosure in the Instagram caption, not on the image.

## Important Limitation

Canva edits are transactional. Codex can draft the edit and show thumbnails, but final save should happen only after the user confirms the preview is correct.

## Human Review Checklist

- Outfit is readable within one second.
- Mira identity is consistent.
- The image feels like a believable daily moment, not a posed ad.
- Slide 2 has only one short sentence.
- No comment-bait or shopping-list copy appears on the carousel.
- No logos, brand marks, or fake endorsements appear.
