# M05 002-L01 Carousel A｜提示詞與單次版型修正

內建 `image_gen`。三張生成參照依序為 M05 核准臉部、M05 核准全身比例、W37 L01 已核准 Reel 全身圖。v2 編輯只以上一張 v1 候選為輸入。兩版輸出均已留存，v1 因 Canva 裁切超限退件；使用者於 2026-09-30 回覆「可以，沿用這張」，核准 v2 作為 Carousel A 與後續 B/C 的服裝、人物及場景基準。

## v1 Hero prompt

```text
Use case: photorealistic-natural. Create Carousel Hero A for Mira's approachable Taiwan daily-outfit fashion magazine, a separate near-square portrait composition for a 1240×1350 Canva cover slot (width-to-height 0.9185), full person head to both shoes, outfit readable immediately. The dressing decision is a hip-bone-length short jacket with high-waisted wide trousers so the waistline and trouser drape stay visible.

Input image 1 is the approved M05 face and hairstyle identity anchor; image 2 is her approved full-body proportion anchor. Neither reference supplies this week's clothes, pose or background. Input image 3 is the approved W37 L01 Reel still and is the exact wardrobe, styling, bag placement, architecture-studio scene and light reference, but this Carousel Hero must be a newly composed photograph, not a crop or duplicate of that 9:16 image.

Show this same youthful adult East Asian woman in a small architecture studio beside an open sample table under viewer-left window daylight. She stands upright with a slight natural weight shift and gently places one slim material swatch flat on the table corner; face remains clearly visible and relaxed, and the action does not cover the jacket hem or waistband. Exact clothes: optical-white unpadded short cotton-twill jacket ending at the hip bone, pale-blue short-sleeve cotton shirt tucked into deep-indigo high-waisted lightweight wide trousers, black flat loafers, small caramel-brown shoulder bag. Both trouser hems hang above the floor and show the shoe toes.

Photograph with a full-frame mirrorless 50mm prime at chest height, level optical axis. Available daylight and plausible room bounce, contact shadows, natural skin texture, flyaway hairs, lived-in folds, restrained grain and slight optical softness. Compose for the cover slot with enough margin around head and shoes and a physically coherent sample table; polished through framing and materials, approachable rather than luxury advertising. No readable text, logo, watermark, extra person or fashion-elongated anatomy.
```

## v2 targeted edit prompt

```text
Use case: precise-object-edit / identity-preserve. This is a single targeted canvas-width correction of the supplied Mira W37 L01 Carousel Hero A candidate. Expand the photograph horizontally on both sides into a SQUARE 1:1 frame, so it can later be center-cropped to the Canva cover slot width:height 0.9185 without cutting the woman's head or shoes. Keep the photographed woman at exactly the same apparent size, central position and upright posture. Preserve her face, dark side-parted bob, natural expression, both hands and their existing interaction, optical-white cropped jacket, pale-blue tucked shirt, deep-indigo high-waisted wide trousers, black loafers, caramel-brown shoulder bag, and their colors and lengths exactly. Do not zoom in, crop vertically or redesign any outfit item. Extend only the left and right edges with physically continuous architecture-studio window, sample table, plant, pinned boards, shelves, floor and matching daylight/perspective; no repeated or floating objects. Keep the original head-to-shoes content intact in the center. Photoreal editorial camera image, no readable text, logo, watermark or additional person.
```

v2 實際輸出為 1254×1254，與 v1 比較，場景變寬且人物視覺尺寸略縮，故紀錄為修正版候選，不宣稱逐像素保留。
