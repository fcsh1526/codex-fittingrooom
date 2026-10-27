# Codex Image Generation Briefs

Use these briefs with Codex's in-workspace image generation flow. Store accepted candidates in `generated_images/` and score them in `image_review_template.csv`.

## 2026-W33-001 / M05 - 輕量防護外層

- Internal model role: M05 visual around-20
- Reader projection: A very young adult reader who wants clean daily outfits that feel current, simple, and practical without drifting into teen or school styling.
- Visual profile: East Asian woman with an around-20 youthful adult look, soft oval face, fresh natural skin with visible human texture, dark brown shoulder-length bob with a soft side part, bright attentive eyes with relaxed naturally responsive expressions, petite-to-medium healthy proportions, clean daily polish.
- Prompt visual age language: around 20, youthful adult
- Outfit: 短版 bomber／薄風衣
- Palette / fabric / fit: 奶油白／海軍藍／橄欖綠 / 輕量尼龍／棉混紡 / 短版微寬肩
- Occasion: 通勤／城市旅行
- Scene: 乾淨灰白室內牆面與柔光窗邊
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Image Prompt

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.
Use internal model M05 only as a private production profile; do not render or include the model ID or any text in the image.
East Asian woman with an around-20 youthful adult look, soft oval face, fresh natural skin with visible human texture, dark brown shoulder-length bob with a soft side part, bright attentive eyes with relaxed naturally responsive expressions, petite-to-medium healthy proportions, clean daily polish.
Prompt visual age language: around 20, youthful adult.
Express age through styling and presence, NOT wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.
Outfit: 短版 bomber／薄風衣; palette 奶油白／海軍藍／橄欖綠; fabric 輕量尼龍／棉混紡; fit 短版微寬肩.
Styling rules: 只留一個主色外層；下身用高腰直筒或九分褲平衡。.
Scene: 乾淨灰白室內牆面與柔光窗邊. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.
Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only lateral position, body angle, pose, gaze, hand interaction, and expression.
Body proportion lock: match the approved full-body anchor's head-to-height ratio, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not shrink the head, raise the crotch, narrow the torso, or lengthen the legs.
Camera system: photograph with a full-frame mirrorless camera and a 50mm prime lens, using a lower-chest-to-sternum camera height and a level optical axis. State aperture, shutter speed, ISO, and white balance in every prompt; use f/4, 1/250 s, ISO 200, and 5200 K as the daylight baseline, adjusting only when physically required by the scene. Keep camera body, focal length, camera height, subject distance, horizon, white balance, rendering logic, and person scale fixed across A/B/C. No low angle, smartphone, computational portrait mode, DSLR simulation, wide angle, phone-lens distortion, forced perspective, or leg elongation unless the user explicitly overrides the camera standard.
Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.
Composition: create A/B/C for the assigned v3-B master at these exact target ratios: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1). A must keep the full outfit readable; B follows its motion-frame orientation; C keeps the required outfit detail readable. Do not reuse one narrow portrait for all three slots. Keep the full hairstyle below an 8% top safe margin whenever the head appears, and keep face/outfit focus inside the central 70% so the untouched Canva fill remains publishable. No visible logos, no text, no watermark.
Avoid: tiny head, nine-head fashion elongation, inconsistent body-to-leg ratio, low-angle leg stretching, supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.
```

## 2026-W33-002 / M02 - 縮短比例

- Internal model role: M02 visual late-20s
- Reader projection: A practical adult reader who wants clean daily outfits that are current, wearable, and easy to adapt across work and leisure.
- Visual profile: East Asian woman with a late-20s youthful adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, natural warm fair skin with visible human texture, approachable composed expression, healthy slim-to-average proportions.
- Prompt visual age language: late 20s, youthful
- Outfit: 七分褲／褲裙／九分直筒褲
- Palette / fabric / fit: 黑／深靛藍／灰／奶油白 / 西裝料／彈性棉 / 高腰合身至小腿
- Occasion: 咖啡廳／創意辦公室
- Scene: 極簡咖啡廳暖白牆面
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Image Prompt

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.
Use internal model M02 only as a private production profile; do not render or include the model ID or any text in the image.
East Asian woman with a late-20s youthful adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, natural warm fair skin with visible human texture, approachable composed expression, healthy slim-to-average proportions.
Prompt visual age language: late 20s, youthful.
Express age through styling and presence, NOT wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.
Outfit: 七分褲／褲裙／九分直筒褲; palette 黑／深靛藍／灰／奶油白; fabric 西裝料／彈性棉; fit 高腰合身至小腿.
Styling rules: 短版上衣或外套搭高腰下身；鞋面保持乾淨。.
Scene: 極簡咖啡廳暖白牆面. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.
Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only lateral position, body angle, pose, gaze, hand interaction, and expression.
Body proportion lock: match the approved full-body anchor's head-to-height ratio, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not shrink the head, raise the crotch, narrow the torso, or lengthen the legs.
Camera system: photograph with a full-frame mirrorless camera and a 50mm prime lens, using a lower-chest-to-sternum camera height and a level optical axis. State aperture, shutter speed, ISO, and white balance in every prompt; use f/4, 1/250 s, ISO 200, and 5200 K as the daylight baseline, adjusting only when physically required by the scene. Keep camera body, focal length, camera height, subject distance, horizon, white balance, rendering logic, and person scale fixed across A/B/C. No low angle, smartphone, computational portrait mode, DSLR simulation, wide angle, phone-lens distortion, forced perspective, or leg elongation unless the user explicitly overrides the camera standard.
Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.
Composition: create A/B/C for the assigned v3-B master at these exact target ratios: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1). A must keep the full outfit readable; B follows its motion-frame orientation; C keeps the required outfit detail readable. Do not reuse one narrow portrait for all three slots. Keep the full hairstyle below an 8% top safe margin whenever the head appears, and keep face/outfit focus inside the central 70% so the untouched Canva fill remains publishable. No visible logos, no text, no watermark.
Avoid: tiny head, nine-head fashion elongation, inconsistent body-to-leg ratio, low-angle leg stretching, supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.
```

## 2026-W33-003 / M01 - 工作圍裙與口袋罩裙

- Internal model role: M01 visual early-20s
- Reader projection: A young adult reader who wants clean daily outfits that are current, approachable, and easy to adapt without feeling childish.
- Visual profile: East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
- Prompt visual age language: early 20s
- Outfit: 帆布罩裙／utility vest
- Palette / fabric / fit: 原色帆布／工裝藍／磚紅 / 帆布／工業棉／府綢 / 直身可調肩帶
- Occasion: 展覽／市集／街拍
- Scene: 採光美術館與淺灰地面
- Canva master: v3-A / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- Exact slot targets: A/cover_image=1160x1190 (0.9748:1); B/motion_crop=980x430 (2.2791:1); C/detail_image=1080x1080 (1.0:1)

### Image Prompt

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.
Use internal model M01 only as a private production profile; do not render or include the model ID or any text in the image.
East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
Prompt visual age language: early 20s.
Express age through styling and presence, NOT wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.
Outfit: 帆布罩裙／utility vest; palette 原色帆布／工裝藍／磚紅; fabric 帆布／工業棉／府綢; fit 直身可調肩帶.
Styling rules: 用一個口袋或工具腰包做主角；底層保持素色。.
Scene: 採光美術館與淺灰地面. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.
Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only lateral position, body angle, pose, gaze, hand interaction, and expression.
Body proportion lock: match the approved full-body anchor's head-to-height ratio, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not shrink the head, raise the crotch, narrow the torso, or lengthen the legs.
Camera system: photograph with a full-frame mirrorless camera and a 50mm prime lens, using a lower-chest-to-sternum camera height and a level optical axis. State aperture, shutter speed, ISO, and white balance in every prompt; use f/4, 1/250 s, ISO 200, and 5200 K as the daylight baseline, adjusting only when physically required by the scene. Keep camera body, focal length, camera height, subject distance, horizon, white balance, rendering logic, and person scale fixed across A/B/C. No low angle, smartphone, computational portrait mode, DSLR simulation, wide angle, phone-lens distortion, forced perspective, or leg elongation unless the user explicitly overrides the camera standard.
Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.
Composition: create A/B/C for the assigned v3-A master at these exact target ratios: A/cover_image=1160x1190 (0.9748:1); B/motion_crop=980x430 (2.2791:1); C/detail_image=1080x1080 (1.0:1). A must keep the full outfit readable; B follows its motion-frame orientation; C keeps the required outfit detail readable. Do not reuse one narrow portrait for all three slots. Keep the full hairstyle below an 8% top safe margin whenever the head appears, and keep face/outfit focus inside the central 70% so the untouched Canva fill remains publishable. No visible logos, no text, no watermark.
Avoid: tiny head, nine-head fashion elongation, inconsistent body-to-leg ratio, low-angle leg stretching, supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.
```

## 2026-W33-004 / M03 - 復古腰帶與絲巾

- Internal model role: M03 visual mid-30s
- Reader projection: A stylish adult reader who wants practical outfits with softness, confidence, and enough polish for work or weekend.
- Visual profile: East Asian woman with a well-maintained mid-30s look, softly defined oval face with gentle cheeks and balanced jawline, dark brown medium-to-long hair with polished natural movement, natural makeup, relaxed confident posture, healthy slim-to-average build, smooth well-maintained skin with realistic fine texture.
- Prompt visual age language: mid 30s look, well-maintained
- Outfit: 寬皮帶／絲巾腰帶／復古肩包
- Palette / fabric / fit: 焦糖棕／酒紅／印花藍／黑 / 皮革／絲／仿絲 / 腰間固定、衣服簡潔
- Occasion: 約會／旅行／週末
- Scene: 城市騎樓與柔和早晨光線
- Canva master: v3-E / Mira Template Master v3 - E Cross-Boundary Weekend Air
- Exact slot targets: A/cover_image=1120x1050 (1.0667:1); B/motion_crop=1120x410 (2.7317:1); C/detail_image=1060x1010 (1.0495:1)

### Image Prompt

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.
Use internal model M03 only as a private production profile; do not render or include the model ID or any text in the image.
East Asian woman with a well-maintained mid-30s look, softly defined oval face with gentle cheeks and balanced jawline, dark brown medium-to-long hair with polished natural movement, natural makeup, relaxed confident posture, healthy slim-to-average build, smooth well-maintained skin with realistic fine texture.
Prompt visual age language: mid 30s look, well-maintained.
Express age through styling and presence, NOT wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.
Outfit: 寬皮帶／絲巾腰帶／復古肩包; palette 焦糖棕／酒紅／印花藍／黑; fabric 皮革／絲／仿絲; fit 腰間固定、衣服簡潔.
Styling rules: 全身最多一個花紋；腰帶或絲巾負責造型記憶點。.
Scene: 城市騎樓與柔和早晨光線. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.
Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only lateral position, body angle, pose, gaze, hand interaction, and expression.
Body proportion lock: match the approved full-body anchor's head-to-height ratio, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not shrink the head, raise the crotch, narrow the torso, or lengthen the legs.
Camera system: photograph with a full-frame mirrorless camera and a 50mm prime lens, using a lower-chest-to-sternum camera height and a level optical axis. State aperture, shutter speed, ISO, and white balance in every prompt; use f/4, 1/250 s, ISO 200, and 5200 K as the daylight baseline, adjusting only when physically required by the scene. Keep camera body, focal length, camera height, subject distance, horizon, white balance, rendering logic, and person scale fixed across A/B/C. No low angle, smartphone, computational portrait mode, DSLR simulation, wide angle, phone-lens distortion, forced perspective, or leg elongation unless the user explicitly overrides the camera standard.
Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.
Composition: create A/B/C for the assigned v3-E master at these exact target ratios: A/cover_image=1120x1050 (1.0667:1); B/motion_crop=1120x410 (2.7317:1); C/detail_image=1060x1010 (1.0495:1). A must keep the full outfit readable; B follows its motion-frame orientation; C keeps the required outfit detail readable. Do not reuse one narrow portrait for all three slots. Keep the full hairstyle below an 8% top safe margin whenever the head appears, and keep face/outfit focus inside the central 70% so the untouched Canva fill remains publishable. No visible logos, no text, no watermark.
Avoid: tiny head, nine-head fashion elongation, inconsistent body-to-leg ratio, low-angle leg stretching, supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.
```

## 2026-W33-005 / M04 - 柔和色塊與觸覺材質

- Internal model role: M04 visual early-40s
- Reader projection: A polished mature reader who wants modern outfits that feel current, composed, elegant, and wearable without looking overly young or overly formal.
- Visual profile: East Asian woman with an elegant early-40s look, longer narrow oval face with defined cheekbones and a slightly sharper jawline, straight dark brown chin-to-shoulder bob with a clean side part, natural warm fair skin with smooth well-maintained texture, attentive intelligent eyes with naturally responsive subtle expressions, slightly taller average-slim healthy proportions, composed but not rigid editorial presence.
- Prompt visual age language: early 40s look, elegant
- Outfit: 奶油針織／薄紗百褶裙／府綢襯衫
- Palette / fabric / fit: 奶油白／天藍／沙色／酒紅 / 薄針織／雪紡／棉府綢 / 柔軟上身＋有結構下身
- Occasion: 日常／通勤／早午餐
- Scene: 米白工作室與木質長椅
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Image Prompt

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.
Use internal model M04 only as a private production profile; do not render or include the model ID or any text in the image.
East Asian woman with an elegant early-40s look, longer narrow oval face with defined cheekbones and a slightly sharper jawline, straight dark brown chin-to-shoulder bob with a clean side part, natural warm fair skin with smooth well-maintained texture, attentive intelligent eyes with naturally responsive subtle expressions, slightly taller average-slim healthy proportions, composed but not rigid editorial presence.
Prompt visual age language: early 40s look, elegant.
Express age through styling and presence, NOT wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.
Outfit: 奶油針織／薄紗百褶裙／府綢襯衫; palette 奶油白／天藍／沙色／酒紅; fabric 薄針織／雪紡／棉府綢; fit 柔軟上身＋有結構下身.
Styling rules: 兩個柔和色做主色，棕或酒紅只放鞋包。.
Scene: 米白工作室與木質長椅. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.
Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only lateral position, body angle, pose, gaze, hand interaction, and expression.
Body proportion lock: match the approved full-body anchor's head-to-height ratio, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not shrink the head, raise the crotch, narrow the torso, or lengthen the legs.
Camera system: photograph with a full-frame mirrorless camera and a 50mm prime lens, using a lower-chest-to-sternum camera height and a level optical axis. State aperture, shutter speed, ISO, and white balance in every prompt; use f/4, 1/250 s, ISO 200, and 5200 K as the daylight baseline, adjusting only when physically required by the scene. Keep camera body, focal length, camera height, subject distance, horizon, white balance, rendering logic, and person scale fixed across A/B/C. No low angle, smartphone, computational portrait mode, DSLR simulation, wide angle, phone-lens distortion, forced perspective, or leg elongation unless the user explicitly overrides the camera standard.
Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.
Composition: create A/B/C for the assigned v3-B master at these exact target ratios: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1). A must keep the full outfit readable; B follows its motion-frame orientation; C keeps the required outfit detail readable. Do not reuse one narrow portrait for all three slots. Keep the full hairstyle below an 8% top safe margin whenever the head appears, and keep face/outfit focus inside the central 70% so the untouched Canva fill remains publishable. No visible logos, no text, no watermark.
Avoid: tiny head, nine-head fashion elongation, inconsistent body-to-leg ratio, low-angle leg stretching, supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.
```
