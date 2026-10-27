# T03 — nonfront_reference_repeat

狀態：待執行；本檔不是通過紀錄。

- 起始／穿搭圖：LOOK1_START（從 ../input_assets.csv 找真實路徑；相關圖必須已經視覺核准）。
- 額外角色參照：FACE;BODY。none 時確定沒有殘留上次角色參照。
- 比較對象：T02；變因：exact_repeat。
- 時長先規劃 6 秒、9:16；實際依所有組別共同支援設定。解析度、模型與模式都先由 UI 確認，不在文字提示冒填。
- 只做一個鏡頭，不加剪接、第二套或其他人物。
- 與 T02 的下方英文、輸入與全部 UI 設定完全相同。

## 可貼入 Grok 的提示詞

```text
Use the selected character reference for facial identity and body proportions only; do not copy its clothes, background or pose. Animate the attached library starting image as one continuous vertical full-body shot. Keep her head and gaze in their initial orientation. She makes one small, natural weight shift while remaining beside the return desk; the book stays in its original relation to her hands and the desk. The camera stays locked. Keep the open mist-grey thin shirt, cream midi dress, white low-top canvas shoes, small navy shoulder bag and silver earrings exactly as shown. Preserve the library, window light and realistic body proportions. No dialogue, text, extra people or wardrobe change.
```

## 回填

結果寫入 ../trial_results.csv 和 ../frame_review.csv；未跑、功能不支援、參照未被選取、視覺失敗要分開記錄。禁止替尚未產生的影片打分。

