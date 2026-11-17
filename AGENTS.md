# Mira Project Instructions

## 雲端與新環境接手

先讀 `10_automation/CLOUD_HANDOFF.md`，再依下方順序讀主流程與最新狀態。Reel 的六種方法、三層觀看目的、人物表演、IG 參考及運鏡經驗都在版本庫內，入口為 `09_sops/mira_reel_method_catalog.md` 和 `11_skills/mira-reel-director/SKILL.md`。技能未出現在環境清單時直接讀取版本庫中的 SKILL.md。專案的 `.agents/skills/` 提供對應入口。

## 2026-11-04 IG 分頁保護

IG 參考研究沿用使用者現有分頁，除非明確要求，不建立新 IG 分頁。預設用頁面播放與可見畫面紀錄觀察，不對 IG blob 影片呼叫本次失敗的 `downloadMedia`；不將研究用 IG 頁標記 `markDeliverable`／`markHandoff`。若意外多出分頁，先保存原頁與新增頁的網址、分頁識別及出現時間，不立即關閉使用者可能正在看的頁面。11/4 額外頁實際於 15:48 建立，早於後來交付標記；根本原因未定，詳 `10_automation/diagnostics/2026-11-04_ig_unexpected_tab/REPORT.md`，勿誤寫成通知或交付標記已確診。

## 2026-11-03 情境表演與現況核對

自然表情／動作、參考拆解及提示詞比較另讀 `11_skills/mira-reel-director/references/performance-and-reference.md`。連結情境目的、注意對象與關鍵可見反應；動作合理連貫即可保留變體，不強制逐秒仿拍。工具抽格、助理解讀與使用者澄清分開；一次偏好不等於穩定方法或發布核准。接續前依精確版本與最新收據核對，避免把歷史待審重開成現行工作；既有授權與新圖／品質檢查規則維持。

## 2026-10-30 製作檢查

新製／重做Mira Reel另讀 `11_skills/mira-reel-director/references/production-checkpoints.md`：觀眾看點與人物動機先定、實際畫幅尺度比較、同路線先測接點、按弧長安排步速、遮擋按秒剪輯；同機制兩次失敗後改設計或轉研究。使用者的免逐步核准授權不免品質檢查。解碼、抽樣、原速動態審查、使用者接受及發布分開記錄。

## 現行最高原則：開放方法庫、研究與製作並行 — 2026-10-29

先定觀眾看點，再定套數、服裝資訊、人物表演、鏡頭與方法；最後推導素材。一支可單套、兩套或多套，不以舊五種方法限制創作。單一模特兒一致性保留；週五主題／十套素材／五支Reel仍作產量基準，單片如何取用依企劃，不再要求每支恰好兩套或兩套都入片。新方案的額外素材需求須明列。

逐步觀察其他IG帳號並擴充方法庫，同時持續推進具體Reel；小批參考研究不能阻塞製作。既有素材先評估再補圖；固定鏡頭活潑表演、走近、入出畫都可選，行走與複雜曲線非預設。單片接受、重複成功、觀眾成效分別記錄。導演技能的 references/research-and-production.md 定義執行節奏。此原則優先於下方歷史兩套／五方法固定敘述；原影像核准、原速與逐圖審查仍有效。


Before working on Mira, read these files in order:

1. `10_automation/CANONICAL_WORKFLOW.md`
2. `CURRENT_STATUS.md`
3. `10_automation/runs/{active_week}/publishing_structure.md`
4. `09_sops/mira_instagram_caption_sop.md` when writing Instagram copy

After these required reads, use `10_automation/MIRA_EDITORIAL_HANDOFF.md` as the current cross-week entry and read the selected series' specific plan/approval records. A missing current planning-week structure must be reported as missing; do not treat a prior delivery week as today's planning week. Historical pending/paused entries are superseded by the latest scoped receipts. The W37 M02 pilot gate is recorded as passed on 2026-09-29 in the canonical workflow; check that latest record rather than treating the historical gate condition below as a new pause request.

The standard weekly production contract below remains in force. Explicit user-approved series pilots, including the M03 five-look commute film, follow their own approved look lists and storyboards; a pilot exception neither changes the weekly quota nor should be forced back into the standard two-look cut.

Use the `mira-image-daily` skill for image planning, generation, or review.

For Reel format selection, whole-film storyboards, camera/character route planning, or continuity repair, use `11_skills/mira-reel-director/SKILL.md` (the versioned source for the `mira-reel-director` skill). Start from `09_sops/mira_reel_method_catalog.md`; derive required images only after the connected film plan. Shared-space films require a common scene/time model for both overhead routes and camera-view previs. This directing skill complements `mira-image-daily` and does not change the weekly production contract or approval scopes.

Current non-negotiable production rule: five weekly themes, one model per theme, two looks per model, ten looks total. Produce five Reels per week; every Reel keeps one model; its one, two or multiple looks are selected by its editorial purpose. Every look needs a native 9:16 full-person Reel source plus a usable styling-proof view, and a separate three-frame Carousel set: A full person, B scene application, C accessory detail. Reuse an existing proof view only after vertical framing and clarity review; otherwise generate the missing view. Read `09_sops/mira_reel_production_sop.md` for video work. The historical W37 M02 pilot gate passed on 2026-09-29; do not reactivate its old mass-production pause. New stills are candidates until user visual approval.

Do not repeatedly stop for confirmation between routine in-scope steps. Pause only for user visual approval, missing identity references, a genuinely ambiguous editorial decision, or an external action requiring authority.
