# Codex Generation Handoff - 2026-W33-002 / M02

Use this file to generate the reel image candidates inside Codex.

## Reference Images

For Hero A, attach the approved references in this order: Image 1 = face/hairstyle identity; Image 2 = loose body proportion.

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_face.png
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_full.png
```

For an optional B/C edit after Hero approval: Image 1 = accepted Hero A; Image 2 = face/hairstyle identity; Image 3 = loose body proportion.

## Output Filenames

Save generated candidates as:

```text
2026-W33-002_M02_reel_candidate_A.png
2026-W33-002_M02_reel_candidate_B.png
2026-W33-002_M02_reel_candidate_C.png
```

## Candidate Prompts

Generate Hero A only. Do not generate B/C until the user accepts A. B/C are optional production derivatives for a required publishing sequence, not A/B tests.

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 咖啡廳／創意辦公室 — 縮短比例: 短版上衣或外套搭高腰下身.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at 極簡咖啡廳暖白牆面, for 咖啡廳／創意辦公室. She is just setting down a coffee cup, looking toward the window, with her other hand resting naturally near her bag. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 七分褲／褲裙／九分直筒褲. Palette: 黑／深靛藍／灰／奶油白. Materials: 西裝料／彈性棉. Fit: 高腰合身至小腿. Styling direction: 短版上衣或外套搭高腰下身；鞋面保持乾淨。. Do not add or substitute garments.

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look with a natural 50mm perspective at chest height. Use available natural light appropriate to the location, mixed with believable ambient light; realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest and unposed; polished through framing, color and material detail rather than beauty retouching.

Composition: native 9:16 vertical frame for 1080x1920 delivery. Keep the full figure, complete hairstyle and both shoes visible with enough real environment to establish the location.

No readable text, logos or watermark. Avoid studio polish and catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Change only the framing and continuation of the movement: use a small three-quarter turn or lateral step, a changed gaze, and one natural hand interaction. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: native 9:16 vertical frame for 1080x1920 delivery. Keep the full figure, complete hairstyle and both shoes visible with enough real environment to establish the location.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Change only the framing and one small hand action: create a knees-up or waist-up view that clearly shows the most useful garment construction, layering, fabric and accessory details. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: native 9:16 vertical frame for 1080x1920 delivery. Keep the full figure, complete hairstyle and both shoes visible with enough real environment to establish the location.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


## After Generation

Update:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W33\generated_images\2026-W33-002\reel\review_sheet.csv
```