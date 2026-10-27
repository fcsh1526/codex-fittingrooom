# W30-004 Continuous Video Motion Brief v1

Status: motion concept for approval; no video generated and nothing published.

## Purpose

Test whether a real continuous lifestyle action can reduce immediate skipping compared with the previous static-image Reel. This is not a slideshow, crop animation, push-in, pan, or image morph.

## Inputs

- Start-frame and identity/session reference: `2026-W30-004_M05_reel_accepted_A.png`
- End-motion reference only: `2026-W30-004_M05_reel_accepted_B.png`
- Delivery: 1080 x 1920, 9:16
- Duration: 6.0 seconds
- Audio and title are added later; the generated video contains no text

## One continuous shot

The camera remains locked in the same position for the entire shot. No cuts.

| Time | Physical action |
|---|---|
| 0.00-1.20 s | Start with visible motion immediately. She finishes lowering the ceramic coffee cup onto its saucer. Fingers release the handle naturally after contact; the cup and saucer do not slide or deform. |
| 1.20-2.80 s | She pauses and looks through the window, with one natural blink, a small breath, and minimal shoulder and hair movement. She never looks into the camera. |
| 2.80-4.30 s | Her gaze drops toward the hanging handbag. Her free hand reaches down and closes naturally around the existing strap while her torso leans forward slightly. |
| 4.30-6.00 s | She begins rising from the stool and lifts the handbag strap toward her shoulder. One hand briefly touches the counter for balance. End during the believable half-rising movement, close to accepted B rather than fully walking away. |

## Motion behavior

- Movement is quiet, ordinary, and physically weighted—not fashion posing.
- Face, hands, hair, shirt, trousers, bag, cup, saucer, stool, and counter remain temporally consistent.
- Hair and loose shirt fabric react subtly to body movement; no wind effect.
- Keep both legs uncrossed. Feet remain grounded and move only as required to begin standing.
- Preserve realistic hand contact with the cup, counter, and bag strap.
- Keep the face readable and stable; no facial redesign between frames.
- No dramatic steam, liquid splash, exaggerated smile, or theatrical reaction.

## Locked visual treatment

- Same woman, youthful-adult appearance, facial identity, body build, and shoulder-length dark-brown bob
- Same lightweight white cotton shirt, rolled sleeves, chocolate-brown trousers, ivory loafers, dark-brown leather bag, and minimal jewelry
- Same used neighborhood café, street-facing window, cup and saucer, stool, counter wear, window marks, and summer exterior
- Same unretouched documentary-magazine look
- Simulated full-frame mirrorless camera, 50 mm prime lens, chest-height level optical axis
- `f/4`, `1/250 s`, `ISO 200`, white balance `5200 K`
- Same neutral window daylight, skin tone, depth of field, fine grain, and optical softness

## Video-generation prompt

```text
Animate the supplied accepted café image as one continuous six-second documentary fashion shot. The camera is completely locked: no pan, tilt, zoom, push-in, reframing, shake, cut, transition, or time jump.

Visible motion begins on the first frame. The woman naturally finishes lowering the existing ceramic coffee cup onto its existing saucer and releases the handle after real contact. She pauses, looks quietly through the window, blinks once, and breathes subtly. Her gaze then drops toward the existing dark-brown handbag hanging from the stool. Her free hand reaches down, takes the existing strap, and she begins rising naturally while her other hand briefly touches the counter for balance. End halfway through standing, with the strap moving toward her shoulder. She never looks at the camera.

Preserve the exact woman, face, hairstyle, body proportions, white rolled-sleeve cotton shirt, chocolate-brown trousers, ivory loafers, dark-brown bag, jewelry, cup, saucer, stool, worn counter, window, café equipment, summer exterior, lighting, exposure, depth of field, grain, and unretouched documentary texture from the source image. Hands and fingers remain anatomically correct and maintain physical contact. Legs stay uncrossed and feet stay grounded. Hair and shirt move only slightly in response to her body.

Simulate the same full-frame mirrorless camera and 50 mm prime lens at chest height, f/4, 1/250 s, ISO 200, white balance 5200 K. Maintain one neutral window-light color across face, neck, and hands.

No image morphing, identity drift, facial warping, beauty smoothing, plastic skin, extra fingers, fused hands, floating cup, sliding saucer, changing bag, changing clothing, liquid splash, exaggerated steam, background movement, new people, added objects, text, logos, or watermark.
```

## Opening title after video approval

Add later in editing, not inside video generation:

```text
上班前的
咖啡時光
```

- Visible from 0.00 to 1.45 seconds
- Upper-left window area
- No entrance animation

## Approval gate

Do not generate until the user approves the action sequence, especially the transition from cup placement to reaching for the bag and beginning to stand.
