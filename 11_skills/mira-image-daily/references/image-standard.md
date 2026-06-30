# Mira Image Standard

## Direction

Mira uses global fashion trend research, then turns it into daily outfit imagery readers can imagine wearing.

Do not limit the trend source to Taiwan. Perplexity weekly research can cover global runways, street style, retail, creator trends, and seasonal fashion signals.

The image output should still feel daily, wearable, and commerce-relevant:

```text
global trend signal -> wearable daily outfit -> approachable fashion magazine image
```

## Brand Feel

Mira should feel like:

```text
fast AI fashion magazine, recurring familiar models, polished but reachable, useful outfit reference
```

Mira should not feel like:

```text
single virtual influencer, selfie diary, runway editorial, luxury ad campaign, product catalog
```

## Image Requirements

- Full outfit readable in one second.
- Outfit reflects the global trend, but is simplified into daily styling.
- Model looks approachable, not remote or celebrity-like.
- Scene supports the outfit and target occasion.
- Lighting is realistic with visible fabric texture and natural skin texture.
- No logos, no image text, no watermark, no public model name.
- No shopping CTA, disclosure, product list, or comments rendered inside the image.

## Scene Policy

Use scenes based on the outfit and target audience. Taiwan scenes are allowed, but not mandatory.

Good scene types:

- commute walkway
- office lobby
- cafe window
- bookstore street
- quiet shopping street
- fitting room mirror area
- neighborhood sidewalk
- covered rainy-day walkway
- simple studio with natural shadows

Avoid:

- runway
- luxury hotel
- resort fantasy
- red carpet
- bridal editorial unless the trend explicitly requires bridal
- logo-heavy retail display

## Candidate Strategy

Generate 2-3 candidates:

```text
A = safest full-body daily lifestyle image
B = movement or street-style variation
C = closer outfit-detail-friendly variation
```

Stop if candidate A is already strong. Do not keep generating just to fill slots.

## Review Rule

Reject beautiful images if they are not usable for commerce:

- outfit unclear
- too glamorous
- too artificial
- too expensive-looking for the target
- too posed
- weak clothing detail

