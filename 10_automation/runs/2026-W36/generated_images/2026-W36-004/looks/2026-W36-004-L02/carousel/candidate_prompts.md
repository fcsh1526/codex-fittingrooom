# Production Prompts (compatibility file)

Generate and review Carousel Hero A first. After A is accepted, create B Scene Application and C Accessory Detail from the same identity and exact outfit lock. These are required publishing assets, not A/B tests.

---

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 奶油白短袖上衣配酒紅斜裁緞面中長裙，裙身有垂墜，其他單品不再增加光澤.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at 藝文中心演出廳外的票務長廊與均勻室內光, for 旅行晚餐／藝文活動. She is 從自助取票機取出紙票後沿長廊走向入口，肩背包貼近身側. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 奶油白合身短袖細針織上衣；酒紅高腰斜裁緞面中長裙；深棕方頭低跟鞋；深棕小型肩背包；小型金色耳釘. Palette: 奶油白／酒紅／深棕／金色. Materials: 細針織／霧光緞面／霧面皮革. Fit: 上衣合身落腰；裙身高腰斜裁貼身後自然展開；鞋型低跟方頭. Styling direction: 上衣完整收進裙腰；不加腰帶與項鍊；鞋包同為深棕. Do not add or substitute garments.

Visual proof to preserve: 奶油白上衣保持霧面，酒紅裙身的斜裁線與自然垂墜成為唯一視覺重點. Practical styling rule: 有光澤的緞面裙只配一件霧面素色上衣，配件維持深色小尺寸.

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look with a natural 50mm perspective at chest height. Use available natural light appropriate to the location, mixed with believable ambient light; realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest and unposed; polished through framing, color and material detail rather than beauty retouching.

Composition: create specifically for the v3-A cover_image frame, 1160x1190 (0.9748:1), role full_body. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No readable text, logos or watermark. Avoid studio polish and catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Create the Carousel scene-application frame for the same complete outfit, not the next moment in a continuous action. Show how the outfit works in the intended occasion through a different corner or wider environmental view of the location, or another believable setting for the same occasion. Keep the styling readable while giving the place a clear editorial role. Preserve the same woman, exact garments and styling placement, body build, season, color treatment and documentary camera character. If the location changes, rebuild its available light and contact shadows naturally instead of copying the Hero background lighting. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-A motion_crop frame, 980x430 (2.2791:1), role horizontal_motion. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.


---

Edit the accepted Hero A; do not generate an independent reinterpretation.

Input roles: Image 1 is the accepted Hero A and is the scene, outfit and photographic anchor. Image 2 preserves identity and hairstyle. Image 3 is a loose body-proportion reference.

Create the Carousel accessory-detail frame. Move closer to the one accessory that carries the styling decision, such as the bag, shoes, scarf, belt or jewelry, while retaining enough garment context to understand how it works with the outfit. Use a physically simple pose; do not invent a difficult grip or make fingers the focal point. Preserve the same woman, exact garments and styling placement, location, season, natural light, color treatment and documentary realism. Keep fabric drape, folds, occlusion and shadows physically integrated rather than pasted on.

Composition: create specifically for the v3-A detail_image frame, 1080x1080 (1.0000:1), role outfit_detail. Keep the intended face, outfit detail and environmental context readable without relying on a later hard crop.

No new garments or accessories, readable text, logos, watermark, studio polish or catalog posing.
