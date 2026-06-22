# AI 虛擬穿搭創作者營運系統

這個工作區把 90 天 roadmap 落成可執行的內容營運系統，目標是用 AI 虛擬人物穿搭內容驗證台灣繁中市場的變現能力。

## 使用順序

1. 換電腦或新對話時，先看 `COMPUTER_B_SYNC.md`。
2. 每天先產生操作台：

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 -Action cockpit -TodayDate 2026-06-22
```

3. 打開 `10_automation/DAILY_COCKPIT.html`，照 top item 做事。
4. 若需要看完整架構，讀 `10_automation/AUTOMATION_ARCHITECTURE_BRIEF.md`。
5. 若要看內容隊列，讀 `10_automation/PUBLISH_QUEUE.md`。

目前策略是 production-first：

```text
持續產出精美 carousel。
IG 零流量或 visibility test 只作為旁支數據，不阻塞 carousel 生產。
有非零流量後才進入聯盟商品、品牌合作或會員變現。
```

## 核心 KPI

- 內容收藏率：優先判斷題材是否有穿搭參考價值。
- 連結點擊率：目標 3% 以上，驗證購物意圖。
- 聯盟成交與佣金：第一階段至少跑出 1 筆成交。
- LINE 或 Email 名單：90 天目標 1,000 筆，作為未來訂閱與品牌合作資產。
- 品牌合作訊號：至少 1 個品牌洽談或可寄出的 media kit。

## 商業原則

- 不使用真人照片換衣，只使用自建虛擬人物。
- 每篇 AI 圖與聯盟內容都要揭露。
- 前 90 天不碰庫存，先用聯盟、數位產品、品牌合作驗證。
- 每週只保留有數據支持的內容桶，避免靠主觀審美決策。
