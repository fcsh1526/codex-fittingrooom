# 本機前襟／領口診斷：原速 QA 與合成助手

日期：2026-10-08。工具已準備；建立工具本身沒有生成、取回或驗收任何新影片。

## 輸入和保護

`native_pair_tools.py` 可接受任意真正新來源的路徑、精確 SHA256 與原生半開區間 `[start,end)`。每次核對 storyboard 的四個核准素材和八個保留成片，不改寫來源、核准或全域狀態。輸出僅能放在本資料夾的新子資料夾；所有新檔使用 exclusive creation，既有子資料夾拒絕覆寫。途中失敗的輸出保留，不標成通過。

影片一律要求來源與輸出原生 720×1280／24fps。整幅 raster 不裁切、不縮放、不改速、不倒放、不凍結、不重播、不強制動作同步。來源音軌不带入，純影像編碼；不烙字。QA 板上的幀號與頭部裁切只用於檢查，不進影片。

## 先檢查每段新來源

請使用本機已設定的 Python。以下 `SOURCE`、`ACTUAL_SHA` 和新輸出名稱都必須換成實際值：

```text
python -B native_pair_tools.py inspect --source SOURCE --sha ACTUAL_SHA --start 0 --end 145 --out-dir QA_A_attempt01
```

`--end` 可省略以檢查完整解碼範圍。產物包含完整解碼資訊、25 全圖檢查點、5 頭部窗口、原生樣本與來源 SHA。實際幀數不足時不能照填145。樣本未涵蓋的手／衣接觸瞬間仍須另外完整播放或查看原生幀；此工具沒有替代正常速度觀看。

實際審查後，另存來源 QA JSON；必須含：

```json
{
  "source_sha256": "ACTUAL_SHA",
  "approved_sampled_dynamic_qa": true,
  "reviewed_native_frames_half_open": [0, 145],
  "reviewer": "ACTUAL_REVIEWER",
  "findings": "ACTUAL_OBSERVATIONS",
  "continuous_visual_review": "ACTUAL_STATUS"
}
```

範例的 `true` 只說明機器介面，不是本輪核准；沒有真實審查不得寫入。A、B 各需自己的 QA，選段必須落在已審查區間。

## 兩段都可用後再合成

```text
python -B native_pair_tools.py compose --a SOURCE_A --a-sha ACTUAL_A_SHA --a-qa ACTUAL_A_QA --a-start 0 --a-end 144 --b SOURCE_B --b-sha ACTUAL_B_SHA --b-qa ACTUAL_B_QA --b-start 0 --b-end 144 --out-dir review_v1 --name M02_front_opening_review_v1
```

兩段各144幀，18幀／0.75秒交疊，預計270幀／11.25秒。若因衣服閱讀或接點改選區間，產物重新計算真實幀數、時間、mapping 和檢查邊界，不沿用270。

產物包括：

- 完整原生研究影片與 SHA／收據。
- 25 全圖、5 頭部檢查點。
- 全部18交疊幀，加上前後各8幀的全圖與頭部板、單幀原圖。
- 原生 A／B frame mapping、完整輸出解碼及保護檔核對。

預設 A[0,144)、B[0,144) 時，交疊 output[126,144)，邊界 output[118,152)，每次兩來源各前進一原生幀。B權重為 `(overlap_index+1)/18`。

## 仍需實際驗收

來源動態通過不等於兩套交疊通過；兩個核准 proof 也並非像素重合。臉／肩／手、包帶、窗台／桌沿／椅墊／書架均須看整個交疊，不能只看起始圖。若出現雙臉或場景呼吸，不以加長淡化、改速或移動人物補救。

合成工具永遠輸出 `research_candidate_pending_combined_visual_review`。正常速度整片、編輯用途及使用者視覺核准另記；沒有发布或流量結果。這是中景診斷，不是新的全身兩套正式發布版。
