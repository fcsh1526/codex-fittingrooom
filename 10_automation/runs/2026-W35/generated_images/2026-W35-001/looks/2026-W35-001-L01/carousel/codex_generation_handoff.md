# Codex Generation Handoff - 2026-W35-001-L01 / M05

Use this file to generate the carousel image candidates inside Codex.

## Reference Images

For Hero A, attach the approved references in this order: Image 1 = face/hairstyle identity; Image 2 = loose body proportion.

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png
```

For required Carousel B/C edits after Hero approval: Image 1 = accepted Carousel Hero A; Image 2 = face/hairstyle identity; Image 3 = loose body proportion.

## Output Filenames

Save generated candidates as:

```text
2026-W35-001-L01_M05_carousel_candidate_A.png
2026-W35-001-L01_M05_carousel_candidate_B.png
2026-W35-001-L01_M05_carousel_candidate_C.png
```

## Candidate Prompts

Generate and review Carousel Hero A first. After A is accepted, create B Scene Application and C Accessory Detail from the same identity and exact outfit lock. These are required publishing assets, not A/B tests.

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 用無鋪棉短版高領夾克做可脫式外層，內搭與下身保持薄身.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at 台北辦公大樓有棚入口與早晨自然側光, for 通勤／空調辦公室. She is 走向感應閘門時一手拿門禁卡，另一手自然扶住肩背包帶. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 石墨黑無鋪棉短版高領薄夾克；奶油白合身棉質短袖上衣；米灰高腰窄直筒褲；黑色方頭樂福鞋；深灰小型肩背包. Palette: 石墨黑／奶油白／米灰／深灰. Materials: 薄尼龍混紡／棉質／薄西裝料／霧面皮革. Fit: 夾克短版微寬肩；內搭合身；長褲高腰窄直筒. Styling direction: 夾克拉鍊敞開至胸口；高領自然立起；全身只保留外套一個寬鬆點. Do not add or substitute garments.

Visual proof to preserve: 短版高領落在腰線附近，合身短袖與窄直筒褲完整可見，外層讀得出無鋪棉薄度. Practical styling rule: 高領外套選薄身無鋪棉款，內搭短袖、下身窄直筒，比例只留一個寬鬆點.

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look with a natural 50mm perspective at chest height. Use available natural light appropriate to the location, mixed with believable ambient light; realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest and unposed; polished through framing, color and material detail rather than beauty retouching.

Composition: create specifically for the v3-B cover_image frame, 1240x1350 (0.9185:1), role full_body. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No readable text, logos or watermark. Avoid studio polish and catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Create the Carousel scene-application frame for the same complete outfit, not the next moment in a continuous action. Show how the outfit works in the intended occasion through a different corner or wider environmental view of the location, or another believable setting for the same occasion. Keep the styling readable while giving the place a clear editorial role. Preserve the same woman, exact garments and styling placement, body build, season, color treatment and documentary camera character. If the location changes, rebuild its available light and contact shadows naturally instead of copying the Hero background lighting. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-B motion_crop frame, 1140x560 (2.0357:1), role horizontal_motion. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Create the Carousel accessory-detail frame. Move closer to the one accessory that carries the styling decision, such as the bag, shoes, scarf, belt or jewelry, while retaining enough garment context to understand how it works with the outfit. Use a physically simple pose; do not invent a difficult grip or make fingers the focal point. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-B detail_image frame, 1180x1350 (0.8741:1), role outfit_detail. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


## After Generation

Update:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-001\looks\2026-W35-001-L01\carousel\review_sheet.csv
```