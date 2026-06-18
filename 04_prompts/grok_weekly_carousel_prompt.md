# Grok Weekly Carousel Prompt Template

Use this when generating image assets for a weekly Instagram carousel.

## Identity-Preserving Prompt

```text
Using the attached fictional AI virtual creator reference image as the subject, keep the same fictional identity, face, hairstyle, skin tone, body proportions, calm expression, and realistic Taiwan city style. Only replace the outfit.

Dress Mika Lin in {clothing_item}, color palette {color_palette}, fabric {fabric}, fit {fit}.

Styling rules: {styling_rules}.

Scene: {scene}. Use a practical Taiwan daily-life setting, realistic natural light, no luxury logos, no brand signage.

Camera: vertical fashion social media image, clear full outfit from head to shoes, clean composition, outfit easy to inspect on a phone screen.

Output 3-5 variations.
```

## Negative Prompt

```text
AI virtual outfit only; fictional person; no real person likeness; no celebrity; no childlike appearance; no school uniform; no nudity; no sexualized pose; no visible brand logos; no luxury logo; no fake endorsement; no distorted hands; no extra fingers; no unreadable text; no watermark.
```

## Reach-Recovery Version

Use this if Instagram reach is zero and we need a simpler second test:

```text
Create one clean vertical Instagram image of Mika Lin, a fictional AI virtual fashion creator. Keep the same calm Taiwan city identity. Full-body outfit visible. Simple neutral background. Minimal editorial look.

Outfit: {clothing_item}
Colors: {color_palette}
Styling: {styling_rules}
Scene: plain studio wall or simple office lobby

No text on image. No logos. No dramatic editorial pose. Make it easy to understand in one second.
```

