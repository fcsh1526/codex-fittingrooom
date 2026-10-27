# T09 — two_looks_hard_cut_a

狀態：待執行；本檔不是通過紀錄。

- 起始／穿搭圖：LOOK1_START;LOOK2_START（從 ../input_assets.csv 找真實路徑；相關圖必須已經視覺核准）。
- 額外角色參照：FACE;BODY。none 時確定沒有殘留上次角色參照。
- 比較對象：T02;T08；變因：two_looks_one_generation。
- 時長先規劃 6 秒、9:16；實際依所有組別共同支援設定。解析度、模型與模式都先由 UI 確認，不在文字提示冒填。
- 兩套各占影片一半，6 秒時在第 3 秒直接切鏡；LOOK1_START 是首鏡，LOOK2_START 是第二鏡服裝與場景參照，不擅自設為尾幀。
- 請先在 UI 真正選取圖片／參照，再貼下方英文；內部輸入代號不貼進提示。

## 可貼入 Grok 的提示詞

```text
Use the selected character reference for the same woman's facial identity and body proportions in both shots; do not copy its clothes, background or pose. Create exactly two vertical full-body shots of equal duration, with one direct hard cut halfway through. First half: reproduce the complete mist-grey shirt and cream dress outfit, white sneakers, navy shoulder bag and library from the library outfit image; she makes one small weight shift. Second half: reproduce the complete mist-blue shirt and navy dress outfit, off-white slip-ons, grey tote and floristry setting from the floristry outfit image; she makes one small weight shift. Both cameras remain locked and her head orientation remains close to its source image. Each outfit stays unchanged within its own shot. Switch the entire scene only at the cut. No clothing morph, dissolve, dialogue, text or extra people.
```

## 回填

結果寫入 ../trial_results.csv 和 ../frame_review.csv；未跑、功能不支援、參照未被選取、視覺失敗要分開記錄。禁止替尚未產生的影片打分。

