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
- Lighting is physically integrated with the scene: one readable source direction, matching color temperature, visible face/body falloff, contact shadows, and ambient color spill.
- The model must look photographed in the location, never independently lit or pasted onto the background.
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

All candidates are the same outfit session. A/B/C must keep the exact same garments, layers, palette, shoes, bag, jewelry, and styling placement. Only pose, camera distance, and framing may change.

Reference images lock identity, hair baseline, and body proportions only. They do not prescribe expression, pose, hand position, camera angle, background, lighting, or outfit.

- A: asymmetric three-quarter stance, natural weight shift, attentive eyes, subtle expression.
- B: candid mid-step or turning movement, different gaze, natural hand interaction.
- C: closer or detail-friendly angle, different camera height and body direction.

Reject a set when A/B/C repeat the same centered stance, straight arms, gaze, or frozen expression.

Stop if candidate A is already strong. Do not keep generating just to fill slots.

## Review Rule

Reject beautiful images if they are not usable for commerce:

- outfit unclear
- too glamorous
- too artificial
- too expensive-looking for the target
- too posed
- weak clothing detail
- subject/background lighting mismatch
- shadowless or front-lit face when the scene light is directional
- missing shoe contact shadows or halo/cutout edges
- any garment, color, shoe, bag, or accessory drift across A/B/C
- frozen or passport-like expression
- repeated pose, gaze, and hand position across A/B/C
- white borders or letterboxing
