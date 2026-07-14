# Perplexity 公開網頁輸出規格

目的：保留你現有的 Perplexity 每週自動研究流程，以世界潮流趨勢作為上游來源，但把輸出改成固定格式的公開網頁，讓 Codex 可以穩定拆解成 prompt、內容排程與商品導購資料。台灣只作為下游商品搜尋、內容語氣與導購落地層。

## 週次標準

- 全流程只採用 ISO 8601 週次。
- 每週從星期一開始；W01 是包含該年度第一個星期四的那一週。
- 週報標題、公開網址、`data/index.json`、CSV 的 `week` 欄位與本週日期範圍必須一致。
- `本週日期` 必須輸出該 ISO 週星期一至星期日的完整日期範圍。
- 範例：`2026-W27` 對應 `2026-06-29` 至 `2026-07-05`。

## 建議做法

1. 在 Perplexity 建立或沿用「AI 虛擬穿搭趨勢」Space。
2. 把現有每週 Task 移入 Space 或改用同一套 Space instructions。
3. 每週產出一個公開網頁或公開 thread，權限設為 anyone with link。
4. 每週 09:30 短會時，把最新 URL 貼給 Codex。
5. 不要求第一階段 API 自動化；如果公開網頁格式連續 2 週穩定，再評估 Sonar API。

## 可貼進 Perplexity Task 的 Prompt

```text
你是 AI 虛擬穿搭雜誌 Mira 的全球流行趨勢研究員。請每週搜尋網路，整理本週適合女性虛擬模特兒影像創作的服飾流行單品與提示詞。研究範圍以世界潮流為上游來源，必須涵蓋國際精品設計師、日韓潮流品牌、歐美街頭/輕奢、快時尚與大眾流行。顯示欄位使用台灣繁體中文，國際英文原詞只保留在來源、notes 與搜尋關鍵字區。

週次必須採 ISO 8601：星期一為每週第一天，W01 為包含年度第一個星期四的週。標題的 YYYY-WXX、本週日期範圍、公開網址、index.json 與 CSV week 欄位必須完全一致。

請輸出成一個可公開分享的網頁，格式必須固定，讓後續可以被人工或 Codex 拆解成 CSV。不要把趨勢來源限縮在台灣；台灣只用於把全球趨勢轉成可搜尋、可購買、可發文、可導購的內容。

顯示語言規則：
- trend_name、clothing_item、occasion 與平台文案只能使用自然台灣繁中，不得中英文混排。
- 英文國際原詞放在 global_context、Product Search Keywords 或 CSV notes。
- Capri Pants → 七分褲；Fisherman Sandals → 漁夫涼鞋；Sheer Layering → 透膚疊穿；Butter Yellow → 奶油黃；Scarf-as-Belt → 絲巾腰帶。
- Perplexity 不分配 M01-M05；人物、表情、姿勢、鏡頭與背景由 Codex 統一控制。

必要區塊如下：

1. Weekly Trend Summary
- 本週日期
- 本週全球趨勢總結 150-250 字
- 台灣落地提醒 80-120 字
- 本週最值得做的前三個主題

2. Trend Topics
請列出 5 個趨勢主題。每個主題包含：
- trend_name
- trend_origin：international_designer / japan_korea / western_street_luxury / fast_fashion_mass
- global_context
- why_now
- audience
- occasion
- core_items：5 個
- color_palettes：3 組
- scenes：3 個
- search_keywords：Pinterest、Google、小紅書、蝦皮/品牌官網關鍵字
- taiwan_localization：台灣可搜尋、可搭配、可導購的落地方式
- content_angles：收藏型、導購型、互動型各 1 個
- risk_notes
- score：全球趨勢強度、視覺辨識度、收藏潛力、台灣導購潛力，各 1-5 分

3. Item Prompt List
請產出 20 個可直接給 AI 圖像工具使用的單品 prompt。每個 prompt 必須包含：
- id
- trend_name
- trend_origin
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
請按品類列出全球趨勢原詞與台灣可搜尋商品字詞：
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

model_identity 固定填 assigned_by_codex。
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
- 是否保留全球趨勢來源，不把研究限縮成台灣流行。
- 是否每個主題都有平台內容角度與 CTA。
- 顯示欄位是否為自然台灣繁中，英文原詞是否只出現在來源或 notes。

## 不建議的輸出

- 只有長篇趨勢文章，沒有可複製 CSV。
- 每週欄位名稱不同。
- 只列品牌名稱，沒有商品搜尋字。
- 只做高價精品或海外商品。
- 沒有平台 CTA 與導購意圖。
