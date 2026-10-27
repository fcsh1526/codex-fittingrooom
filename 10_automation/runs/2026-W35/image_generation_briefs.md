# Codex Image Generation Briefs

Use these briefs with Codex's in-workspace image generation flow. Store accepted candidates in `generated_images/` and score them in `image_review_template.csv`.

## 2026-W35-001 / M05 - 輕量高領外套

- Internal model role: M05 visual around-20
- Reader projection: A very young adult reader who wants clean daily outfits that feel current, simple, and practical without drifting into teen or school styling.
- Visual profile: East Asian woman with an around-20 youthful adult look, soft oval face, fresh natural skin with visible human texture, dark brown shoulder-length bob with a soft side part, bright attentive eyes with relaxed naturally responsive expressions, petite-to-medium healthy proportions, clean daily polish.
- Prompt visual age language: around 20, youthful adult
- Outfit: 薄身高領夾克
- Palette / fabric / fit: 石墨黑、米灰、奶油白 / 薄尼龍混紡 / 短版立領、微寬肩
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 先選無鋪棉的高領薄外套，裡面維持夏天的短袖穿法。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 早晚需要外套，但厚外套一穿就悶，進室內更不舒服。
- Opening hook: 八月想穿高領外套，先選薄一點的
- Visual proof: 短版高領外套的長度在腰部附近，裡面的短袖和直筒褲都看得見；領口拉起或放下都能穿。
- Practical rule: 高領外套選無鋪棉的薄款，裡面搭短袖，下身配直筒褲，全身不要同時穿得寬鬆。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W35-002 / M01 - 深棕麂皮配件

- Internal model role: M01 visual early-20s
- Reader projection: A young adult reader who wants clean daily outfits that are current, approachable, and easy to adapt without feeling childish.
- Visual profile: East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
- Prompt visual age language: early 20s
- Outfit: 深棕麂皮肩背包
- Palette / fabric / fit: 巧克力棕、奶油白、靛藍 / 霧面麂皮 / 中小型柔軟方形
- Occasion: 咖啡廳
- Content engine: utility_with_immersion
- Dressing decision: 白 T 配深色直筒牛仔褲，八月穿也不會太厚；再背一個深棕麂皮包，秋天的感覺就有了。
- One visible action: 剛放下咖啡杯，視線自然看向窗外，另一手停在隨身包旁
- Audience problem: 衣櫃多半是黑白基本款，想提早穿出秋天的感覺，又怕穿得太厚。
- Opening hook: 八月想搭麂皮，先從包包下手
- Visual proof: 白 T 和牛仔褲都選輕薄材質，整套只有包包使用麂皮。
- Practical rule: 麂皮包搭白 T 和深色直筒牛仔褲，其他單品不要再用麂皮，避免同時加入厚外套。
- Scene: assigned_by_codex
- Canva master: v3-E / Mira Template Master v3 - E Cross-Boundary Weekend Air
- Exact slot targets: A/cover_image=1120x1050 (1.0667:1); B/motion_crop=1120x410 (2.7317:1); C/detail_image=1060x1010 (1.0495:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W35-003 / M03 - 運動外套配長裙

- Internal model role: M03 visual mid-30s
- Reader projection: A stylish adult reader who wants practical outfits with softness, confidence, and enough polish for work or weekend.
- Visual profile: East Asian woman with a well-maintained mid-30s look, softly defined oval face with gentle cheeks and balanced jawline, dark brown medium-to-long hair with polished natural movement, natural makeup, relaxed confident posture, healthy slim-to-average build, believable skin texture with normal human tonal variation.
- Prompt visual age language: mid 30s look, well-maintained
- Outfit: 深海軍藍輕量運動外套
- Palette / fabric / fit: 海軍藍、灰白、深灰 / 薄尼龍 / 短版立領、袖口微收
- Occasion: 上班
- Content engine: utility_with_immersion
- Dressing decision: 長裙外面加一件短版薄運動外套，再配平底球鞋，上班穿也不會太正式。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 長裙常常搭得太正式或太甜，平日上班反而不敢穿。
- Opening hook: 長裙不想穿得太正式，可以搭運動外套
- Visual proof: 短版運動外套搭直筒長裙，再配平底球鞋，正式和休閒的比例剛好。
- Practical rule: 長裙配一件短版薄運動外套，鞋子選沒有明顯標誌的平底球鞋。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W35-004 / M02 - 窄版絲巾的小結

- Internal model role: M02 visual late-20s
- Reader projection: A practical adult reader who wants clean daily outfits that are current, wearable, and easy to adapt across work and leisure.
- Visual profile: East Asian woman with a late-20s youthful adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, natural warm fair skin with visible human texture, approachable composed expression, healthy slim-to-average proportions.
- Prompt visual age language: late 20s, youthful
- Outfit: 黑白細窄絲巾
- Palette / fabric / fit: 黑白、白、深藍 / 輕薄絲質 / 窄長方形
- Occasion: 辦公室
- Content engine: utility_with_immersion
- Dressing decision: 白襯衫領口繫一條窄版絲巾，打一個小結，胸前就不再戴項鍊。
- One visible action: 自然行走中，視線離開鏡頭，一手與包或衣物產生可信互動
- Audience problem: 每天都穿白上衣，但加項鍊又覺得太制式、太像上班制服。
- Opening hook: 白襯衫加一條窄版絲巾就有變化
- Visual proof: 白襯衫領口有一個窄版絲巾小結，下身搭素色直筒褲，胸前沒有其他配件。
- Practical rule: 白上衣只加一條窄版絲巾，結放在鎖骨下方，鞋子和包包選同一個中性色。
- Scene: assigned_by_codex
- Canva master: v3-A / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- Exact slot targets: A/cover_image=1160x1190 (0.9748:1); B/motion_crop=980x430 (2.2791:1); C/detail_image=1080x1080 (1.0:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W35-005 / M04 - 深色直筒牛仔褲配柔色上衣

- Internal model role: M04 visual early-40s
- Reader projection: A polished mature reader who wants modern outfits that feel current, composed, elegant, and wearable without looking overly young or overly formal.
- Visual profile: East Asian woman with an elegant early-40s look, longer narrow oval face with defined cheekbones and a slightly sharper jawline, straight dark brown chin-to-shoulder bob with a clean side part, natural warm fair skin with believable fine texture and tonal variation, attentive intelligent eyes with naturally responsive subtle expressions, slightly taller average-slim healthy proportions, composed but not rigid editorial presence.
- Prompt visual age language: early 40s look, elegant
- Outfit: 深靛直筒丹寧褲
- Palette / fabric / fit: 深靛藍、柔霧粉、米灰 / 薄身棉質丹寧 / 中高腰直筒
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 深色直筒牛仔褲配柔色緞面上衣，再搭低跟鞋，上班穿也不會太休閒。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 想穿牛仔褲去上班，又怕整套看起來像週末休閒服。
- Opening hook: 牛仔褲穿去上班，上衣不要再選 T 恤
- Visual proof: 深色牛仔褲比較硬挺，上衣選有光澤、會自然垂下的布料，再搭低跟鞋。
- Practical rule: 深色直筒牛仔褲配柔色緞面上衣，鞋子選低跟鞋或尖頭平底鞋，避免再加休閒圖案。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```
