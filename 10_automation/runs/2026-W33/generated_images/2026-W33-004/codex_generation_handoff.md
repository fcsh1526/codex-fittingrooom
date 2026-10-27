# Codex Generation Handoff - 2026-W33-004 / M03

Use this file to generate the carousel image candidates inside Codex.

## Reference Images

Attach both approved reference start images to the image-generation request:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png
```

## Output Filenames

Save generated candidates as:

```text
2026-W33-004_M03_candidate_A.png
2026-W33-004_M03_candidate_B.png
2026-W33-004_M03_candidate_C.png
```

## Candidate Prompts

Asset A: integrated-scene Hero and session lock

Required image inputs:
- Face identity anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png
- Full-body proportion anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png
- Session rule: Accepted Hero A is created in this step.

Create a photorealistic vertical lifestyle fashion photograph for Mira. Internal model M03 is production metadata only; never render model IDs, names, captions, logos, or watermarks.

Identity and anatomy:
Preserve the exact facial identity and core hairstyle from the face anchor. Match the full-body anchor's realistic head size, shoulder width, torso length, waist and hip placement, knee height, leg-to-torso balance, arm length, and hand size. Use plausible adult proportions rather than runway or nine-head elongation. The reference pose, expression, studio background, and reference outfit are not part of the identity.

Trend and outfit:
- Trend: 復古腰帶與絲巾
- Garments: 寬皮帶／絲巾腰帶／復古肩包
- Palette: 焦糖棕／酒紅／印花藍／黑
- Fabric: 皮革／絲／仿絲
- Fit: 腰間固定、衣服簡潔
- Occasion: 約會／旅行／週末
- Styling: 全身最多一個花紋；腰帶或絲巾負責造型記憶點。

Scene and camera:
Use a believable daily-life setting that supports the occasion. Scene hint: 城市騎樓與柔和早晨光線. Treat person and environment as one exposure photographed with a full-frame mirrorless camera and a 50mm prime lens near chest height with a level optical axis. Daylight starting settings: f/4, 1/250 s, ISO 200, white balance 5200 K; adjust only when the scene physically requires it, and state the final settings explicitly. Keep camera body, focal length, height, white balance, and rendering logic locked across A/B/C. Never substitute a smartphone, computational portrait mode, DSLR simulation, low angle, or wide-angle perspective unless the user explicitly overrides the camera standard. One visible or inferable light source must affect face, hair, garments, hands, shoes, foreground, floor, and background consistently. Include ambient color spill, natural contact shadows, shared depth of field, restrained grain, slight optical softness, natural skin texture, flyaway hairs, and small fabric wrinkles.

Canva frame target:
- Delivery surface: Carousel
- Assigned master: v3-E / Mira Template Master v3 - E Cross-Boundary Weekend Air
- Slot: cover_image
- Exact frame: 1120 x 1050 px
- Required width:height ratio: 1.0667:1
- Composition role: full_body
Compose specifically for this frame ratio; do not reuse one narrow portrait composition for all A/B/C slots. Keep the entire hairstyle and head below an 8% top safe margin whenever the head appears. Keep the face and outfit focus inside the central 70%. For full-body views, leave real scene space above the hair and below the feet. No borders or letterboxing. The untouched Canva frame fill must remain publishable without manual focal-point adjustment. The 15% crop ceiling applies only during Carousel normalization.

Asset direction:
Show the full figure with surrounding environment. Use a relaxed asymmetric stance and one physically believable interaction with a foreground or scene object, including visible contact pressure and contact shadow.

Age rendering:
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin is smooth and well-maintained.

Avoid:
tiny head, fashion-elongated body, raised crotch, stretched legs, low or wide camera angle, mannequin posture, floating hands or feet, independent subject lighting, cutout edges, halo, plastic skin, plastic fabric, garment drift, celebrity likeness, sexualized or childlike styling, text, logos, and watermark.


---

Asset B: movement variation edited from the accepted Hero A

Required image inputs:
- Face identity anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png
- Full-body proportion anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png
- Session rule: Attach accepted Hero A as the edit target/session lock in addition to both model anchors. Do not generate an independent reinterpretation.

Create a photorealistic vertical lifestyle fashion photograph for Mira. Internal model M03 is production metadata only; never render model IDs, names, captions, logos, or watermarks.

Identity and anatomy:
Preserve the exact facial identity and core hairstyle from the face anchor. Match the full-body anchor's realistic head size, shoulder width, torso length, waist and hip placement, knee height, leg-to-torso balance, arm length, and hand size. Use plausible adult proportions rather than runway or nine-head elongation. The reference pose, expression, studio background, and reference outfit are not part of the identity.

Trend and outfit:
- Trend: 復古腰帶與絲巾
- Garments: 寬皮帶／絲巾腰帶／復古肩包
- Palette: 焦糖棕／酒紅／印花藍／黑
- Fabric: 皮革／絲／仿絲
- Fit: 腰間固定、衣服簡潔
- Occasion: 約會／旅行／週末
- Styling: 全身最多一個花紋；腰帶或絲巾負責造型記憶點。

Scene and camera:
Use a believable daily-life setting that supports the occasion. Scene hint: 城市騎樓與柔和早晨光線. Treat person and environment as one exposure photographed with a full-frame mirrorless camera and a 50mm prime lens near chest height with a level optical axis. Daylight starting settings: f/4, 1/250 s, ISO 200, white balance 5200 K; adjust only when the scene physically requires it, and state the final settings explicitly. Keep camera body, focal length, height, white balance, and rendering logic locked across A/B/C. Never substitute a smartphone, computational portrait mode, DSLR simulation, low angle, or wide-angle perspective unless the user explicitly overrides the camera standard. One visible or inferable light source must affect face, hair, garments, hands, shoes, foreground, floor, and background consistently. Include ambient color spill, natural contact shadows, shared depth of field, restrained grain, slight optical softness, natural skin texture, flyaway hairs, and small fabric wrinkles.

Canva frame target:
- Delivery surface: Carousel
- Assigned master: v3-E / Mira Template Master v3 - E Cross-Boundary Weekend Air
- Slot: motion_crop
- Exact frame: 1120 x 410 px
- Required width:height ratio: 2.7317:1
- Composition role: horizontal_motion
Compose specifically for this frame ratio; do not reuse one narrow portrait composition for all A/B/C slots. Keep the entire hairstyle and head below an 8% top safe margin whenever the head appears. Keep the face and outfit focus inside the central 70%. For full-body views, leave real scene space above the hair and below the feet. No borders or letterboxing. The untouched Canva frame fill must remain publishable without manual focal-point adjustment. The 15% crop ceiling applies only during Carousel normalization.

Asset direction:
Edit accepted Hero A into a candid three-quarter turn or small lateral movement. Change gaze and one hand action, but keep the same scene, outfit construction, identity, body build, light source, and camera treatment. Use a deliberately horizontal environmental composition with a readable face and torso/outfit gesture; do not squeeze a full standing figure into the shallow frame.

Age rendering:
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin is smooth and well-maintained.

Avoid:
tiny head, fashion-elongated body, raised crotch, stretched legs, low or wide camera angle, mannequin posture, floating hands or feet, independent subject lighting, cutout edges, halo, plastic skin, plastic fabric, garment drift, celebrity likeness, sexualized or childlike styling, text, logos, and watermark.


---

Asset C: outfit-detail variation edited from the accepted Hero A

Required image inputs:
- Face identity anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png
- Full-body proportion anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png
- Session rule: Attach accepted Hero A as the edit target/session lock in addition to both model anchors. Do not generate an independent reinterpretation.

Create a photorealistic vertical lifestyle fashion photograph for Mira. Internal model M03 is production metadata only; never render model IDs, names, captions, logos, or watermarks.

Identity and anatomy:
Preserve the exact facial identity and core hairstyle from the face anchor. Match the full-body anchor's realistic head size, shoulder width, torso length, waist and hip placement, knee height, leg-to-torso balance, arm length, and hand size. Use plausible adult proportions rather than runway or nine-head elongation. The reference pose, expression, studio background, and reference outfit are not part of the identity.

Trend and outfit:
- Trend: 復古腰帶與絲巾
- Garments: 寬皮帶／絲巾腰帶／復古肩包
- Palette: 焦糖棕／酒紅／印花藍／黑
- Fabric: 皮革／絲／仿絲
- Fit: 腰間固定、衣服簡潔
- Occasion: 約會／旅行／週末
- Styling: 全身最多一個花紋；腰帶或絲巾負責造型記憶點。

Scene and camera:
Use a believable daily-life setting that supports the occasion. Scene hint: 城市騎樓與柔和早晨光線. Treat person and environment as one exposure photographed with a full-frame mirrorless camera and a 50mm prime lens near chest height with a level optical axis. Daylight starting settings: f/4, 1/250 s, ISO 200, white balance 5200 K; adjust only when the scene physically requires it, and state the final settings explicitly. Keep camera body, focal length, height, white balance, and rendering logic locked across A/B/C. Never substitute a smartphone, computational portrait mode, DSLR simulation, low angle, or wide-angle perspective unless the user explicitly overrides the camera standard. One visible or inferable light source must affect face, hair, garments, hands, shoes, foreground, floor, and background consistently. Include ambient color spill, natural contact shadows, shared depth of field, restrained grain, slight optical softness, natural skin texture, flyaway hairs, and small fabric wrinkles.

Canva frame target:
- Delivery surface: Carousel
- Assigned master: v3-E / Mira Template Master v3 - E Cross-Boundary Weekend Air
- Slot: detail_image
- Exact frame: 1060 x 1010 px
- Required width:height ratio: 1.0495:1
- Composition role: outfit_detail
Compose specifically for this frame ratio; do not reuse one narrow portrait composition for all A/B/C slots. Keep the entire hairstyle and head below an 8% top safe margin whenever the head appears. Keep the face and outfit focus inside the central 70%. For full-body views, leave real scene space above the hair and below the feet. No borders or letterboxing. The untouched Canva frame fill must remain publishable without manual focal-point adjustment. The 15% crop ceiling applies only during Carousel normalization.

Asset direction:
Edit accepted Hero A into a knees-up or waist-up outfit-detail composition. Preserve the exact neckline, layers, sleeves, fabric behavior, accessories, identity, scene, and lighting treatment.

Age rendering:
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin is smooth and well-maintained.

Avoid:
tiny head, fashion-elongated body, raised crotch, stretched legs, low or wide camera angle, mannequin posture, floating hands or feet, independent subject lighting, cutout edges, halo, plastic skin, plastic fabric, garment drift, celebrity likeness, sexualized or childlike styling, text, logos, and watermark.


## After Generation

Update:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W33\generated_images\2026-W33-004\review_sheet.csv
```