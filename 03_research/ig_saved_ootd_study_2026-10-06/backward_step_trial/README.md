# M02 固定鏡位退一步：獨立動態試做

開始：2026-10-06，使用者對前述下一步回覆「ok」。第一波五支、既有並排／轉身／配對研究成片保留。

## 最新結果：兩套動作可用，但接段不通過；新 B 起點待逐張核准

使用者核准近起點v2後，一次 near_A1 生成確實退遠；一次 B1 生成確實走近。各為720×1280、24fps、145幀／6.041667秒，根據25全圖、5頭部及完整145下肢序列的root抽查未見明顯換臉／換衣／大幅背景跳變。正常速度完整播放與使用者影片核准未宣稱。

原生試剪v1為8.25秒，A[0,72)與B[0,144)，0.75秒／18幀疊加；完整技術解碼通過，五支待發與三個舊研究成片SHA保持相同。root已看25輸出檢查點與全27過場前後連續幀；雙臉重影明顯，接點不通過，保留診斷檔但不送為可發布影片。

新分鏡在 `revised_storyboard_v3.md`：以實際 A f96／4秒為人物距離與房間基準，換成核准 L02 衣服。內建影像生成一張base，再只修人物距離一次；selected v2在L02週次素材的 `reel/body_distance_matched_start_v2/`。頭位更接近，但不是像素精準對齊；還需逐張使用者核准及真正新B來源驗收。沒有送入Grok、沒有新B2或新核准成片。第一波／Drive未改，沒有文字、音樂、改速或發布。以下較早近起點待核准紀錄為歷史。

## 歷史結果：原全身起點兩次失敗，新近距離起點當時待核准

A1、A2 已完成並下載，皆 720×1280／24fps／145 格／約 6.0417 秒。逐格腳步與檢查點显示原後方腳向前／外移，人物沒有退遠縮小；相同設定的一次補做已用完。抽查身分、衣服與背景未見明顯大跳變，仍不能把姿態可用當成後退成功或服裝資訊增加。第二套未開始，未組成新兩套成片。

改分鏡參見 `revised_storyboard_v2.md`。既有 proof 改了攝影機觀看距離，不能直接充當固定背景的近人物起點；原核准照保留。內建影像生成另做 L01 候選，再針對頭頂留白修正一次；送審版本為 v2，人物靠近、先看衣襟／腰線，941×1672，SHA256 `e85778d9d38b7541cc5cf96fb73ea047c26da22c8179fe10b8c30f5c38356cb7`，存於週次素材的 `reel/backward_step_v2/`。尚待使用者逐張視覺核准，未送入 Grok；新圖不能保證未來後退或背景穩定。

原五支發布影片與先前核准素材未覆蓋，沒有 Drive 更新或發布。以下為原全身起點的操作紀錄。

## 源圖與分鏡

沿用 2026-W37-001-L01 / L02 已逐張核准的 paired_scene_v1 full masters。當前 M02 v3 face / full 在 CSV approved 且檔案存在；Grok 需實際選 `Mira M02 v3` 與服裝圖的 First frame。

第一套：霧灰敞開捲袖薄襯衫、奶油白洋裝、白色綁帶帆布鞋、深藍小肩包。第二套：霧藍敞開捲袖襯衫、深藍方領中長洋裝、米白無鞋帶便鞋、灰托特。依核准影像保留領口、衣長、剪裁、顏色与配件。

圖書館中央水磨石走道，左有座椅與小桌植物，右有書櫃／垂藤；靜態可見短距離空間，不能推定精確深度。只沿中央線退一小步，保持前向、扶包的手與敞開衣襟。相機固定。不側移、摸家具、換場、撥髮或完整轉身。

**兩張起始圖已是完整全身。** 本輪驗證自然距離變化、衣料與腳步連續、背景固定，不宣稱後退才揭露全身或必然新增服裝資訊。若沒有服裝資訊增益，只記為動態診斷結果，不擴為產線。

## 操作設定與門檻

先 A，6s / 720p / 9:16 / 音訊 off / First frame + Mira M02 v3，實際 UI 與輸出尺寸分開記。取回、檢查 A 後才開始 B。每段第一次失敗最多重試一次，降低難度或停止本條機制，不掩飾環境錯誤。

合成時若可用：原生連續片段與動作速度，兩套一次 0.75 秒疊加，無字無音。片長依實際可用時序，先看頭／腰／腳和背景位置再選接點；不能強制同步或為湊秒数延長／凍結／倒放／重播。新成片待使用者視覺核准。

## 記錄

每段保留 `submitted_prompt.txt`、實際設定、送出時間／生成等待時間、進度與完成頁截圖、來源 URL／本機原片、解碼與抽樣 QA。正常速度完整觀看與使用者視覺核准保持獨立；沒有完成就不標 passed。主動製作時間僅在有計時證據時填值。

狀態以 `trial_manifest.json` 和每段 `submission.json`／`retrieval.json`／`sampled_review.json` 為準。


### Selected static candidate v3

Independent v2 QA found the L01 dark-blue strap inherited into the L02 grey tote. A strap-only correction produced selectedv3, SHA `f8098adfefc9be66ffcfea9bc3bad424e3f5e34a30a343d50dc4478f10af16e6`, actual941×1672. Onebase+two targetededits are retained and honestly recorded as one additional wardrobe-regression correction beyond the normal one-edit guideline. Root visible review sees greystrap restored and v2 person/scene geometry retained; independentv3 QA and user still approval remain separate. No new B generation or upload from this still. Prompt/receipt in L02 `reel/body_distance_matched_start_v2/`.


### 2026-10-07：新 B v3 已核准

使用者 `OK` 核准精確 v3 起始圖（SHA `f8098adfefc9be66ffcfea9bc3bad424e3f5e34a30a343d50dc4478f10af16e6`）的臉、服裝與構圖。此核准只含靜態，尚無新 B 來源或成片核准。下一步固定鏡位走近，以實際 A/B 18 對交疊幀選接點，保留原速及 0.75 秒疊化。Grok 目前待安全驗證，尚未送生成；原五支發布檔與研究成片保留。
