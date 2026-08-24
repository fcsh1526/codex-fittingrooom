# Codex Generation Handoff - 2026-W35-002-L02 / M01

Use this file to generate the carousel image candidates inside Codex.

## Reference Images

For Hero A, attach the approved references in this order: Image 1 = face/hairstyle identity; Image 2 = loose body proportion.

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png
```

For required Carousel B/C edits after Hero approval: Image 1 = accepted Carousel Hero A; Image 2 = face/hairstyle identity; Image 3 = loose body proportion.

## Output Filenames

Save generated candidates as:

```text
2026-W35-002-L02_M01_carousel_candidate_A.png
2026-W35-002-L02_M01_carousel_candidate_B.png
2026-W35-002-L02_M01_carousel_candidate_C.png
```

## Candidate Prompts

Generate and review Carousel Hero A first. After A is accepted, create B Scene Application and C Accessory Detail from the same identity and exact outfit lock. These are required publishing assets, not A/B tests.

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 用一雙深棕麂皮低跟鞋替薄棉洋裝增加換季觸感，其餘配件維持光滑材質.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at 台北安靜選物店的木質展示桌與街窗自然光, for 週末逛街／午餐. She is 站在展示桌旁拿起一只小型陶杯查看，雙腳自然錯步並留下可信鞋底接觸影. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 奶油白無袖薄棉直身中長洋裝；巧克力棕方頭麂皮低跟鞋；黑色小型光滑皮革肩背包；細版銀色耳環. Palette: 奶油白／巧克力棕／黑色／銀色. Materials: 薄棉平織／霧面麂皮／光滑皮革. Fit: 洋裝自然直身至小腿中段；鞋型方頭低跟；包款小型. Styling direction: 麂皮只出現在鞋；洋裝無厚重疊穿；包款不用麂皮. Do not add or substitute garments.

Visual proof to preserve: 奶油白薄棉洋裝與深棕霧面鞋形成清楚材質落差，麂皮焦點集中在腳下. Practical styling rule: 麂皮配件包或鞋只選一件，服裝保持透氣輕薄.

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look with a natural 50mm perspective at chest height. Use available natural light appropriate to the location, mixed with believable ambient light; realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest and unposed; polished through framing, color and material detail rather than beauty retouching.

Composition: create specifically for the v3-E cover_image frame, 1120x1050 (1.0667:1), role full_body. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No readable text, logos or watermark. Avoid studio polish and catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Create the Carousel scene-application frame for the same complete outfit, not the next moment in a continuous action. Show how the outfit works in the intended occasion through a different corner or wider environmental view of the location, or another believable setting for the same occasion. Keep the styling readable while giving the place a clear editorial role. Preserve the same woman, exact garments and styling placement, body build, season, color treatment and documentary camera character. If the location changes, rebuild its available light and contact shadows naturally instead of copying the Hero background lighting. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-E motion_crop frame, 1120x410 (2.7317:1), role horizontal_motion. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Create the Carousel accessory-detail frame. Move closer to the one accessory that carries the styling decision, such as the bag, shoes, scarf, belt or jewelry, while retaining enough garment context to understand how it works with the outfit. Use a physically simple pose; do not invent a difficult grip or make fingers the focal point. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-E detail_image frame, 1060x1010 (1.0495:1), role outfit_detail. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


## After Generation

Update:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-002\looks\2026-W35-002-L02\carousel\review_sheet.csv
```