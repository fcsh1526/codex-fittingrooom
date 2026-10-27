# Production Prompts (compatibility file)

Generate Hero A only. Do not generate B/C until the user accepts A. B/C are optional production derivatives for a required publishing sequence, not A/B tests.

---

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 不穿八月不實用的皮外套，改用深棕皮革樂福鞋與同色小包增加俐落感.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at department store fitting area, for 通勤. She is 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 挺度適中的白色棉質圓領短袖；深海軍藍高腰直筒褲；深棕方頭樂福鞋；深棕小型肩背包. Palette: 白色／深海軍藍／深棕. Materials: 棉質／薄西裝料／霧面皮革. Fit: 上衣自然合身；下身高腰直筒；鞋型方頭低跟. Styling direction: 鞋與包使用同一深棕皮革色；不增加皮外套. Do not add or substitute garments.

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
