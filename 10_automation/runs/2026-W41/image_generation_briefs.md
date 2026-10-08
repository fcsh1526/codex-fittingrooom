# Codex Image Generation Briefs

Use these briefs with Codex's in-workspace image generation flow. Store accepted candidates in `generated_images/` and score them in `image_review_template.csv`.

## 2026-W41-001 / M05 - 短領口薄外套與俐落短比例

- Internal model role: M05 visual around-20
- Reader projection: A very young adult reader who wants clean daily outfits that feel current, simple, and practical without drifting into teen or school styling.
- Visual profile: East Asian woman with an around-20 youthful adult look, soft oval face, fresh natural skin with visible human texture, dark brown shoulder-length bob with a soft side part, bright attentive eyes with relaxed naturally responsive expressions, petite-to-medium healthy proportions, clean daily polish.
- Prompt visual age language: around 20, youthful adult
- Outfit: 奶油白短版無鋪棉立領外套
- Palette / fabric / fit: 奶油白、白、可可棕 / 薄斜紋棉或輕量尼龍 / 短版立領、無鋪棉、可敞開
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 選一件無鋪棉短版立領外套，搭短袖棉上衣和直筒褲，室內扣上、室外敞開。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 想在冷氣房加外套，走到室外又怕太厚太悶。
- Opening hook: 外套先看領口與衣長
- Visual proof: 短立領與腰胯上方衣長一眼可見；外套敞開露出短袖，配直筒長褲，薄與短的關係清楚。
- Practical rule: 外層選無鋪棉短版立領，內搭短袖棉上衣，下身固定直筒褲。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W41-002 / M01 - 格紋單品與素色留白

- Internal model role: M01 visual early-20s
- Reader projection: A young adult reader who wants clean daily outfits that are current, approachable, and easy to adapt without feeling childish.
- Visual profile: East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
- Prompt visual age language: early 20s
- Outfit: 奶油白海軍藍薄格紋襯衫
- Palette / fabric / fit: 奶油白、海軍藍、炭灰 / 薄棉府綢 / 微寬鬆尖領、袖口可翻折
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 讓薄格紋襯衫成為唯一圖案，搭深色直筒褲和素色配件。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 喜歡格紋，但一穿上身就覺得整套太花、不像平日通勤。
- Opening hook: 格紋只放一件就夠
- Visual proof: 奶油白與海軍藍格紋只出現在上衣，炭灰直筒褲和黑鞋留白；不靠背景也能看懂主圖案位置。
- Practical rule: 一套只留一件格紋主角，其餘單品選素色，配色沿用格紋裡的深色。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W41-003 / M02 - 可可棕直筒丹寧

- Internal model role: M02 visual late-20s
- Reader projection: A practical adult reader who wants clean daily outfits that are current, wearable, and easy to adapt across work and leisure.
- Visual profile: East Asian woman with a late-20s youthful adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, natural warm fair skin with visible human texture, approachable composed expression, healthy slim-to-average proportions.
- Prompt visual age language: late 20s, youthful
- Outfit: 可可棕高腰直筒丹寧褲
- Palette / fabric / fit: 可可棕、奶油白、黑 / 中薄丹寧 / 高腰直筒、褲腳落在鞋面上方
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 用可可棕直筒丹寧配奶油白棉上衣，鞋包固定黑色。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 藍色牛仔褲穿膩了，卻不知道棕色丹寧怎麼搭才不沉重。
- Opening hook: 棕色牛仔褲配白上衣
- Visual proof: 可可棕褲子、奶油白上衣、黑鞋包三色分工明確；直筒褲腳停在鞋面上方。
- Practical rule: 可可棕直筒丹寧搭奶油白上衣，鞋包維持黑色，整套最多三種主色。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W41-004 / M03 - 放鬆剪裁與輕薄西裝

- Internal model role: M03 visual mid-30s
- Reader projection: A stylish adult reader who wants practical outfits with softness, confidence, and enough polish for work or weekend.
- Visual profile: East Asian woman with a well-maintained mid-30s look, softly defined oval face with gentle cheeks and balanced jawline, dark brown medium-to-long hair with polished natural movement, natural makeup, relaxed confident posture, healthy slim-to-average build, believable skin texture with normal human tonal variation.
- Prompt visual age language: mid 30s look, well-maintained
- Outfit: 米白輕薄單排扣西裝外套
- Palette / fabric / fit: 米白、白、深藍 / 輕薄混紡斜紋 / 微寬鬆單排扣、可翻袖
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 用無鋪棉輕薄西外搭棉質短袖上衣和直筒褲，保留一件正式外層即可。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 每天穿西裝上班很容易像制服，脫掉外套又少了正式感。
- Opening hook: 西裝裡面換成棉上衣
- Visual proof: 西外維持肩線與翻領，棉上衣露出簡單圓領；袖口翻折、直筒褲把正式和日常分成兩層。
- Practical rule: 無鋪棉西外配棉質短袖，褲子選直筒，袖口翻折一折即可。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W41-005 / M04 - 亮色包款與首飾單點

- Internal model role: M04 visual early-40s
- Reader projection: A polished mature reader who wants modern outfits that feel current, composed, elegant, and wearable without looking overly young or overly formal.
- Visual profile: East Asian woman with an elegant early-40s look, longer narrow oval face with defined cheekbones and a slightly sharper jawline, straight dark brown chin-to-shoulder bob with a clean side part, natural warm fair skin with believable fine texture and tonal variation, attentive intelligent eyes with naturally responsive subtle expressions, slightly taller average-slim healthy proportions, composed but not rigid editorial presence.
- Prompt visual age language: early 40s look, elegant
- Outfit: 鈷藍小肩包
- Palette / fabric / fit: 鈷藍、白、炭灰 / 霧面皮革或輕量合成皮 / 小容量、短肩帶、方弧輪廓
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 用一只鈷藍小肩包當唯一亮色，其餘服裝維持白、灰、黑。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 整身都穿黑白灰，拍照時常覺得沒有一個明確焦點。
- Opening hook: 中性色只亮一個配件
- Visual proof: 鈷藍只出現在小肩包，白上衣與炭灰直筒褲形成中性底盤；銀色耳飾尺寸小、不搶包。
- Practical rule: 亮色只放在一只小包，衣服控制在白、灰、黑，金屬配件選小尺寸。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```
