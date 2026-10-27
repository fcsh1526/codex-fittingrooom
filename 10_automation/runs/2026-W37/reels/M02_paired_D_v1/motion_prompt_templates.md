# 動態提示詞與實際送出紀錄

更新：2026-10-05。四張配對來源均已獲使用者靜態核准；A 初版、B 初版及 A 的一次重試已送出並下載。下方用途草案不是實際生成收據，精確送出文字與當次 UI 證據以各 attempt 資料夾為準。

| 來源 | 精確提示詞 | 當次實際輸入 | 狀態 |
|---|---|---|---|
| A 初版 | [送出文字](grok_A_attempt_01/submitted_prompt.txt) | L01 中景 First frame＋L01 全身 Reference＋Mira M02 v3 | 拉遠超過配對尺度，新增落地盆栽；不採原尾段 |
| B 初版 | [送出文字](grok_B_attempt_01/submitted_prompt.txt) | L02 全身 First frame＋Mira M02 v3 | 保留候選；末段仍推近，完整播放與配對驗收待完成 |
| A 重試 | [送出文字](grok_A_attempt_02/submitted_prompt.txt) | 同一 L01 中景 First frame＋全身 Reference＋Mira M02 v3 | 解碼與15點抽查完成，約3.5秒起全身大致停穩、無新增落地盆栽；採作驗收候選，完整播放待完成 |

兩段已組成11.25秒v2，使用者2026-10-05對完整預覽回覆「ok」，此份乾淨畫面核准。原構圖v1有上下雙臉，v2固定等比例修正A構圖後減少位移；兩版各270幀解碼與整段交疊抽查完成，未另補寫完整觀看自述。以 [本輪驗收](REVIEW.md) 為準，不能把提示詞的相機停止秒數直接當實際驗收結果。

三次 UI 均為影片、6s、720p、直式、音訊關閉，不指定 Last frame；實際模型版本未顯示。先填完整文字，再選人物，最後確認中景仍為 First frame。角色選入會改變附件角色，不能只檢查提示詞中的名稱。

先核對Grok當次人物參照、First frame／Reference角色、時長、直式與音訊設定。以下只能配合實際已選入且使用者核准的檔案，沒有使用內部ID當魔法指令。

## A：第一套重點→完整

Use the selected character reference for the woman’s identity. Start from the approved medium portrait; the attached full-person photograph defines the complete outfit and the same library alcove. In one continuous shot, first give a clear view of the cream curved neckline framed by the open mist-gray shirt. Dolly back once, smoothly and level, to show her entire calf-length dress, navy shoulder bag and both white canvas shoes. Complete the camera move before the ending full-person interval, allowing the complete outfit to remain readable while she continues a small natural weight shift and lightly steadies the bag strap. Keep the chest-height perspective, face, shirt sleeves, neckline, waist seam, dress length and all background objects consistent. No turn-around, wardrobe change, text, cuts or additional camera motion.

## B：第二套完整→重點

Use the selected character reference for the same woman. Start from the approved full-person photograph of the blue-shirt and navy-dress outfit in the matched library alcove. First let the complete outfit read clearly in the same viewing position as the previous full-person shot. Then dolly in once, smoothly and level, to a face-included medium view showing the navy square neckline, open mist-blue shirt fronts and waist. Finish the camera move before the ending interval so these clothing boundaries remain clear. Keep her existing small natural weight shift and light gray-tote strap contact; preserve the gray canvas tote, ivory flat canvas slip-on shoes, silver studs, shirt sleeves and dress construction. Maintain the same daylight and rigid scene geometry. No changing outfit, slipping shoulders, turning away, text, cuts or additional camera motion.

## 不預設通過

上述是鏡頭用途，不保證模型精確按秒數執行。來源不足以留下中景／全身閱讀片段，或拉遠憑空改裙／鞋／背景，都退回單鏡檢查；不得改速、定格或混用另一套衣服補救。每個候選最多先重試一次，仍失敗就重新選擇已驗證的鏡位，另寫分鏡原因。
