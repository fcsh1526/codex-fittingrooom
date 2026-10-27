# Codex Generation Handoff - 2026-W34-005-L01 / M01

Use this file to generate the carousel image candidates inside Codex.

## Reference Images

For Hero A, attach the approved references in this order: Image 1 = face/hairstyle identity; Image 2 = loose body proportion.

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png
```

For an optional B/C edit after Hero approval: Image 1 = accepted Hero A; Image 2 = face/hairstyle identity; Image 3 = loose body proportion.

## Output Filenames

Save generated candidates as:

```text
2026-W34-005-L01_M01_carousel_candidate_A.png
2026-W34-005-L01_M01_carousel_candidate_C.png
```

## Candidate Prompts

Generate Hero A only. Do not generate B/C until the user accepts A. The planned sequence for this look is A, C. B/C are optional production derivatives for a required publishing sequence, not A/B tests.

Use case: photorealistic-natural.

Asset: Hero A for Mira, a daily-outfit fashion magazine. It should make one dressing decision immediately readable: 把窄版印花絲巾綁在包帶根部，衣服只使用素色.

Input images: Image 1 is the model's identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference's studio pose, expression, lighting, background or clothes.

A candid real photograph of the same adult East Asian woman at 安靜文具店的木質展示長桌與窗邊自然光, for 通勤／採買. She is 從展示桌拿起托特包，包帶絲巾自然垂落且手指接觸合理. Show one clear action and natural hand-object interaction.

Outfit, immediately readable: 奶油白無袖棉質上衣；卡其高腰直筒褲；淺棕樂福鞋；深棕小型托特包；藍棕印花窄版絲巾綁於包帶. Palette: 奶油白／卡其／淺棕／深棕／藍色. Materials: 棉質／薄西裝料／霧面皮革／輕薄仿絲. Fit: 上衣自然合身；長褲高腰直筒；絲巾窄版. Styling direction: 絲巾只綁包帶並保留一個藍色重點；全身不加第二種印花. Do not add or substitute garments.

Visual proof to preserve: 素色穿搭、深棕包款與包帶上的單條窄版絲巾同時可見. Practical styling rule: 絲巾主色呼應鞋或包，全身不再加入第二種印花.

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


## After Generation

Update:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W34\generated_images\2026-W34-005\looks\2026-W34-005-L01\carousel\review_sheet.csv
```