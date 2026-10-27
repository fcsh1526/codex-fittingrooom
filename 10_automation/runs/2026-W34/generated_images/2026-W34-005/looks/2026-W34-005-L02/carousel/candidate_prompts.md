# Production Prompts (compatibility file)

Generate Hero A only. Do not generate B/C until the user accepts A. The planned sequence for this look is A, C. B/C are optional production derivatives for a required publishing sequence, not A/B tests.

---

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 把窄版印花絲巾綁在包帶根部，衣服只使用素色.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at 街區烘焙店的外帶櫃檯與柔和早晨側光, for 週末／早午餐. She is 酒紅肩背包自然背在身側，奶油白與深藍絲巾從包帶根部垂下；人物站在外帶窗口旁，一手自然輕放窗台，另一手放鬆垂下，視線看向街道. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 黑色無袖棉質上衣；象牙白高腰直筒褲；酒紅尖頭平底鞋；酒紅小型肩背包；奶油白與深藍窄版印花絲巾綁於包帶. Palette: 黑色／象牙白／酒紅／奶油白／深藍. Materials: 棉質／薄西裝料／霧面皮革／輕薄仿絲. Fit: 上衣自然合身；長褲高腰直筒；絲巾窄版. Styling direction: 絲巾只綁包帶；酒紅鞋包同色；衣服維持黑白. Do not add or substitute garments.

Visual proof to preserve: 黑白服裝與酒紅鞋包形成清楚色塊，絲巾只作為包帶細節. Practical styling rule: 服裝先保持兩個素色，再用同色鞋包與一條窄版絲巾補充層次.

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look with a natural 50mm perspective at chest height. Use available natural light appropriate to the location, mixed with believable ambient light; realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest and unposed; polished through framing, color and material detail rather than beauty retouching.

Composition: create specifically for the v3-B cover_image frame, 1240x1350 (0.9185:1), role full_body. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No readable text, logos or watermark. Avoid studio polish and catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Create an alternate editorial view of the same complete outfit, not the next moment in a continuous action. Use either a different corner or camera angle within the same location, or a different believable setting for the same occasion. Change the pose, gaze and one natural object interaction so the frame adds a distinct way to read the outfit. Preserve the same woman, exact garments and styling placement, body build, season, color treatment and documentary camera character. If the location changes, rebuild its available light and contact shadows naturally instead of copying the Hero background lighting. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-B motion_crop frame, 1140x560 (2.0357:1), role horizontal_motion. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Change only the framing and one small hand action: create a knees-up or waist-up view that clearly shows the most useful garment construction, layering, fabric and accessory details. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-B detail_image frame, 1180x1350 (0.8741:1), role outfit_detail. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.
