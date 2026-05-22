# Perplexity 週報網站狀態

檢查日期：2026-05-22  
網站首頁：https://mika-lin-weekly.pplx.app/  
列表資料：https://mika-lin-weekly.pplx.app/data/index.json

## 目前判斷

這個網站形式符合工作流需求：
- 有固定首頁。
- 有歷期列表頁。
- 有機器可讀的 `data/index.json`。
- 每週週報有穩定 URL，例如 `https://mika-lin-weekly.pplx.app/weeks/2026-W20.html`。

## 2026-W21-test 驗收

測試週報：https://mika-lin-weekly.pplx.app/weeks/2026-W21-test.html  
直接 CSV：https://mika-lin-weekly.pplx.app/data/2026-W21-test.csv

2026-W21-test 已符合 Codex 工作流規格：
- 有 5 個 Trend Topics。
- 有 6-8 件代表性單品。
- 有 20 個 Item Prompt List。
- 有 7 則 IG / 小紅書 / Pinterest 平台內容計畫。
- 有 20 筆 `Machine-readable Export` CSV，且欄位符合 `04_prompts/item_prompt_database.csv`。
- `data/index.json` 已包含 `2026-W21-test`。

2026-W19 與 2026-W20 可視為歷史檔案，不需回填。

## 後續使用方式

每週短會時，優先貼首頁 URL 或最新週報 URL。Codex 檢查順序：
1. 讀 `data/index.json` 找最新週報。
2. 讀最新 `weeks/YYYY-WXX.html`。
3. 確認是否有 20 筆 CSV。
4. 若 CSV 存在，轉入 `04_prompts/item_prompt_database.csv`。
5. 若 CSV 不存在，要求 Perplexity 重新生成或提供 Markdown 備案。

## Day 2 結論

網站架構與新規格都已成立。W21-test 的 20 筆 CSV 已匯入 `04_prompts/item_prompt_database.csv`。下一步進入 Day 3：從 `04_prompts/w21_test_priority_prompts.md` 的 10 個 prompt 開始做 Grok + OpenAI 圖像 A/B 測試。
