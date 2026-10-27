# Codex Image Generation Briefs

Use these briefs with Codex's in-workspace image generation flow. Store accepted candidates in `generated_images/` and score them in `image_review_template.csv`.

## 2026-W37-001 / M02 - 可拆式輕薄疊穿

- Internal model role: M02 visual late-20s
- Reader projection: A practical adult reader who wants clean daily outfits that are current, wearable, and easy to adapt across work and leisure.
- Visual profile: East Asian woman with a late-20s youthful adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, natural warm fair skin with visible human texture, approachable composed expression, healthy slim-to-average proportions.
- Prompt visual age language: late 20s, youthful
- Outfit: 霧灰無內裡棉質薄襯衫；奶油白不透膚細肩帶小腿中長洋裝；白色低筒帆布鞋；深海軍藍小肩包；細銀耳環
- Palette / fabric / fit: 霧灰／奶油白／海軍藍 / 輕薄棉府綢／不透膚棉混紡／帆布 / 襯衫下襬及上臀、敞開；洋裝自然直落；平底鞋
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 冷氣房用可脫薄襯衫罩住肩臂，洋裝本身可以單穿
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 室外偏熱、冷氣房又需要遮住肩臂，如何選可脫的薄層？
- Opening hook: 冷氣房用可脫薄襯衫罩住肩臂，洋裝本身可以單穿
- Visual proof: 敞開襯衫露出完整洋裝，薄袖折痕與肩包帶清楚可見
- Practical rule: 冷氣房用可脫薄襯衫罩住肩臂，洋裝本身可以單穿
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W37-002 / M05 - 短外層配長流動下身

- Internal model role: M05 visual around-20
- Reader projection: A very young adult reader who wants clean daily outfits that feel current, simple, and practical without drifting into teen or school styling.
- Visual profile: East Asian woman with an around-20 youthful adult look, soft oval face, fresh natural skin with visible human texture, dark brown shoulder-length bob with a soft side part, bright attentive eyes with relaxed naturally responsive expressions, petite-to-medium healthy proportions, clean daily polish.
- Prompt visual age language: around 20, youthful adult
- Outfit: 光學白無鋪棉短版薄斜紋夾克；淡藍短袖棉襯衫紮入腰頭；深靛藍高腰薄料長寬褲；黑色平底樂福鞋；焦糖棕小方包
- Palette / fabric / fit: 白／淡藍／深靛藍／焦糖棕 / 薄棉斜紋／棉府綢／垂墜萊賽爾 / 夾克下襬停腰骨；長褲離地且露出鞋尖
- Occasion: 上班
- Content engine: utility_with_immersion
- Dressing decision: 上身用腰骨長度的短外套，讓寬褲腰線與垂墜清楚可見
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 寬鬆上衣和寬褲一起穿，如何讓腰線清楚？
- Opening hook: 上身用腰骨長度的短外套，讓寬褲腰線與垂墜清楚可見
- Visual proof: 白夾克下襬與高腰深藍褲形成清楚長短差，褲管不堆地
- Practical rule: 上身用腰骨長度的短外套，讓寬褲腰線與垂墜清楚可見
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W37-003 / M04 - 柔軟材質配結構輪廓

- Internal model role: M04 visual early-40s
- Reader projection: A polished mature reader who wants modern outfits that feel current, composed, elegant, and wearable without looking overly young or overly formal.
- Visual profile: East Asian woman with an elegant early-40s look, longer narrow oval face with defined cheekbones and a slightly sharper jawline, straight dark brown chin-to-shoulder bob with a clean side part, natural warm fair skin with believable fine texture and tonal variation, attentive intelligent eyes with naturally responsive subtle expressions, slightly taller average-slim healthy proportions, composed but not rigid editorial presence.
- Prompt visual age language: early 40s look, elegant
- Outfit: 深海軍藍無內裡肩線清楚的輕薄外套；米白圓領無袖緞面中長洋裝；黑色低跟樂福鞋；黑色小腋下包；細銀耳環
- Palette / fabric / fit: 海軍藍／米白／黑 / 薄西裝料／不透膚緞面／霧面皮革 / 外套及上臀、自然肩線不誇張；裙身直落小腿
- Occasion: 辦公室
- Content engine: utility_with_immersion
- Dressing decision: 只用肩線明確的外套增加結構，洋裝保留柔軟垂墜
- One visible action: 自然行走中，視線離開鏡頭，一手與包或衣物產生可信互動
- Audience problem: 想穿柔軟衣料，如何保留一處明確的衣服輪廓？
- Opening hook: 只用肩線明確的外套增加結構，洋裝保留柔軟垂墜
- Visual proof: 深色肩線與米白緞面柔軟折光形成對比
- Practical rule: 只用肩線明確的外套增加結構，洋裝保留柔軟垂墜
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W37-004 / M01 - 復古 T 字帶鞋日常化

- Internal model role: M01 visual early-20s
- Reader projection: A young adult reader who wants clean daily outfits that are current, approachable, and easy to adapt without feeling childish.
- Visual profile: East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
- Prompt visual age language: early 20s
- Outfit: 白色短袖棉府綢襯衫；深灰高腰及踝直筒褲；酒紅色低粗跟T字帶鞋，腳背中央直帶連接踝前橫帶、包頭；黑色小肩包；黑色窄皮帶
- Palette / fabric / fit: 白／深灰／酒紅／黑 / 棉府綢／薄西裝料／霧面皮革 / 直筒褲止於踝上、不遮腳背；鞋跟低而寬
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 基本款配T字帶鞋時縮短褲長，露出腳背的T字結構
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 基本款想搭T字帶鞋，褲裙要多長才看得見鞋帶？
- Opening hook: 基本款配T字帶鞋時縮短褲長，露出腳背的T字結構
- Visual proof: 白襯衫與灰褲保持簡潔，酒紅鞋的直帶與橫帶完整可見
- Practical rule: 基本款配T字帶鞋時縮短褲長，露出腳背的T字結構
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W37-005 / M03 - 麂皮與皮革一件亮點

- Internal model role: M03 visual mid-30s
- Reader projection: A stylish adult reader who wants practical outfits with softness, confidence, and enough polish for work or weekend.
- Visual profile: East Asian woman with a well-maintained mid-30s look, softly defined oval face with gentle cheeks and balanced jawline, dark brown medium-to-long hair with polished natural movement, natural makeup, relaxed confident posture, healthy slim-to-average build, believable skin texture with normal human tonal variation.
- Prompt visual age language: mid 30s look, well-maintained
- Outfit: 奶油白無袖棉麻襯衫；深咖啡高腰薄棉麻直筒褲；焦糖色短毛麂皮小肩包；黑色低跟樂福鞋；細銀耳環
- Palette / fabric / fit: 奶油白／深咖啡／焦糖／黑 / 棉麻／短毛麂皮／霧面皮革 / 上衣紮入；直筒褲離地；小包位於腰側
- Occasion: 週末
- Content engine: utility_with_immersion
- Dressing decision: 入秋先用麂皮小包，衣服保留薄棉麻
- One visible action: 自然行走中，視線離開鏡頭，一手與包或衣物產生可信互動
- Audience problem: 想加麂皮材質，又不想整身厚重，配件如何選？
- Opening hook: 入秋先用麂皮小包，衣服保留薄棉麻
- Visual proof: 焦糖麂皮絨面貼近奶油白棉麻，黑鞋低調不搶材質對比
- Practical rule: 入秋先用麂皮小包，衣服保留薄棉麻
- Scene: assigned_by_codex
- Canva master: v3-C / Mira Template Master v3 - C Cross-Boundary Noir
- Exact slot targets: A/cover_image=1230x1350 (0.9111:1); B/motion_crop=1000x460 (2.1739:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```
