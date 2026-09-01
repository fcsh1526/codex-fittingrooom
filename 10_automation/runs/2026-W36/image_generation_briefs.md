# Codex Image Generation Briefs

Use these briefs with Codex's in-workspace image generation flow. Store accepted candidates in `generated_images/` and score them in `image_review_template.csv`.

## 2026-W36-001 / M05 - 輕薄機能疊穿

- Internal model role: M05 visual around-20
- Reader projection: A very young adult reader who wants clean daily outfits that feel current, simple, and practical without drifting into teen or school styling.
- Visual profile: East Asian woman with an around-20 youthful adult look, soft oval face, fresh natural skin with visible human texture, dark brown shoulder-length bob with a soft side part, bright attentive eyes with relaxed naturally responsive expressions, petite-to-medium healthy proportions, clean daily polish.
- Prompt visual age language: around 20, youthful adult
- Outfit: 薄風衣＋背心洋裝
- Palette / fabric / fit: 霧灰、奶油白、橄欖綠 / 薄尼龍、棉 / 可脫外層、內層柔軟
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 用無鋪棉薄風衣罩在柔軟內搭外，外層可脫，穿搭主體不依賴厚度。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 早晚想有外層，進冷氣房卻不想穿得悶重。
- Opening hook: 外套選薄，換季就能穿
- Visual proof: 同一套以薄風衣拉鍊關閉與敞開呈現；外層有結構、內層是柔軟洋裝，兩層功能一眼分開。
- Practical rule: 薄風衣只當可脫外層，內搭選背心或細肩帶洋裝，顏色維持兩到三色。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W36-002 / M02 - 短外套配長流動下身

- Internal model role: M02 visual late-20s
- Reader projection: A practical adult reader who wants clean daily outfits that are current, wearable, and easy to adapt across work and leisure.
- Visual profile: East Asian woman with a late-20s youthful adult look, softly defined oval face, gentle cheeks, balanced jawline, dark brown medium-to-long hair with natural movement, natural warm fair skin with visible human texture, approachable composed expression, healthy slim-to-average proportions.
- Prompt visual age language: late 20s, youthful
- Outfit: 短版夾克＋長寬褲
- Palette / fabric / fit: 深靛藍、光學白、炭灰 / 薄棉斜紋、薄西裝料 / 落腰短版、高腰長版
- Occasion: 上班
- Content engine: utility_with_immersion
- Dressing decision: 用短版外層停在腰骨、配薄料長寬褲，保留活動量但讓長短差清楚。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 不想穿緊身褲，但寬鬆上下一起穿又容易沒有比例。
- Opening hook: 上短下長，寬褲不拖比例
- Visual proof: 短夾克下襬落在腰骨，長寬褲從腰線直落鞋面；前後景都能看出兩段長度。
- Practical rule: 外層選落腰短版，下身選高腰薄料長寬褲，上衣只露出一小段。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W36-003 / M01 - 麂皮質感小面積入秋

- Internal model role: M01 visual early-20s
- Reader projection: A young adult reader who wants clean daily outfits that are current, approachable, and easy to adapt without feeling childish.
- Visual profile: East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
- Prompt visual age language: early 20s
- Outfit: 棉麻基本款＋麂皮配件
- Palette / fabric / fit: 焦糖棕、奶油白、黑 / 麂皮、棉麻 / 輕薄服裝、一個觸感焦點
- Occasion: 週末
- Content engine: utility_with_immersion
- Dressing decision: 只放一個麂皮配件，讓夏季棉麻衣服先承接觸感變化。
- One visible action: 自然行走中，視線離開鏡頭，一手與包或衣物產生可信互動
- Audience problem: 想有秋季質感，但現在穿全套麂皮太熱也不實用。
- Opening hook: 麂皮先買一個就夠
- Visual proof: 奶油白棉麻服裝保持輕盈，焦糖麂皮包成為唯一明顯觸感焦點；材質對比在近身畫面可見。
- Practical rule: 夏季棉麻套裝只搭一個焦糖麂皮包或鞋，其他配件改用光滑皮革。
- Scene: assigned_by_codex
- Canva master: v3-C / Mira Template Master v3 - C Cross-Boundary Noir
- Exact slot targets: A/cover_image=1230x1350 (0.9111:1); B/motion_crop=1000x460 (2.1739:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W36-004 / M04 - 絲巾效果與緞面垂墜

- Internal model role: M04 visual early-40s
- Reader projection: A polished mature reader who wants modern outfits that feel current, composed, elegant, and wearable without looking overly young or overly formal.
- Visual profile: East Asian woman with an elegant early-40s look, longer narrow oval face with defined cheekbones and a slightly sharper jawline, straight dark brown chin-to-shoulder bob with a clean side part, natural warm fair skin with believable fine texture and tonal variation, attentive intelligent eyes with naturally responsive subtle expressions, slightly taller average-slim healthy proportions, composed but not rigid editorial presence.
- Prompt visual age language: early 40s look, elegant
- Outfit: 緞面中長裙＋素色背心
- Palette / fabric / fit: 香檳、黑、酒紅 / 緞面、細針織 / 上短下垂墜
- Occasion: 晚餐
- Content engine: utility_with_immersion
- Dressing decision: 以一件緞面中長裙建立垂墜焦點，上身保持素色與短比例。
- One visible action: 自然行走中，視線離開鏡頭，一手與包或衣物產生可信互動
- Audience problem: 基本款穿得很乾淨，拍照卻沒有一個看得懂的造型重點。
- Opening hook: 一件緞面裙就有焦點
- Visual proof: 霧面素色背心對上有光澤的緞面裙，裙身裹身線與垂墜方向清楚，配件不搶主角。
- Practical rule: 緞面中長裙配素色短版上衣，腰間只加細腰帶，不再疊第二個花紋。
- Scene: assigned_by_codex
- Canva master: v3-A / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- Exact slot targets: A/cover_image=1160x1190 (0.9748:1); B/motion_crop=980x430 (2.2791:1); C/detail_image=1080x1080 (1.0:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```

## 2026-W36-005 / M03 - 深紅色小面積亮點

- Internal model role: M03 visual mid-30s
- Reader projection: A stylish adult reader who wants practical outfits with softness, confidence, and enough polish for work or weekend.
- Visual profile: East Asian woman with a well-maintained mid-30s look, softly defined oval face with gentle cheeks and balanced jawline, dark brown medium-to-long hair with polished natural movement, natural makeup, relaxed confident posture, healthy slim-to-average build, believable skin texture with normal human tonal variation.
- Prompt visual age language: mid 30s look, well-maintained
- Outfit: 黑灰基底＋深紅小包
- Palette / fabric / fit: 黑、炭灰、櫻桃紅 / 針織、光滑皮革 / 俐落基底、小尺寸配件
- Occasion: 通勤
- Content engine: utility_with_immersion
- Dressing decision: 全身維持黑灰，只放一個深紅配件，把色彩控制在可日常使用的尺度。
- One visible action: 已經向目的地方向跨出一步，視線看向前方，一手自然整理肩背包或外套
- Audience problem: 衣櫃多是黑白灰，想加顏色又怕一穿就太高調。
- Opening hook: 黑灰穿搭只加一個紅
- Visual proof: 炭灰上衣與黑褲形成穩定底色，櫻桃紅小包位於腰線附近成為唯一彩色區塊。
- Practical rule: 黑灰基底只選一個櫻桃紅包或鞋，其他配件全部回到黑、銀或深棕。
- Scene: assigned_by_codex
- Canva master: v3-B / Mira Template Master v3 - B Cross-Boundary Symmetric
- Exact slot targets: A/cover_image=1240x1350 (0.9185:1); B/motion_crop=1140x560 (2.0357:1); C/detail_image=1180x1350 (0.8741:1)

### Production instruction

```text
Use 11_skills/mira-image-daily/scripts/prepare_daily_image_job.py as the only prompt generator.
Generate and approve one Hero A first. B Motion and C Detail are optional production derivatives, not A/B tests, and may be created only from the accepted Hero when the publishing format needs them.
Keep prompt-generation rules in the Mira skill and image standard; keep anatomy, contact-shadow, identity, crop-safety, and platform checks in the separate review sheet.
```
