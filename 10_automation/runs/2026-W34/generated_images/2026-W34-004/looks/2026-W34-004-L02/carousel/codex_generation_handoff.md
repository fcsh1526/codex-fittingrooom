# Codex Generation Handoff - 2026-W34-004-L02 / M05

Use this file to generate the carousel image candidates inside Codex.

## Reference Images

For Hero A, attach the approved references in this order: Image 1 = face/hairstyle identity; Image 2 = loose body proportion.

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png
```

For an optional B/C edit after Hero approval: Image 1 = accepted Hero A; Image 2 = face/hairstyle identity; Image 3 = loose body proportion.

## Output Filenames

Save generated candidates as:

```text
2026-W34-004-L02_M05_carousel_candidate_A.png
2026-W34-004-L02_M05_carousel_candidate_B.png
```

## Candidate Prompts

Generate Hero A only. Do not generate B/C until the user accepts A. The planned sequence for this look is A, B. B/C are optional production derivatives for a required publishing sequence, not A/B tests.

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 用合身棉質短袖作為日常層次，降低吊帶洋裝的睡衣感.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at 大型書店的雜誌書架與均勻室內自然光, for 週末／書店. She is 從書架抽出一本雜誌後低頭翻看，另一手扶著肩背包. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 合身奶油白棉質圓領短袖；霧面深棕直身吊帶洋裝；深棕細帶平底鞋；焦糖棕小型肩背包. Palette: 奶油白／深棕／焦糖棕. Materials: 棉質／霧面緞面／霧面皮革. Fit: 內搭合身；洋裝直身至小腿中段. Styling direction: 短袖完整貼合肩線；洋裝無蕾絲、開衩或強烈光澤. Do not add or substitute garments.

Visual proof to preserve: 淺色短袖與深色直身洋裝的層次清楚，材質讀起來像日裝而非睡衣. Practical styling rule: 同色系洋裝與鞋包保持安靜，靠棉質短袖增加日常感.

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look with a natural 50mm perspective at chest height. Use available natural light appropriate to the location, mixed with believable ambient light; realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest and unposed; polished through framing, color and material detail rather than beauty retouching.

Composition: create specifically for the v3-A cover_image frame, 1160x1190 (0.9748:1), role full_body. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No readable text, logos or watermark. Avoid studio polish and catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Create an alternate editorial view of the same complete outfit, not the next moment in a continuous action. Use either a different corner or camera angle within the same location, or a different believable setting for the same occasion. Change the pose, gaze and one natural object interaction so the frame adds a distinct way to read the outfit. Preserve the same woman, exact garments and styling placement, body build, season, color treatment and documentary camera character. If the location changes, rebuild its available light and contact shadows naturally instead of copying the Hero background lighting. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-A motion_crop frame, 980x430 (2.2791:1), role horizontal_motion. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Change only the framing and one small hand action: create a knees-up or waist-up view that clearly shows the most useful garment construction, layering, fabric and accessory details. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-A detail_image frame, 1080x1080 (1.0000:1), role outfit_detail. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


## After Generation

Update:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W34\generated_images\2026-W34-004\looks\2026-W34-004-L02\carousel\review_sheet.csv
```