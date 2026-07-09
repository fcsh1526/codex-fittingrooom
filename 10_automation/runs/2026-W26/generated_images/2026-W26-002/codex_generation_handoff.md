# Codex Generation Handoff - 2026-W26-002 / M02 v3

Use this file to regenerate W26-002 inside Codex with the approved M02 v3 model anchors.

## Do Not Use

Do not use these old assets or Canva draft:

```text
2026-W26-002_M02_candidate_A_v2.png
2026-W26-002_M02_candidate_B_v2.png
2026-W26-002_M02_candidate_C_v2.png
https://www.canva.com/d/BADXM4PGvSs2Rlh
```

Reason: these were generated before the approved M02 v3 references and use the old model identity.

## Reference Images

Use both approved M02 v3 references as identity anchors:

```text
02_brand/reference_models/M02_start_v3_face.png
02_brand/reference_models/M02_start_v3_full.png
```

## Naming

Save the Codex-generated outputs as:

```text
2026-W26-002_M02_v3_candidate_A.png
2026-W26-002_M02_v3_candidate_B.png
2026-W26-002_M02_v3_candidate_C.png
```

## Prompt A - Full-Body Cover

```text
Create a realistic vertical 4:5 lifestyle fashion image for an AI fashion magazine.

Use the M02 v3 face and full-body references as strict identity anchors. Keep the same face structure, hairstyle identity, apparent age range, and healthy slim-to-average body proportions. Do not use any previous W26-002 generated images as identity reference.

Subject: East Asian woman with a youthful late-20s adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, warm fair skin with visible human texture, approachable composed expression.

Outfit: black and white polka dot midi dress, satin or light chiffon texture, straight or soft A-line fit, subtle red accent such as a slim belt or lip color, simple black Mary Jane flats or low heels, small black shoulder bag. The full outfit must be readable in one second.

Scene: quiet bookstore street or cafe-window sidewalk, realistic daily-life setting, soft natural light, wearable weekend date outfit mood.

Avoid: old M02 identity drift, visible logos, image text, watermark, luxury hotel, runway pose, celebrity likeness, childlike styling, plastic skin, supermodel proportions.
```

## Prompt B - Motion Crop

```text
Create a realistic vertical 4:5 lifestyle fashion image using the same M02 v3 identity anchors.

Keep the same face structure, hairstyle identity, apparent age range, and body proportions from the references. Do not use old W26-002 images as references.

Outfit: black and white polka dot dress, subtle red accent, simple black shoes, small black shoulder bag. Pose should feel like a natural street-style walking moment, with the dress movement visible and the face still consistent with M02 v3.

Scene: bookstore street, quiet shopping street, or cafe window. Keep the image useful for a later horizontal motion crop.

Avoid: exaggerated pose, runway mood, supermodel distance, visible logos, text, watermark, luxury ad feeling, plastic skin, old-model face drift.
```

## Prompt C - Detail-Friendly Closing Frame

```text
Create a realistic vertical 4:5 lifestyle fashion image using the same M02 v3 identity anchors.

Keep the same face structure, hairstyle identity, apparent age range, and body proportions from the references. Do not use old W26-002 images as references.

Outfit: black and white polka dot dress with readable fabric texture, subtle red accent, black shoes, small shoulder bag. Compose slightly closer than Candidate A but keep the outfit readable from head to shoes. The image should work as the closing detail frame for a 3-slide carousel.

Scene: cafe-window sidewalk or quiet bookstore street. Realistic skin texture and natural light.

Avoid: logos, image text, watermark, luxury ad feeling, plastic skin, cropped head, cropped feet, old-model face drift.
```

## Fast Review

Reject a candidate if any of these are true:

```text
face does not match M02 v3
hair identity changed too much
body proportions drifted
outfit is unclear in 1 second
head or feet are badly cropped
hands/feet are visibly broken
image contains text, watermark, or logo
style feels like runway, luxury ad, or celebrity photo
```

After generation, update:

```text
10_automation/runs/2026-W26/generated_images/2026-W26-002/review_sheet.csv
```
