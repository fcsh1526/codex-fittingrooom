# Perplexity 週報網站狀態

檢查日期：2026-05-21  
網站首頁：https://mika-lin-weekly.pplx.app/  
列表資料：https://mika-lin-weekly.pplx.app/data/index.json

## 目前判斷

這個網站形式符合工作流需求：
- 有固定首頁。
- 有歷期列表頁。
- 有機器可讀的 `data/index.json`。
- 每週週報有穩定 URL，例如 `https://mika-lin-weekly.pplx.app/weeks/2026-W20.html`。

## 目前不足

2026-W20 是歷史檔案版，尚未完整符合 Codex 工作流規格：
- 只有 8 件代表單品，未拆成 20 個 item prompts。
- 尚未看到 `Machine-readable Export` CSV code block。
- 尚未看到 7 則 IG / 小紅書 / Pinterest 平台內容計畫。
- Grok prompt 仍以舊表述為主，尚未全部改成「fictional AI virtual creator」安全表述。
- 頁面註記新規格自 2026-W22 起完整套用。

## 後續使用方式

每週短會時，優先貼首頁 URL 或最新週報 URL。Codex 檢查順序：
1. 讀 `data/index.json` 找最新週報。
2. 讀最新 `weeks/YYYY-WXX.html`。
3. 確認是否有 20 筆 CSV。
4. 若 CSV 存在，轉入 `04_prompts/item_prompt_database.csv`。
5. 若 CSV 不存在，要求 Perplexity 重新生成或提供 Markdown 備案。

## Day 2 結論

網站架構已成立。下一步不是再換平台，而是讓 Perplexity 從下一期開始使用 `03_research/perplexity_task_prompt_day1.md` 的全球趨勢 + 台灣落地 + CSV 匯出規格。
