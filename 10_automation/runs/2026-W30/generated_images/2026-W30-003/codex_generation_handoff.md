# Codex Generation Handoff - 2026-W30-003 / M01

Use this file to generate the carousel image candidates inside Codex.

## Reference Images

Attach both approved reference start images to the image-generation request:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png
```

## Output Filenames

Save generated candidates as:

```text
2026-W30-003_M01_candidate_A.png
2026-W30-003_M01_candidate_B.png
2026-W30-003_M01_candidate_C.png
```

## Candidate Prompts

Asset A: integrated-scene Hero and session lock

Required image inputs:
- Face identity anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png
- Full-body proportion anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png
- Session rule: Accepted Hero A is created in this step.

Create a photorealistic vertical lifestyle fashion photograph for Mira. Internal model M01 is production metadata only; never render model IDs, names, captions, logos, or watermarks.

Identity and anatomy:
Preserve the exact facial identity and core hairstyle from the face anchor. Match the full-body anchor's realistic head size, shoulder width, torso length, waist and hip placement, knee height, leg-to-torso balance, arm length, and hand size. Use plausible adult proportions rather than runway or nine-head elongation. The reference pose, expression, studio background, and reference outfit are not part of the identity.

Trend and outfit:
- Trend: 漁夫涼鞋續熱
- Garments: 漁夫涼鞋＋寬褲
- Palette: 黑/棕/奶油白
- Fabric: 皮革編織/橡膠底
- Fit: 鞋款主導、上身簡潔
- Occasion: 旅行與戶外
- Styling: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。

Scene and camera:
Use a believable daily-life setting that supports the occasion. Scene hint: 乾淨的室內灰白牆面與柔光窗邊. Treat person and environment as one exposure captured in-camera with a normal 50mm full-frame-equivalent lens near chest height and a level optical axis. One visible or inferable light source must affect face, hair, garments, hands, shoes, foreground, floor, and background consistently. Include ambient color spill, natural contact shadows, shared depth of field, restrained grain, slight optical softness, natural skin texture, flyaway hairs, and small fabric wrinkles.

Canva frame target:
- Assigned master: v3-A / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- Slot: cover_image
- Exact frame: 1160 x 1190 px
- Required width:height ratio: 0.9748:1
- Composition role: full_body
Compose specifically for this frame ratio; do not reuse one narrow portrait composition for all A/B/C slots. Keep the entire hairstyle and head below an 8% top safe margin whenever the head appears. Keep the face and outfit focus inside the central 70%. For full-body views, leave real scene space above the hair and below the feet. No borders or letterboxing. The untouched Canva frame fill must remain publishable without manual focal-point adjustment.

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
- Face identity anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png
- Full-body proportion anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png
- Session rule: Attach accepted Hero A as the edit target/session lock in addition to both model anchors. Do not generate an independent reinterpretation.

Create a photorealistic vertical lifestyle fashion photograph for Mira. Internal model M01 is production metadata only; never render model IDs, names, captions, logos, or watermarks.

Identity and anatomy:
Preserve the exact facial identity and core hairstyle from the face anchor. Match the full-body anchor's realistic head size, shoulder width, torso length, waist and hip placement, knee height, leg-to-torso balance, arm length, and hand size. Use plausible adult proportions rather than runway or nine-head elongation. The reference pose, expression, studio background, and reference outfit are not part of the identity.

Trend and outfit:
- Trend: 漁夫涼鞋續熱
- Garments: 漁夫涼鞋＋寬褲
- Palette: 黑/棕/奶油白
- Fabric: 皮革編織/橡膠底
- Fit: 鞋款主導、上身簡潔
- Occasion: 旅行與戶外
- Styling: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。

Scene and camera:
Use a believable daily-life setting that supports the occasion. Scene hint: 乾淨的室內灰白牆面與柔光窗邊. Treat person and environment as one exposure captured in-camera with a normal 50mm full-frame-equivalent lens near chest height and a level optical axis. One visible or inferable light source must affect face, hair, garments, hands, shoes, foreground, floor, and background consistently. Include ambient color spill, natural contact shadows, shared depth of field, restrained grain, slight optical softness, natural skin texture, flyaway hairs, and small fabric wrinkles.

Canva frame target:
- Assigned master: v3-A / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- Slot: motion_crop
- Exact frame: 980 x 430 px
- Required width:height ratio: 2.2791:1
- Composition role: horizontal_motion
Compose specifically for this frame ratio; do not reuse one narrow portrait composition for all A/B/C slots. Keep the entire hairstyle and head below an 8% top safe margin whenever the head appears. Keep the face and outfit focus inside the central 70%. For full-body views, leave real scene space above the hair and below the feet. No borders or letterboxing. The untouched Canva frame fill must remain publishable without manual focal-point adjustment.

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
- Face identity anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png
- Full-body proportion anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png
- Session rule: Attach accepted Hero A as the edit target/session lock in addition to both model anchors. Do not generate an independent reinterpretation.

Create a photorealistic vertical lifestyle fashion photograph for Mira. Internal model M01 is production metadata only; never render model IDs, names, captions, logos, or watermarks.

Identity and anatomy:
Preserve the exact facial identity and core hairstyle from the face anchor. Match the full-body anchor's realistic head size, shoulder width, torso length, waist and hip placement, knee height, leg-to-torso balance, arm length, and hand size. Use plausible adult proportions rather than runway or nine-head elongation. The reference pose, expression, studio background, and reference outfit are not part of the identity.

Trend and outfit:
- Trend: 漁夫涼鞋續熱
- Garments: 漁夫涼鞋＋寬褲
- Palette: 黑/棕/奶油白
- Fabric: 皮革編織/橡膠底
- Fit: 鞋款主導、上身簡潔
- Occasion: 旅行與戶外
- Styling: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。

Scene and camera:
Use a believable daily-life setting that supports the occasion. Scene hint: 乾淨的室內灰白牆面與柔光窗邊. Treat person and environment as one exposure captured in-camera with a normal 50mm full-frame-equivalent lens near chest height and a level optical axis. One visible or inferable light source must affect face, hair, garments, hands, shoes, foreground, floor, and background consistently. Include ambient color spill, natural contact shadows, shared depth of field, restrained grain, slight optical softness, natural skin texture, flyaway hairs, and small fabric wrinkles.

Canva frame target:
- Assigned master: v3-A / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- Slot: detail_image
- Exact frame: 1080 x 1080 px
- Required width:height ratio: 1.0000:1
- Composition role: outfit_detail
Compose specifically for this frame ratio; do not reuse one narrow portrait composition for all A/B/C slots. Keep the entire hairstyle and head below an 8% top safe margin whenever the head appears. Keep the face and outfit focus inside the central 70%. For full-body views, leave real scene space above the hair and below the feet. No borders or letterboxing. The untouched Canva frame fill must remain publishable without manual focal-point adjustment.

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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W30\generated_images\2026-W30-003\review_sheet.csv
```