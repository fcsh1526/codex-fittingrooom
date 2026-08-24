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
- Dressing decision: 先用無鋪棉的高領薄夾克做可脫式外層，保留夏季內搭。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 早晚需要外套，但厚外套一穿就悶、進室內又無法活動。
- Opening hook: 外套先買薄，八月就能穿
- Visual proof: 短版高領外層落在腰線附近，內搭貼身短袖，下身為窄直筒褲；開扣與拉起高領的前後對照看得出用途。
- Practical rule: 高領外套選薄身無鋪棉款，內搭短袖、下身窄直筒，比例只保留一個寬鬆點。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W35-002 / M01 - 深棕麂皮觸感

- Internal model role: M01 visual early-20s
- Reader projection: A young adult reader who wants clean daily outfits that are current, approachable, and easy to adapt without feeling childish.
- Visual profile: East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
- Prompt visual age language: early 20s
- Outfit: 深棕麂皮肩背包
- Palette / fabric / fit: 巧克力棕、奶油白、靛藍 / 霧面麂皮 / 中小型柔軟方形
- Occasion: 咖啡廳
- Content engine: utility_with_immersion
- Dressing decision: 把深棕麂皮放在包款，搭配白上衣與深靛丹寧，讓觸感成為唯一重點。
- One visible action: 剛放下咖啡杯，視線自然看向窗外，另一手停在隨身包旁
- Audience problem: 衣櫃都是黑白基本款，想要有秋季感又怕一換季就穿得太厚。
- Opening hook: 只換一個包，秋季感就出來
- Visual proof: 霧面麂皮包與光滑棉質、乾淨丹寧形成材質對比；全身只用巧克力棕一個深色焦點。
- Practical rule: 麂皮只放在一個配件，服裝用白上衣加深靛直筒丹寧，避免同時加入厚外套。
- Scene: assigned_by_codex
- Canva master: v3-E / Mira Template Master v3 - E Cross-Boundary Weekend Air
- Exact slot targets: A/cover_image=1120x1050 (1.0667:1); B/motion_crop=1120x410 (2.7317:1); C/detail_image=1060x1010 (1.0495:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W35-003 / M03 - 運動外層配裙裝

- Internal model role: M03 visual mid-30s
- Reader projection: A stylish adult reader who wants practical outfits with softness, confidence, and enough polish for work or weekend.
- Visual profile: East Asian woman with a well-maintained mid-30s look, softly defined oval face with gentle cheeks and balanced jawline, dark brown medium-to-long hair with polished natural movement, natural makeup, relaxed confident posture, healthy slim-to-average build, believable skin texture with normal human tonal variation.
- Prompt visual age language: mid 30s look, well-maintained
- Outfit: 深海軍藍輕量運動外套
- Palette / fabric / fit: 海軍藍、灰白、深灰 / 薄尼龍 / 短版立領、袖口微收
- Occasion: 上班
- Content engine: utility_with_immersion
- Dressing decision: 用一件乾淨的輕量運動外層壓低裙裝的正式感，鞋子保持平底。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 裙裝常被穿得太正式或太甜，平日上班不敢穿。
- Opening hook: 裙子太甜？加一件運動外層
- Visual proof: 霧面運動外層的水平拉鍊與中長窄裙的垂直線條並列，鞋子以平底球鞋收住，正式與休閒界線清楚。
- Practical rule: 中長裙配一件短版輕量運動外層，鞋子選平底球鞋，其他配件不加運動標誌。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W35-004 / M02 - 窄領巾與蝴蝶結細節

- Internal model role: M02 visual late-20s
- Reader projection: A practical adult reader who wants clean daily outfits that are current, wearable, and easy to adapt across work and leisure.
- Visual profile: East Asian woman with a late-20s youthful adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, natural warm fair skin with visible human texture, approachable composed expression, healthy slim-to-average proportions.
- Prompt visual age language: late 20s, youthful
- Outfit: 黑白細窄絲巾
- Palette / fabric / fit: 黑白、白、深藍 / 輕薄絲質 / 窄長方形
- Occasion: 辦公室
- Content engine: utility_with_immersion
- Dressing decision: 用一條窄絲巾在領口做一個小蝴蝶結，其他配件退到最少。
- One visible action: 自然行走中，視線離開鏡頭，一手與包或衣物產生可信互動
- Audience problem: 每天都穿白上衣，但加項鍊又覺得太制式、太像上班制服。
- Opening hook: 白上衣只要多一個小結
- Visual proof: 白襯衫領口出現窄絲巾蝴蝶結，胸前不再堆項鍊；下身純色直筒褲，焦點集中且第一眼可辨識。
- Practical rule: 白上衣只加一條窄絲巾，結放在鎖骨下方，包與鞋維持同色中性調。
- Scene: assigned_by_codex
- Canva master: v3-A / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- Exact slot targets: A/cover_image=1160x1190 (0.9748:1); B/motion_crop=980x430 (2.2791:1); C/detail_image=1080x1080 (1.0:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W35-005 / M04 - 深色直筒丹寧與柔和上衣

- Internal model role: M04 visual early-40s
- Reader projection: A polished mature reader who wants modern outfits that feel current, composed, elegant, and wearable without looking overly young or overly formal.
- Visual profile: East Asian woman with an elegant early-40s look, longer narrow oval face with defined cheekbones and a slightly sharper jawline, straight dark brown chin-to-shoulder bob with a clean side part, natural warm fair skin with believable fine texture and tonal variation, attentive intelligent eyes with naturally responsive subtle expressions, slightly taller average-slim healthy proportions, composed but not rigid editorial presence.
- Prompt visual age language: early 40s look, elegant
- Outfit: 深靛直筒丹寧褲
- Palette / fabric / fit: 深靛藍、柔霧粉、米灰 / 薄身棉質丹寧 / 中高腰直筒
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 用深靛直筒丹寧搭一件薄緞面柔色上衣，再以低跟鞋完成通勤比例。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 想穿丹寧去上班，但牛仔褲常讓整套看起來像週末休閒服。
- Opening hook: 丹寧上班，關鍵在上衣材質
- Visual proof: 深靛直筒丹寧的硬挺線條對上柔霧緞面上衣的光澤與垂墜，鞋子改為低跟而非球鞋，場合差異一眼可見。
- Practical rule: 深靛直筒丹寧配一件薄緞面柔色上衣，鞋子選低跟或尖頭平底，避免再加休閒圖案。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```
