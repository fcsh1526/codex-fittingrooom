# Production Prompts (compatibility file)

Generate Hero A only. Do not generate B/C until the user accepts A. B/C are optional production derivatives for a required publishing sequence, not A/B tests.

---

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 選霧面直身吊帶洋裝，裡面加一件合身白色短袖，改成白天可以直接穿的層次.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at MRT-adjacent weekday walkway, for 日常外出／早午餐. She is 剛放下咖啡杯，視線自然看向窗外，另一手停在隨身包旁. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 合身白色棉質圓領短袖；霧面黑色直身吊帶洋裝；黑色平底鞋；酒紅小型肩背包. Palette: 黑色／白色／酒紅. Materials: 棉質／霧面緞面／霧面皮革. Fit: 內搭合身；洋裝直身至膝下. Styling direction: 白色短袖穿在吊帶洋裝內；洋裝避免蕾絲與強烈光澤. Do not add or substitute garments.

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look with a natural 50mm perspective at chest height. Use available natural light appropriate to the location, mixed with believable ambient light; realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest and unposed; polished through framing, color and material detail rather than beauty retouching.

Composition: create specifically for the v3-A cover_image frame, 1160x1190 (0.9748:1), role full_body. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No readable text, logos or watermark. Avoid studio polish and catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Change only the framing and continuation of the movement: use a small three-quarter turn or lateral step, a changed gaze, and one natural hand interaction. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-A motion_crop frame, 980x430 (2.2791:1), role horizontal_motion. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Change only the framing and one small hand action: create a knees-up or waist-up view that clearly shows the most useful garment construction, layering, fabric and accessory details. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-A detail_image frame, 1080x1080 (1.0000:1), role outfit_detail. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.
