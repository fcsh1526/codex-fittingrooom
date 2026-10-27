# Codex Generation Handoff - 2026-W30-004 / M05

Use this file to generate the reel image candidates inside Codex.

## Reference Images

Attach both approved reference start images to the image-generation request:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png
```

## Output Filenames

Save generated candidates as:

```text
2026-W30-004_M05_reel_v3_candidate_A.png
2026-W30-004_M05_reel_v3_candidate_B.png
2026-W30-004_M05_reel_v3_candidate_C.png
```

## Candidate Prompts

Asset A: integrated-scene Hero and session lock

Required image inputs:
- Face identity anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png
- Full-body proportion anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png
- Session rule: Accepted Hero A is created in this step.

Create a photorealistic vertical lifestyle fashion photograph for Mira. Internal model M05 is production metadata only; never render model IDs, names, captions, logos, or watermarks.

Identity and anatomy:
Preserve the exact facial identity and core hairstyle from the face anchor. Match the full-body anchor's realistic head size, shoulder width, torso length, waist and hip placement, knee height, leg-to-torso balance, arm length, and hand size. Use plausible adult proportions rather than runway or nine-head elongation. The reference pose, expression, studio background, and reference outfit are not part of the identity.

Trend and outfit:
- Trend: 奶油黃作為新中性色
- Garments: 奶油黃針織背心與襯衫
- Palette: 奶油黃/奶油白/巧克力棕
- Fabric: 薄針織/棉
- Fit: 合身上身+直筒下身
- Occasion: 日常與通勤
- Styling: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。

Scene and camera:
Use a believable daily-life setting that supports the occasion. Scene hint: 乾淨的室內灰白牆面與柔光窗邊. Treat person and environment as one exposure photographed with a full-frame mirrorless camera and a 50mm prime lens near chest height with a level optical axis. Daylight starting settings: f/4, 1/250 s, ISO 200, white balance 5200 K; adjust only when the scene physically requires it, and state the final settings explicitly. Keep camera body, focal length, height, white balance, and rendering logic locked across A/B/C. Never substitute a smartphone, computational portrait mode, DSLR simulation, low angle, or wide-angle perspective unless the user explicitly overrides the camera standard. Use one soft neutral daylight source from the window and let it affect the subject and environment as one exposure. Keep skin color consistent across forehead, cheeks, nose, jaw, neck, and visible hands, with gentle natural luminance falloff only. Treat the face reference as an identity anchor, not a lighting reference. Do not introduce mixed color temperatures across the face, orange wood bounce on skin, blue skylight cast, split lighting, glossy facial highlights, artificial skin glow, or beauty retouching. Preserve natural skin texture, natural contact shadows, shared depth of field, restrained grain, slight optical softness, flyaway hairs, and small fabric wrinkles.

Reel frame target:
- Delivery surface: Reel
- Direct frame: 1080 x 1920 px
- Required width:height ratio: 9:16 (0.5625:1)
- Composition role: vertical_hero
Compose directly for 9:16. Do not generate a square, 4:5, 2:3, or Carousel master and crop it later. The Canva 15% crop rule does not apply to Reel. If the source is not composed as 9:16, regenerate it. Keep the full hairstyle below an 8% top safe margin and keep the face, outfit focus, and physical interaction away from the extreme top and bottom interface zones. No borders or letterboxing.

Asset direction:
Show the full figure with surrounding environment. Use a relaxed asymmetric stance and one physically believable interaction with a foreground or scene object, including visible contact pressure and contact shadow. Use a direct 9:16 composition with no square, 4:5, 2:3, or Canva intermediate crop. Keep the key action, face, outfit, and physical interaction readable in the final vertical frame.

Age rendering:
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin has natural fine texture, restrained highlights, and an even neutral color without waxy smoothing.

Avoid:
tiny head, fashion-elongated body, raised crotch, stretched legs, low or wide camera angle, mannequin posture, floating hands or feet, independent subject lighting, cutout edges, halo, plastic skin, plastic fabric, garment drift, celebrity likeness, sexualized or childlike styling, text, logos, and watermark.


---

Asset B: movement variation edited from the accepted Hero A

Required image inputs:
- Face identity anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png
- Full-body proportion anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png
- Session rule: Attach accepted Hero A as the edit target/session lock in addition to both model anchors. Do not generate an independent reinterpretation.

Create a photorealistic vertical lifestyle fashion photograph for Mira. Internal model M05 is production metadata only; never render model IDs, names, captions, logos, or watermarks.

Identity and anatomy:
Preserve the exact facial identity and core hairstyle from the face anchor. Match the full-body anchor's realistic head size, shoulder width, torso length, waist and hip placement, knee height, leg-to-torso balance, arm length, and hand size. Use plausible adult proportions rather than runway or nine-head elongation. The reference pose, expression, studio background, and reference outfit are not part of the identity.

Trend and outfit:
- Trend: 奶油黃作為新中性色
- Garments: 奶油黃針織背心與襯衫
- Palette: 奶油黃/奶油白/巧克力棕
- Fabric: 薄針織/棉
- Fit: 合身上身+直筒下身
- Occasion: 日常與通勤
- Styling: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。

Scene and camera:
Use a believable daily-life setting that supports the occasion. Scene hint: 乾淨的室內灰白牆面與柔光窗邊. Treat person and environment as one exposure photographed with a full-frame mirrorless camera and a 50mm prime lens near chest height with a level optical axis. Daylight starting settings: f/4, 1/250 s, ISO 200, white balance 5200 K; adjust only when the scene physically requires it, and state the final settings explicitly. Keep camera body, focal length, height, white balance, and rendering logic locked across A/B/C. Never substitute a smartphone, computational portrait mode, DSLR simulation, low angle, or wide-angle perspective unless the user explicitly overrides the camera standard. Use one soft neutral daylight source from the window and let it affect the subject and environment as one exposure. Keep skin color consistent across forehead, cheeks, nose, jaw, neck, and visible hands, with gentle natural luminance falloff only. Treat the face reference as an identity anchor, not a lighting reference. Do not introduce mixed color temperatures across the face, orange wood bounce on skin, blue skylight cast, split lighting, glossy facial highlights, artificial skin glow, or beauty retouching. Preserve natural skin texture, natural contact shadows, shared depth of field, restrained grain, slight optical softness, flyaway hairs, and small fabric wrinkles.

Reel frame target:
- Delivery surface: Reel
- Direct frame: 1080 x 1920 px
- Required width:height ratio: 9:16 (0.5625:1)
- Composition role: vertical_motion
Compose directly for 9:16. Do not generate a square, 4:5, 2:3, or Carousel master and crop it later. The Canva 15% crop rule does not apply to Reel. If the source is not composed as 9:16, regenerate it. Keep the full hairstyle below an 8% top safe margin and keep the face, outfit focus, and physical interaction away from the extreme top and bottom interface zones. No borders or letterboxing.

Asset direction:
Edit accepted Hero A into a candid three-quarter turn or small lateral movement. Change gaze and one hand action, but keep the same scene, outfit construction, identity, body build, light source, and camera treatment. Use a direct 9:16 composition with no square, 4:5, 2:3, or Canva intermediate crop. Keep the key action, face, outfit, and physical interaction readable in the final vertical frame.

Age rendering:
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin has natural fine texture, restrained highlights, and an even neutral color without waxy smoothing.

Avoid:
tiny head, fashion-elongated body, raised crotch, stretched legs, low or wide camera angle, mannequin posture, floating hands or feet, independent subject lighting, cutout edges, halo, plastic skin, plastic fabric, garment drift, celebrity likeness, sexualized or childlike styling, text, logos, and watermark.


---

Asset C: outfit-detail variation edited from the accepted Hero A

Required image inputs:
- Face identity anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png
- Full-body proportion anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png
- Session rule: Attach accepted Hero A as the edit target/session lock in addition to both model anchors. Do not generate an independent reinterpretation.

Create a photorealistic vertical lifestyle fashion photograph for Mira. Internal model M05 is production metadata only; never render model IDs, names, captions, logos, or watermarks.

Identity and anatomy:
Preserve the exact facial identity and core hairstyle from the face anchor. Match the full-body anchor's realistic head size, shoulder width, torso length, waist and hip placement, knee height, leg-to-torso balance, arm length, and hand size. Use plausible adult proportions rather than runway or nine-head elongation. The reference pose, expression, studio background, and reference outfit are not part of the identity.

Trend and outfit:
- Trend: 奶油黃作為新中性色
- Garments: 奶油黃針織背心與襯衫
- Palette: 奶油黃/奶油白/巧克力棕
- Fabric: 薄針織/棉
- Fit: 合身上身+直筒下身
- Occasion: 日常與通勤
- Styling: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。

Scene and camera:
Use a believable daily-life setting that supports the occasion. Scene hint: 乾淨的室內灰白牆面與柔光窗邊. Treat person and environment as one exposure photographed with a full-frame mirrorless camera and a 50mm prime lens near chest height with a level optical axis. Daylight starting settings: f/4, 1/250 s, ISO 200, white balance 5200 K; adjust only when the scene physically requires it, and state the final settings explicitly. Keep camera body, focal length, height, white balance, and rendering logic locked across A/B/C. Never substitute a smartphone, computational portrait mode, DSLR simulation, low angle, or wide-angle perspective unless the user explicitly overrides the camera standard. Use one soft neutral daylight source from the window and let it affect the subject and environment as one exposure. Keep skin color consistent across forehead, cheeks, nose, jaw, neck, and visible hands, with gentle natural luminance falloff only. Treat the face reference as an identity anchor, not a lighting reference. Do not introduce mixed color temperatures across the face, orange wood bounce on skin, blue skylight cast, split lighting, glossy facial highlights, artificial skin glow, or beauty retouching. Preserve natural skin texture, natural contact shadows, shared depth of field, restrained grain, slight optical softness, flyaway hairs, and small fabric wrinkles.

Reel frame target:
- Delivery surface: Reel
- Direct frame: 1080 x 1920 px
- Required width:height ratio: 9:16 (0.5625:1)
- Composition role: vertical_detail
Compose directly for 9:16. Do not generate a square, 4:5, 2:3, or Carousel master and crop it later. The Canva 15% crop rule does not apply to Reel. If the source is not composed as 9:16, regenerate it. Keep the full hairstyle below an 8% top safe margin and keep the face, outfit focus, and physical interaction away from the extreme top and bottom interface zones. No borders or letterboxing.

Asset direction:
Edit accepted Hero A into a knees-up or waist-up outfit-detail composition. Preserve the exact neckline, layers, sleeves, fabric behavior, accessories, identity, scene, and lighting treatment. Use a direct 9:16 composition with no square, 4:5, 2:3, or Canva intermediate crop. Keep the key action, face, outfit, and physical interaction readable in the final vertical frame.

Age rendering:
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin has natural fine texture, restrained highlights, and an even neutral color without waxy smoothing.

Avoid:
tiny head, fashion-elongated body, raised crotch, stretched legs, low or wide camera angle, mannequin posture, floating hands or feet, independent subject lighting, cutout edges, halo, plastic skin, plastic fabric, garment drift, celebrity likeness, sexualized or childlike styling, text, logos, and watermark.


## After Generation

Update:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W30\generated_images\2026-W30-004\reel\review_sheet.csv
```
