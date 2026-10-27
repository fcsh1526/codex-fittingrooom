# Codex Generation Handoff - 2026-W34-002 / M04

Use this file to generate the carousel image candidates inside Codex.

## Reference Images

For Hero A, attach the approved references in this order: Image 1 = face/hairstyle identity; Image 2 = loose body proportion.

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_face.png
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_full.png
```

For an optional B/C edit after Hero approval: Image 1 = accepted Hero A; Image 2 = face/hairstyle identity; Image 3 = loose body proportion.

## Output Filenames

Save generated candidates as:

```text
2026-W34-002_M04_candidate_A.png
2026-W34-002_M04_candidate_B.png
2026-W34-002_M04_candidate_C.png
```

## Candidate Prompts

Generate Hero A only. Do not generate B/C until the user accepts A. B/C are optional production derivatives for a required publishing sequence, not A/B tests.

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 改用薄款無內裡的微鬆西裝外套，內層只留一件素色無袖上衣.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at simple studio wall with neutral shadows, for 上班／簡報. She is 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 炭灰薄款無內裡微鬆西裝外套；黑色素面無袖上衣；炭灰直筒西裝褲；黑色尖頭平底鞋；深棕小型肩背包；細版金屬耳環. Palette: 炭灰／黑色／深棕／銀色. Materials: 薄西裝料／棉質／霧面皮革. Fit: 外套微鬆有肩線；內搭合身；下身直筒. Styling direction: 外套敞開穿著；內搭與配件維持簡單. Do not add or substitute garments.

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look with a natural 50mm perspective at chest height. Use available natural light appropriate to the location, mixed with believable ambient light; realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest and unposed; polished through framing, color and material detail rather than beauty retouching.

Composition: create specifically for the v3-B cover_image frame, 1240x1350 (0.9185:1), role full_body. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No readable text, logos or watermark. Avoid studio polish and catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Change only the framing and continuation of the movement: use a small three-quarter turn or lateral step, a changed gaze, and one natural hand interaction. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-B motion_crop frame, 1140x560 (2.0357:1), role horizontal_motion. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Change only the framing and one small hand action: create a knees-up or waist-up view that clearly shows the most useful garment construction, layering, fabric and accessory details. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-B detail_image frame, 1180x1350 (0.8741:1), role outfit_detail. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


## After Generation

Update:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W34\generated_images\2026-W34-002\review_sheet.csv
```