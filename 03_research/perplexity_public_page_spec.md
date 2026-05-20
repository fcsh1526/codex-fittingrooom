# Perplexity 公開網頁輸出規格

目的：保留你現有的 Perplexity 每週自動研究流程，但把輸出改成固定格式的公開網頁，讓 Codex 可以穩定拆解成 prompt、內容排程與商品導購資料。

## 建議做法

1. 在 Perplexity 建立或沿用「AI 虛擬穿搭趨勢」Space。
2. 把現有每週 Task 移入 Space 或改用同一套 Space instructions。
3. 每週產出一個公開網頁或公開 thread，權限設為 anyone with link。
4. 每週 09:30 短會時，把最新 URL 貼給 Codex。
5. 不要求第一階段 API 自動化；如果公開網頁格式連續 2 週穩定，再評估 Sonar API。

## 可貼進 Perplexity Task 的 Prompt

```text
你是台灣繁中市場的 AI 虛擬穿搭創作者研究員。請每週搜尋網路，整理本週適合 20-35 歲台灣女性的小資通勤、韓系日常、雨天穿搭、小隻女顯高、約會/週末穿搭趨勢。

請輸出成一個可公開分享的網頁，格式必須固定，讓後續可以被人工或 Codex 拆解成 CSV。內容請使用繁體中文，商品方向以台灣可買、可搜尋、非高價精品為優先。

必要區塊如下：

1. Weekly Trend Summary
- 本週日期
- 本週總結 150-250 字
- 本週最值得做的前三個主題

2. Trend Topics
請列出 5 個趨勢主題。每個主題包含：
- trend_name
- why_now
- audience
- occasion
- core_items：5 個
- color_palettes：3 組
- scenes：3 個
- search_keywords：Pinterest、Google、小紅書、蝦皮/品牌官網關鍵字
- content_angles：收藏型、導購型、互動型各 1 個
- risk_notes
- score：台灣可購買性、視覺辨識度、收藏潛力、導購潛力，各 1-5 分

3. Item Prompt List
請產出 20 個可直接給 AI 圖像工具使用的單品 prompt。每個 prompt 必須包含：
- id
- trend_name
- audience
- occasion
- clothing_item
- color_palette
- fabric
- fit
- styling_rules
- pose
- background
- camera_style
- shopping_keywords
- platform_priority：Instagram / 小紅書 / Pinterest
- cta

4. Product Search Keywords
請按品類列出台灣可搜尋商品字詞：
- tops
- bottoms
- outerwear
- shoes
- bags
- accessories

5. Platform Content Plan
請產出 7 則內容建議，欄位包含：
- date_suggestion
- platform
- format
- trend_name
- caption_angle
- cta
- disclosure

6. Machine-readable Export
請最後輸出一段 CSV code block，欄位必須完全如下，不要多欄、不要少欄：
id,week,trend_name,audience,occasion,clothing_item,color_palette,fabric,fit,styling_rules,model_identity,pose,background,camera_style,negative_prompt,shopping_keywords,affiliate_links,status,notes

model_identity 固定填 Mika Lin。
negative_prompt 固定填：AI virtual outfit only; no real person; no celebrity; no childlike appearance; no nudity; no logo.
affiliate_links 先留空。
status 固定填 draft。
notes 可放資料來源或操作提醒。
```

## Codex 檢查標準

- 是否有公開 URL。
- 是否有 5 個趨勢主題。
- 是否有 20 個 item prompts。
- 是否有固定欄位 CSV code block。
- 是否能直接轉進 `04_prompts/item_prompt_database.csv`。
- 是否有台灣可搜尋商品字詞。
- 是否每個主題都有平台內容角度與 CTA。

## 不建議的輸出

- 只有長篇趨勢文章，沒有可複製 CSV。
- 每週欄位名稱不同。
- 只列品牌名稱，沒有商品搜尋字。
- 只做高價精品或海外商品。
- 沒有平台 CTA 與導購意圖。
