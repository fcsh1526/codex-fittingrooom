# Grok Imagine 提示詞模板

## 使用模式

Grok Imagine 目前要分成兩種模式，不要混用：

1. **換裝 / identity-preserving edit 模式**：已經有 Mika Lin 的參考圖時使用。這是 Day 3 測試的主模式，重點是保留人物，只換衣服。
2. **從零生成 / character generation 模式**：還沒有 Mika Lin 參考圖，或要重新建立人物基準圖時使用。重點是生成同一個虛擬人物。

Day 3 的 `day3_grok_prompts.md` 使用的是第 1 種模式，因為我們要測 Grok 是否能根據參考圖穩定換衣。

## 模式 1：換裝 / identity-preserving edit

適用情境：
- 已有 Mika Lin 固定虛擬人物參考圖。
- 使用 Grok Imagine 的圖片輸入或 edit 流程。
- 目標是保留臉、髮型、膚色、身形、姿勢、光線與背景，只換衣服。

模板：

```text
Using the attached fictional AI virtual creator reference image as the subject, keep the same fictional identity, face, hairstyle, skin tone, body proportions, pose, lighting and background. Only replace the outfit.

Dress Mika Lin in `{clothing_item}` in `{color_palette}`, made of `{fabric}`, with `{fit}` fit.

Styling: `{styling_rules}`.

Pose: `{pose}`.

Background: `{background}`.

Camera style: `{camera_style}`, vertical fashion social media image, clear full outfit, clean composition.

Do not alter identity. Do not create a real person likeness. Do not add visible brand logos. Output 3-4 variations.
```

Negative prompt:

```text
AI virtual outfit only; no real person; no celebrity; no childlike appearance; no school uniform; no nudity; no sexualized pose; no visible brand logos; no luxury logo; no fake brand endorsement; no distorted hands; no extra fingers; no unreadable text; no watermark.
```

## 模式 2：從零生成 / character generation

適用情境：
- 還沒有 Mika Lin 參考圖。
- 需要建立人物基準圖。
- 不做換衣，而是生成同一位虛擬人物的初始形象。

模板：

Create a realistic fashion editorial image of the same fictional AI virtual creator named Mika Lin. She is a Taiwanese woman in her late 20s with a soft oval face, natural warm fair skin, deep brown collarbone-length layered hair with a subtle wave, clean natural makeup, healthy slim body proportion, and a calm friendly city style. She should look like the same person across all images.

Outfit: `{clothing_item}` in `{color_palette}`, made of `{fabric}`, with `{fit}` fit.

Styling: `{styling_rules}`.

Pose: `{pose}`.

Background: `{background}` in Taiwan urban daily life, realistic natural light.

Camera style: `{camera_style}`, vertical fashion social media image, clear full outfit, clean composition, no visible brand logos.

Negative prompt: no celebrity resemblance, no real person reference, no childlike appearance, no school uniform, no nudity, no sexualized pose, no distorted hands, no extra fingers, no unreadable text, no luxury logo, no watermark, no fake brand endorsement.

## 2:3 Pinterest 版本

Use a vertical 2:3 composition. Leave clean negative space at top for title overlay. Full outfit must be visible from head to shoes. Make clothing texture and silhouette easy to inspect.

## IG Carousel 封面版本

Use a clean front-facing or three-quarter pose. Keep the background simple. The outfit should be immediately recognizable in a small thumbnail.

## 小紅書筆記版本

Use a more everyday lifestyle scene, such as Taipei MRT exit, cafe street, office lobby, rainy sidewalk, or weekend bookstore. Keep the look practical and shoppable.

## 產圖檢查

每批圖至少檢查：
- 是否仍像同一個人。
- 服裝輪廓是否清楚。
- 手、腳、包包、鈕扣、拉鍊是否有明顯錯誤。
- 是否出現品牌 logo 或難以辨識文字。
- 是否需要標註 AI 虛擬穿搭示意。
