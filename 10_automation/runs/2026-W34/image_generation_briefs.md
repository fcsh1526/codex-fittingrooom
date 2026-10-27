# Codex Image Generation Briefs

Use these briefs with Codex's in-workspace image generation flow. Store accepted candidates in `generated_images/` and score them in `image_review_template.csv`.

## 2026-W34-001 / M03 - 寬版牛津襯衫日常穿法

- Internal model role: M03 visual mid-30s
- Reader projection: A stylish adult reader who wants practical outfits with softness, confidence, and enough polish for work or weekend.
- Visual profile: East Asian woman with a well-maintained mid-30s look, softly defined oval face with gentle cheeks and balanced jawline, dark brown medium-to-long hair with polished natural movement, natural makeup, relaxed confident posture, healthy slim-to-average build, believable skin texture with normal human tonal variation.
- Prompt visual age language: mid 30s look, well-maintained
- Outfit: 海軍藍寬版純棉牛津襯衫；淺藍直筒牛仔褲；白色帆布鞋；深棕帆布側背包
- Palette / fabric / fit: 海軍藍／淺藍／白色／深棕 / 純棉牛津布／丹寧／帆布 / 上衣寬版落肩；下身高腰直筒
- Occasion: 通勤／上課
- Content engine: utility_with_immersion
- Dressing decision: 選寬版落肩牛津襯衫，袖口捲至手肘，下擺自然放在直筒牛仔褲外
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 牛津襯衫一穿就像制服，紮進褲子又太正式
- Opening hook: 牛津襯衫不紮，也能穿得俐落
- Visual proof: 完整看見寬版襯衫下擺、直筒牛仔褲褲型與捲起袖口
- Practical rule: 上衣選寬版落肩，下身維持直筒，不加入其他制服元素
- Scene: Taipei office lobby with soft daylight
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W34-002 / M04 - 微鬆西裝外套日常穿法

- Internal model role: M04 visual early-40s
- Reader projection: A polished mature reader who wants modern outfits that feel current, composed, elegant, and wearable without looking overly young or overly formal.
- Visual profile: East Asian woman with an elegant early-40s look, longer narrow oval face with defined cheekbones and a slightly sharper jawline, straight dark brown chin-to-shoulder bob with a clean side part, natural warm fair skin with believable fine texture and tonal variation, attentive intelligent eyes with naturally responsive subtle expressions, slightly taller average-slim healthy proportions, composed but not rigid editorial presence.
- Prompt visual age language: early 40s look, elegant
- Outfit: 炭灰薄款無內裡微鬆西裝外套；黑色素面無袖上衣；炭灰直筒西裝褲；黑色尖頭平底鞋；深棕小型肩背包；細版金屬耳環
- Palette / fabric / fit: 炭灰／黑色／深棕／銀色 / 薄西裝料／棉質／霧面皮革 / 外套微鬆有肩線；內搭合身；下身直筒
- Occasion: 上班／簡報
- Content engine: utility_with_immersion
- Dressing decision: 改用薄款無內裡的微鬆西裝外套，內層只留一件素色無袖上衣
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 西裝外套太像正式套裝，平常上班以外不知道怎麼穿
- Opening hook: 西裝外套，先把內搭簡化
- Visual proof: 外套敞開、內搭線條乾淨，下身直筒並完整呈現放鬆輪廓
- Practical rule: 外套已有明確肩線時，內搭與配件都維持簡單
- Scene: simple studio wall with neutral shadows
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W34-003 / M02 - 皮革鞋包調整通勤感

- Internal model role: M02 visual late-20s
- Reader projection: A practical adult reader who wants clean daily outfits that are current, wearable, and easy to adapt across work and leisure.
- Visual profile: East Asian woman with a late-20s youthful adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, natural warm fair skin with visible human texture, approachable composed expression, healthy slim-to-average proportions.
- Prompt visual age language: late 20s, youthful
- Outfit: 挺度適中的白色棉質圓領短袖；深海軍藍高腰直筒褲；深棕方頭樂福鞋；深棕小型肩背包
- Palette / fabric / fit: 白色／深海軍藍／深棕 / 棉質／薄西裝料／霧面皮革 / 上衣自然合身；下身高腰直筒；鞋型方頭低跟
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 不穿八月不實用的皮外套，改用深棕皮革樂福鞋與同色小包增加俐落感
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 白色T恤和直筒褲舒服，但穿去上班容易顯得太休閒
- Opening hook: 白色T恤去上班，鞋子先換掉
- Visual proof: 完整呈現白色T恤、直筒褲與同一深棕色鞋包的關係
- Practical rule: 基本款服裝只加一組同色皮革鞋包，其他配件保持乾淨
- Scene: department store fitting area
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W34-004 / M05 - 黑色吊帶洋裝日常疊穿

- Internal model role: M05 visual around-20
- Reader projection: A very young adult reader who wants clean daily outfits that feel current, simple, and practical without drifting into teen or school styling.
- Visual profile: East Asian woman with an around-20 youthful adult look, soft oval face, fresh natural skin with visible human texture, dark brown shoulder-length bob with a soft side part, bright attentive eyes with relaxed naturally responsive expressions, petite-to-medium healthy proportions, clean daily polish.
- Prompt visual age language: around 20, youthful adult
- Outfit: 合身白色棉質圓領短袖；霧面黑色直身吊帶洋裝；黑色平底鞋；酒紅小型肩背包
- Palette / fabric / fit: 黑色／白色／酒紅 / 棉質／霧面緞面／霧面皮革 / 內搭合身；洋裝直身至膝下
- Occasion: 日常外出／早午餐
- Content engine: utility_with_immersion
- Dressing decision: 選霧面直身吊帶洋裝，裡面加一件合身白色短袖，改成白天可以直接穿的層次
- One visible action: 剛放下咖啡杯，視線自然看向窗外，另一手停在隨身包旁
- Audience problem: 黑色吊帶洋裝容易像睡衣，只敢在約會或晚餐時穿
- Opening hook: 吊帶洋裝加一件白T，就能日常穿
- Visual proof: 白色短袖領口與袖子清楚露出，黑色吊帶洋裝保持直身且沒有強烈光澤
- Practical rule: 內搭要合身，洋裝要直身且霧面
- Scene: MRT-adjacent weekday walkway
- Canva master: v3-A / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- Exact slot targets: A/cover_image=1160x1190 (0.9748:1); B/motion_crop=980x430 (2.2791:1); C/detail_image=1080x1080 (1.0:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W34-005 / M01 - 絲巾包帶配色

- Internal model role: M01 visual early-20s
- Reader projection: A young adult reader who wants clean daily outfits that are current, approachable, and easy to adapt without feeling childish.
- Visual profile: East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
- Prompt visual age language: early 20s
- Outfit: 奶油白無袖棉質上衣；卡其高腰直筒褲；淺棕樂福鞋；深棕小型托特包；藍棕印花窄版絲巾綁於包帶
- Palette / fabric / fit: 奶油白／卡其／淺棕／深棕／藍色 / 棉質／薄西裝料／霧面皮革／輕薄仿絲 / 上衣自然合身；下身高腰直筒；絲巾窄版
- Occasion: 通勤／週末
- Content engine: utility_with_immersion
- Dressing decision: 把窄版印花絲巾綁在包帶根部，衣服只使用素色
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 想用絲巾增加配色，但台灣八月繫在頸部太熱，也會重複先前的絲巾襯衫內容
- Opening hook: 天氣太熱，絲巾改綁在包上
- Visual proof: 畫面看見素色穿搭、深棕包款與包帶上的單條窄版絲巾
- Practical rule: 絲巾保留一個主色呼應鞋或包，全身不再加入第二種印花
- Scene: quiet cafe street in Taipei
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```
