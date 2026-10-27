# Mira Image Standard

## Direction

Mira uses global fashion trend research, then turns it into daily outfit imagery readers can imagine wearing.

Do not limit the trend source to Taiwan. Perplexity weekly research can cover global runways, street style, retail, creator trends, and seasonal fashion signals.

The image output should still feel daily, wearable, and commerce-relevant:

```text
global trend signal -> wearable daily outfit -> approachable fashion magazine image
```

Every daily image begins with one practical `dressing_decision` and one `visible_action`. Mira uses `utility_with_immersion`: the outfit solves one concrete dressing question while the setting, sequence and photographic detail create an immersive identity/lifestyle experience.

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
- Photograph with a full-frame mirrorless camera and a 50mm prime lens, using a level optical axis near chest height. Do not use a smartphone, computational portrait mode, DSLR simulation, low angle, or wide-angle elongation unless the user explicitly overrides the camera standard.
- Use camera terms only to control high-level look, viewpoint and composition. Do not state fixed aperture, shutter speed, ISO or white balance in GPT Image prompts.
- Describe visible realism instead: available natural light, believable ambient spill, real skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness.
- Build one coherent in-camera scene. Person, foreground, floor, and background must share light direction, white balance, depth of field, grain, edge softness, and ambient color spill.
- Include plausible physical interaction or overlap so the person is grounded in the scene rather than isolated against a backdrop.
- Outfit reflects the global trend, but is simplified into daily styling.
- Model looks approachable, not remote or celebrity-like.
- Scene supports the outfit and target occasion.
- Lighting is physically integrated with the scene: one readable source direction, matching color temperature, visible face/body falloff, contact shadows, and ambient color spill.
- The model must look photographed in the location, never independently lit or pasted onto the background.
- No logos, no image text, no watermark, no public model name.
- No shopping CTA, disclosure, product list, or comments rendered inside the image.

## Delivery Surface Policy

- Every approved look requires both a `reel` job and a `carousel` job.
- Reel: create one full-person A directly for a 9:16 frame intended for 1080x1920 delivery, and one usable styling-proof view per look. Record actual source pixels. Five weekly Reels each keep one model and its two looks. Select proof imagery only after vertical framing and clarity review; generate the missing view if necessary. Do not use Canva slot geometry or its 15% crop allowance for native Reel generation. See `09_sops/mira_reel_production_sop.md` in the project for dynamic QA and reference tests.
- Carousel: always create three exact-role images for the connected Canva template: A full-person Hero, B scene application, and C accessory detail. The 15% center-crop ceiling applies only when normalizing approved Carousel sources to those exact Canva pixels.
- Preserve identity, exact outfit, scene logic, and camera treatment across both surfaces, but create separate compositions for each target geometry.

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

- access-control turnstiles, ticket gates, or badge-scanning scenes
- visible access cards or poses built around presenting a small card to the camera
- runway
- luxury hotel
- resort fantasy
- red carpet
- bridal editorial unless the trend explicitly requires bridal
- logo-heavy retail display

## Hero-First Production Sequence

Generate one Carousel Hero first, then complete its required three-frame set:

```text
A = full-person integrated-scene Hero and session lock
B = required scene-application frame in another corner, wider environmental view, or suitable setting for the same occasion
C = required accessory-detail frame with enough garment context to show the styling relationship
```

This is not an A/B test. Generate A only, review it, and if one defect is correctable make one targeted edit to the same A without changing its content direction. B/C must never be generated as competing Hero options. They use accepted A as the edit target/session lock plus the face and full-body anchors. Keep exact garments, layers, palette, shoes, bag, jewelry, identity, body build, scene logic, and photographic character. C may use a closer crop; avoid complicated grips or making fingers the focal point.

Reference images lock identity, hair baseline, and body proportions only. They do not prescribe expression, pose, hand position, camera angle, background, lighting, or outfit.

- A: natural weight shift with physical contact or foreground overlap and one coherent scene exposure.
- B: a scene-application image showing the outfit functioning in its intended occasion. It is not the next action in a timeline.
- C: an accessory-detail image derived from A, preserving identity and exact styling while showing how the accessory supports the outfit.

Reject a set when A/B/C repeat the same centered stance, straight arms, gaze, or frozen expression.

Do not create B/C until A passes. Both are required for Carousel. Reject B/C if editing drifts wardrobe, identity, body build, or scene lighting.

## Prompt / Review Separation

Hero base prompts should be skimmable and normally 120-220 English words, ordered as intended use and dressing decision -> input-image roles -> scene and one visible action -> outfit -> photographic treatment -> composition -> short constraints. Use no more than five essential exclusions.

Keep these requirements in the review sheet instead of repeating them in the base prompt: detailed anatomy, body-part measurements, contact-shadow inspection, the 8% top margin, central 70% platform safety, exact crop tolerance, and final platform fit. A failed review may trigger one specific edit; it must not trigger a larger negative-prompt list.

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
