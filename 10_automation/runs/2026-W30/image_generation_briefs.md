# Codex Image Generation Briefs

Use these briefs with Codex's in-workspace image generation flow. Store accepted candidates in `generated_images/` and score them in `image_review_template.csv`.

## 2026-W30-001 / M04 - 薄紗與透視層次

- Internal model role: M04 visual early-40s
- Reader projection: A polished mature reader who wants modern outfits that feel current, composed, elegant, and wearable without looking overly young or overly formal.
- Visual profile: East Asian woman with an elegant early-40s look, longer narrow oval face with defined cheekbones and a slightly sharper jawline, straight dark brown chin-to-shoulder bob with a clean side part, natural warm fair skin with smooth well-maintained texture, attentive intelligent eyes with naturally responsive subtle expressions, slightly taller average-slim healthy proportions, composed but not rigid editorial presence.
- Prompt visual age language: early 40s look, elegant
- Outfit: 薄紗罩衫與透視上衣
- Palette / fabric / fit: 奶油白/黑/煙灰 / 雪紡/歐根紗 / 微寬鬆疊穿
- Occasion: 通勤
- Scene: 乾淨的室內灰白牆面與柔光窗邊
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Image Prompt

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.
Use internal model M04 only as a private production profile; do not render or include the model ID or any text in the image.
East Asian woman with an elegant early-40s look, longer narrow oval face with defined cheekbones and a slightly sharper jawline, straight dark brown chin-to-shoulder bob with a clean side part, natural warm fair skin with smooth well-maintained texture, attentive intelligent eyes with naturally responsive subtle expressions, slightly taller average-slim healthy proportions, composed but not rigid editorial presence.
Prompt visual age language: early 40s look, elegant.
Express age through styling and presence, NOT wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.
Outfit: 薄紗罩衫與透視上衣; palette 奶油白/黑/煙灰; fabric 雪紡/歐根紗; fit 微寬鬆疊穿.
Styling rules: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。.
Scene: 乾淨的室內灰白牆面與柔光窗邊. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.
Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only lateral position, body angle, pose, gaze, hand interaction, and expression.
Body proportion lock: match the approved full-body anchor's head-to-height ratio, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not shrink the head, raise the crotch, narrow the torso, or lengthen the legs.
Camera geometry: use a 70mm full-frame-equivalent perspective, lower-chest-to-sternum camera height, and a level optical axis. Keep focal length, camera height, subject distance, horizon, and person scale fixed across A/B/C. No low angle, wide angle, phone-lens distortion, forced perspective, or leg elongation.
Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.
Composition: create A/B/C for the assigned v3-B master at these exact target ratios: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1). A must keep the full outfit readable; B follows its motion-frame orientation; C keeps the required outfit detail readable. Do not reuse one narrow portrait for all three slots. Keep the full hairstyle below an 8% top safe margin whenever the head appears, and keep face/outfit focus inside the central 70% so the untouched Canva fill remains publishable. No visible logos, no text, no watermark.
Avoid: tiny head, nine-head fashion elongation, inconsistent body-to-leg ratio, low-angle leg stretching, supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.
```

## 2026-W30-002 / M03 - 七分褲回歸

- Internal model role: M03 visual mid-30s
- Reader projection: A stylish adult reader who wants practical outfits with softness, confidence, and enough polish for work or weekend.
- Visual profile: East Asian woman with a well-maintained mid-30s look, softly defined oval face with gentle cheeks and balanced jawline, dark brown medium-to-long hair with polished natural movement, natural makeup, relaxed confident posture, healthy slim-to-average build, smooth well-maintained skin with realistic fine texture.
- Prompt visual age language: mid 30s look, well-maintained
- Outfit: 七分褲＋背心與襯衫
- Palette / fabric / fit: 黑/白/海軍藍 / 西裝料/彈性棉 / 合身七分褲+上寬下窄
- Occasion: 城市散步與咖啡廳
- Scene: 乾淨的室內灰白牆面與柔光窗邊
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Image Prompt

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.
Use internal model M03 only as a private production profile; do not render or include the model ID or any text in the image.
East Asian woman with a well-maintained mid-30s look, softly defined oval face with gentle cheeks and balanced jawline, dark brown medium-to-long hair with polished natural movement, natural makeup, relaxed confident posture, healthy slim-to-average build, smooth well-maintained skin with realistic fine texture.
Prompt visual age language: mid 30s look, well-maintained.
Express age through styling and presence, NOT wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.
Outfit: 七分褲＋背心與襯衫; palette 黑/白/海軍藍; fabric 西裝料/彈性棉; fit 合身七分褲+上寬下窄.
Styling rules: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。.
Scene: 乾淨的室內灰白牆面與柔光窗邊. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.
Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only lateral position, body angle, pose, gaze, hand interaction, and expression.
Body proportion lock: match the approved full-body anchor's head-to-height ratio, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not shrink the head, raise the crotch, narrow the torso, or lengthen the legs.
Camera geometry: use a 70mm full-frame-equivalent perspective, lower-chest-to-sternum camera height, and a level optical axis. Keep focal length, camera height, subject distance, horizon, and person scale fixed across A/B/C. No low angle, wide angle, phone-lens distortion, forced perspective, or leg elongation.
Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.
Composition: create A/B/C for the assigned v3-B master at these exact target ratios: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1). A must keep the full outfit readable; B follows its motion-frame orientation; C keeps the required outfit detail readable. Do not reuse one narrow portrait for all three slots. Keep the full hairstyle below an 8% top safe margin whenever the head appears, and keep face/outfit focus inside the central 70% so the untouched Canva fill remains publishable. No visible logos, no text, no watermark.
Avoid: tiny head, nine-head fashion elongation, inconsistent body-to-leg ratio, low-angle leg stretching, supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.
```

## 2026-W30-003 / M01 - 漁夫涼鞋續熱

- Internal model role: M01 visual early-20s
- Reader projection: A young adult reader who wants clean daily outfits that are current, approachable, and easy to adapt without feeling childish.
- Visual profile: East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
- Prompt visual age language: early 20s
- Outfit: 漁夫涼鞋＋寬褲
- Palette / fabric / fit: 黑/棕/奶油白 / 皮革編織/橡膠底 / 鞋款主導、上身簡潔
- Occasion: 旅行與戶外
- Scene: 乾淨的室內灰白牆面與柔光窗邊
- Canva master: v3-A / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- Exact slot targets: A/cover_image=1160x1190 (0.9748:1); B/motion_crop=980x430 (2.2791:1); C/detail_image=1080x1080 (1.0:1)

### Image Prompt

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.
Use internal model M01 only as a private production profile; do not render or include the model ID or any text in the image.
East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
Prompt visual age language: early 20s.
Express age through styling and presence, NOT wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.
Outfit: 漁夫涼鞋＋寬褲; palette 黑/棕/奶油白; fabric 皮革編織/橡膠底; fit 鞋款主導、上身簡潔.
Styling rules: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。.
Scene: 乾淨的室內灰白牆面與柔光窗邊. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.
Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only lateral position, body angle, pose, gaze, hand interaction, and expression.
Body proportion lock: match the approved full-body anchor's head-to-height ratio, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not shrink the head, raise the crotch, narrow the torso, or lengthen the legs.
Camera geometry: use a 70mm full-frame-equivalent perspective, lower-chest-to-sternum camera height, and a level optical axis. Keep focal length, camera height, subject distance, horizon, and person scale fixed across A/B/C. No low angle, wide angle, phone-lens distortion, forced perspective, or leg elongation.
Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.
Composition: create A/B/C for the assigned v3-A master at these exact target ratios: A/cover_image=1160x1190 (0.9748:1); B/motion_crop=980x430 (2.2791:1); C/detail_image=1080x1080 (1.0:1). A must keep the full outfit readable; B follows its motion-frame orientation; C keeps the required outfit detail readable. Do not reuse one narrow portrait for all three slots. Keep the full hairstyle below an 8% top safe margin whenever the head appears, and keep face/outfit focus inside the central 70% so the untouched Canva fill remains publishable. No visible logos, no text, no watermark.
Avoid: tiny head, nine-head fashion elongation, inconsistent body-to-leg ratio, low-angle leg stretching, supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.
```

## 2026-W30-004 / M05 - 奶油黃作為新中性色

- Internal model role: M05 visual around-20
- Reader projection: A very young adult reader who wants clean daily outfits that feel current, simple, and practical without drifting into teen or school styling.
- Visual profile: East Asian woman with an around-20 youthful adult look, soft oval face, fresh natural skin with visible human texture, dark brown shoulder-length bob with a soft side part, bright attentive eyes with relaxed naturally responsive expressions, petite-to-medium healthy proportions, clean daily polish.
- Prompt visual age language: around 20, youthful adult
- Outfit: 奶油黃針織背心與襯衫
- Palette / fabric / fit: 奶油黃/奶油白/巧克力棕 / 薄針織/棉 / 合身上身+直筒下身
- Occasion: 日常與通勤
- Scene: 乾淨的室內灰白牆面與柔光窗邊
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Image Prompt

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.
Use internal model M05 only as a private production profile; do not render or include the model ID or any text in the image.
East Asian woman with an around-20 youthful adult look, soft oval face, fresh natural skin with visible human texture, dark brown shoulder-length bob with a soft side part, bright attentive eyes with relaxed naturally responsive expressions, petite-to-medium healthy proportions, clean daily polish.
Prompt visual age language: around 20, youthful adult.
Express age through styling and presence, NOT wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.
Outfit: 奶油黃針織背心與襯衫; palette 奶油黃/奶油白/巧克力棕; fabric 薄針織/棉; fit 合身上身+直筒下身.
Styling rules: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。.
Scene: 乾淨的室內灰白牆面與柔光窗邊. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.
Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only lateral position, body angle, pose, gaze, hand interaction, and expression.
Body proportion lock: match the approved full-body anchor's head-to-height ratio, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not shrink the head, raise the crotch, narrow the torso, or lengthen the legs.
Camera geometry: use a 70mm full-frame-equivalent perspective, lower-chest-to-sternum camera height, and a level optical axis. Keep focal length, camera height, subject distance, horizon, and person scale fixed across A/B/C. No low angle, wide angle, phone-lens distortion, forced perspective, or leg elongation.
Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.
Composition: create A/B/C for the assigned v3-B master at these exact target ratios: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1). A must keep the full outfit readable; B follows its motion-frame orientation; C keeps the required outfit detail readable. Do not reuse one narrow portrait for all three slots. Keep the full hairstyle below an 8% top safe margin whenever the head appears, and keep face/outfit focus inside the central 70% so the untouched Canva fill remains publishable. No visible logos, no text, no watermark.
Avoid: tiny head, nine-head fashion elongation, inconsistent body-to-leg ratio, low-angle leg stretching, supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.
```

## 2026-W30-005 / M02 - 絲巾腰帶與胯部綁法

- Internal model role: M02 visual late-20s
- Reader projection: A practical adult reader who wants clean daily outfits that are current, wearable, and easy to adapt across work and leisure.
- Visual profile: East Asian woman with a late-20s youthful adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, natural warm fair skin with visible human texture, approachable composed expression, healthy slim-to-average proportions.
- Prompt visual age language: late 20s, youthful
- Outfit: 絲巾腰帶＋牛仔褲
- Palette / fabric / fit: 奶油底復古圖案/牛仔藍/白 / 絲/仿絲 / 配件疊加、衣服保持簡潔
- Occasion: 週末街拍與旅行
- Scene: 乾淨的室內灰白牆面與柔光窗邊
- Canva master: v3-E / Mira Template Master v3 - E Cross-Boundary Weekend Air
- Exact slot targets: A/cover_image=1120x1050 (1.0667:1); B/motion_crop=1120x410 (2.7317:1); C/detail_image=1060x1010 (1.0495:1)

### Image Prompt

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand.
Use internal model M02 only as a private production profile; do not render or include the model ID or any text in the image.
East Asian woman with a late-20s youthful adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, natural warm fair skin with visible human texture, approachable composed expression, healthy slim-to-average proportions.
Prompt visual age language: late 20s, youthful.
Express age through styling and presence, NOT wrinkles. East Asian women look significantly younger than Western age norms. Skin is smooth and well-maintained.
Outfit: 絲巾腰帶＋牛仔褲; palette 奶油底復古圖案/牛仔藍/白; fabric 絲/仿絲; fit 配件疊加、衣服保持簡潔.
Styling rules: 全身不超過 3 種顏色；不出現明顯 Logo；用 1 件主角 + 2 個細節完成造型。.
Scene: 乾淨的室內灰白牆面與柔光窗邊. Make it feel like a believable Taiwan daily-life moment, not a runway or brand advertisement.
Outfit continuity: A/B/C are the same outfit session. Lock every garment, layer, color, shoe, bag, jewelry item, and styling placement; vary only lateral position, body angle, pose, gaze, hand interaction, and expression.
Body proportion lock: match the approved full-body anchor's head-to-height ratio, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not shrink the head, raise the crotch, narrow the torso, or lengthen the legs.
Camera geometry: use a 70mm full-frame-equivalent perspective, lower-chest-to-sternum camera height, and a level optical axis. Keep focal length, camera height, subject distance, horizon, and person scale fixed across A/B/C. No low angle, wide angle, phone-lens distortion, forced perspective, or leg elongation.
Lighting integration: use one scene-motivated directional source. Match its direction and color temperature on face, neck, arms, clothes, shoes, and bag; preserve visible light falloff, ambient color spill, and grounded contact shadows. Match subject contrast, grain, depth of field, and edge softness to the background.
Composition: create A/B/C for the assigned v3-E master at these exact target ratios: A/cover_image=1120x1050 (1.0667:1); B/motion_crop=1120x410 (2.7317:1); C/detail_image=1060x1010 (1.0495:1). A must keep the full outfit readable; B follows its motion-frame orientation; C keeps the required outfit detail readable. Do not reuse one narrow portrait for all three slots. Keep the full hairstyle below an 8% top safe margin whenever the head appears, and keep face/outfit focus inside the central 70% so the untouched Canva fill remains publishable. No visible logos, no text, no watermark.
Avoid: tiny head, nine-head fashion elongation, inconsistent body-to-leg ratio, low-angle leg stretching, supermodel proportions, luxury hotel background, runway pose, plastic skin, flawless beauty render, pasted-on subject, frontal beauty light, shadowless face, halo edges, missing contact shadows, outfit drift across A/B/C, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, wrinkle-based age cues, numeric true-age labels.
```
