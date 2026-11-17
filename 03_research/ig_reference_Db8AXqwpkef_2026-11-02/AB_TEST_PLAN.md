# 細膩人物表演：動作描述與動機句的對照設計

後續更新2026-11-02：共用首圖已獲使用者接受，A/B各一次已生成、下載、解碼、抽樣及製作完整原速左右對照。尚待原速觀感比較；無法固定seed，不能宣告動機句的因果優勢。最新範圍與實際差異見 10_automation/runs/2026-W44/performance_AB_2026-11-02/RESULT_REVIEW.md，下方製作前狀態保留為歷史。

2026-11-02。最新狀態：共同分鏡／俯視示意及共用首圖候選已完成，首圖待使用者視覺確認；尚未送 A/B 影片、未取得測試結果。延續 W44 素材研究，不開新週產量；目前沒有 W45 publishing_structure.md。分支與實際圖檢查見 10_automation/runs/2026-W44/performance_AB_2026-11-02/STILL_REVIEW.md。

## 使用者目的

這支街角赴約片是第一個參考案例，長期目的為讓 Mira 的人物表情、反應與身體動作更像真人拍攝。之後不要求每支仿拍，也不以無目的走路作預設。使用者明確肯定上週最後幾支影片細膩表情與動作的效果；其中特定 M02 第二鏡已有精確核准紀錄。個別版本的退件與待審仍保留。

## 既有證據

| 案例 | 證據／可借之處 | 限制 |
|---|---|---|
| M02_restart_review_v2_trim1s.mp4 | USER_ACCEPTANCE.md 明確接受 11 秒版，尤其第二鏡細緻、活潑。規劃紀錄為視線互動、放慢／停步、轉肩、手臂與笑容的連續發展 | 不能推論某句提示造成成功；本次在該資料夾未找到原始兩鏡完整送出提示。抽樣圖非原速驗收 |
| M02 第一秒舉手刪除 | 使用者指出舉手與後續劇情不連貫，刪除後接受 | 動作更多不代表更好；節點需要前因與銜接 |
| M01_lively_review_v1.mp4 | 第 2 秒左右轉身手飄移，已退件 | 表演吸引力不能抵銷肢體錯誤；轉身與展臂同時做有失敗紀錄 |
| M01_lively_review_v2.mp4 | 已改為轉肩時手近身，回正後才抬手 | 仍待使用者觀看，不能作成功基準 |
| street_meeting_2026-10-30/trial_01 | submitted_prompt.txt 明確已有朋友等待、認出朋友、笑容展開、放慢停步等動機與動作敘述 | 使用者相對改善回饋不等於此處全片各項通過；原片與新測試的起始圖／鏡頭不同，不能當 A/B 因果證據 |

基準來源：10_automation/runs/2026-W44/M02_restart_2026-10-30/USER_ACCEPTANCE.md、STATUS.md、PLAN.md；lively_models_2026-10-30/M01_TRIAL.md；street_meeting_2026-10-30/trial_01/submitted_prompt.txt。

## 唯一比較變因

- A：一組完整且有先後的可見動作，已包含自然表情、察看方向、過街與走近。
- B：完整保留 A，只在最前方多加一句，說明該側看是過街前察看來車。
- A 不降格為單調走路；B 不加新表情、手勢、車輛或鏡頭。要回答的是簡短的原因句是否有額外幫助。
- 這是兩個條件，第一輪各一次只產生兩支探索片。沒有可固定 seed 時，隨機差異仍在；單輪結果不宣稱可重複或普遍有效。

### 共同動作文字（草案，送出前需依實際首圖確認方向）

One continuous real-time shot. She walks along the pavement toward the curb. At the curb, she briefly turns her head and eyes toward the lane on screen right. Her gaze returns to her direction of travel, then she steps off the curb and walks diagonally toward the camera. As she comes closer, her eyes meet the lens and her relaxed expression gradually opens into a warm smile. Her arms, bag and clothing respond naturally to her steps. End in a comfortable waist-up view with consistent head-to-body proportions. Locked camera, coherent daylight and stable street geometry.

### 只加在 B 前方的句子

Her brief glance toward the lane is to check for approaching traffic before crossing.

上述文字尚未送出；若起始圖的車流方向不同，先將共同文字修正一次，再用同一文字供 A、B，不在兩條件之間分別改句。原片末段有背景重構圖；本測試暫用相同固定鏡頭隔離文字變因，不能宣稱同時驗證了原片運鏡重現。

## 共同輸入與準備

預定同一位 M02、同一套已用造型、同一張起始圖與同一組身份參照，直式 9:16、原速、同一生成介面／模型，預定 10 秒；實際支援項目送出前核對並凍結。解析度、首尾幀、seed、身份參照、實際送出文字與影片 UUID 逐項記錄，不支援者記 unknown／unsupported，不冒稱已控制。

起始圖尚未鎖定：此前 77ed722c… 是無道路的石牆站姿圖；M02_restart 的咖啡店廣場圖也沒有可直接證明支援過街的路緣／車道配置。現已製作同一場景示意與新過街首圖：performance_AB_2026-11-02/start_candidate_v2.png，941×1672，待使用者確認。首版人物約68%畫高過大，做一次取景修正後約33%，比設計40–45%更遠；實際偏差保留在 STILL_REVIEW.md，不視為精準投影或已核准。新生成照片按 Mira 現行規則逐張視覺核准後才可送影片。

共同故事只保留必要次序：人物已在街角 → 到路緣察看 → 過街接近 → 與鏡頭視線相遇、笑容展開。臉部和手部保留自然變化空間，不逐秒要求眨眼、呼吸、抬手、扭肩或列出十幾種微動作。較完整服裝閱讀在前中段，後段靠近用於眼神與表情。

## 如何比較

先以 X／Y 隱藏條件標籤原速觀看；記錄觀看者、觀看範圍與回饋，不先用故事文字解釋畫面。比較表現：

1. 側看的目標是否落在車道方向，察看與跨出路緣的先後是否清楚。
2. 眼神是否從道路回到行進方向，再與鏡頭建立互動；笑容有發展而非固定貼住。
3. 步伐、重心、手臂、提物與衣料是否連動，有無飄移、跳腳、比例突變。
4. 相鄰行動是否連貫，有無無原因舉手、突然停等或其他多餘表演。
5. 觀眾是否能直接感到一個生活中的接近／會合，以及服裝是否仍可讀。
6. 有無多出車輛、改路緣、背景變形或鏡頭移動；這些也列為動機句可能引入的副作用。

每項記可見／不符／不確定與時間點，不用未校準總分代表科學精準度。看不見的腳部記未能判定，不能標為零滑移。技術檢查、抽樣、原速全片審查、使用者接受及發布分開。

OpenMontage 的角色：抽取相同時間點與可疑片段、保存檔案規格與版本；表演與意義仍由助理和使用者判讀。沒有獨立語意識別或物理品質保證。

## 如何累積成可用經驗

- 第一輪只選出有希望的提示方式與可用片段，保留失敗原因；不能用兩支片確定未來都能成功。
- 再遇到不同人物或情境，例如聽到招呼後回看、拿到飲料後回應店員，用已有效的策略製作正常 Reel，觀察是否再次成立，不先把整週改為大量實驗。
- 跨情境重複成立後，將可重用的「情境／注意對象 → 反應 → 身體動作 → 情緒變化」與必要限制加入方法庫。不是把看車、低頭或笑容當每片必做清單。
- 保留「單片接受」「多次可用」「跨情境成立」三種證據，觀眾成效另記。未知結果保持空白；尚未產生新影片、費用或發布項目。
