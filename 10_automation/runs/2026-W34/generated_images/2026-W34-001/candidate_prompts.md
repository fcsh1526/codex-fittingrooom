# Production Prompts (compatibility file)

Generate Hero A only. Do not generate B/C until the user accepts A. B/C are optional production derivatives for a required publishing sequence, not A/B tests.

---

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 選寬版落肩牛津襯衫，袖口捲至手肘，下擺自然放在直筒牛仔褲外.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at Taipei office lobby with soft daylight, for 通勤／上課. She is 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 海軍藍寬版純棉牛津襯衫；淺藍直筒牛仔褲；白色帆布鞋；深棕帆布側背包. Palette: 海軍藍／淺藍／白色／深棕. Materials: 純棉牛津布／丹寧／帆布. Fit: 上衣寬版落肩；下身高腰直筒. Styling direction: 襯衫袖口捲至手肘且下擺不紮；不加領帶、徽章或百褶裙. Do not add or substitute garments.

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
