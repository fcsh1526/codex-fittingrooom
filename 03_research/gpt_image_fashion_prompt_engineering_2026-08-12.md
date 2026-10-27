# Mira × GPT Image：每日穿搭與高級紀實雜誌感提示詞研究

研究日期：2026-08-12  
研究範圍：GPT 圖片生成的提示詞工程、寫實人物、服飾呈現、參考圖一致性，以及 Mira 工作流的修正方向。  
本階段不生成圖片，也不做 A/B 測試。

## 1. 研究目標

讓 Mira 的圖片從「規格正確但像 AI 型錄」轉為：

> 一張真實生活中可能被攝影師捕捉到的每日穿搭照片；服裝一眼可讀，人物與環境可信，高級感來自選景、構圖、色彩與系列一致性，而不是磨皮、棚拍或過度戲劇化。

## 2. 官方資料的直接結論

### 2.1 使用穩定且可維護的提示詞結構

OpenAI 建議依「背景／場景 → 主體 → 關鍵細節 → 限制」的順序撰寫，並說明圖片用途。複雜要求適合使用短標籤或分段，不需要特殊的提示詞語法。[OpenAI GPT Image Prompting Guide：Prompting Fundamentals](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide#2-prompting-fundamentals)

對 Mira 的含意：每張圖先回答「這張圖要替受眾解決哪一個穿搭情境」，再寫人物、動作、服裝與攝影語言。

### 2.2 寫實感來自「被捕捉的真實瞬間」與材質，不是參數堆疊

官方寫實範例使用明確動作、自然光、真實皮膚與磨損材質，並要求畫面誠實、未擺拍、不美化、不重度修圖。官方也明確指出：詳細相機參數可能只被寬鬆理解；相機描述應主要用來控制高層次的觀感與構圖，不應期待精確的物理模擬。[OpenAI：Photorealistic Images that Feel “natural”](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide#43-photorealistic-images-that-feel-natural)

對 Mira 的含意：

- 保留「全片幅無反相機、自然 50mm 視角、胸口高度」作為視覺語言。
- 移除 `f/4、1/250 s、ISO 200、5200 K` 等固定曝光資料。
- 用「陰天窗光、室內環境光、正常色彩、皮膚紋理、零碎髮絲、衣料折痕、輕微顆粒與光學柔度」描述肉眼可見的結果。

### 2.3 人物圖要寫清楚動作、視線與物件互動

官方建議描述人物在畫面中的尺度、取景範圍、視線和手部互動，例如完整全身與雙腳、看向物件而非鏡頭、手自然握住物件。這些描述比抽象的「自然姿勢」更能控制動作幾何。[OpenAI：People, pose, and action](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide#2-prompting-fundamentals)

對 Mira 的含意：每張 Hero 只安排一個清楚、可繼續發展的動作，例如「已經跨出一步，同時輕扶肩背帶」，不要同時要求多個姿勢或情緒。

### 2.4 多張參考圖必須標明各自角色

官方建議逐張標示輸入圖的用途，並明說如何互相作用。編輯時要清楚區分「必須保持」與「可以改變」；虛擬試衣範例則鎖定人物身份，只更換服裝，並要求衣料垂墜、折痕、遮擋、光線和陰影一致。[OpenAI：Multi-image inputs](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide#2-prompting-fundamentals)；[OpenAI：Virtual Clothing Try-On](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide#52-virtual-clothing-try-on)

對 Mira 的含意：

- Image 1：臉部與髮型身份參考。
- Image 2：大致身形比例參考。
- 明說不要複製參考圖的棚拍光線、僵直姿勢、表情與服裝。
- 不再逐項列出眼鼻唇、膝高、臂長、手掌大小等十多個鎖定點。

### 2.5 先有乾淨基礎提示詞，再做單一修改

官方並不否定長提示詞，但建議從乾淨的基礎版本開始，以一次一項的小修改迭代；在後續編輯中重申真正不能漂移的內容。[OpenAI：Iterate instead of overloading](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide#2-prompting-fundamentals)

這不是 A/B 測試。Mira 的新原則是：先生成一張符合內容目標的 Hero；若只錯一項，就對同一張圖做一次局部修正，而不是重寫整份提示詞後生成另一個競品版本。

### 2.6 原生直式尺寸可直接指定

GPT Image 2 支援符合尺寸條件的自訂比例，官方也列出直式輸出。對 Mira 而言，Reel 起始圖應直接生成 9:16，不再先生成其他比例再裁切。[OpenAI Image Generation Guide：Size and quality options](https://developers.openai.com/api/docs/guides/image-generation#size-and-quality-options)

## 3. 現有 Mira 提示詞為何容易失真

本次對照檔案：`10_automation/runs/2026-W33/generated_images/2026-W33-001/reel/hero_A_prompt_v1.md`。

現有提示詞約 600 多個英文單字，同時包含身份、身材量測、穿搭、構圖安全區、相機曝光、光線物理、解剖、負面詞與平台裁切要求。主要問題不是單一「污染詞」，而是四類要求混在同一層：

1. **內容意圖被技術規格淹沒**：觀眾應該先看懂「雨天通勤的輕薄外套」，模型卻同時要處理大量攝影與幾何鎖定。
2. **真實與完美互相衝突**：`unretouched documentary` 與嚴密臉型鎖定、完美解剖、全面一致的單一光源並存，容易產生精緻但僵硬的 AI 人像。
3. **固定曝光資料沒有可靠收益**：官方明確說詳細相機規格只會被寬鬆理解。
4. **負面清單過長**：多次描述不要什麼，會分散主要的正向場景、動作和服裝訊號。
5. **參考圖本身帶有棚拍質感**：即使提示詞說不要複製，光滑皮膚、正面對稱與均勻光線仍可能成為強烈視覺先驗。這不是只靠增加負面詞就能完全消除的問題。

## 4. 新的 Mira 提示詞架構

以下字數是 Mira 的工作流建議，不是 OpenAI 的硬性限制：Hero 基礎提示詞以 **120–220 個英文單字**為目標。

```text
Use case / Asset
說明用途、平台比例，以及這張圖要傳達的單一穿搭決策。

Input roles
Image 1 是身份參考；Image 2 是大致身形參考。
說明哪些視覺內容不要從參考圖複製。

Scene + one action
真實地點、季節／天氣、人物正在做的一個動作、視線與手部互動。

Outfit
由外到內列出服飾、顏色、材質、版型；補充最容易漂移的一項服裝特徵。

Photographic language
photorealistic、candid、unretouched documentary fashion editorial；
全片幅無反與自然 50mm 視角只控制整體觀感；描述可見的光線和材質。

Composition + short constraints
取景範圍、雙腳／服裝是否完整、環境比例。
最後只留 3–5 個真正必要的限制。
```

### 硬規則

- 一張圖只有一個主要穿搭命題、一個場景、一個可見動作。
- 相機只寫系統觀感、焦段視角、機位和取景；不寫固定曝光四要素。
- 「高級雜誌感」必須拆成可見結果：克制配色、真實選景、乾淨構圖、自然姿勢、材質可讀、系列一致。
- 負面限制最多一行，優先保留：無文字、無標誌、無浮水印、無棚拍型錄姿勢、無錯季厚重服裝。
- 手指、鞋底接觸、人物比例、裁切安全區、服裝漂移都放到 QA 清單，不塞進基礎提示詞。

## 5. W33-001 可直接使用的 Hero 提示詞

```text
Use case: photorealistic-natural.

Asset: a native 9:16 opening frame for Mira. It should immediately communicate a light outer layer for a rainy summer commute.

Input images: Image 1 is the woman’s identity and hairstyle reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy either reference’s studio pose, lighting, background or clothes.

A candid real photograph of the same young East Asian woman leaving an ordinary office lobby in Taiwan on a rain-damp summer morning. She is mid-step, looking toward the street, lightly holding a small dark-brown shoulder bag strap.

Her outfit is immediately readable: an olive cropped, unlined matte summer windbreaker worn open; a cream sleeveless cotton top; deep-navy high-waisted ankle-length straight trousers; and off-white low-top casual shoes. The windbreaker must look thin, airy and unpadded, with its hem moving slightly as she walks.

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look, natural 50mm perspective at chest height. Soft overcast window light with subtle indoor ambient light, realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest and unposed; polished through framing, color and material detail rather than beauty retouching.

Full body and both shoes visible, with enough surrounding architecture to establish the real location. No readable text, logos or watermark. Avoid studio polish, catalog posing and winter-weight clothing.
```

這個版本保留：身份、穿搭、台灣雨天通勤、原生 9:16、全片幅無反、50mm、完整鞋子與高級紀實感。它移除：曝光數字、身體量測清單、中央 70%／頂部 8% 等操作規格、長負面清單和不必要的物理光線重複。

## 6. 可重複使用的每日穿搭模板

```text
Use case: photorealistic-natural.

Asset: a native [9:16 / target ratio] image for Mira, a daily-outfit fashion magazine. It should communicate [one dressing decision] at first glance.

Input images: Image 1 is the model’s face and hairstyle identity reference. Image 2 is a loose body-proportion reference. Keep her recognizable, but do not copy the references’ pose, expression, studio lighting, background, or clothes.

A candid real photograph of the same woman at [specific ordinary location] during [season, time and weather]. She is [one physically clear action], looking [gaze direction], while [one natural hand–object interaction].

Her outfit is immediately readable: [outer layer], [top], [bottom], [shoes], [one accessory]. Emphasize [the single garment feature most likely to drift: fabric weight, hem, fit, opening, or layering].

Photorealistic, unretouched documentary fashion editorial. Full-frame mirrorless look with a natural [50mm / justified focal-length] perspective at [eye/chest] height. [Visible natural light] mixed with [believable ambient light], realistic skin texture, flyaway hairs, lived-in fabric folds, restrained grain and slight optical softness. Honest, unposed and everyday; polished through framing, color and material detail rather than beauty retouching.

[Framing and environment instruction]. No readable text, logos or watermark. Avoid studio polish, catalog posing and [one content-specific failure].
```

## 7. 衍生圖片的簡短編輯提示詞

### 7.1 Carousel 的穿搭細節圖

```text
Edit the accepted Hero into a closer outfit-detail photograph. Keep the same woman, exact garments, colors, location, weather, and natural light. Change only the framing and her small hand action: show the windbreaker opening, cream top, trouser waist, and bag strap at a natural waist-up distance. Preserve realistic fabric drape and skin texture. Keep the moment candid and unretouched. No new accessories, text, logos or watermark.
```

### 7.2 同一系列的環境沉浸圖

```text
Using the accepted Hero as the identity, outfit and visual anchor, place the same woman a few steps farther outside under the covered office entrance. She continues the same walk and looks toward the wet street. Preserve her exact outfit construction and the rainy-summer lighting. Use a wider environmental composition with the person smaller in frame, natural 50mm perspective, restrained color and ordinary Taiwan street detail. Keep it grounded, candid and unretouched. No cinematic grading, text, logos or watermark.
```

這兩段屬於對「已接受 Hero」的單一編輯，不應重新貼上完整 Hero 提示詞。

## 8. 工作流修正建議

```text
每週趨勢資料
→ 每日只定義一個穿搭決策
→ 選擇一個真實場景與一個可見動作
→ 套用 120–220 字 Hero 基礎提示詞
→ 直接生成原生目標比例
→ 以獨立 QA 清單檢查
→ 若只有一項錯誤，對同一張圖做單一局部修正
→ Hero 接受後，才衍生 Detail／Environment／影片起始畫面
```

### 生成前必填欄位

1. 今天替受眾解決的穿搭決策。
2. 季節、天氣、時間與真實地點。
3. 一個能看懂的動作。
4. 精確服裝清單與最容易漂移的一項材質／版型。
5. 圖片用途與比例。

### 生成後 QA（不放入提示詞）

- 人物身份是否可辨識，但沒有複製參考圖棚拍質感。
- 服裝季節、厚薄、版型、層次與顏色是否正確。
- 手部互動、雙腳接地、人物比例與遮擋是否可信。
- 光線方向、人物與環境色溫、接觸陰影是否一致。
- 皮膚、頭髮、衣料是否有真實細節，而非塑膠感。
- 平台安全區與裁切是否可用。
- 圖片是否真的回答當日穿搭命題。

## 9. 應修改與應保留的現行規則

| 類別 | 決定 |
|---|---|
| 全片幅無反相機觀感 | 保留 |
| 自然 50mm 視角與胸口高度 | 保留，依特殊畫面需要才改 |
| `photorealistic`、紀實、未修圖 | 保留，改成可見材質與真實瞬間 |
| 原生 9:16 Reel 圖 | 保留 |
| 精確服裝清單 | 保留，但只強調一項最容易漂移的特徵 |
| M01–M05 身份參考 | 保留，簡化角色說明 |
| 固定 f 值、快門、ISO、白平衡 | 從提示詞移除 |
| 身體各部位逐項量測鎖定 | 移除，改為大致身形參考與生成後 QA |
| 中央 70%、頂部 8% 等安全區數字 | 移到版面／QA 規格 |
| 長負面提示詞 | 改成最後一行 3–5 項關鍵限制 |
| A/B/C 同時生成與評分 | 停止；先接受一張 Hero，再做必要衍生 |

## 10. 對「為什麼其他 GPT 生圖較好」的結論

這次資料支持的判斷是：**模型不是主要瓶頸，Mira 現有的控制方式才是。** 一般對話中的 GPT 圖片通常收到一個明確場景與風格要求，因此模型能自行完成攝影決策；Mira 舊提示詞則把內容、攝影、幾何、平台、解剖與 QA 同時強制進入生成階段，並使用帶棚拍質感的身份參考圖，結果就容易正確但不自然。

第一優先修正不是增加更多「防 AI」詞，而是：縮短基礎提示詞、讓真實動作與場景成為主訊號、把 QA 從提示詞移出，並避免讓參考圖的棚拍質感主導結果。

## 11. 主要官方來源

- [OpenAI — GPT Image Generation Models Prompting Guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- [OpenAI — Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [OpenAI — GPT Image 2 model](https://developers.openai.com/api/docs/models/gpt-image-2)
