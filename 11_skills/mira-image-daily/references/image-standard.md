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
- Body proportions must match the approved full-body anchor: head-to-height ratio, shoulder width, torso length, hip placement, knee height, and lower-leg length.
- Use a normal 50mm full-frame-equivalent perspective with a level optical axis near chest height. No low angle or wide-angle elongation.
- Build one coherent in-camera scene. Person, foreground, floor, and background must share light direction, white balance, depth of field, grain, edge softness, and ambient color spill.
- Include plausible physical interaction or overlap so the person is grounded in the scene rather than isolated against a backdrop.
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

Generate a controlled three-asset session:

```text
A = integrated-scene Hero and session lock
B = movement variation edited from accepted A
C = outfit-detail variation edited from accepted A
```

All assets are the same photographed outfit session. Generate A first. If required, apply one lighting/camera-finish edit to A without changing its content. B/C must use accepted A as the edit target/session lock plus the face and full-body anchors. Keep exact garments, layers, palette, shoes, bag, jewelry, identity, body build, scene identity, and lighting logic. C may use a closer crop; B may change pose and gaze.

Reference images lock identity, hair baseline, and body proportions only. They do not prescribe expression, pose, hand position, camera angle, background, lighting, or outfit.

- A: natural weight shift with physical contact or foreground overlap and one coherent scene exposure.
- B: candid turn or small movement derived from A, with changed gaze and natural hand interaction.
- C: knees-up or waist-up outfit detail derived from A, preserving identity, garment construction, and scene treatment.

Reject a set when A/B/C repeat the same centered stance, straight arms, gaze, or frozen expression.

Do not create B/C until A passes. Reject B/C if editing drifts wardrobe, identity, body build, or scene lighting.

## Review Rule

Reject beautiful images if they are not usable for commerce:

- outfit unclear
- head size, torso length, waist-to-knee ratio, or knee-to-ankle ratio drifting from the approved full-body anchor
- inconsistent body-to-leg proportions across A/B/C
- tiny head, nine-head fashion elongation, low-angle leg stretching, or wide-angle perspective distortion
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
